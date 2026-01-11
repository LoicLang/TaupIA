"""
Fonctions de requête sur ChromaDB.

Ce module fournit les fonctions pour interroger les collections :
- Recherche de questions par chapitre/difficulté
- Recherche d'exercices adaptés
- RAG sur le cours
"""

import json
from typing import Optional, List, Dict

import chromadb
from google import genai

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    GOOGLE_API_KEY,
    CHROMA_DIR,
    COLLECTION_QUESTIONS,
    COLLECTION_EXERCICES,
    COLLECTION_COURS,
    EMBEDDING_MODEL,
)

# Configure Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)


def get_chroma_client() -> chromadb.PersistentClient:
    """Retourne le client ChromaDB."""
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_query_embedding(text: str) -> list[float]:
    """Génère un embedding pour une requête."""
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    return result.embeddings[0].values


# =============================================================================
# REQUÊTES SUR LES QUESTIONS
# =============================================================================

def get_chapters() -> list[dict]:
    """Retourne la liste des chapitres disponibles avec leurs stats."""
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(COLLECTION_QUESTIONS)
    
    # Récupérer toutes les métadonnées
    results = collection.get(include=["metadatas"])
    
    chapters = {}
    for meta in results["metadatas"]:
        cid = meta["chapter_id"]
        if cid not in chapters:
            chapters[cid] = {
                "id": cid,
                "title": meta["chapter_title"],
                "semestre": meta["semestre"],
                "importance": meta["chapter_importance"],
                "question_count": 0,
                "difficulties": set()
            }
        chapters[cid]["question_count"] += 1
        chapters[cid]["difficulties"].add(meta["difficulty"])
    
    # Convertir sets en listes triées
    for ch in chapters.values():
        ch["difficulties"] = sorted(list(ch["difficulties"]))
    
    return sorted(chapters.values(), key=lambda x: (x["semestre"], x["title"]))


def get_random_question(
    chapter_id: str,
    difficulty: Optional[int] = None,
    question_type: Optional[str] = None,
    exclude_ids: Optional[list[str]] = None
) -> Optional[dict]:
    """
    Retourne une question aléatoire selon les critères.
    
    Args:
        chapter_id: ID du chapitre
        difficulty: Niveau de difficulté (1-5), None = tous
        question_type: Type de question, None = tous
        exclude_ids: IDs à exclure (questions déjà posées)
    
    Returns:
        Dictionnaire avec la question et ses métadonnées
    """
    import random
    
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(COLLECTION_QUESTIONS)
    
    def try_get_questions(where_filter):
        """Helper pour récupérer des questions avec un filtre."""
        results = collection.get(
            where=where_filter,
            include=["metadatas", "documents"]
        )
        
        if not results["ids"]:
            return []
        
        candidates = []
        for i, qid in enumerate(results["ids"]):
            if exclude_ids and qid in exclude_ids:
                continue
            candidates.append({
                "id": qid,
                "document": results["documents"][i],
                **results["metadatas"][i]
            })
        return candidates
    
    candidates = []
    
    # Essai 1 : Avec la difficulté exacte (+/- 1)
    if difficulty is not None:
        where_filter = {
            "$and": [
                {"chapter_id": chapter_id},
                {"difficulty": {"$gte": max(1, difficulty - 1)}},
                {"difficulty": {"$lte": min(5, difficulty + 1)}}
            ]
        }
        if question_type:
            where_filter["$and"].append({"question_type": question_type})
        
        candidates = try_get_questions(where_filter)
    
    # Essai 2 : Juste le chapitre (fallback)
    if not candidates:
        where_filter = {"chapter_id": chapter_id}
        if question_type:
            where_filter = {
                "$and": [
                    {"chapter_id": chapter_id},
                    {"question_type": question_type}
                ]
            }
        candidates = try_get_questions(where_filter)
    
    # Essai 3 : Tout le chapitre sans filtre de type
    if not candidates:
        candidates = try_get_questions({"chapter_id": chapter_id})
    
    if not candidates:
        return None
    
    return random.choice(candidates)


def search_similar_questions(query: str, chapter_id: Optional[str] = None, n_results: int = 3) -> list[dict]:
    """
    Recherche des questions similaires par embedding.
    Utile pour trouver des questions de relance.
    """
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(COLLECTION_QUESTIONS)
    
    query_embedding = get_query_embedding(query)
    
    where_filter = {"chapter_id": chapter_id} if chapter_id else None
    
    results = collection.query(
        query_embeddings=[query_embedding],
        where=where_filter,
        n_results=n_results,
        include=["metadatas", "documents", "distances"]
    )
    
    questions = []
    for i in range(len(results["ids"][0])):
        questions.append({
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "distance": results["distances"][0][i],
            **results["metadatas"][0][i]
        })
    
    return questions


# =============================================================================
# REQUÊTES SUR LES EXERCICES
# =============================================================================

def get_exercise_by_difficulty(
    chapter_id: Optional[str] = None,
    difficulty: int = 3,
    exclude_ids: Optional[list[str]] = None
) -> Optional[dict]:
    """
    Retourne un exercice adapté au niveau.
    
    Priorité de recherche :
    1. Difficulté EXACTE demandée
    2. Difficulté ±1 (seulement si aucun exercice exact)
    3. N'importe quelle difficulté (seulement si aucun dans la plage)
    
    Args:
        chapter_id: ID du chapitre (optionnel)
        difficulty: Niveau souhaité (1-5)
        exclude_ids: Exercices déjà faits
    """
    import random
    
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(COLLECTION_EXERCICES)
    
    def build_filter(diff_filter: dict) -> dict:
        """Construit le filtre avec la condition de difficulté donnée."""
        where_clauses = [diff_filter]
        if chapter_id:
            where_clauses.append({"chapter_id": chapter_id})
        return {"$and": where_clauses} if len(where_clauses) > 1 else where_clauses[0]
    
    def filter_and_pick(results: dict) -> Optional[dict]:
        """Filtre les exclusions et retourne un exercice au hasard."""
        if not results["ids"]:
            return None
        
        candidates = []
        for i, eid in enumerate(results["ids"]):
            if exclude_ids and eid in exclude_ids:
                continue
            candidates.append({
                "id": eid,
                "document": results["documents"][i],
                **results["metadatas"][i]
            })
        
        if not candidates:
            return None
        
        return random.choice(candidates)
    
    # 1. Chercher difficulté EXACTE
    exact_filter = build_filter({"difficulty": difficulty})
    results = collection.get(
        where=exact_filter,
        include=["metadatas", "documents"]
    )
    exercise = filter_and_pick(results)
    if exercise:
        return exercise
    
    # 2. Fallback: difficulté ±1
    nearby_filter = build_filter({
        "$and": [
            {"difficulty": {"$gte": max(1, difficulty - 1)}},
            {"difficulty": {"$lte": min(5, difficulty + 1)}}
        ]
    })
    results = collection.get(
        where=nearby_filter,
        include=["metadatas", "documents"]
    )
    exercise = filter_and_pick(results)
    if exercise:
        return exercise
    
    # 3. Fallback ultime: n'importe quel exercice du chapitre
    if chapter_id:
        chapter_filter = {"chapter_id": chapter_id}
        results = collection.get(
            where=chapter_filter,
            include=["metadatas", "documents"]
        )
        exercise = filter_and_pick(results)
        if exercise:
            return exercise
    
    # 4. Dernier recours: n'importe quel exercice
    results = collection.get(include=["metadatas", "documents"])
    return filter_and_pick(results)


def search_exercises_by_notion(notion: str, n_results: int = 5) -> list[dict]:
    """Recherche des exercices par notion/concept."""
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(COLLECTION_EXERCICES)
    
    query_embedding = get_query_embedding(notion)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "documents", "distances"]
    )
    
    exercises = []
    for i in range(len(results["ids"][0])):
        exercises.append({
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "distance": results["distances"][0][i],
            **results["metadatas"][0][i]
        })
    
    return exercises


# =============================================================================
# RAG SUR LE COURS
# =============================================================================

def search_cours(query: str, n_results: int = 3, section: Optional[str] = None) -> list[dict]:
    """
    Recherche dans le cours de référence.
    
    Args:
        query: Question ou concept à rechercher
        n_results: Nombre de chunks à retourner
        section: Filtrer par section (optionnel)
    
    Returns:
        Liste de chunks pertinents avec métadonnées
    """
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(COLLECTION_COURS)
    
    query_embedding = get_query_embedding(query)
    
    where_filter = None
    if section:
        where_filter = {"section": {"$contains": section}}
    
    results = collection.query(
        query_embeddings=[query_embedding],
        where=where_filter,
        n_results=n_results,
        include=["metadatas", "documents", "distances"]
    )
    
    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i],
            **results["metadatas"][0][i]
        })
    
    return chunks


def get_rag_context(
    question: str,
    chapter_id: str = None,
    top_k: int = 3
) -> List[Dict]:
    """
    Récupère les chunks pertinents avec métadonnées complètes pour le debug RAG.
    
    Cette fonction est l'interface principale pour le panneau de debug RAG.
    Elle convertit les distances ChromaDB en scores de pertinence (0-100%).
    
    Args:
        question: La question ou le concept à rechercher
        chapter_id: Optionnel, ID du chapitre pour filtrer les résultats
        top_k: Nombre minimum de chunks à retourner (défaut: 3)
    
    Returns:
        Liste de dictionnaires avec:
        - chunk_id: Identifiant unique du chunk
        - content: Contenu textuel complet du chunk
        - score: Score de pertinence (0-100%, plus haut = meilleur)
        - metadata: Dictionnaire avec chapitre, section, difficulté, etc.
    
    Exemple de retour:
        [{
            'chunk_id': 'cours_chunk_0012',
            'content': '**Définition (Sous-groupe)** Soit (G, *) un groupe...',
            'score': 87.5,
            'metadata': {
                'chapter': 'Structures algébriques',
                'section': 'III Groupes',
                'subsection': 'III.2 Sous-groupes',
                'difficulty': 2,
                'has_definition': True,
                'has_theorem': False,
                'has_proof': False,
                'has_example': False
            }
        }]
    """
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(COLLECTION_COURS)
    
    # Générer l'embedding de la question
    query_embedding = get_query_embedding(question)
    
    # Requête ChromaDB avec top_k résultats
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["metadatas", "documents", "distances"]
    )
    
    # Convertir les résultats en format structuré
    rag_chunks = []
    
    for i in range(len(results["ids"][0])):
        # Récupérer les données brutes
        chunk_id = results["ids"][0][i]
        content = results["documents"][0][i]
        distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]
        
        # Convertir la distance en score de pertinence (0-100%)
        # ChromaDB utilise la distance L2, plus petit = plus proche
        # Formule: score = max(0, 100 - distance * 40)
        # Cela donne ~100% pour distance 0, ~60% pour distance 1, ~20% pour distance 2
        score = max(0, min(100, 100 - distance * 40))
        
        # Estimer la difficulté basée sur le contenu
        content_lower = content.lower()
        difficulty = 2  # Par défaut: niveau intermédiaire
        if "démonstration" in content_lower or "preuve" in content_lower:
            difficulty = 4  # Les preuves sont plus complexes
        elif "exemple" in content_lower or "application" in content_lower:
            difficulty = 1  # Les exemples sont plus accessibles
        elif "théorème" in content_lower or "proposition" in content_lower:
            difficulty = 3  # Théorèmes: niveau avancé
        
        # Construire le chunk structuré
        rag_chunk = {
            "chunk_id": chunk_id,
            "content": content,
            "score": round(score, 1),
            "metadata": {
                "chapter": "Structures algébriques",  # Fixe pour ce cours
                "section": metadata.get("section", ""),
                "subsection": metadata.get("subsection", ""),
                "difficulty": difficulty,
                "has_definition": metadata.get("has_definition", False),
                "has_theorem": metadata.get("has_theorem", False),
                "has_proof": metadata.get("has_proof", False),
                "has_example": metadata.get("has_example", False),
                "chunk_index": metadata.get("chunk_index", 0),
                "char_count": metadata.get("char_count", len(content))
            }
        }
        
        rag_chunks.append(rag_chunk)
    
    # Trier par score décroissant (au cas où)
    rag_chunks.sort(key=lambda x: x["score"], reverse=True)
    
    return rag_chunks


def get_context_for_evaluation(question: str, student_answer: str, n_chunks: int = 3) -> str:
    """
    Construit le contexte RAG pour évaluer une réponse.
    
    Combine la question et la réponse pour trouver le contexte le plus pertinent.
    """
    # Recherche basée sur la question
    query = f"{question}\n\nRéponse de l'étudiant: {student_answer}"
    chunks = search_cours(query, n_results=n_chunks)
    
    if not chunks:
        return ""
    
    context_parts = []
    for chunk in chunks:
        section_info = f"[{chunk['section']}"
        if chunk.get('subsection'):
            section_info += f" > {chunk['subsection']}"
        section_info += "]"
        
        context_parts.append(f"{section_info}\n{chunk['text']}")
    
    return "\n\n---\n\n".join(context_parts)


# =============================================================================
# UTILITAIRES
# =============================================================================

def get_collection_stats() -> dict:
    """Retourne les statistiques des collections."""
    chroma_client = get_chroma_client()
    
    stats = {}
    for name in [COLLECTION_QUESTIONS, COLLECTION_EXERCICES, COLLECTION_COURS]:
        try:
            coll = chroma_client.get_collection(name)
            stats[name] = {
                "count": coll.count(),
                "metadata": coll.metadata
            }
        except Exception as e:
            stats[name] = {"error": str(e)}
    
    return stats


if __name__ == "__main__":
    # Test des requêtes
    print("=" * 60)
    print("TEST DES REQUÊTES CHROMADB")
    print("=" * 60)
    
    print("\n📊 Statistiques des collections:")
    stats = get_collection_stats()
    for name, info in stats.items():
        print(f"  - {name}: {info}")
    
    print("\n📚 Chapitres disponibles:")
    chapters = get_chapters()
    for ch in chapters[:5]:
        print(f"  - {ch['id']}: {ch['title']} ({ch['question_count']} questions)")
    
    if chapters:
        print(f"\n🎲 Question aléatoire du chapitre {chapters[0]['id']}:")
        q = get_random_question(chapters[0]['id'])
        if q:
            print(f"  ID: {q['id']}")
            print(f"  Type: {q['question_type']}")
            print(f"  Difficulté: {q['difficulty']}")
            print(f"  Question: {q['question_raw'][:100]}...")
    
    print("\n🔍 Recherche RAG 'sous-groupe':")
    chunks = search_cours("Qu'est-ce qu'un sous-groupe ?", n_results=2)
    for chunk in chunks:
        print(f"  - [{chunk['section']}] (distance: {chunk['distance']:.3f})")
        print(f"    {chunk['text'][:150]}...")


