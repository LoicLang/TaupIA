---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Congruences", "Petit Théorème de Fermat", "Somme géométrique"]
---

# Énoncé
1. [cite_start]Montrer que pour tout $n \in \mathbb{N}$, l'entier $3^{2n} - 1$ est divisible par 8[cite: 13].
2. [cite_start]Montrer que $4^{1001} + 11$ est divisible par 15[cite: 14].
3. [cite_start]Montrer que $2^{123} + 3^{121}$ est divisible par 11[cite: 15].
4. [cite_start]Montrer que $3^{126} + 5^{126}$ est un multiple de 13[cite: 16].
5. Calculer le reste de la division euclidienne de :
   (a) [cite_start]$1357^{2013}$ par 5[cite: 18].
   (b) [cite_start]$3^{2189}$ par 25[cite: 19].
   (c) [cite_start]$49^{90021}$ par 13[cite: 20].

# Indications
- **Q1 :** Remarquez que $3^{2n} = (3^2)^n = 9^n$ et utilisez une congruence modulo 8.
- **Q2 :** Cherchez la période des puissances de 4 modulo 15 ou remarquez $4^2 \equiv 1 [15]$.
- **Q3 :** Petit théorème de Fermat pour réduire les exposants modulo 10 (car 11 est premier).
- **Q5a :** Réduisez la base modulo 5 puis l'exposant modulo 4 (Fermat).

# Correction
1. **Méthode 1 :** $3^{2n} - 1 = 9^n - 1^n = (9-1)\sum_{k=0}^{n-1} 9^k = 8 \times K$.
   [cite_start]**Méthode 2 :** $9 \equiv 1 [8] \implies 9^n \equiv 1 [8] \implies 3^{2n} - 1 \equiv 0 [8]$[cite: 120, 123].
2. $4^2 = 16 \equiv 1 [15]$. Donc $4^{1001} = (4^2)^{500} \times 4 \equiv 1^{500} \times 4 \equiv 4 [15]$.
   [cite_start]Alors $4^{1001} + 11 \equiv 4 + 11 \equiv 15 \equiv 0 [15]$[cite: 127, 128].
3. Modulo 11 : $2^5 = 32 \equiv -1 \implies 2^{10} \equiv 1$.
   $2^{123} = (2^5)^{24} \times 2^3 \equiv (-1)^{24} \times 8 \equiv 8 [11]$.
   $3^5 = 243 = 22 \times 11 + 1 \equiv 1 [11]$.
   $3^{121} = (3^5)^{24} \times 3 \equiv 1 \times 3 \equiv 3 [11]$.
   [cite_start]Somme : $8 + 3 = 11 \equiv 0 [11]$[cite: 130, 131, 134, 136].
4. Modulo 13 : $3^3 = 27 \equiv 1 [13]$ et $5^2 = 25 \equiv -1 [13]$.
   $3^{126} = (3^3)^{42} \equiv 1^{42} \equiv 1$.
   $5^{126} = (5^2)^{63} \equiv (-1)^{63} \equiv -1$.
   [cite_start]Somme : $1 + (-1) = 0 [13]$[cite: 142, 143, 144].
5. **(a)** $1357 \equiv 2 [5]$. D'après Fermat, $2^4 \equiv 1 [5]$. $2013 = 4 \times 503 + 1$.
   [cite_start]$1357^{2013} \equiv 2^{2013} \equiv (2^4)^{503} \times 2^1 \equiv 2 [5]$[cite: 150, 153].
   **(b)** $3^3 = 27 \equiv 2 [25]$. $(3^3)^7 = 3^{21} \equiv 2^7 = 128 \equiv 3 [25]$.
   $25 | 3^{21} - 3 \implies 25 | 3(3^{20}-1)$. Comme $25 \wedge 3 = 1$, $3^{20} \equiv 1 [25]$.
   $2189 = 20 \times 109 + 9$. $3^{2189} \equiv (3^{20})^{109} \times 3^9 \equiv 3^9$.
   [cite_start]Or $3^9 = (3^3)^3 = 27^3 \equiv 2^3 = 8 [25]$[cite: 155, 157].
   **(c)** Modulo 13 : $49 \equiv -3 \equiv 10$. Fermat : $49^{12} \equiv 1 [13]$.
   $90021 = 12 \times 7501 + 9$.
   [cite_start]$49^{90021} \equiv 49^9 \equiv (-3)^9 = -(3^3)^3 = -27^3 \equiv -1^3 = -1 \equiv 12 [13]$[cite: 159, 160].