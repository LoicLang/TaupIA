---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Valuation p-adique", "Puissances parfaites", "Premiers entre eux"]
---

# Énoncé
Soient $a, b \in \mathbb{N}^*$ et $k \in \mathbb{N} \setminus \{0, 1\}$.
Montrer que si $a$ et $b$ sont premiers entre eux, et si $ab$ est la puissance $k$-ième d'un entier, alors $a$ et $b$ sont eux-mêmes des puissances $k$-ièmes d'entiers.

# Indications
- Utilisez la décomposition en facteurs premiers via la valuation $p$-adique $v_p$.
- Si $ab = c^k$, quelle relation a-t-on sur les exposants $v_p(a) + v_p(b)$ ?
- Utilisez $a \wedge b = 1$ pour montrer que pour tout $p$, soit $v_p(a) = 0$, soit $v_p(b) = 0$.

# Correction
Soit $c$ tel que $ab = c^k$.
[cite_start]Pour tout nombre premier $p$, on a $v_p(ab) = v_p(c^k)$, donc $v_p(a) + v_p(b) = k v_p(c)$[cite: 355].
Comme $a \wedge b = 1$, $a$ et $b$ n'ont aucun facteur premier en commun.
Pour un $p$ donné :
- Soit $p$ ne divise pas $a$ ($v_p(a)=0$), alors $v_p(b) = k v_p(c)$, qui est un multiple de $k$.
- Soit $p$ ne divise pas $b$ ($v_p(b)=0$), alors $v_p(a) = k v_p(c)$, qui est un multiple de $k$.
[cite_start]Dans tous les cas, pour tout premier $p$, $v_p(a)$ est un multiple de $k$ et $v_p(b)$ est un multiple de $k$ [cite: 356-357].
[cite_start]Cela signifie exactement que $a$ et $b$ sont des puissances $k$-ièmes parfaites [cite: 388-392].