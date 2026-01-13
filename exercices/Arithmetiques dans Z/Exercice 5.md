---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Divisibilité", "Congruences", "Analyse-Synthèse", "Système de congruences"]
---

# Énoncé
1. Montrer que, pour tout $n \in \mathbb{Z}$, le nombre $n(n+2)(7n-5)$ est divisible par 6.
2. Pour quels entiers $n \in \mathbb{Z}$ l'entier $n+1$ divise-t-il $n+7$ ?
3. Pour quels entiers $n \in \mathbb{Z}$ l'entier $n^2+(n+1)^2+(n+3)^2$ est-il divisible par 10 ?

# Indications
- **Q1 :** Remarquez que $7n-5 \equiv n+1 [6]$. Vous vous ramenez au produit de trois entiers consécutifs.
- **Q2 :** Utilisez le fait que si $a | b$, alors $a | b - a$. Cela permet d'éliminer $n$.
- **Q3 :** Étudiez la divisibilité par 2 et par 5 séparément ($10 = 2 \times 5$). Réduisez l'expression modulo 2 et modulo 5.

# Correction
1. **Divisibilité par 6 :**
   On travaille modulo 6 : $7n - 5 \equiv n + 1 [6]$ (car $7 \equiv 1$ et $-5 \equiv 1$).
   Donc $n(n+2)(7n-5) \equiv n(n+2)(n+1) [6]$.
   Le terme $n(n+1)(n+2)$ est le produit de trois entiers consécutifs. Parmi eux, il y a nécessairement un multiple de 3 et au moins un multiple de 2 (pair). [cite_start]Le produit est donc divisible par $2 \times 3 = 6$ [cite: 183-187].

2. **Diviseurs de $n+7$ :**
   **Analyse :** Si $n+1 | n+7$, alors $n+1$ divise aussi $(n+7) - (n+1) = 6$.
   Les diviseurs de 6 dans $\mathbb{Z}$ sont $D_6 = \{-6, -3, -2, -1, 1, 2, 3, 6\}$.
   On a donc $n+1 \in D_6$, soit $n \in \{-7, -4, -3, -2, 0, 1, 2, 5\}$.
   **Synthèse :** On vérifie que ces valeurs conviennent (c'est toujours vrai ici par construction).
   [cite_start]$S = \{-7, -4, -3, -2, 0, 1, 2, 5\}$ [cite: 188-194].

3. **Divisibilité par 10 :**
   Posons $A = n^2 + (n+1)^2 + (n+3)^2 = 3n^2 + 8n + 10 \equiv 3n^2 + 8n [10]$.
   On cherche $n$ tel que $A \equiv 0 [10]$, ce qui équivaut à $A \equiv 0 [2]$ **et** $A \equiv 0 [5]$.
   * **Modulo 2 :** $3n^2 + 8n \equiv n^2 \equiv n [2]$. [cite_start]Donc $n$ doit être **pair** ($n \equiv 0 [2]$) [cite: 202-209].
   * **Modulo 5 :** $3n^2 + 8n \equiv 3n^2 + 3n = 3n(n+1) [5]$.
       Comme 5 est premier, $5 | 3n(n+1) \iff 5 | n$ ou $5 | n+1$.
       [cite_start]Donc $n \equiv 0 [5]$ ou $n \equiv -1 \equiv 4 [5]$ [cite: 210-212].
   * **Bilan :** On cherche les entiers pairs qui sont congrus à 0 ou 4 modulo 5.
       - Si $n \equiv 0 [5]$ et $n$ pair $\implies n$ multiple de 10 ($n \equiv 0 [10]$).
       - Si $n \equiv 4 [5]$ et $n$ pair $\implies n$ se termine par 4 ($n \equiv 4 [10]$).
   
   [cite_start]$S = \{10k \mid k \in \mathbb{Z}\} \cup \{10k + 4 \mid k \in \mathbb{Z}\}$ [cite: 224-228].