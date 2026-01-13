---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Groupe", "Régularité", "Ensemble fini", "Principe des tiroirs / Bijection"]
---

# Énoncé
Soit $E$ un ensemble fini non vide muni d'une loi de composition interne $\cdot$ associative, pour laquelle tous les éléments de $E$ sont réguliers. Montrer que $(E, \cdot)$ est un groupe.

---

# Indications
1. Montrer que pour tout $g \in E$, l'application de translation à gauche $L_g : x \mapsto g \cdot x$ est une bijection.
2. En déduire l'existence d'un candidat pour l'élément neutre et prouver sa neutralité bilatérale.
3. Utiliser la surjectivité pour prouver l'existence d'un inverse à droite, puis montrer qu'il est bilatéral.

---

# Correction

Pour montrer que $(E, \cdot)$ est un groupe, nous devons prouver l'associativité, l'existence d'un élément neutre bilatéral et l'existence d'un symétrique bilatéral pour chaque élément.

### 1. Traduction de la régularité et finitude
Soit $g \in E$. Considérons l'application $L_g : E \to E$ définie par $L_g(x) = g \cdot x$.
- **Injectivité :** Par hypothèse, tout élément de $E$ est régulier à gauche. Ainsi, $g \cdot x = g \cdot y \implies x = y$. $L_g$ est donc injective.
- **Bijectivité :** $E$ est un ensemble fini et $L_g$ est une application injective de $E$ dans lui-même. Par propriété des ensembles finis, $L_g$ est donc une bijection.
Par un raisonnement symétrique, l'application de translation à droite $R_g : x \mapsto x \cdot g$ est également une bijection.

### 2. Existence et unicité de l'élément neutre
Soit $a \in E$. Puisque $L_a$ est surjective, il existe un élément $e \in E$ tel que $L_a(e) = a$, c'est-à-dire $a \cdot e = a$.
Montrons que $e$ est un neutre à gauche pour tout élément $x \in E$ :
- Pour tout $x \in E$, on a $a \cdot (e \cdot x) = (a \cdot e) \cdot x$ par associativité.
- Comme $a \cdot e = a$, on obtient $a \cdot (e \cdot x) = a \cdot x$.
- Par régularité à gauche de $a$, on en déduit $e \cdot x = x$. $e$ est donc un neutre à gauche.

De même, en utilisant $R_a$, on montre l'existence d'un neutre à droite $e'$ tel que $\forall x \in E, x \cdot e' = x$.
Par un résultat classique, on a $e = e \cdot e' = e'$, donc $e$ est l'unique élément neutre bilatéral de $E$.

### 3. Existence des symétriques
Soit $x \in E$.
- Puisque $L_x$ est surjective, il existe $y \in E$ tel que $L_x(y) = e$, soit $x \cdot y = e$. $y$ est un symétrique à droite de $x$.
- Puisque $R_x$ est surjective, il existe $y' \in E$ tel que $R_x(y') = e$, soit $y' \cdot x = e$. $y'$ est un symétrique à gauche de $x$.
- En utilisant l'associativité : $y' = y' \cdot e = y' \cdot (x \cdot y) = (y' \cdot x) \cdot y = e \cdot y = y$.
Ainsi, $y$ est le symétrique bilatéral de $x$.

**Conclusion :** La loi est associative, admet un élément neutre et tout élément est symétrisable. $(E, \cdot)$ est donc un groupe.