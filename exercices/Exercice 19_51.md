---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Corps", "Sous-corps", "Isomorphisme de corps", "Quantité conjuguée"]
---

# Énoncé

Soit $a \in \mathbb{Q}_+^*$ tel que $\sqrt{a} \notin \mathbb{Q}$. On définit :
$$\mathbb{Q}(\sqrt{a}) = \{ \lambda + \mu \sqrt{a} \mid (\lambda, \mu) \in \mathbb{Q}^2 \}$$

1. Montrer que $\mathbb{Q}(\sqrt{a})$ est un sous-corps de $\mathbb{R}$.
2. Les corps $\mathbb{Q}(\sqrt{2})$ et $\mathbb{Q}(\sqrt{3})$ sont-ils isomorphes ?

---

# Indications

- **Pour la question 1 :** Utilisez la caractérisation des sous-corps. Pour l'inversibilité, pensez à multiplier par la **quantité conjuguée** $\lambda - \mu\sqrt{a}$.
- **Pour la question 2 :** Raisonnez par l'absurde. Si $\phi$ est un isomorphisme de $\mathbb{Q}(\sqrt{2})$ dans $\mathbb{Q}(\sqrt{3})$, montrez que l'image de $x = \sqrt{2}$ doit vérifier $\phi(x)^2 = 2$. Cherchez ensuite si un tel élément existe dans $\mathbb{Q}(\sqrt{3})$.

---

# Correction

### 1. $\mathbb{Q}(\sqrt{a})$ est un sous-corps de $\mathbb{R}$

$\mathbb{Q}(\sqrt{a})$ est un sous-ensemble de $\mathbb{R}$ par définition de $\sqrt{a}$. Vérifions les critères de structure :

* **Non-vacuité et élément unité :** $1 = 1 + 0\sqrt{a} \in \mathbb{Q}(\sqrt{a})$ (en prenant $\lambda=1, \mu=0$). De même $0 \in \mathbb{Q}(\sqrt{a})$.
* **Stabilité par soustraction :** Soient $z = \lambda + \mu\sqrt{a}$ et $z' = \lambda' + \mu'\sqrt{a}$.
    $z - z' = (\lambda - \lambda') + (\mu - \mu')\sqrt{a}$. Comme $\mathbb{Q}$ est un corps, $\lambda - \lambda' \in \mathbb{Q}$ et $\mu - \mu' \in \mathbb{Q}$, donc $z - z' \in \mathbb{Q}(\sqrt{a})$. $(\mathbb{Q}(\sqrt{a}), +)$ est un sous-groupe de $(\mathbb{R}, +)$.
* **Stabilité par multiplication :** $z \cdot z' = (\lambda\lambda' + a\mu\mu') + (\lambda\mu' + \lambda'\mu)\sqrt{a}$. Par stabilité de $\mathbb{Q}$ par $+$ et $\times$, les coefficients sont rationnels, donc $z \cdot z' \in \mathbb{Q}(\sqrt{a})$.
* **Inversibilité des éléments non nuls :** Soit $z = \lambda + \mu\sqrt{a} \neq 0$.
    Remarquons d'abord que $\lambda^2 - a\mu^2 \neq 0$. En effet, si $\lambda^2 - a\mu^2 = 0$ :
    - Si $\mu \neq 0$, alors $a = (\lambda/\mu)^2$, donc $\sqrt{a} = |\lambda/\mu| \in \mathbb{Q}$, ce qui est exclu.
    - Si $\mu = 0$, alors $\lambda^2 = 0 \implies \lambda = 0$, donc $z=0$, ce qui est exclu.
    Utilisons la quantité conjuguée :
    $$\frac{1}{\lambda + \mu\sqrt{a}} = \frac{\lambda - \mu\sqrt{a}}{(\lambda + \mu\sqrt{a})(\lambda - \mu\sqrt{a})} = \frac{\lambda}{\lambda^2 - a\mu^2} - \frac{\mu}{\lambda^2 - a\mu^2}\sqrt{a}$$
    Les coefficients appartiennent à $\mathbb{Q}$, donc $z^{-1} \in \mathbb{Q}(\sqrt{a})$.

$\mathbb{Q}(\sqrt{a})$ est donc un sous-corps de $\mathbb{R}$.

### 2. Isomorphisme entre $\mathbb{Q}(\sqrt{2})$ et $\mathbb{Q}(\sqrt{3})$

Supposons qu'il existe un isomorphisme de corps $\phi : \mathbb{Q}(\sqrt{2}) \to \mathbb{Q}(\sqrt{3})$.
* Un morphisme de corps envoie nécessairement $1$ sur $1$. Par récurrence, $\phi(n) = n$ pour tout $n \in \mathbb{N}$, puis par structure de corps, $\phi(q) = q$ pour tout $q \in \mathbb{Q}$.
* Soit $x = \sqrt{2} \in \mathbb{Q}(\sqrt{2})$. On a $x^2 = 2$.
* Alors $\phi(x^2) = \phi(2) \implies \phi(x)^2 = 2$.
* Cherchons si un élément $y = \lambda + \mu\sqrt{3} \in \mathbb{Q}(\sqrt{3})$ peut vérifier $y^2 = 2$ :
    $$(\lambda + \mu\sqrt{3})^2 = \lambda^2 + 3\mu^2 + 2\lambda\mu\sqrt{3} = 2$$
    Comme $\sqrt{3} \notin \mathbb{Q}$, cette égalité impose $2\lambda\mu = 0$ (unicité de l'écriture dans la base $(1, \sqrt{3})$).
    - Si $\mu = 0$, alors $\lambda^2 = 2$, ce qui impose $\sqrt{2} \in \mathbb{Q}$ (Absurde).
    - Si $\lambda = 0$, alors $3\mu^2 = 2 \implies \mu^2 = 2/3$. Or $2/3$ n'est pas le carré d'un rationnel (car l'équation $3p^2 = 2q^2$ n'a pas de solution entière non nulle d'après l'exposant de la valuation 2-adique ou 3-adique).

**Conclusion :** Il n'existe pas d'élément de carré $2$ dans $\mathbb{Q}(\sqrt{3})$. Les deux corps ne sont donc pas isomorphes.