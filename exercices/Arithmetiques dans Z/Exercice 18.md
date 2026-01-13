---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Valuation p-adique", "Divisibilité", "PGCD"]
---

# Énoncé
Soient $a, b \in \mathbb{Z}$ et $n \in \mathbb{N}$.
1. Montrer que si $a^2$ divise $b^2$, alors $a$ divise $b$.
2. Montrer que $(a \wedge b)^n = a^n \wedge b^n$.

# Indications
- Utilisez la valuation $p$-adique $v_p(x)$ (exposant de $p$ dans la décomposition de $x$).
- Rappelez-vous que $v_p(x^k) = k v_p(x)$ et $x | y \iff \forall p, v_p(x) \le v_p(y)$.
- Rappelez-vous que $v_p(a \wedge b) = \min(v_p(a), v_p(b))$.

# Correction
1.  **Divisibilité :**
    $a^2 | b^2 \iff \forall p \in \mathbb{P}, v_p(a^2) \le v_p(b^2)$.
    $\iff \forall p, 2 v_p(a) \le 2 v_p(b)$.
    $\iff \forall p, v_p(a) \le v_p(b)$ (en divisant par 2).
    [cite_start]$\iff a | b$ [cite: 365-373].

2.  **PGCD et puissance :**
    Pour tout nombre premier $p$ :
    $v_p((a \wedge b)^n) = n \times v_p(a \wedge b) = n \times \min(v_p(a), v_p(b))$.
    $v_p(a^n \wedge b^n) = \min(v_p(a^n), v_p(b^n)) = \min(n v_p(a), n v_p(b))$.
    Comme $n \ge 0$, on peut sortir le $n$ du minimum : $\min(nx, ny) = n \min(x, y)$.
    Les valuations sont identiques pour tout $p$, donc les entiers sont égaux :
    [cite_start]$(a \wedge b)^n = a^n \wedge b^n$ [cite: 374-382].