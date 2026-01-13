---
chapitre: "Arithmétique dans Z"
difficulte: "★☆☆☆"
notions: ["PGCD", "Algorithme d'Euclide", "Premiers entre eux"]
---

# Énoncé
Soit $n \in \mathbb{Z}$. Justifier que les entiers $n^3 + n^2 + 1$ et $n^2 - n + 1$ sont premiers entre eux.

# Indications
- Utilisez l'algorithme d'Euclide comme si vous divisiez des polynômes.
- Le but est d'obtenir un reste constant (égal à 1).

# Correction
On applique l'algorithme d'Euclide successif :
1.  $(n^3 + n^2 + 1) = (n+2)(n^2 - n + 1) + (n - 1)$.
    [cite_start]Le premier reste est $R_1 = n - 1$[cite: 286].
2.  On divise maintenant le diviseur précédent par ce reste :
    $(n^2 - n + 1) = n(n - 1) + 1$.
    [cite_start]Le second reste est $R_2 = 1$[cite: 287].
[cite_start]Le dernier reste non nul est 1, donc le PGCD vaut 1. Les deux entiers sont toujours premiers entre eux [cite: 289-290].