---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Centre d'un groupe", "Sous-groupe", "Morphisme de groupes", "Injectivité", "Surjectivité"]
---

# Énoncé
Soit $(G, *)$ un groupe, on note $Z(G)$ le *centre* de $G$ qui est par définition l'ensemble des éléments de $G$ qui commutent avec tous les éléments de $G$ :
$$Z(G) = \{x \in G \mid \forall g \in G, x * g = g * x\}$$

1. Dans le cas où $G$ est commutatif, que dire de $Z(G)$ ?
2. Montrer que $Z(G)$ est un sous-groupe de $G$.
3. Soient $(G, *)$ et $(H, \times)$ deux groupes et $f : G \to H$ un morphisme de groupes. Montrer que :
   (a) si $f$ est surjectif, alors $f(Z(G)) \subset Z(H)$
   (b) si $f$ est injectif, alors $f^{-1}(Z(H)) \subset Z(G)$.

---

# Indications
- **Question 1 :** Appliquez directement la définition d'un groupe commutatif (ou abélien).
- **Question 2 :** Utilisez la caractérisation habituelle des sous-groupes : non-vacuité (le neutre commute-t-il avec tout le monde ?), stabilité par la loi et stabilité par inverse.
- **Question 3(a) :** Prenez $y \in f(Z(G))$ et $h \in H$. Puisque $f$ est surjectif, $h$ possède un antécédent dans $G$. Utilisez la propriété de morphisme.
- **Question 3(b) :** Prenez $x \in f^{-1}(Z(H))$, ce qui signifie $f(x) \in Z(H)$. Pour montrer que $x \in Z(G)$, comparez $f(x*g)$ et $f(g*x)$ pour tout $g \in G$.

---

# Correction

### 1. Cas d'un groupe commutatif
Si $G$ est commutatif (abélien), par définition, tous ses éléments commutent entre eux : $\forall(x, g) \in G^2, x * g = g * x$. 
Ainsi, tout élément $x \in G$ appartient à $Z(G)$. On a donc **$Z(G) = G$**.

### 2. $Z(G)$ est un sous-groupe de $G$
Vérifions les critères de caractérisation :
- **Non-vacuité :** L'élément neutre $e$ vérifie $\forall g \in G, e * g = g = g * e$. Donc $e \in Z(G)$, l'ensemble est non vide.
- **Stabilité par la loi :** Soient $x, y \in Z(G)$. Pour tout $g \in G$ :
  $(x * y) * g = x * (y * g) = x * (g * y)$ (car $y \in Z(G)$)
  $(x * y) * g = (x * g) * y = (g * x) * y$ (car $x \in Z(G)$)
  $(x * y) * g = g * (x * y)$.
  Donc $(x * y) \in Z(G)$.
- **Stabilité par l'inverse :** Soit $x \in Z(G)$. On a $x * g = g * x$ pour tout $g \in G$.
  Multiplions à gauche et à droite par $x^{-1}$ :
  $x^{-1} * (x * g) * x^{-1} = x^{-1} * (g * x) * x^{-1}$
  $(x^{-1} * x) * (g * x^{-1}) = (x^{-1} * g) * (x * x^{-1})$
  $e * g * x^{-1} = x^{-1} * g * e \implies g * x^{-1} = x^{-1} * g$.
  Donc $x^{-1} \in Z(G)$.
**Conclusion :** $Z(G)$ est un sous-groupe de $G$.

### 3. Morphismes et centres
**(a) $f$ surjectif $\implies f(Z(G)) \subset Z(H)$**
Soit $y \in f(Z(G))$. Il existe $x \in Z(G)$ tel que $y = f(x)$. Soit $h \in H$.
Comme $f$ est surjectif, il existe $g \in G$ tel que $h = f(g)$.
$y \times h = f(x) \times f(g) = f(x * g)$ (car $f$ est un morphisme)
Comme $x \in Z(G)$, $x * g = g * x$, donc :
$y \times h = f(g * x) = f(g) \times f(x) = h \times y$.
Ceci étant vrai pour tout $h \in H$, $y \in Z(H)$. On a bien $f(Z(G)) \subset Z(H)$.

**(b) $f$ injectif $\implies f^{-1}(Z(H)) \subset Z(G)$**
Soit $x \in f^{-1}(Z(H))$, alors $f(x) \in Z(H)$. Soit $g \in G$.
Calculons $f(x * g)$ et $f(g * x)$ :
$f(x * g) = f(x) \times f(g)$
$f(g * x) = f(g) \times f(x)$
Comme $f(x) \in Z(H)$, il commute avec tous les éléments de $H$, notamment avec $f(g)$. 
Donc $f(x) \times f(g) = f(g) \times f(x)$, ce qui implique $f(x * g) = f(g * x)$.
Comme $f$ est injectif, $f(u) = f(v) \implies u = v$.
D'où $x * g = g * x$ pour tout $g \in G$.
Ainsi $x \in Z(G)$, d'où $f^{-1}(Z(H)) \subset Z(G)$.