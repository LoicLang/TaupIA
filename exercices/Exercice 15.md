---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Anneau commutatif", "Corps", "Composition de fonctions", "Élément neutre", "Distributivité"]
---

# Énoncé
Soit $P$ l'ensemble des fonctions paires définies sur $\mathbb{R}$ à valeurs dans $\mathbb{R}$.

1. $(P, +, \times)$ est-il un anneau ? Est-il commutatif ? Est-il un corps ?
2. $(P, +, \circ)$ est-il un anneau ? Est-il commutatif ?

---

# Indications
- **Question 1 :** Pour $(P, +, \times)$, vérifiez d'abord que $P$ est un sous-anneau de l'anneau des fonctions $\mathcal{F}(\mathbb{R}, \mathbb{R})$. Un élément neutre pour la multiplication $\times$ (la fonction constante égale à 1) est-il une fonction paire ?
- **Question 2 :** Pour la loi de composition $\circ$, vérifiez si l'élément neutre habituel (l'application identité $\text{Id} : x \mapsto x$) appartient à $P$. Pensez également à vérifier la distributivité à gauche de $\circ$ sur $+$ : a-t-on $h \circ (f+g) = h \circ f + h \circ g$ pour toutes fonctions de $P$ ?

---

# Correction

### 1. Étude de $(P, +, \times)$
* **Structure d'anneau :** L'ensemble $\mathcal{F}(\mathbb{R}, \mathbb{R})$ muni de l'addition et de la multiplication usuelles des fonctions est un anneau commutatif. Montrons que $P$ en est un sous-anneau :
    - **Stabilité pour $+$ :** La somme de deux fonctions paires est paire. La fonction nulle ($x \mapsto 0$) est paire. $(P, +)$ est donc un sous-groupe de $(\mathcal{F}(\mathbb{R}, \mathbb{R}), +)$.
    - **Élément neutre pour $\times$ :** La fonction unité $\mathbf{1} : x \mapsto 1$ vérifie $\mathbf{1}(-x) = 1 = \mathbf{1}(x)$. Elle est donc paire, d'où $\mathbf{1} \in P$.
    - **Stabilité pour $\times$ :** Soient $f, g \in P$. $(f \times g)(-x) = f(-x)g(-x) = f(x)g(x) = (f \times g)(x)$. Le produit est donc une fonction paire.
    $P$ est un sous-anneau de $\mathcal{F}(\mathbb{R}, \mathbb{R})$, c'est donc un **anneau**.
* **Commutativité :** La multiplication des fonctions à valeurs réelles est commutative, donc $(P, +, \times)$ est un **anneau commutatif**.
* **Corps :** Pour être un corps, tout élément non nul doit être inversible. Considérons la fonction paire $f(x) = x^2$. Elle s'annule en $0$. Elle ne peut donc pas avoir d'inverse pour la loi $\times$ (car $(f \times g)(0) = 0$ pour toute fonction $g$). $(P, +, \times)$ **n'est pas un corps**.

### 2. Étude de $(P, +, \circ)$
* **Stabilité de $\circ$ :** Soient $f, g \in P$. $(f \circ g)(-x) = f(g(-x)) = f(g(x)) = (f \circ g)(x)$. La composition de deux fonctions paires est bien une fonction paire.
* **Élément neutre pour $\circ$ :** Le neutre usuel pour la composition est l'application identité $\text{Id} : x \mapsto x$. Or, $\text{Id}(-x) = -x$, tandis que $\text{Id}(x) = x$. Puisque $-x \neq x$ pour $x \neq 0$, $\text{Id}$ n'est pas une fonction paire. **$P$ ne possède pas d'élément neutre pour $\circ$**, donc $(P, +, \circ)$ **n'est pas un anneau** (selon la définition standard exigeant un neutre multiplicatif).
* **Distributivité :** Même sans neutre, vérifions la distributivité. Si la distributivité à droite est vérifiée ($(f+g) \circ h = f \circ h + g \circ h$), la distributivité à gauche est généralement fausse : $h \circ (f+g) \neq h \circ f + h \circ g$ (par exemple avec $h(x) = x^2$).
* **Commutativité :** La composition de fonctions n'est en général **pas commutative**. Par exemple, si $f(x)=2$ et $g(x)=x^2+1$, alors $(f \circ g)(x) = 2$ et $(g \circ f)(x) = 2^2+1 = 5$.