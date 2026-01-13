---
chapitre: "Arithmétique dans Z"
difficulte: "★☆☆☆"
notions: ["Base 10", "Critères de divisibilité", "Congruences"]
---

# Énoncé
Soit $n \in \mathbb{N}$. On note $a_0, \dots, a_r$ les chiffres de $n$ en base 10 (c'est-à-dire $n = \sum_{k=0}^r a_k 10^k$).
1. Montrer que $n$ est divisible par 4 si et seulement si l'entier formé par ses deux derniers chiffres ($a_0 + 10a_1$) l'est.
2. Montrer que $n$ est divisible par 3 (respectivement 9) si et seulement si la somme de ses chiffres $\sum a_k$ l'est.
3. Déterminer une condition nécessaire et suffisante sur les chiffres pour que $n$ soit divisible par 11.

# Indications
- Écrivez la décomposition de $n$ en base 10.
- **Q1 :** Remarquez que $100$ est un multiple de 4.
- **Q2 :** Utilisez $10 \equiv 1 [3]$ (et modulo 9).
- **Q3 :** Utilisez $10 \equiv -1 [11]$.

# Correction
1. **Divisibilité par 4 :**
   Pour $k \ge 2$, $10^k = 100 \times 10^{k-2} = 4 \times 25 \times 10^{k-2} \equiv 0 [4]$.
   Donc $n = \sum_{k=0}^r a_k 10^k \equiv a_0 + 10a_1 + 0 + \dots [4]$.
   [cite_start]$n$ est divisible par 4 ssi $a_0 + 10a_1$ est divisible par 4 [cite: 229-233].

2. **Divisibilité par 3 et 9 :**
   $10 \equiv 1 [3] \implies \forall k, 10^k \equiv 1 [3]$.
   Donc $n = \sum a_k 10^k \equiv \sum a_k [3]$.
   $n$ est divisible par 3 ssi la somme de ses chiffres l'est. [cite_start]La démonstration est identique modulo 9 [cite: 213-217].

3. **Divisibilité par 11 :**
   $10 \equiv -1 [11] \implies 10^k \equiv (-1)^k [11]$.
   Donc $n = \sum_{k=0}^r a_k 10^k \equiv \sum_{k=0}^r a_k (-1)^k [11]$.
   [cite_start]$n$ est divisible par 11 ssi la somme alternée de ses chiffres ($a_0 - a_1 + a_2 - \dots$) est divisible par 11 [cite: 218-223].