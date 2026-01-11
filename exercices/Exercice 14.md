---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Sous-anneau", "Corps", "Automorphisme d'anneau", "Éléments inversibles"]
---

# Énoncé
On pose $\mathbb{Z}[i] = \{a + ib, (a, b) \in \mathbb{Z}^2\}$.

1. Montrer que $\mathbb{Z}[i]$ est un sous-anneau de $\mathbb{C}$. S'agit-il d'un corps ?
2. Montrer que la conjugaison est un automorphisme de l'anneau $\mathbb{Z}[i]$.
3. Quels sont les éléments inversibles de $\mathbb{Z}[i]$ ?

---

# Indications
- **Sous-anneau :** Vérifiez que $\mathbb{Z}[i]$ est un sous-groupe de $(\mathbb{C}, +)$, qu'il contient $1$ et qu'il est stable par multiplication.
- **Corps :** Un corps est un anneau où tout élément non nul est inversible. Testez l'inversibilité d'un élément simple comme $2$.
- **Automorphisme :** Vérifiez que la conjugaison $z \mapsto \bar{z}$ est un morphisme d'anneau (compatible avec $+$ et $\times$, et $f(1)=1$) et qu'elle est bijective de $\mathbb{Z}[i]$ dans lui-même.
- **Éléments inversibles :** Soit $z = a+ib \in \mathbb{Z}[i]$. Si $z$ est inversible, alors son inverse $z^{-1}$ est dans $\mathbb{Z}[i]$. Utilisez la norme au carré $N(z) = |z|^2 = a^2+b^2$ et montrez que $N(z)$ doit être un diviseur de $1$ dans $\mathbb{Z}$.

---

# Correction

### 1. Structure de $\mathbb{Z}[i]$
**Sous-anneau :**
Pour montrer que $\mathbb{Z}[i]$ est un sous-anneau de $(\mathbb{C}, +, \times)$, vérifions les critères de stabilité :
* **Stabilité pour $+$ :** $0 = 0 + i0 \in \mathbb{Z}[i]$. Soient $z = a+ib$ et $z' = a'+ib'$ deux éléments de $\mathbb{Z}[i]$. Alors $z-z' = (a-a') + i(b-b')$. Comme $a-a' \in \mathbb{Z}$ et $b-b' \in \mathbb{Z}$, $z-z' \in \mathbb{Z}[i]$. Donc $(\mathbb{Z}[i], +)$ est un sous-groupe de $(\mathbb{C}, +)$.
* **Présence de l'unité :** $1 = 1 + i0 \in \mathbb{Z}[i]$.
* **Stabilité pour $\times$ :** $zz' = (aa'-bb') + i(ab'+a'b)$. Comme les produits et sommes d'entiers sont des entiers, $zz' \in \mathbb{Z}[i]$.
$\mathbb{Z}[i]$ est donc un sous-anneau de $\mathbb{C}$.

**Est-ce un corps ?**
Non. Dans un corps, tout élément non nul doit être inversible. 
Considérons $2 = 2 + i0 \in \mathbb{Z}[i]$. Son inverse dans $\mathbb{C}$ est $\frac{1}{2} = 0.5 + i0$. 
Puisque $0.5 \notin \mathbb{Z}$, cet inverse n'appartient pas à $\mathbb{Z}[i]$. 
$\mathbb{Z}[i]$ n'est donc pas un corps.

### 2. Automorphisme de conjugaison
Soit $f : z \mapsto \bar{z}$. 
* **Compatibilité avec les lois :** On sait que pour tous $z, z' \in \mathbb{C}$, $\overline{z+z'} = \bar{z} + \bar{z}'$ et $\overline{zz'} = \bar{z}\bar{z}'$. De plus $f(1) = \bar{1} = 1$. 
* **Stabilité de l'ensemble :** Si $z = a+ib \in \mathbb{Z}[i]$, alors $f(z) = a-ib$. Comme $-b \in \mathbb{Z}$, $f(z) \in \mathbb{Z}[i]$.
* **Bijectivité :** La conjugaison est sa propre réciproque ($f \circ f = \text{id}$), ce qui assure la bijectivité.
$f$ est donc un automorphisme de l'anneau $\mathbb{Z}[i]$.

### 3. Éléments inversibles
Soit $z \in \mathbb{Z}[i]$. $z$ est inversible s'il existe $z' \in \mathbb{Z}[i]$ tel que $zz' = 1$. 
En prenant le module au carré, on a $|z|^2 |z'|^2 = |1|^2 = 1$.
Posons $z = a+ib$. Alors $N(z) = a^2+b^2 \in \mathbb{N}$. 
L'égalité $N(z) N(z') = 1$ dans $\mathbb{N}$ impose que $N(z) = 1$.
On cherche donc $(a, b) \in \mathbb{Z}^2$ tels que $a^2+b^2 = 1$. Les seules solutions sont :
* $(1, 0) \implies z = 1$
* $(-1, 0) \implies z = -1$
* $(0, 1) \implies z = i$
* $(0, -1) \implies z = -i$

Les éléments inversibles de $\mathbb{Z}[i]$ sont donc **$\{1, -1, i, -i\}$**.