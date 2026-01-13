---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Systèmes de congruences", "Théorème des restes chinois", "Bézout"]
---

# Énoncé
1. Résoudre dans $\mathbb{Z}$ l'équation $5x \equiv 2 [34]$.
2. Résoudre dans $\mathbb{Z}$ le système $\begin{cases} x \equiv 3 [5] \\ x \equiv 4 [7] \end{cases}$.
3. Résoudre le système $\begin{cases} x \wedge y = 3 \\ x + y = 21 \end{cases}$.

# Indications
- **Q1 :** Trouvez l'inverse de 5 modulo 34 (Bézout).
- **Q2 :** Écrivez $x = 5k + 3$ et injectez dans la seconde équation.
- **Q3 :** Posez $x = 3x'$, $y = 3y'$ avec $x' \wedge y' = 1$.

# Correction
1.  **$5x \equiv 2 [34]$**
    On cherche $u$ tel que $5u \equiv 1 [34]$.
    $34 = 6 \times 5 + 4$, $5 = 1 \times 4 + 1$.
    $1 = 5 - 4 = 5 - (34 - 6 \times 5) = 7 \times 5 - 1 \times 34$.
    Donc $7 \times 5 \equiv 1 [34]$. L'inverse est 7.
    $x \equiv 7 \times 2 \equiv 14 [34]$.
    $S = \{14 + 34k \mid k \in \mathbb{Z}\}$.

2.  **Système chinois :**
    $x \equiv 3 [5] \implies x = 5k + 3$.
    $5k + 3 \equiv 4 [7] \implies 5k \equiv 1 [7]$.
    Inverse de 5 mod 7 : $3 \times 5 = 15 \equiv 1 [7]$. Donc on multiplie par 3.
    $k \equiv 3 \times 1 \equiv 3 [7]$. Donc $k = 7j + 3$.
    $x = 5(7j + 3) + 3 = 35j + 15 + 3 = 35j + 18$.
    $S = \{18 + 35k \mid k \in \mathbb{Z}\}$.

3.  **PGCD et Somme :**
    $x = 3x'$, $y = 3y'$ avec $x' \wedge y' = 1$.
    $3x' + 3y' = 21 \implies x' + y' = 7$.
    On cherche les couples d'entiers positifs premiers entre eux dont la somme vaut 7 :
    - $(1, 6)$ : $1 \wedge 6 = 1$ (OK) $\to (3, 18)$.
    - $(2, 5)$ : $2 \wedge 5 = 1$ (OK) $\to (6, 15)$.
    - $(3, 4)$ : $3 \wedge 4 = 1$ (OK) $\to (9, 12)$.
    Et les symétriques.
    Solutions : $\{(3, 18), (6, 15), (9, 12), (12, 9), (15, 6), (18, 3)\}$.