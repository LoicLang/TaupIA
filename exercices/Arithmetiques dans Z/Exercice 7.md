---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Congruences", "Carrés modulo n"]
---

# Énoncé
Soient $x, y \in \mathbb{Z}$. Montrer que $x^2 + y^2$ est divisible par 7 si et seulement si $x$ et $y$ sont tous deux divisibles par 7.

# Indications
- Calculez les carrés possibles modulo 7 (les résidus quadratiques).
- Cherchez si une somme de deux de ces carrés peut valoir 0 modulo 7 autrement que par $0+0$.

# Correction
**Sens direct ($\Leftarrow$) :** Si $7|x$ et $7|y$, alors $x \equiv 0$ et $y \equiv 0 [7]$, donc $x^2 + y^2 \equiv 0 [7]$. C'est trivial.

**Sens réciproque ($\Rightarrow$) :**
On calcule les carrés modulo 7 :
$0^2 \equiv 0$, $1^2 \equiv 1$, $2^2 \equiv 4$, $3^2 \equiv 2$.
[cite_start]Comme $(-k)^2 \equiv k^2$, les seules valeurs possibles pour un carré modulo 7 sont $\{0, 1, 2, 4\}$[cite: 240].
On cherche à obtenir $0$ en sommant deux valeurs de cet ensemble :
- $0 + 0 = 0$ (OK)
- $0 + 1 \neq 0$, $0 + 2 \neq 0$, $0 + 4 \neq 0$
- $1 + 1 = 2$, $1 + 2 = 3$, $1 + 4 = 5$
- $2 + 2 = 4$, $2 + 4 = 6$
- $4 + 4 = 8 \equiv 1$
La seule solution est $0+0$. Donc $x^2 \equiv 0 [7]$ et $y^2 \equiv 0 [7]$.
[cite_start]Comme 7 est premier, cela implique $x \equiv 0 [7]$ et $y \equiv 0 [7]$ [cite: 241-247].