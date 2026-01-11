"""
Script pour corriger le formatage LaTeX dans le JSON des questions.

Le problème: les questions sont formatées comme "$Texte avec \LaTeX$"
ce qui fait que tout le texte est traité comme du LaTeX math.

La solution: transformer en "Texte avec $\LaTeX$" où seules les
vraies formules sont entre $.
"""

import json
import re
from pathlib import Path

# Chemin du fichier
JSON_FILE = Path(__file__).parent.parent / "questions_cours_kholle_mpsi_final.json"
OUTPUT_FILE = JSON_FILE  # On écrase le fichier original


def fix_latex_formatting(text: str) -> str:
    """
    Corrige le formatage LaTeX d'un texte.
    
    Transforme: "$Soit f : G \to H un morphisme...$"
    En: "Soit $f : G \to H$ un morphisme..."
    """
    if not text:
        return text
    
    text = text.strip()
    
    # Si le texte ne commence pas par $, il est probablement déjà OK
    if not text.startswith('$'):
        return text
    
    # Enlever les $ externes
    if text.startswith('$') and text.endswith('$'):
        text = text[1:-1].strip()
    
    # Maintenant on doit identifier les formules LaTeX et les entourer de $
    # Patterns qui indiquent du LaTeX
    latex_commands = [
        r'\\to', r'\\rightarrow', r'\\leftarrow', r'\\leftrightarrow',
        r'\\Rightarrow', r'\\Leftarrow', r'\\Leftrightarrow',
        r'\\forall', r'\\exists', r'\\nexists',
        r'\\in', r'\\notin', r'\\subset', r'\\subseteq', r'\\supset',
        r'\\cup', r'\\cap', r'\\setminus', r'\\emptyset',
        r'\\mathbb\{[A-Z]\}', r'\\mathcal\{[A-Z]\}',
        r'\\frac\{', r'\\sqrt\{', r'\\sum', r'\\prod', r'\\int',
        r'\\geq', r'\\leq', r'\\neq', r'\\equiv', r'\\approx',
        r'\\times', r'\\cdot', r'\\circ',
        r'\\ell', r'\\infty', r'\\partial',
        r'\\lim', r'\\sup', r'\\inf', r'\\max', r'\\min',
        r'\\sin', r'\\cos', r'\\tan', r'\\ln', r'\\log', r'\\exp',
        r'\\alpha', r'\\beta', r'\\gamma', r'\\delta', r'\\epsilon', r'\\varepsilon',
        r'\\lambda', r'\\mu', r'\\sigma', r'\\omega', r'\\pi',
        r'\^', r'_',  # Exposants et indices
    ]
    
    # Créer un pattern pour détecter les segments avec du LaTeX
    # Un segment LaTeX est une séquence qui contient des commandes LaTeX
    # entourée de lettres/chiffres/symboles mathématiques
    
    # Approche: on va scanner le texte et identifier les "zones LaTeX"
    # Une zone LaTeX commence quand on voit une commande \ et se termine
    # quand on arrive à un mot français ou une ponctuation forte
    
    # Mots français qui marquent la fin d'une formule
    french_markers = [
        'soit', 'soient', 'un', 'une', 'le', 'la', 'les', 'de', 'du', 'des',
        'et', 'ou', 'que', 'qui', 'pour', 'avec', 'dans', 'sur', 'par',
        'montrer', 'démontrer', 'énoncer', 'donner', 'calculer', 'déterminer',
        'est', 'sont', 'si', 'alors', 'donc', 'car', 'comme',
        'tout', 'toute', 'tous', 'toutes', 'aucun', 'aucune',
        'fonction', 'application', 'ensemble', 'groupe', 'anneau', 'corps',
        'morphisme', 'homomorphisme', 'isomorphisme', 'sous-groupe',
        'injective', 'surjective', 'bijective', 'continue', 'dérivable',
        'convergente', 'divergente', 'bornée', 'croissante', 'décroissante',
        'propriété', 'théorème', 'lemme', 'proposition', 'corollaire',
        'définition', 'exemple', 'remarque', 'attention',
        'on', 'a', 'peut', 'doit', 'faut', 'existe', 'tel', 'telle',
        'vrai', 'faux', 'vraie', 'fausse', 'toujours', 'jamais',
        'premier', 'première', 'dernier', 'dernière',
        'positif', 'négatif', 'nul', 'nulle',
    ]
    
    # Pattern pour un mot français (avec accents)
    word_pattern = r'\b(' + '|'.join(french_markers) + r')\b'
    
    # Diviser le texte en tokens
    # On garde les séparateurs (espaces, ponctuation)
    tokens = re.split(r'(\s+|[.,;:!?(){}[\]])', text)
    
    result = []
    in_formula = False
    formula_buffer = []
    
    for token in tokens:
        if not token:
            continue
        
        # Est-ce un mot français?
        is_french = re.match(word_pattern, token, re.IGNORECASE)
        
        # Est-ce que ça contient du LaTeX?
        has_latex = any(re.search(cmd, token) for cmd in latex_commands)
        
        # Est-ce un espace ou ponctuation?
        is_separator = re.match(r'^[\s.,;:!?()]+$', token)
        
        if has_latex:
            # On entre ou continue dans une formule
            if not in_formula:
                in_formula = True
                formula_buffer = []
            formula_buffer.append(token)
        elif is_french:
            # Un mot français termine la formule
            if in_formula and formula_buffer:
                # Fermer la formule
                formula_text = ''.join(formula_buffer).strip()
                if formula_text:
                    result.append(f'${formula_text}$')
                formula_buffer = []
                in_formula = False
            result.append(token)
        elif is_separator:
            if in_formula:
                # Les espaces/ponctuation peuvent faire partie de la formule
                # ou la terminer selon le contexte
                if token.strip() in 'alan.,;:!?':
                    # Ponctuation forte = fin de formule
                    if formula_buffer:
                        formula_text = ''.join(formula_buffer).strip()
                        if formula_text:
                            result.append(f'${formula_text}$')
                        formula_buffer = []
                        in_formula = False
                    result.append(token)
                else:
                    formula_buffer.append(token)
            else:
                result.append(token)
        else:
            # Autre token (lettres, chiffres, symboles)
            if in_formula:
                formula_buffer.append(token)
            else:
                # Vérifier si c'est une variable mathématique isolée (une lettre)
                if re.match(r'^[a-zA-Z]$', token) or re.match(r'^[a-zA-Z]_', token):
                    # Potentiellement une variable, mais on la laisse pour l'instant
                    pass
                result.append(token)
    
    # Fermer toute formule restante
    if in_formula and formula_buffer:
        formula_text = ''.join(formula_buffer).strip()
        if formula_text:
            result.append(f'${formula_text}$')
    
    final_text = ''.join(result)
    
    # Nettoyer les $ consécutifs ou vides
    final_text = re.sub(r'\$\s*\$', '', final_text)
    final_text = re.sub(r'\s+', ' ', final_text)
    
    return final_text.strip()


def process_json():
    """Traite le fichier JSON et corrige le formatage LaTeX."""
    
    print(f"Lecture de {JSON_FILE}...")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Compteurs
    questions_fixed = 0
    
    # Parcourir tous les chapitres
    for chapter_id, chapter_data in data.items():
        if chapter_id == "metadata":
            continue
        
        questions = chapter_data.get("questions_cours", [])
        for q in questions:
            # Corriger la question
            original = q.get("question", "")
            if original.startswith('$'):
                fixed = fix_latex_formatting(original)
                q["question"] = fixed
                questions_fixed += 1
                print(f"  Fixed: {chapter_id} - {q.get('id', '?')}")
            
            # Corriger aussi les attendus, erreurs, relances
            for field in ["attendus", "erreurs_frequentes", "relances_prof"]:
                items = q.get(field, [])
                for i, item in enumerate(items):
                    if isinstance(item, str) and item.startswith('$'):
                        items[i] = fix_latex_formatting(item)
    
    print(f"\n{questions_fixed} questions corrigées.")
    
    # Sauvegarder
    print(f"Sauvegarde dans {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Terminé!")


if __name__ == "__main__":
    process_json()


