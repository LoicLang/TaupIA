"""
Ingestion des données dans ChromaDB.

Ce module gère l'indexation de :
- Questions de cours (JSON)
- Exercices (.md)
- Cours de référence (.md)

Chaque document est enrichi de métadonnées pertinentes pour le RAG.
"""

import json
import re
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings
import google.generativeai as genai

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    GOOGLE_API_KEY,
    CHROMA_DIR,
    QUESTIONS_FILE,
    GRAPH_FILE,
    EXERCICES_DIR,
    COURS_DIR,
    COLLECTION_QUESTIONS,
    COLLECTION_EXERCICES,
    COLLECTION_COURS,
    EMBEDDING_MODEL,
)


# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)


def get_chroma_client() -> chromadb.PersistentClient:
    """Retourne le client ChromaDB persistant."""
    CHROMA_DIR.mkdir(exist_ok=True)
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False)
    )


def get_embedding(text: str) -> list[float]:
    """Génère un embedding via Gemini."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
    )
    return result['embedding']


def load_graph() -> dict:
    """Charge le graphe des dépendances entre chapitres."""
    with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_chapter_metadata(chapter_id: str, graph: dict) -> dict:
    """Extrait les métadonnées d'un chapitre depuis le graphe."""
    ref = graph.get("referentiel_mpsi", {})
    chapter_data = ref.get(chapter_id, {})
    
    return {
        "titre": chapter_data.get("titre", ""),
        "semestre": chapter_data.get("semestre", 0),
        "importance": chapter_data.get("importance", 0),
        "prerequis": json.dumps(chapter_data.get("prerequis", [])),
        "notions": json.dumps(chapter_data.get("notions", [])[:10]),  # Top 10 notions
        "capacites_exigibles": json.dumps(chapter_data.get("capacites_exigibles", [])),
    }


# =============================================================================
# INGESTION DES QUESTIONS DE COURS
# =============================================================================

def ingest_questions(chroma_client: chromadb.PersistentClient, force: bool = False):
    """
    Ingère les questions de cours dans ChromaDB.
    
    Métadonnées par question :
    - chapter_id : ID du chapitre (ex: "STRUC_ALG")
    - chapter_title : Titre lisible du chapitre
    - question_type : Type de question (definition, theoreme_enonce, etc.)
    - difficulty : Niveau de difficulté (1-5)
    - temps_estime_min : Temps estimé en minutes
    - has_demo : Si c'est une démonstration
    - notions_cles : Notions clés extraites de la question
    """
    
    # Supprimer et recréer la collection si force=True
    if force:
        try:
            chroma_client.delete_collection(COLLECTION_QUESTIONS)
        except:
            pass
    
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_QUESTIONS,
        metadata={"description": "Questions de cours pour khôlles MPSI"}
    )
    
    # Vérifier si déjà ingéré
    if collection.count() > 0 and not force:
        print(f"Collection '{COLLECTION_QUESTIONS}' déjà peuplée ({collection.count()} documents)")
        return
    
    # Charger les données
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    graph = load_graph()
    
    documents = []
    metadatas = []
    ids = []
    embeddings = []
    
    # Parcourir tous les chapitres
    for chapter_id, chapter_data in data.items():
        if chapter_id == "metadata":
            continue
            
        chapter_meta = get_chapter_metadata(chapter_id, graph)
        questions = chapter_data.get("questions_cours", [])
        
        for q in questions:
            q_id = q.get("id", f"{chapter_id}_{len(ids)}")
            
            # Document = question + attendus pour meilleur embedding
            doc_text = f"""Question: {q.get('question', '')}

Attendus:
{chr(10).join('- ' + a for a in q.get('attendus', []))}

Erreurs fréquentes:
{chr(10).join('- ' + e for e in q.get('erreurs_frequentes', []))}"""
            
            # Métadonnées enrichies
            meta = {
                "chapter_id": chapter_id,
                "chapter_title": chapter_meta.get("titre", chapter_data.get("titre", "")),
                "semestre": chapter_meta.get("semestre", 0),
                "chapter_importance": chapter_meta.get("importance", 0),
                "question_type": q.get("type", "unknown"),
                "difficulty": q.get("difficulte", 3),
                "temps_estime_min": q.get("temps_estime_min", 5),
                "has_demo": "demo" in q.get("type", "").lower(),
                "question_raw": q.get("question", ""),
                "attendus_json": json.dumps(q.get("attendus", []), ensure_ascii=False),
                "erreurs_frequentes_json": json.dumps(q.get("erreurs_frequentes", []), ensure_ascii=False),
                "relances_prof_json": json.dumps(q.get("relances_prof", []), ensure_ascii=False),
            }
            
            documents.append(doc_text)
            metadatas.append(meta)
            ids.append(q_id)
            
            print(f"  Embedding question {q_id}...")
            embeddings.append(get_embedding(doc_text))
    
    # Insérer dans ChromaDB
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        print(f"✓ {len(documents)} questions ingérées dans '{COLLECTION_QUESTIONS}'")


# =============================================================================
# INGESTION DES EXERCICES
# =============================================================================

def parse_exercise_frontmatter(content: str) -> tuple[dict, str]:
    """Parse le frontmatter YAML d'un exercice .md"""
    meta = {}
    body = content
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()
            
            # Parse simple du YAML
            for line in frontmatter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    
                    # Parser les listes
                    if value.startswith("[") and value.endswith("]"):
                        value = [v.strip().strip('"\'') for v in value[1:-1].split(",")]
                    
                    meta[key] = value
    
    return meta, body


def extract_exercise_sections(content: str) -> dict:
    """Extrait les sections d'un exercice (Énoncé, Indications, Correction)."""
    sections = {
        "enonce": "",
        "indications": "",
        "correction": ""
    }
    
    # Patterns pour les sections
    patterns = {
        "enonce": r"#\s*Énoncé\s*\n(.*?)(?=#|$)",
        "indications": r"#\s*Indications?\s*\n(.*?)(?=#|$)",
        "correction": r"#\s*Correction\s*\n(.*?)(?=#|$)",
    }
    
    for section, pattern in patterns.items():
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section] = match.group(1).strip()
    
    return sections


def difficulty_stars_to_int(stars: str) -> int:
    """Convertit '★★☆☆☆' en entier (2)."""
    if isinstance(stars, int):
        return stars
    return stars.count("★") if isinstance(stars, str) else 3


def ingest_exercices(chroma_client: chromadb.PersistentClient, force: bool = False):
    """
    Ingère les exercices dans ChromaDB.
    
    Métadonnées par exercice :
    - exercise_id : Nom du fichier
    - chapter : Chapitre concerné
    - difficulty : Niveau de difficulté (1-5)
    - notions : Liste des notions abordées
    - has_correction : Si une correction est disponible
    - has_indications : Si des indices sont disponibles
    """
    
    if force:
        try:
            chroma_client.delete_collection(COLLECTION_EXERCICES)
        except:
            pass
    
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_EXERCICES,
        metadata={"description": "Exercices de khôlles MPSI"}
    )
    
    if collection.count() > 0 and not force:
        print(f"Collection '{COLLECTION_EXERCICES}' déjà peuplée ({collection.count()} documents)")
        return
    
    graph = load_graph()
    
    documents = []
    metadatas = []
    ids = []
    embeddings = []
    
    # Parcourir les fichiers d'exercices (y compris dans les sous-dossiers)
    for md_file in EXERCICES_DIR.glob("**/*.md"):
        print(f"  Processing {md_file.name}...")
        
        content = md_file.read_text(encoding='utf-8')
        frontmatter, body = parse_exercise_frontmatter(content)
        sections = extract_exercise_sections(body)
        
        # Inclure le dossier parent dans l'ID pour éviter les doublons
        parent_folder = md_file.parent.name
        exercise_id = f"{parent_folder}_{md_file.stem}"
        
        # Mapper le chapitre au format du graphe
        chapter_name = frontmatter.get("chapitre", "")
        chapter_id = None
        for cid, cdata in graph.get("referentiel_mpsi", {}).items():
            if cdata.get("titre", "").lower() in chapter_name.lower() or chapter_name.lower() in cdata.get("titre", "").lower():
                chapter_id = cid
                break
        
        # Document = énoncé pour le matching
        doc_text = f"""Exercice: {md_file.stem}
Chapitre: {chapter_name}
Notions: {', '.join(frontmatter.get('notions', [])) if isinstance(frontmatter.get('notions'), list) else frontmatter.get('notions', '')}

Énoncé:
{sections['enonce']}"""
        
        meta = {
            "exercise_id": exercise_id,
            "chapter": chapter_name,
            "chapter_id": chapter_id or "",
            "difficulty": difficulty_stars_to_int(frontmatter.get("difficulte", "★★★")),
            "notions_json": json.dumps(frontmatter.get("notions", []) if isinstance(frontmatter.get("notions"), list) else [frontmatter.get("notions", "")], ensure_ascii=False),
            "has_correction": len(sections["correction"]) > 50,
            "has_indications": len(sections["indications"]) > 20,
            "enonce": sections["enonce"],
            "indications": sections["indications"],
            "correction": sections["correction"],
        }
        
        documents.append(doc_text)
        metadatas.append(meta)
        ids.append(exercise_id)
        embeddings.append(get_embedding(doc_text))
    
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        print(f"✓ {len(documents)} exercices ingérés dans '{COLLECTION_EXERCICES}'")


# =============================================================================
# INGESTION DU COURS
# =============================================================================

def chunk_markdown(content: str, chunk_size: int = 1500, overlap: int = 200) -> list[dict]:
    """
    Découpe le cours en chunks intelligents basés sur la structure.
    Préserve les sections et sous-sections.
    """
    chunks = []
    
    # Pattern pour détecter les headers
    header_pattern = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
    
    # Trouver tous les headers avec leurs positions
    headers = [(m.start(), m.group(1), m.group(2)) for m in header_pattern.finditer(content)]
    
    if not headers:
        # Pas de structure, chunker simplement
        for i in range(0, len(content), chunk_size - overlap):
            chunk_text = content[i:i + chunk_size]
            chunks.append({
                "text": chunk_text,
                "section": "",
                "subsection": "",
                "level": 0
            })
        return chunks
    
    # Découper par sections
    current_section = ""
    current_subsection = ""
    
    for i, (pos, level, title) in enumerate(headers):
        # Déterminer la fin de cette section
        end_pos = headers[i + 1][0] if i + 1 < len(headers) else len(content)
        section_content = content[pos:end_pos]
        
        # Mettre à jour le contexte
        level_num = len(level)
        if level_num <= 2:
            current_section = title
            current_subsection = ""
        else:
            current_subsection = title
        
        # Si la section est trop longue, la découper
        if len(section_content) > chunk_size:
            for j in range(0, len(section_content), chunk_size - overlap):
                chunk_text = section_content[j:j + chunk_size]
                chunks.append({
                    "text": chunk_text,
                    "section": current_section,
                    "subsection": current_subsection,
                    "level": level_num
                })
        else:
            chunks.append({
                "text": section_content,
                "section": current_section,
                "subsection": current_subsection,
                "level": level_num
            })
    
    return chunks


def ingest_cours(chroma_client: chromadb.PersistentClient, force: bool = False):
    """
    Ingère tous les fichiers de cours dans ChromaDB.
    
    Métadonnées par chunk :
    - source_file : Nom du fichier source
    - section : Section principale (ex: "III Groupes")
    - subsection : Sous-section (ex: "III.1 Axiomatique")
    - chunk_index : Index du chunk dans le document
    - has_definition : Contient une définition
    - has_theorem : Contient un théorème
    - has_proof : Contient une démonstration
    """
    
    if force:
        try:
            chroma_client.delete_collection(COLLECTION_COURS)
        except:
            pass
    
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_COURS,
        metadata={"description": "Cours de référence MPSI"}
    )
    
    if collection.count() > 0 and not force:
        print(f"Collection '{COLLECTION_COURS}' déjà peuplée ({collection.count()} documents)")
        return
    
    documents = []
    metadatas = []
    ids = []
    embeddings = []
    
    chunk_counter = 0
    
    # Parcourir tous les fichiers de cours
    for cours_file in COURS_DIR.glob("*.md"):
        print(f"  Traitement de {cours_file.name}...")
        content = cours_file.read_text(encoding='utf-8')
        chunks = chunk_markdown(content)
        
        for chunk in chunks:
            chunk_id = f"cours_chunk_{chunk_counter:04d}"
            text = chunk["text"]
            
            # Détecter le type de contenu
            text_lower = text.lower()
            has_definition = "définition" in text_lower or "definition" in text_lower
            has_theorem = "théorème" in text_lower or "proposition" in text_lower or "lemme" in text_lower
            has_proof = "démonstration" in text_lower or "preuve" in text_lower
            has_example = "exemple" in text_lower
            
            meta = {
                "source_file": cours_file.name,
                "chunk_index": chunk_counter,
                "section": chunk["section"],
                "subsection": chunk["subsection"],
                "level": chunk["level"],
                "has_definition": has_definition,
                "has_theorem": has_theorem,
                "has_proof": has_proof,
                "has_example": has_example,
                "char_count": len(text),
            }
            
            documents.append(text)
            metadatas.append(meta)
            ids.append(chunk_id)
            
            section_preview = chunk['section'][:30] if chunk['section'] else cours_file.stem[:20]
            print(f"    Embedding chunk {chunk_counter+1} ({section_preview}...)")
            embeddings.append(get_embedding(text))
            chunk_counter += 1
    
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        print(f"✓ {len(documents)} chunks de cours ingérés dans '{COLLECTION_COURS}'")


# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

def ingest_all(force: bool = False):
    """Ingère toutes les données dans ChromaDB."""
    print("=" * 60)
    print("INGESTION DES DONNÉES DANS CHROMADB")
    print("=" * 60)
    
    chroma_client = get_chroma_client()
    
    print("\n📚 Ingestion des questions de cours...")
    ingest_questions(chroma_client, force=force)
    
    print("\n📝 Ingestion des exercices...")
    ingest_exercices(chroma_client, force=force)
    
    print("\n📖 Ingestion du cours de référence...")
    ingest_cours(chroma_client, force=force)
    
    print("\n" + "=" * 60)
    print("✅ INGESTION TERMINÉE")
    print("=" * 60)
    
    # Résumé
    print("\nRésumé des collections :")
    for name in [COLLECTION_QUESTIONS, COLLECTION_EXERCICES, COLLECTION_COURS]:
        coll = chroma_client.get_collection(name)
        print(f"  - {name}: {coll.count()} documents")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingestion des données Khôlleur AI")
    parser.add_argument("--force", "-f", action="store_true", help="Forcer la réingestion")
    args = parser.parse_args()
    
    ingest_all(force=args.force)
