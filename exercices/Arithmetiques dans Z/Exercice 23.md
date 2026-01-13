---
chapitre: "Arithmétique dans Z"
difficulte: "★★★☆"
notions: ["Théorème de Wilson", "Factorielle", "Inversibles"]
---

# Énoncé
1. Soit $n$ un nombre premier.
   (a) Résoudre $x^2 \equiv 1 [n]$ dans $[\![0, n-1]\!]$.
   (b) En déduire que $(n-1)! \equiv -1 [n]$.
2. Réciproquement, montrer que si $(n-1)! \equiv -1 [n]$, alors $n$ est premier.

# Indications
- **Q1a :** $n | (x-1)(x+1)$.
- **Q1b :** Dans le produit $(n-1)!$, regroupez chaque élément avec son inverse mod $n$. Quels sont les éléments qui sont leur propre inverse ?
- **Q2 :** Si $n$ est composé, il a un diviseur $d < n$ qui divise aussi $(n-1)!$.

# Correction
1.  (a) $x^2 \equiv 1 [n] \iff n | (x-1)(x+1)$.
    Comme $n$ est premier, $n | x-1$ ou $n | x+1$.
    [cite_start]Dans $[\![0, n-1]\!]$, les solutions sont $1$ et $n-1$ (sauf si $n=2$ où $1 \equiv -1$) [cite: 446-456].
    (b) Dans le produit $\prod_{k=1}^{n-1} k$, chaque élément $k$ est multiplié par son inverse $k^{-1}$ modulo $n$.
    Les seuls éléments qui sont leur propre inverse sont 1 et $n-1$ (d'après 1a).
    Tous les autres se simplifient par paires ($k \cdot k^{-1} \equiv 1$).
    [cite_start]Il reste donc $1 \times (n-1) \equiv -1 [n]$ [cite: 458-467].

2.  Supposons $(n-1)! \equiv -1 [n]$.
    Soit $d$ un diviseur de $n$ avec $1 < d < n$.
    Alors $d$ apparaît dans le produit $1 \times 2 \times \dots \times d \times \dots \times (n-1)$.
    Donc $d$ divise $(n-1)!$.
    Comme $(n-1)! = k n - 1$, on a $1 = k n - (n-1)!$.
    $d$ divise $n$ et $(n-1)!$, donc $d$ divise 1. Impossible.
    [cite_start]Donc $n$ n'a pas de diviseur strict, il est premier [cite: 468-475].