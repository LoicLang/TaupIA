# Guide de Test Mobile

## Changements effectués

### ✅ Corrections UI

1. **Texte header corrigé** : Le texte "MPSI · Oral Mathematics Training System" est maintenant visible en blanc (avec opacity: 0.7) sur fond noir
2. **Compteur (6q) retiré** : Les chapitres dans le selectbox n'affichent plus le compteur de questions
3. **Énoncé amélioré** :
   - Séparateur horizontal ajouté après le titre
   - Taille de police augmentée à 1.1rem
   - Line-height augmenté à 1.8 pour meilleure lisibilité
   - Font-weight: 500 pour plus de présence
   - Padding: 1rem 0 pour aérer

4. **Logo TauIA** : Système d'intégration prêt (placer `logo.png` dans `/assets/`)

## Test sur Mobile

### Option 1 : Streamlit Mobile View
```bash
streamlit run app.py --server.address=0.0.0.0
```
Puis ouvrir depuis ton téléphone sur le même réseau avec l'IP locale de ton Mac.

### Option 2 : Browser DevTools
1. Lancer l'app : `streamlit run app.py`
2. Ouvrir dans Chrome
3. F12 → Toggle Device Toolbar (Ctrl+Shift+M)
4. Sélectionner "iPhone 12 Pro" ou "iPhone SE"

### Checklist Mobile

- [ ] Header visible et lisible
- [ ] Logo TauIA visible (si ajouté)
- [ ] Selectbox chapitre sans (6q)
- [ ] Énoncé de question bien visible et lisible
- [ ] Boutons tactiles (min 48px)
- [ ] Forms photo-first fonctionnels
- [ ] Upload photo fonctionne
- [ ] Pas de scroll horizontal
- [ ] Progress bar claire

## Points d'attention Mobile-First

✅ Font-size: 16px minimum pour textarea (évite zoom iOS)
✅ Boutons: min-height 48px pour tactile
✅ Gap: 1.5rem entre sections
✅ Padding responsive dans @media (max-width: 768px)
✅ Selectbox: min-height 48px sur mobile

## Responsive déjà implémenté

Voir CSS lines 644-699 pour les règles @media mobile :
- Header padding réduit
- Font-sizes ajustés
- Forms optimisés
- Textarea: font-size 16px (ligne 692)

## Pour ajouter le logo

1. Copier l'image TauIA dans `/assets/logo.png`
2. Relancer l'app
3. Le logo apparaîtra automatiquement dans le header
