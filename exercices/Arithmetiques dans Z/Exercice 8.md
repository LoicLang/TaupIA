---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Nombres premiers", "Divisibilité", "Congruences"]
---

# Énoncé
Soit $p$ un nombre premier tel que $p \notin \{2, 3\}$. Montrer que $p^2 - 1$ est divisible par 24.

# Indications
- $24 = 3 \times 8$. Montrez la divisibilité par 3 et par 8 séparément.
- Factorisez $p^2 - 1 = (p-1)(p+1)$.
- Utilisez le fait que $p$ est impair et non multiple de 3.

# Correction
On veut montrer que $24 | (p-1)(p+1)$. Comme $3 \wedge 8 = 1$, il suffit de montrer que le produit est divisible par 3 et par 8.

1.  **Divisibilité par 8 :**
    $p$ est premier et $p \neq 2$, donc $p$ est impair.
    Ainsi, $p-1$ et $p+1$ sont deux entiers pairs consécutifs.
    Le produit de deux pairs consécutifs est toujours divisible par 8 (l'un est multiple de 2, l'autre est multiple de 4, donc $2 \times 4 = 8$).
    [cite_start]Donc $8 | p^2 - 1$ [cite: 249-251].

2.  **Divisibilité par 3 :**
    $p$ est premier et $p \neq 3$, donc $p$ n'est pas divisible par 3.
    Donc $p \equiv 1 [3]$ ou $p \equiv 2 [3]$.
    - Si $p \equiv 1 [3]$, alors $p-1 \equiv 0 [3]$, donc $3 | p-1$.
    - Si $p \equiv 2 [3]$, alors $p+1 \equiv 3 \equiv 0 [3]$, donc $3 | p+1$.
    [cite_start]Dans les deux cas, le produit $(p-1)(p+1)$ est divisible par 3 [cite: 256-260].

[cite_start]**Conclusion :** $p^2 - 1$ est divisible par $3 \times 8 = 24$ [cite: 261-262].