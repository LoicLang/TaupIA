---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Corps", "Idéal", "Anneau commutatif", "Inversibilité"]
---

# Énoncé
Soit $A$ un anneau commutatif non réduit à $\{0\}$. Montrer que $A$ est un corps si et seulement si les seuls idéaux de $A$ sont $\{0\}$ et $A$.

---

# Indications
- **Sens direct ($\implies$) :** Si un idéal $I$ contient un élément non nul $x$, utilisez l'existence de son inverse pour montrer que $1 \in I$.
- **Sens réciproque ($\impliedby$) :** Pour tout $x \neq 0$, considérez l'idéal principal engendré par $x$ (noté $xA$) et montrez qu'il doit contenir $1$.

---

# Correction

Nous devons démontrer une équivalence ($\iff$). Soit $A$ un anneau commutatif.

### 1. Sens direct ($\implies$)
Supposons que $A$ est un corps. Soit $I$ un idéal de $A$.
* Si $I = \{0\}$, la condition est vérifiée.
* Si $I \neq \{0\}$, alors il existe un élément $x \in I$ tel que $x \neq 0$.
* Puisque $A$ est un corps, tout élément non nul est inversible. Il existe donc $x^{-1} \in A$ tel que $x \cdot x^{-1} = 1$.
* Par définition d'un idéal, le produit d'un élément de $A$ par un élément de $I$ appartient à $I$. Ainsi, $1 = x^{-1} \cdot x \in I$.
* Puisque $1 \in I$, alors pour tout $a \in A$, $a = a \cdot 1 \in I$.
* On en déduit $I = A$.
Les seuls idéaux d'un corps sont donc $\{0\}$ et $A$.

### 2. Sens réciproque ($\impliedby$)
Supposons que les seuls idéaux de $A$ sont $\{0\}$ et $A$. Pour montrer que $A$ est un corps, nous devons prouver que tout élément non nul de $A$ est inversible.
Soit $x \in A$ tel que $x \neq 0$.
* Considérons l'ensemble $xA = \{x \cdot a \mid a \in A\}$. On vérifie facilement que $xA$ est un idéal de $A$ (appelé idéal principal engendré par $x$).
* Puisque $x = x \cdot 1$, on a $x \in xA$. Comme $x \neq 0$, l'idéal $xA$ n'est pas réduit à $\{0\}$.
* Par hypothèse, le seul idéal non nul de $A$ est $A$ lui-même. Par conséquent, $xA = A$.
* En particulier, l'élément neutre $1$ appartient à $xA$.
* Il existe donc un élément $y \in A$ tel que $x \cdot y = 1$.
* Comme l'anneau est commutatif, $x \cdot y = y \cdot x = 1$.
* L'élément $x$ est donc inversible.

**Conclusion :** Tout élément non nul de $A$ est inversible, $A$ est donc un corps.