---
chapitre: "Arithmétique dans Z"
difficulte: "★☆☆☆"
notions: ["PGCD", "Théorème de Bézout", "Fractions"]
---

# Énoncé
Soit $n \in \mathbb{N}$. [cite_start]La fraction $f = \frac{21n+4}{14n+3}$ est-elle irréductible ? [cite: 21, 22]

# Indications
- Une fraction est irréductible si le numérateur et le dénominateur sont premiers entre eux.
- Cherchez une combinaison linéaire de $(21n+4)$ et $(14n+3)$ qui élimine $n$ (relation de Bézout).

# Correction
On cherche à éliminer $n$ par combinaison linéaire :
[cite_start]$3(14n+3) - 2(21n+4) = (42n + 9) - (42n + 8) = 1$[cite: 165].
On a trouvé deux entiers $u=3$ et $v=-2$ tels que $u(14n+3) + v(21n+4) = 1$.
[cite_start]D'après le **théorème de Bézout**, cela signifie que $(14n+3) \wedge (21n+4) = 1$[cite: 166].
[cite_start]La fraction est donc toujours irréductible[cite: 168].