---
chapitre: "Structures algébriques"
difficulte: "★☆☆☆"
notions: ["Groupe", "LCI", "Élément neutre", "Symétrisabilité", "Morphisme de groupes"]
---

# Énoncé
Soit la loi de composition $\star$ définie sur $\mathbb{R}$ par : 
$$x \star y = \sqrt[3]{x^3 + y^3}$$

1. Montrer que $(\mathbb{R}, \star)$ est un groupe.
2. L'application $f : (\mathbb{R}, \star) \to (\mathbb{R}, +)$ définie par $f(x) = x^3$ est-elle un morphisme de groupes ?

---

# Indications
- **Structure de groupe :** Suivez les étapes classiques : LCI, associativité, élément neutre (vérification bilatérale), et symétrique (vérification bilatérale).
- **Morphisme :** Vérifiez si l'image de la composée est égale à la composée des images : $f(x \star y) = f(x) + f(y)$. Attention, la loi à l'arrivée est l'addition classique.

---

# Correction

### 1. $(\mathbb{R}, \star)$ est un groupe

**LCI et caractère bien défini :**
Pour tout $(x, y) \in \mathbb{R}^2$, $x^3 + y^3 \in \mathbb{R}$. La racine cubique est définie sur $\mathbb{R}$ tout entier, donc $\sqrt[3]{x^3 + y^3}$ est un réel bien défini. La loi $\star$ est une LCI sur $\mathbb{R}$.

**Associativité :**
Soient $x, y, z \in \mathbb{R}$.
$$(x \star y) \star z = \sqrt[3]{(x \star y)^3 + z^3} = \sqrt[3]{(\sqrt[3]{x^3 + y^3})^3 + z^3} = \sqrt[3]{x^3 + y^3 + z^3}$$
De même :
$$x \star (y \star z) = \sqrt[3]{x^3 + (y \star z)^3} = \sqrt[3]{x^3 + (\sqrt[3]{y^3 + z^3})^3} = \sqrt[3]{x^3 + y^3 + z^3}$$
Les deux expressions coïncident, la loi est associative.

**Élément neutre :**
Cherchons $e \in \mathbb{R}$ tel que pour tout $x \in \mathbb{R}$, $x \star e = x$ :
$$x \star e = x \iff \sqrt[3]{x^3 + e^3} = x \iff x^3 + e^3 = x^3 \iff e^3 = 0 \iff e = 0$$
Vérification bilatérale :
- $x \star 0 = \sqrt[3]{x^3 + 0^3} = x$
- $0 \star x = \sqrt[3]{0^3 + x^3} = x$
Le réel $0$ est l'élément neutre.

**Existence du symétrique :**
Soit $x \in \mathbb{R}$. Cherchons $y \in \mathbb{R}$ tel que $x \star y = 0$ :
$$x \star y = 0 \iff \sqrt[3]{x^3 + y^3} = 0 \iff x^3 + y^3 = 0 \iff y^3 = -x^3 \iff y = -x$$
Vérification bilatérale :
- $x \star (-x) = \sqrt[3]{x^3 + (-x)^3} = \sqrt[3]{0} = 0$
- $(-x) \star x = \sqrt[3]{(-x)^3 + x^3} = 0$
Tout élément $x$ admet un symétrique (son opposé au sens classique).

**Conclusion :** $(\mathbb{R}, \star)$ est un groupe. (Il est d'ailleurs abélien car $x^3+y^3 = y^3+x^3$).

### 2. Étude de l'application $f$

Pour que $f$ soit un morphisme de $(\mathbb{R}, \star)$ vers $(\mathbb{R}, +)$, il faut que $\forall(x, y) \in \mathbb{R}^2, f(x \star y) = f(x) + f(y)$.

Calculons chaque membre :
- $f(x \star y) = f(\sqrt[3]{x^3 + y^3}) = (\sqrt[3]{x^3 + y^3})^3 = x^3 + y^3$
- $f(x) + f(y) = x^3 + y^3$ (l'addition ici est la loi usuelle de $\mathbb{R}$)

On a bien $f(x \star y) = f(x) + f(y)$ pour tous réels $x$ et $y$. 
L'application $f$ est donc un **morphisme de groupes**. 
(Comme $f$ est de plus bijective de $\mathbb{R}$ dans $\mathbb{R}$, c'est un isomorphisme de groupes).