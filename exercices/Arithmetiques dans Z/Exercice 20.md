---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Nombres premiers", "Infinitude des nombres premiers"]
---

# Énoncé
Pour tout $n \in \mathbb{N}^*$, on note $p_n$ le $n$-ième nombre premier ($p_1=2, p_2=3, \dots$).
Montrer que pour tout $n \in \mathbb{N} \setminus \{0, 1\}$ :
$$p_{n+1} < p_1 p_2 \dots p_n$$

# Indications
- Considérez l'entier $N = p_1 p_2 \dots p_n - 1$.
- Justifiez que $N$ admet au moins un diviseur premier $q$.
- Montrez que ce diviseur $q$ est nécessairement distinct de tous les $p_i$ pour $i \le n$.
- Concluez en comparant $p_{n+1}$ et $q$.

# Correction
Soit $n \ge 2$. Posons $P = p_1 p_2 \dots p_n - 1$.
Comme $n \ge 2$, le produit contient au moins $p_1 p_2 = 6$, donc $P \ge 5$.
$P$ est un entier strictement supérieur à 1, donc il admet au moins un diviseur premier, notons-le $q$.
Si $q$ était l'un des nombres $p_1, \dots, p_n$, alors $q$ diviserait le produit $p_1 \dots p_n$.
Comme $q$ divise $P$ et le produit, il diviserait leur différence : $(p_1 \dots p_n) - P = 1$.
C'est impossible.
Donc $q$ est un nombre premier qui n'appartient pas à la liste $\{p_1, \dots, p_n\}$.
Puisque $p_{n+1}$ est le plus petit nombre premier n'appartenant pas à cette liste (par définition de l'ordre croissant), on a nécessairement $p_{n+1} \le q$.
Or, $q$ divise $P$, donc $q \le P$.
[cite_start]On obtient finalement : $p_{n+1} \le q \le p_1 \dots p_n - 1 < p_1 \dots p_n$ [cite: 74-76, 393-399].