---
chapitre: "Structures algébriques"
difficulte: "★★★★"
notions: ["Lemme de Cauchy", "Relation d'équivalence", "Classes d'équivalence", "Dénombrement", "Groupe fini"]
---

# Énoncé

Le but de cet exercice est de donner une démonstration rapide et efficace du lemme de Cauchy, basé sur l'étude d'une relation d'équivalence. On rappelle que le lemme de Cauchy affirme que si un nombre premier $p$ divise l'ordre de $G$, alors il existe dans $G$ un élément d'ordre $p$. Vu l'utilité de ce lemme, il peut être conseillé de retenir cette démonstration.

On définit $E \subset G^p$ l'ensemble des $p$-uplets $(x_1, \dots, x_p)$ tels que :
$$x_1 \cdot x_2 \cdot \dots \cdot x_p = e$$
On définit sur $E$ la relation $(x_1, \dots, x_p) \sim (y_1, \dots, y_p)$ si $(y_1, \dots, y_p)$ est obtenu de $(x_1, \dots, x_p)$ par permutation circulaire.

1. Montrer que $\sim$ est une relation d'équivalence.
2. Justifier que les classes d'équivalence sont de cardinal $1$ ou $p$.
3. En considérant le cardinal de $E$, en déduire que le nombre d'éléments d'ordre $p$ est congru à $-1$ modulo $p$ et conclure.

---

# Indications

- **Pour la question 2 :** Montrez d'abord que si $(x_1, \dots, x_p) \in E$, alors toutes ses permutations circulaires appartiennent aussi à $E$. En prolongeant périodiquement la suite $(x_i)$, justifiez que la période minimale est $1$ ou $p$ (car $p$ est premier).
- **Pour la question 3 :** Utilisez la partition de $E$ formée par les classes d'équivalence. Remarquez que pour dénombrer $E$, le choix libre des $p-1$ premiers termes d'un $p$-uplet détermine entièrement le dernier. N'oubliez pas la classe de l'élément trivial $(e, \dots, e)$.

---

# Correction

### 1. La relation $\sim$ est une relation d'équivalence

**Stabilité de $E$ par permutation circulaire :**
Soit $(x_1, \dots, x_p) \in E$. Alors $x_1 \cdot (x_2 \dots x_p) = e$, ce qui implique $(x_2 \dots x_p) = x_1^{-1}$.
En multipliant par $x_1$ à droite : $(x_2 \dots x_p) \cdot x_1 = x_1^{-1} \cdot x_1 = e$.
Ainsi, $(x_2, \dots, x_p, x_1) \in E$. Par récurrence, toutes les permutations circulaires d'un élément de $E$ restent dans $E$.

**Propriétés de la relation :**
- **Réflexivité :** Un élément est sa propre permutation circulaire (décalage de 0).
- **Symétrie :** Si $Y$ est un décalage de $k$ crans de $X$, alors $X$ est un décalage de $p-k$ crans de $Y$.
- **Transitivité :** La composée de deux décalages circulaires est un décalage circulaire.
$\sim$ est donc bien une relation d'équivalence.

### 2. Cardinal des classes d'équivalence

Soit $C$ une classe d'équivalence. Son cardinal correspond à l'orbite d'un élément sous l'action du décalage circulaire. Le cardinal d'une orbite divise l'ordre du groupe agissant (ici $\mathbb{Z}/p\mathbb{Z}$).
Puisque $p$ est premier, les diviseurs de $p$ sont $1$ et $p$.
- Une classe est de cardinal $1$ si et seulement si l'élément est invariant par décalage d'un cran : $x_1 = x_2 = \dots = x_p$. Comme le produit doit valoir $e$, cela revient à chercher les $x$ tels que $x^p = e$.
- Sinon, la classe est de cardinal $p$.

### 3. Preuve du Lemme de Cauchy

**Cardinal de $E$ :**
Pour construire un élément $(x_1, \dots, x_p) \in E$, on choisit librement les $p-1$ premiers éléments dans $G$ (soit $|G|^{p-1}$ choix). Le dernier élément est alors imposé : $x_p = (x_1 \dots x_{p-1})^{-1}$.
Ainsi, $|E| = |G|^{p-1}$. Comme $p$ divise $|G|$ par hypothèse, alors $p$ divise $|E|$, donc $|E| \equiv 0 \pmod p$.

**Dénombrement par classes :**
Soit $n_1$ le nombre de classes de cardinal $1$ et $n_p$ le nombre de classes de cardinal $p$.
D'après l'équation aux classes (partition de $E$) :
$$|E| = n_1 \times 1 + n_p \times p \equiv n_1 \pmod p$$
Comme $|E| \equiv 0 \pmod p$, on en déduit que $n_1 \equiv 0 \pmod p$.
Les classes de cardinal $1$ correspondent aux éléments $(x, \dots, x)$ tels que $x^p = e$.
L'élément $(e, \dots, e)$ est toujours dans $E$, donc $n_1 \ge 1$.
Puisque $n_1$ est un multiple de $p$ et $n_1 \ge 1$, alors $n_1 \ge p$.
Il existe donc au moins $p$ éléments dans $G$ vérifiant $x^p = e$. En excluant le neutre, il reste au moins $p-1$ éléments d'ordre $p$ (car $p$ est premier).
On a bien $n_1 - 1 \equiv -1 \pmod p$.

**Conclusion :** Il existe au moins un (et même au moins $p-1$) élément d'ordre $p$ dans $G$.