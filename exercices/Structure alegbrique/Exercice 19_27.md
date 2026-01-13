---
chapitre: "Structures algébriques"
difficulte: "★★★★"
notions: ["p-groupe", "Centre d'un groupe", "Classes de conjugaison", "Équation aux classes"]
---

# Énoncé

Soit $p$ un entier premier. Soit $G$ un $p$-groupe, c'est-à-dire un groupe tel qu'il existe un entier $\alpha > 0$ (qu'on se fixe pour la suite) tel que $|G| = p^\alpha$. On note $e$ l'élément neutre de $G$. Soit $Z$ le centre de $G$, c'est-à-dire l'ensemble des $x \in G$ commutant avec tous les autres. Pour $x \in G$, on note $C_x$ l'ensemble des commutants de $x$ (les éléments de $G$ commutant avec $x$). 

Le but de l'exercice est de montrer que le centre de $G$ n'est pas réduit à $e$.

1. Montrer que $Z$ est un sous-groupe de $G$, ainsi que $C_x$, pour tout $x \in G$.
2. Trouver une relation entre l'ordre de $C_x$ et le cardinal de la classe de conjugaison de $x$.
3. En déduire qu'il existe $x \neq e$ tel que l'ordre de $C_x$ soit égal à $p^\alpha$, et conclure.

---

# Indications

Le cardinal de la classe de conjugaison de $x$ est le nombre de classes modulo $C_x$, donc $|G|/|C_x|$. Considérer alors la partition formée par les classes de conjugaison, et remarquer que celle de $e$ est triviale. Par étude de la divisibilité par $p$, ce ne peut pas être la seule.

---

# Correction

### 1. Structure de $Z$ et $C_x$

* **Pour le centre $Z$ :** La démonstration est identique à celle de l'Exercice 11. $e$ commute avec tous les éléments, donc $e \in Z$. Si $g, h \in Z$, leur produit commute avec tout élément $x$ car $(gh)x = g(hx) = g(xh) = (gx)h = (xg)h = x(gh)$. L'inverse d'un élément du centre y appartient également.
* **Pour le commutant $C_x$ :** Pour un $x \in G$ fixé, $e \in C_x$ car $ex = xe = x$. Si $g, h \in C_x$, alors $(gh)x = g(hx) = g(xh) = (gx)h = (xg)h = x(gh)$, donc $gh \in C_x$. Enfin, $gx=xg \implies xg^{-1} = g^{-1}x$ par multiplication bilatérale par $g^{-1}$. $C_x$ est donc un sous-groupe de $G$.

### 2. Relation entre $|C_x|$ et la classe de conjugaison

La classe de conjugaison de $x$ est l'ensemble $Orb(x) = \{gxg^{-1} \mid g \in G\}$. 
L'application $f : G/C_x \to Orb(x)$ définie par $f(gC_x) = gxg^{-1}$ est une bijection bien définie. 
D'après le théorème de Lagrange (ou le théorème orbite-stabilisateur), le cardinal de la classe de conjugaison est égal à l'indice du sous-groupe $C_x$ dans $G$ :
$$|Orb(x)| = \frac{|G|}{|C_x|}$$

### 3. Non-trivialité du centre $Z$

Utilisons l'équation aux classes, qui repose sur le fait que les classes de conjugaison forment une partition de $G$ :
$$|G| = \sum_{i=1}^n |Orb(x_i)|$$
Un élément $x$ appartient au centre $Z$ si et seulement si sa classe de conjugaison est réduite à un singleton $\{x\}$, soit $|Orb(x)| = 1$. 
Séparons les classes de cardinal 1 (les éléments de $Z$) des autres :
$$|G| = |Z| + \sum_{|Orb(x_j)| > 1} |Orb(x_j)|$$
Puisque $|G| = p^\alpha$, pour tout $x_j$, $|Orb(x_j)| = p^\alpha / |C_{x_j}| = p^{k_j}$.
Si $|Orb(x_j)| > 1$, alors $k_j \ge 1$, donc $p$ divise $|Orb(x_j)|$.
En regardant l'égalité modulo $p$ :
$$0 \equiv |Z| + 0 \pmod p \implies |Z| \equiv 0 \pmod p$$
Comme $e \in Z$, on a $|Z| \ge 1$. Puisque $|Z|$ est un multiple de $p$, on en déduit $|Z| \ge p$.
Il existe donc au moins $p$ éléments qui commutent avec tout le groupe. Comme $p \ge 2$, il existe au moins un élément $x \neq e$ tel que $x \in Z$, ce qui équivaut à $|C_x| = |G| = p^\alpha$.

**Conclusion :** Le centre $Z$ n'est pas réduit à $\{e\}$.