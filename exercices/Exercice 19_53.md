---
chapitre: "Structures algébriques"
difficulte: "★★★★"
notions: ["Corps fini", "Groupe cyclique", "Exposant d'un groupe", "Racines de polynômes"]
---

# Énoncé

Soit $\mathbb{K}$ un corps fini. On admet que tout polynôme non nul à coefficients dans $\mathbb{K}$, de degré $n \ge 0$, admet au plus $n$ racines. Soit $n = |\mathbb{K}| - 1$.

1. Montrer que tout élément de $\mathbb{K}^*$ est racine de $X^n - 1$.
2. Montrer que s'il n'existe pas un élément de $\mathbb{K}^*$ dont l'ordre est $n$, il existe $p < n$ tel que tout élément de $\mathbb{K}^*$ soit racine de $X^p - 1$.
3. En déduire que $(\mathbb{K}^*, \times)$ est un groupe cyclique.

---

# Indications

1. Utilisez le théorème de **Lagrange** appliqué au groupe multiplicatif $(\mathbb{K}^*, \times)$.
2. $(\mathbb{K}^*, \times)$ est un groupe abélien fini. Utilisez le théorème de l'**exposant** : il existe un élément dont l'ordre est le PPCM des ordres de tous les éléments.
3. Comparez le nombre de racines potentielles au degré du polynôme $X^p - 1$.

---

# Correction

### 1. Application du théorème de Lagrange
Le groupe $(\mathbb{K}^*, \times)$ est un groupe multiplicatif de cardinal $n = |\mathbb{K}| - 1$. 
D'après le corollaire du théorème de Lagrange, l'ordre de tout élément $x \in \mathbb{K}^*$ divise l'ordre du groupe $n$. 
On a donc $x^n = 1$ pour tout $x \in \mathbb{K}^*$. 
Ceci signifie que tout élément de $\mathbb{K}^*$ est racine du polynôme $P(X) = X^n - 1$.

### 2. Utilisation de l'exposant du groupe
$(\mathbb{K}^*, \times)$ est un groupe abélien fini. 
Notons $e$ l'exposant du groupe, défini comme le PPCM des ordres de tous les éléments de $\mathbb{K}^*$. 
D'après les propriétés des groupes abéliens finis, il existe un élément dans le groupe dont l'ordre est exactement $e$. 
* Si aucun élément n'est d'ordre $n$, alors nécessairement $e < n$ (car $e$ divise toujours $n$ par Lagrange).
* Par définition de l'exposant, pour tout $x \in \mathbb{K}^*$, $x^e = 1$. 
En posant $p = e$, on a $p < n$ et chaque élément de $\mathbb{K}^*$ est racine de $X^p - 1$.

### 3. Conclusion par l'absurde
Supposons que le groupe $(\mathbb{K}^*, \times)$ ne soit pas cyclique. 
D'après la question précédente, il existerait alors un entier $p < n$ tel que tous les éléments de $\mathbb{K}^*$ soient racines du polynôme $Q(X) = X^p - 1$. 
Or, le groupe $\mathbb{K}^*$ contient exactement $n$ éléments distincts. Le polynôme $Q$ de degré $p$ possèderait donc $n$ racines distinctes.
Ceci contredit l'hypothèse de l'énoncé selon laquelle un polynôme de degré $p$ admet au plus $p$ racines dans $\mathbb{K}$. 
Par l'absurde, l'exposant $e$ doit être égal à $n$. 
Il existe donc un élément d'ordre $n$ dans $(\mathbb{K}^*, \times)$, ce qui prouve que le groupe est cyclique.