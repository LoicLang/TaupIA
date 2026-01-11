# Khôlleur AI

## Vision
Simuler des khôlles de maths MPSI. L'app challenge l'étudiant, elle n'explique pas le cours. Un sparring partner, pas un prof.

## Stack
- Python 3.x + Streamlit
- Gemini-3-flash-preview pour OCR et évaluation
- Pas de BDD, tout en fichiers locaux
- .env : clé API Gemini (jamais commit)

## Fichiers existants
- cours : 1 fichier .md (structures algébriques)
- exercices : 22 fichiers .md 
- questions_cours_kholle_mpsi_final.json : banque de questions
- graph.json : structure du cours (dépendances entre notions)

## Flow utilisateur cible
1. L'étudiant choisit un chapitre
2. L'app pose une question de khôlle
3. L'étudiant répond (texte ou photo de brouillon)
4. L'app évalue et donne un feedback pédagogique
5. L'étudiant peut continuer ou changer de sujet

## Règles de code
- Simple > clever
- Une fonction = une responsabilité
- Interface en français
- Feedback qui explique l'erreur, pas juste "faux"

## Affichage maths
- Tout le contenu mathématique en LaTeX
- Streamlit : utiliser st.latex() pour les blocs, $...$ pour l'inline dans st.markdown()
- Les JSON contiennent du LaTeX brut, ne pas l'échapper

## Ce qu'on ne fait PAS
- Cours ou explications de zéro
- Système d'auth ou comptes utilisateurs
- Base de données