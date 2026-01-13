---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Sous-groupe", "Racines de l'unité", "Nombres complexes", "Stabilité"]
---

# Énoncé
Montrer que l'ensemble $U_{\infty} = \{z \in \mathbb{C} \mid \exists n \in \mathbb{N}^\star, z^n = 1\}$ muni de la multiplication est un groupe.

---

# Indications
La méthode la plus efficace consiste à montrer que $U_{\infty}$ est un **sous-groupe** du groupe multiplicatif $(\mathbb{C}^\star, \times)$. Pour cela, vérifiez les trois points de la caractérisation :
1. $U_{\infty}$ est un sous-ensemble non vide de $\mathbb{C}^\star$.
2. La stabilité par produit : si $z \in U_{\infty}$ et $w \in U_{\infty}$, alors $zw \in U_{\infty}$.
3. La stabilité par inverse : si $z \in U_{\infty}$, alors $z^{-1} \in U_{\infty}$.

---

# Correction

Pour prouver que $(U_{\infty}, \times)$ est un groupe, nous allons montrer qu'il s'agit d'un sous-groupe du groupe connu $(\mathbb{C}^\star, \times)$.

### 1. Inclusion et non-vacuité
* Tout élément $z \in U_{\infty}$ vérifie $|z|^n = |z^n| = 1$ pour un certain $n \in \mathbb{N}^\star$. Comme $|z| \in \mathbb{R}_+$, cela implique $|z|=1$, donc $z \neq 0$. Ainsi, $U_{\infty} \subset \mathbb{C}^\star$.
* On a $1^1 = 1$, donc $1 \in U_{\infty}$. L'ensemble est non vide.

### 2. Stabilité par la loi (LCI)
Soient $z, w \in U_{\infty}$. Par définition :
* $\exists n \in \mathbb{N}^\star$ tel que $z^n = 1$.
* $\exists m \in \mathbb{N}^\star$ tel que $w^m = 1$.
Considérons le produit $zw$. Comme la multiplication dans $\mathbb{C}$ est associative et commutative, on a :
$$(zw)^{nm} = (z^n)^m \times (w^m)^n = 1^m \times 1^n = 1$$
Comme $nm \in \mathbb{N}^\star$, il existe bien un entier naturel non nul (ici $nm$) tel que $(zw)^{nm} = 1$.
Donc $zw \in U_{\infty}$, la loi est stable sur $U_{\infty}$.

### 3. Stabilité par passage à l'inverse
Soit $z \in U_{\infty}$. Il existe $n \in \mathbb{N}^\star$ tel que $z^n = 1$.
L'élément $z$ est inversible dans $\mathbb{C}^\star$. Son inverse est $z^{-1} = \frac{1}{z}$.
On a alors :
$$(z^{-1})^n = \frac{1}{z^n} = \frac{1}{1} = 1$$
Comme $n \in \mathbb{N}^\star$, on en déduit que $z^{-1} \in U_{\infty}$. L'ensemble est stable par inverse.

### 4. Conclusion sur la structure de groupe
$U_{\infty}$ est un sous-ensemble non vide de $\mathbb{C}^\star$, stable par multiplication et par inverse. D'après le théorème de caractérisation, $(U_{\infty}, \times)$ est un sous-groupe de $(\mathbb{C}^\star, \times)$.
Par définition d'un sous-groupe, $(U_{\infty}, \times)$ est lui-même un groupe. 

**Note sur la rigueur :** Comme $(\mathbb{C}^\star, \times)$ est un groupe abélien, les vérifications bilatérales (neutre à gauche/droite et inverse à gauche/droite) sont héritées de la structure parente. Le neutre de $U_{\infty}$ est $1$ et l'inverse de $z$ est $z^{-1}$.