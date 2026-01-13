---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Nombres premiers", "Identités algébriques", "Nombres de Mersenne"]
---

# Énoncé
Soient $a, n \in \mathbb{N} \setminus \{0, 1\}$. On suppose que $a^n - 1$ est un nombre premier.
1. Montrer que $a = 2$.
2. Montrer que $n$ est un nombre premier.

# Indications
- Utilisez l'identité $x^n - 1 = (x-1)(1 + x + \dots + x^{n-1})$.
- Si $n$ est composé ($n=kl$), utilisez $(a^k)^l - 1$.

# Correction
1.  On a $a^n - 1 = (a-1)(1 + a + \dots + a^{n-1})$.
    Si $a > 2$, alors le premier facteur $a-1 \ge 2$.
    Le second facteur est strictement supérieur à 1 (car $n \ge 2$).
    Donc $a^n - 1$ est le produit de deux entiers strictement supérieurs à 1, il ne peut pas être premier.
    [cite_start]Il faut donc nécessairement $a-1=1$, soit $a=2$ [cite: 401-407].

2.  Supposons que $n$ n'est pas premier. Alors $n = kl$ avec $k, l \ge 2$.
    $2^n - 1 = 2^{kl} - 1 = (2^k)^l - 1$.
    On factorise de la même manière : $(2^k)^l - 1 = (2^k - 1)(1 + 2^k + \dots + 2^{k(l-1)})$.
    Comme $k \ge 2$, $2^k - 1 \ge 3$. Comme $l \ge 2$, le second facteur est $> 1$.
    Donc $2^n - 1$ est composé. Contradiction.
    [cite_start]Donc $n$ est premier [cite: 408-413].