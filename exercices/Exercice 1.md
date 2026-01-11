---
chapitre: "Structures algébriques"
difficulte: "★☆☆☆"
notions: ["LCI", "Commutativité", "Associativité", "Élément neutre", "Symétrisabilité"]
---

# Énoncé
Soit $*$ la loi de composition interne définie sur $\mathbb{R}$ par :
$$x * y = x + y + x^2 y$$

1. Vérifier que $*$ n'est pas commutative, n'est pas associative, que $*$ admet un élément neutre et qu'aucun élément de $\mathbb{R} \setminus \{0\}$ n'admet d'inverse pour $*$.
2. Résoudre les équations suivantes :
   - $2 * x = -3$
   - $x * x = 3$

---

# Indications
- **Commutativité/Associativité :** Cherchez un contre-exemple simple (avec 1 et 2 par exemple).
- **Élément neutre :** Résolvez $x * e = x$ pour tout $x$, puis vérifiez impérativement la neutralité à gauche ($e * x = x$).
- **Inverse :** Pour un $x$ fixé, trouvez $y$ tel que $x * y = e$, puis vérifiez si ce même $y$ satisfait $y * x = e$.
- **Équations :** Injectez la définition de la loi dans l'égalité et résolvez l'équation polynomiale résultante.

---

# Correction

### 1. Étude des propriétés de la loi

**Caractère bien défini :**
La loi $*$ est une application de $\mathbb{R} \times \mathbb{R} \to \mathbb{R}$ car la somme et le produit de réels sont des réels. C'est donc bien une loi de composition interne (LCI) sur $\mathbb{R}$.

**Non-commutativité :**
On compare $x * y$ et $y * x$ :
- $x * y = x + y + x^2 y$
- $y * x = y + x + y^2 x$
Prenons $x = 1$ et $y = 2$ :
- $1 * 2 = 1 + 2 + 1^2 \times 2 = 5$
- $2 * 1 = 2 + 1 + 2^2 \times 1 = 7$
Comme $5 \neq 7$, la loi n'est pas commutative.

**Non-associativité :**
On compare $(x * y) * z$ et $x * (y * z)$ :
Prenons $x=1, y=1, z=1$ :
- $(1 * 1) * 1 = (1 + 1 + 1^2 \times 1) * 1 = 3 * 1 = 3 + 1 + 3^2 \times 1 = 13$
- $1 * (1 * 1) = 1 * 3 = 1 + 3 + 1^2 \times 3 = 7$
Comme $13 \neq 7$, la loi n'est pas associative.

**Élément neutre :**
Cherchons $e \in \mathbb{R}$ tel que pour tout $x \in \mathbb{R}$, $x * e = x$ et $e * x = x$.
- $x * e = x \iff x + e + x^2 e = x \iff e(1 + x^2) = 0$.
Comme $1 + x^2 \neq 0$ pour tout $x \in \mathbb{R}$, la seule solution possible est $e = 0$.
- Vérification à gauche : $0 * x = 0 + x + 0^2 \times x = x$.
L'élément $0$ est donc le neutre (unique) de la loi $*$.

**Symétrisabilité (Inverse) :**
Soit $x \in \mathbb{R} \setminus \{0\}$. Cherchons $y \in \mathbb{R}$ tel que $x * y = 0$ **et** $y * x = 0$.
- $x * y = 0 \iff x + y + x^2 y = 0 \iff y(1 + x^2) = -x \iff y = \frac{-x}{1 + x^2}$.
Testons si ce candidat est un inverse à gauche :
- $y * x = y + x + y^2 x = \frac{-x}{1 + x^2} + x + \left(\frac{-x}{1 + x^2}\right)^2 x$
- $y * x = \frac{-x + x(1+x^2) + \frac{x^3}{1+x^2}}{1+x^2} = \frac{x^3 + \frac{x^3}{1+x^2}}{1+x^2} = \frac{x^3(1+x^2) + x^3}{(1+x^2)^2} = \frac{x^3(2+x^2)}{(1+x^2)^2}$.
Pour $x \neq 0$, cette expression n'est jamais nulle ($x^3 \neq 0$ et $2+x^2 \geq 2$).
Ainsi, $x$ admet un inverse à droite mais pas à gauche. Aucun élément non nul n'est symétrisable.

### 2. Résolution d'équations

**Équation $2 * x = -3$ :**
$$2 + x + 2^2 \times x = -3 \iff 2 + 5x = -3 \iff 5x = -5 \iff x = -1$$
L'ensemble des solutions est $S = \{-1\}$.

**Équation $x * x = 3$ :**
$$x + x + x^2 \times x = 3 \iff x^3 + 2x - 3 = 0$$
On remarque une racine évidente $x = 1$ (car $1+2-3=0$). On factorise par $(x-1)$ :
$x^3 + 2x - 3 = (x-1)(x^2 + x + 3)$.
Le discriminant de $x^2 + x + 3$ est $\Delta = 1^2 - 4 \times 3 = -11 < 0$.
Le trinôme n'admet pas de racines réelles.
L'unique solution réelle est donc $x = 1$. $S = \{1\}$.