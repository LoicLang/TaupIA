---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Nombres premiers", "Infinitude des premiers"]
---

# Énoncé
Pour tout $n \in \mathbb{N}^*$, on note $p_n$ le $n$-ième nombre premier. Montrer que :
$$p_{n+1} < p_1 p_2 \dots p_n$$
(L'énoncé original mentionne $p_{n+1} < p_1 \dots p_n$ pour $n \ge 2$, car pour $n=1$, $3 \not< 2$).

# Indications
- Considérez l'entier $N = p_1 p_2 \dots p_n - 1$.
- Montrez que $N$ admet un diviseur premier $p$.
- Montrez que ce $p$ est distinct de tous les $p_i$ pour $i \le n$.

# Correction
Posons $P = p_1 \dots p_n - 1$.
Comme $n \ge 2$, $P \ge 2 \times 3 - 1 = 5$, donc $P$ admet au moins un diviseur premier $q$.
Si $q$ était l'un des $p_1, \dots, p_n$, alors $q$ diviserait le produit $p_1 \dots p_n$.
Comme $q$ divise aussi $P$, il diviserait leur différence : $(p_1 \dots p_n) - P = 1$. Impossible.
[cite_start]Donc $q$ est un nombre premier qui n'est pas dans la liste $\{p_1, \dots, p_n\}$[cite: 394].
Par conséquent, $q \ge p_{n+1}$.
Or $q$ divise $P$, donc $q \le P$.
[cite_start]Ainsi : $p_{n+1} \le q \le p_1 \dots p_n - 1 < p_1 \dots p_n$ [cite: 396-399].