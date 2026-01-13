---
chapitre: "Arithmétique dans Z"
difficulte: "★★★☆"
notions: ["Nombres de Fermat", "Premiers entre eux", "Récurrence"]
---

# Énoncé
1. Soit $n \in \mathbb{N}^*$. Montrer que si $2^n + 1$ est premier, alors $n$ est une puissance de 2.
2. Pour tout $n \in \mathbb{N}$, on pose $F_n = 2^{2^n} + 1$.
   (a) Montrer que $F_{n+1} = F_0 F_1 \dots F_n + 2$.
   (b) En déduire que pour $m \neq n$, $F_m$ et $F_n$ sont premiers entre eux.

# Indications
- **Q1 :** Si $n$ a un facteur impair $m > 1$, écrivez $n = m \times 2^k$ et utilisez $x^m + 1 = (x+1)(\dots)$ pour $m$ impair.
- **Q2a :** Récurrence et identité remarquable $(x-1)(x+1) = x^2 - 1$.
- **Q2b :** Si $d$ divise $F_n$ et $F_m$ (avec $m < n$), alors $d$ divise le produit des $F_k$ et $F_n$. Utilisez la relation précédente.

# Correction
1.  Supposons que $n$ ne soit pas une puissance de 2. Il admet un diviseur impair $q > 1$.
    $n = q \times 2^k$. Posons $X = 2^{2^k}$. Alors $2^n + 1 = X^q + 1$.
    Comme $q$ est impair, $X+1$ divise $X^q + 1$ (identité $a^q + b^q$).
    $2^{2^k} + 1$ est un diviseur strict de $2^n + 1$ (car $q > 1$). [cite_start]Donc $2^n + 1$ n'est pas premier [cite: 415-422].

2.  (a) Par récurrence. $F_0 = 3$. $F_1 = 5 = 3 + 2$.
    Hérédité : $P_n = \prod_{k=0}^n F_k = F_0 \dots F_{n-1} F_n = (F_n - 2)F_n = (2^{2^n}-1)(2^{2^n}+1) = 2^{2^{n+1}} - 1 = F_{n+1} - 2$.
    [cite_start]Donc $F_{n+1} = P_n + 2$ [cite: 423-431].
    (b) Soit $m < n$. $d = F_n \wedge F_m$.
    $d$ divise $F_m$, donc $d$ divise le produit $F_0 \dots F_n$.
    Or $F_n = F_0 \dots F_{n-1} + 2$.
    Donc $d$ divise $F_n$ et le produit. Il divise donc leur différence : 2.
    Comme les $F_n$ sont impairs, $d$ ne peut pas être 2.
    [cite_start]Donc $d=1$ [cite: 432-441].