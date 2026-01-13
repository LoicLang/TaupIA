---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Congruences", "Factorisation", "Divisibilité"]
---

# Énoncé
Soient $n \in \mathbb{N}^*$ et $a, b \in \mathbb{Z}$. Montrer que si $a \equiv b [n]$, alors $a^n \equiv b^n [n^2]$.

# Indications
- Ne pas confondre avec la compatibilité simple des puissances ($a \equiv b [n] \Rightarrow a^n \equiv b^n [n]$). Ici, le module devient $n^2$.
- Factorisez $a^n - b^n$ par $(a-b)$.
- Utilisez l'hypothèse $a = b + kn$ pour étudier la somme restante modulo $n$.

# Correction
On utilise l'identité remarquable : $a^n - b^n = (a-b) \sum_{k=0}^{n-1} a^k b^{n-1-k}$.
1.  [cite_start]Par hypothèse, $a \equiv b [n]$, donc $n$ divise $(a-b)$ [cite: 263-265].
2.  Regardons la somme $S = \sum_{k=0}^{n-1} a^k b^{n-1-k}$.
    Comme $a \equiv b [n]$, on a $a^k \equiv b^k [n]$ pour tout $k$.
    Chaque terme de la somme est congru à $b^k b^{n-1-k} = b^{n-1} [n]$.
    Il y a $n$ termes dans la somme, donc :
    $S \equiv \sum_{k=0}^{n-1} b^{n-1} \equiv n \times b^{n-1} \equiv 0 [n]$.
    [cite_start]Donc $n$ divise la somme $S$ [cite: 266-271].
3.  On a donc $a^n - b^n = (a-b) \times S$.
    Comme $n | (a-b)$ et $n | S$, leur produit est divisible par $n \times n = n^2$.
    [cite_start]Conclusion : $a^n \equiv b^n [n^2]$ [cite: 272-274].