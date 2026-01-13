---
chapitre: "Structures algébriques"
difficulte: "★☆☆☆"
notions: ["Groupe", "LCI", "Associativité", "Élément neutre", "Symétrisabilité", "Groupe non-abélien"]
---

# Énoncé
On définit sur $\mathbb{R}^2$ la loi de composition interne $*$ par :
$$\forall (x, y), (x', y') \in \mathbb{R}^2, \quad (x, y) * (x', y') = (x + x', ye^{x'} + y'e^{-x})$$

Montrer que $(\mathbb{R}^2, *)$ est un groupe non-abélien.

---

# Indications
- **LCI :** Vérifiez que le résultat appartient bien à $\mathbb{R}^2$.
- **Associativité :** C'est l'étape la plus calculatoire. Calculez séparément $((x, y) * (x', y')) * (x'', y'')$ et $(x, y) * ((x', y') * (x'', y''))$.
- **Élément neutre :** Cherchez un couple $(e_1, e_2)$ tel que $(x, y) * (e_1, e_2) = (x, y)$, puis vérifiez impérativement la neutralité à gauche.
- **Symétrique :** Pour un couple $(x, y)$ donné, cherchez $(x', y')$ tel que $(x, y) * (x', y') = (e_1, e_2)$.
- **Non-abélien :** Trouvez deux couples dont le produit dépend de l'ordre (utilisez des valeurs simples comme 0 et 1).

---

# Correction

### 1. La loi $*$ est une LCI
Soient $(x, y)$ et $(x', y')$ deux éléments de $\mathbb{R}^2$. 
$x+x' \in \mathbb{R}$ et $ye^{x'} + y'e^{-x} \in \mathbb{R}$ par stabilité de l'addition et du produit dans $\mathbb{R}$, et par le fait que l'exponentielle est à valeurs réelles. 
Donc $(x, y) * (x', y') \in \mathbb{R}^2$.

### 2. Associativité
Soient $(x, y), (x', y'), (x'', y'') \in \mathbb{R}^2$.
D'une part :
$$((x, y) * (x', y')) * (x'', y'') = (x+x', ye^{x'} + y'e^{-x}) * (x'', y'')$$
$$= (x+x'+x'', (ye^{x'} + y'e^{-x})e^{x''} + y''e^{-(x+x')})$$
$$= (x+x'+x'', ye^{x'+x''} + y'e^{x''-x} + y''e^{-x-x'})$$

D'autre part :
$$(x, y) * ((x', y') * (x'', y'')) = (x, y) * (x'+x'', y'e^{x''} + y''e^{-x'})$$
$$= (x+x'+x'', ye^{x'+x''} + (y'e^{x''} + y''e^{-x'})e^{-x})$$
$$= (x+x'+x'', ye^{x'+x''} + y'e^{x''-x} + y''e^{-x-x'})$$

Les deux expressions sont égales pour tous éléments de $\mathbb{R}^2$, donc la loi $*$ est associative.

### 3. Élément neutre
Cherchons $(e_1, e_2) \in \mathbb{R}^2$ tel que $(x, y) * (e_1, e_2) = (x, y)$ :
$\begin{cases} x + e_1 = x \\ ye^{e_1} + e_2e^{-x} = y \end{cases} \iff \begin{cases} e_1 = 0 \\ y + e_2e^{-x} = y \end{cases} \iff \begin{cases} e_1 = 0 \\ e_2 = 0 \end{cases}$
Le seul candidat est $(0, 0)$. Vérifions la neutralité à gauche :
$$(0, 0) * (x, y) = (0+x, 0 \cdot e^x + ye^{-0}) = (x, y)$$
L'élément $(0, 0)$ est donc le neutre de la structure.

### 4. Existence du symétrique
Soit $(x, y) \in \mathbb{R}^2$. Cherchons $(x', y')$ tel que $(x, y) * (x', y') = (0, 0)$ :
$\begin{cases} x + x' = 0 \\ ye^{x'} + y'e^{-x} = 0 \end{cases} \iff \begin{cases} x' = -x \\ ye^{-x} + y'e^{-x} = 0 \end{cases} \iff \begin{cases} x' = -x \\ y' = -y \end{cases}$
Le candidat au symétrique est $(-x, -y)$. Vérifions à gauche :
$$(-x, -y) * (x, y) = (-x+x, -ye^x + ye^{-(-x)}) = (0, -ye^x + ye^x) = (0, 0)$$
Tout élément $(x, y)$ admet donc $(-x, -y)$ pour symétrique.

### 5. Caractère non-abélien
Comparons $(1, 0) * (0, 1)$ et $(0, 1) * (1, 0)$ :
- $(1, 0) * (0, 1) = (1+0, 0 \cdot e^0 + 1 \cdot e^{-1}) = (1, e^{-1})$
- $(0, 1) * (1, 0) = (0+1, 1 \cdot e^1 + 0 \cdot e^{-0}) = (1, e)$
Comme $e \neq e^{-1}$, la loi n'est pas commutative.

**Conclusion :** $(\mathbb{R}^2, *)$ possède une LCI associative, un élément neutre et chaque élément est symétrisable ; c'est donc un groupe. La non-commutativité en fait un groupe non-abélien.