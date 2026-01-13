---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Équations diophantiennes", "Algorithme d'Euclide étendu", "Théorème de Bézout"]
---

# Énoncé
Résoudre les équations suivantes dans $\mathbb{Z}^2$ :
1. $131x + 28y = 2$
2. $15x + 6y = 3$
3. $42x + 28y = 14$
4. $9x + 270y = 7$

# Indications
- Vérifiez d'abord si le PGCD des coefficients divise le second membre. Si non, pas de solution.
- Trouvez une solution particulière $(x_0, y_0)$ (Bézout ou évidente).
- La solution générale est de la forme $(x_0 + k \frac{b}{d}, y_0 - k \frac{a}{d})$.

# Correction
1.  **$131x + 28y = 2$**
    PGCD(131, 28) : $131 = 4 \times 28 + 19$, $28 = 1 \times 19 + 9$, $19 = 2 \times 9 + 1$. Donc PGCD = 1.
    Remontée d'Euclide : $1 = 19 - 2 \times 9 = 19 - 2(28 - 19) = 3 \times 19 - 2 \times 28 = 3(131 - 4 \times 28) - 2 \times 28 = 3 \times 131 - 14 \times 28$.
    Solution pour $=1$ : $(3, -14)$. Pour $=2$ : $(6, -28)$.
    Solution générale : $S = \{(6 + 28k, -28 - 131k) \mid k \in \mathbb{Z}\}$.

2.  **$15x + 6y = 3$**
    PGCD(15, 6) = 3. Comme 3 divise 3, il y a des solutions.
    Simplification par 3 : $5x + 2y = 1$.
    Solution évidente : $5(1) + 2(-2) = 1$. $(x_0, y_0) = (1, -2)$.
    Solution générale : $S = \{(1 + 2k, -2 - 5k) \mid k \in \mathbb{Z}\}$.

3.  **$42x + 28y = 14$**
    PGCD(42, 28) = 14. Comme 14 divise 14, solutions possibles.
    Simplification par 14 : $3x + 2y = 1$.
    Solution évidente : $3(1) + 2(-1) = 1$.
    Solution générale : $S = \{(1 + 2k, -1 - 3k) \mid k \in \mathbb{Z}\}$.

4.  **$9x + 270y = 7$**
    PGCD(9, 270) = 9 (car $270 = 9 \times 30$).
    Comme 9 ne divise pas 7, il n'y a **aucune solution**.