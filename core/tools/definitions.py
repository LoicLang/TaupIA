"""
Tool definitions for the Kholleur agent.

All tools use OpenAI-compatible JSON Schema format, which works across
Gemini, Claude, DeepSeek, and Kimi providers.
"""

TOOL_DEFINITIONS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "chercher_concepts",
            "description": (
                "Recherche des concepts mathematiques par mot-cle dans un chapitre. "
                "Retourne les IDs, titres et types des concepts trouves. "
                "Utilise cet outil quand tu ne connais pas l'ID exact d'un concept."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Mot-cle de recherche (ex: 'convergence', 'matrice inversible')",
                    },
                    "chapter_id": {
                        "type": "string",
                        "description": "ID du chapitre pour restreindre la recherche (optionnel)",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Nombre max de resultats (defaut: 5)",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lire_definition",
            "description": (
                "Recupere la definition exacte d'un concept mathematique par son ID. "
                "Retourne le titre, le contenu LaTeX et le type du concept. "
                "Utilise cet outil pour verifier une definition avant d'evaluer un etudiant."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concept_id": {
                        "type": "string",
                        "description": "ID du concept (ex: 'def_suite_convergente', 'thm_bolzano_weierstrass')",
                    },
                },
                "required": ["concept_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lire_theoreme",
            "description": (
                "Recupere un theoreme ou une propriete par son ID. "
                "Retourne l'enonce, la demonstration si disponible, et les hypotheses. "
                "Utilise cet outil pour rappeler un theoreme quand l'etudiant est bloque."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concept_id": {
                        "type": "string",
                        "description": "ID du theoreme ou de la propriete",
                    },
                },
                "required": ["concept_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trouver_prerequis",
            "description": (
                "Trouve les concepts prerequis pour comprendre un concept ou un chapitre donne. "
                "Utilise cet outil quand l'etudiant est bloque pour identifier "
                "quelle notion de base lui manque."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concept_id": {
                        "type": "string",
                        "description": "ID du concept dont on cherche les prerequis (optionnel)",
                    },
                    "chapter_id": {
                        "type": "string",
                        "description": "ID du chapitre dont on cherche les prerequis (optionnel)",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "chercher_exercice",
            "description": (
                "Trouve un exercice adapte testant des concepts specifiques. "
                "Utilise cet outil pour proposer un exercice en lien avec "
                "les concepts que l'etudiant vient de travailler."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concept_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Liste d'IDs de concepts a tester",
                    },
                    "chapter_id": {
                        "type": "string",
                        "description": "ID du chapitre (optionnel)",
                    },
                    "difficulty": {
                        "type": "integer",
                        "description": "Niveau de difficulte souhaite (1-5, defaut: 3)",
                    },
                },
                "required": ["concept_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lire_programme",
            "description": (
                "Recupere les contraintes du programme officiel MPSI pour un chapitre : "
                "notions, prerequis, points de vigilance, capacites exigibles. "
                "Utilise cet outil pour verifier ce qui est attendu au programme."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "chapter_id": {
                        "type": "string",
                        "description": "ID du chapitre",
                    },
                },
                "required": ["chapter_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "choisir_question",
            "description": (
                "Selectionne une question de cours aleatoire pour un chapitre et une difficulte. "
                "Retourne l'enonce, la reponse attendue et les concepts testes."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "chapter_id": {
                        "type": "string",
                        "description": "ID du chapitre",
                    },
                    "difficulty": {
                        "type": "integer",
                        "description": "Niveau de difficulte (1-5)",
                    },
                    "exclude_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "IDs de questions deja posees (a exclure)",
                    },
                },
                "required": ["chapter_id"],
            },
        },
    },
]


def get_tool_definitions() -> list[dict]:
    """Return the full list of tool definitions."""
    return TOOL_DEFINITIONS
