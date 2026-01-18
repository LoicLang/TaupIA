# Changelog - Corrections UI

Date: 2026-01-18

## ✅ Corrections effectuées

### 1. Texte header invisible (noir sur noir)
**Problème** : Le sous-titre "MPSI · Oral Mathematics Training System" était invisible dans le header noir.

**Solution** :
- Changé `color: #AAAAAA` → `color: #FFFFFF` avec `opacity: 0.7`
- Fichier : `app.py` ligne 127
- Meilleure lisibilité sur fond noir tout en gardant l'aspect subtil

### 2. Compteur (6q) dans le selectbox chapitre
**Problème** : Affichage de "(6q)" après le nom du chapitre encombrait l'interface.

**Solution** :
- Retiré le compteur du format d'affichage
- Changé de `f"{ch['title']} ({ch['question_count']}q)"` → `ch['title']`
- Fichiers modifiés :
  - `render_sidebar()` ligne 780
  - `render_setup_mobile()` ligne 885
- Interface plus épurée, focus sur le contenu

### 3. Énoncé de question peu visible
**Problème** : L'énoncé manquait de présence visuelle, difficile à lire.

**Solution** :
- Ajout d'un séparateur horizontal (`<hr>`) après le titre
- Augmentation taille police : `0.95rem` → `1.1rem`
- Line-height augmenté : → `1.8` (meilleure respiration)
- Font-weight renforcé : → `500` (medium)
- Padding ajouté : `1rem 0` (aération)
- Fichier : `app.py` ligne 1003-1013
- L'énoncé est maintenant le focus principal de la card

### 4. Logo TauIA intégré
**Solution** :
- Système de détection automatique du logo dans `/assets/logo.png`
- Fallback élégant si le logo n'est pas présent
- Layout responsive avec colonnes Streamlit
- Filter CSS pour adaptation au fond noir (ligne 135)
- Fichier : `app.py` ligne 1380-1403

**Pour ajouter le logo** :
```bash
# Option 1 : Copie manuelle
cp /path/to/tauia_logo.png assets/logo.png

# Option 2 : Script automatique
python3 scripts/add_logo.py /path/to/tauia_logo.png
```

## 📱 Compatibilité Mobile

Toutes les corrections respectent le principe **mobile-first** :

- ✅ Font-size minimum 16px pour les inputs (évite zoom iOS)
- ✅ Énoncé lisible sur petits écrans (1.1rem avec line-height 1.8)
- ✅ Boutons tactiles 48px minimum
- ✅ Responsive déjà testé dans les media queries existantes (lignes 644-699)

## 🧪 Tests

### Syntaxe Python
```bash
python3 -m py_compile app.py
# ✅ Aucune erreur
```

### Test visuel recommandé
1. Lancer l'app : `streamlit run app.py`
2. Ouvrir DevTools (F12)
3. Toggle Device Toolbar (Ctrl+Shift+M)
4. Tester sur iPhone 12 Pro / iPhone SE
5. Vérifier :
   - [ ] Header lisible (texte blanc sur noir)
   - [ ] Pas de (6q) dans les chapitres
   - [ ] Énoncé bien visible et lisible
   - [ ] Logo visible (si ajouté)

## 📊 Statistiques

- **Fichiers modifiés** : 1 (app.py)
- **Lignes changées** : +46 / -14
- **Fichiers créés** : 3
  - `assets/README.md` (guide logo)
  - `scripts/add_logo.py` (helper script)
  - `MOBILE_TEST.md` (guide de test)

## 🎨 Design System

Toutes les modifications respectent le design system "Engineering Precision" :
- Noir et blanc uniquement
- Typographie Inter + JetBrains Mono
- Pas d'ombres (uniquement bordures)
- Border-radius minimal (2px)
- Animations subtiles (fade only)

## 🚀 Prochaines étapes

Pour finaliser l'intégration du logo :
1. Récupérer l'image TauIA originale
2. La placer dans `assets/logo.png`
3. Relancer l'app

Optionnel :
- Optimiser l'image (PNG optimisé, fond transparent)
- Tester le rendu sur différentes résolutions
- Ajuster la taille si nécessaire (actuellement 40px)
