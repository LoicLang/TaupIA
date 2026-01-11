---
chapitre: "Structures algébriques"
difficulte: "★★★☆"
notions: ["Groupe", "Axiomes minimaux", "Neutralité bilatérale", "Symétrie bilatérale"]
---

# Énoncé
Soit $G$ un ensemble non vide, muni d'une loi de composition interne $\star$ associative. On suppose qu'il existe un élément $e \in G$ tel que :
$$
\begin{cases} 
\forall x \in G, \quad x \star e = x \\
\forall x \in G, \quad \exists y \in G, \quad x \star y = e 
\end{cases}
$$
Montrer que $(G, \star)$ est un groupe.

---

# Indications
Pour montrer que $(G, \star)$ est un groupe, vous devez prouver que l'élément $e$ (neutre à droite) est aussi un neutre à gauche ($e \star x = x$), et que l'élément $y$ (symétrique à droite) est aussi un symétrique à gauche ($y \star x = e$).

1. **Symétrie à gauche :** Pour un $x$ donné, soit $y$ son symétrique à droite. Par hypothèse, $y$ possède lui aussi un symétrique à droite, notons-le $z$. Calculez $y \star x$ en faisant apparaître $z$.
2. **Neutralité à gauche :** Une fois que vous avez prouvé que $y \star x = e$, utilisez ce résultat pour calculer $e \star x$.

---

# Correction

D'après les hypothèses, la loi $\star$ est une LCI associative. Pour que $(G, \star)$ soit un groupe, il faut prouver la bilatéralité du neutre et des symétriques.

### 1. Preuve que le symétrique à droite est un symétrique à gauche
Soit $x \in G$. Par hypothèse, il existe $y \in G$ tel que $x \star y = e$.
Pour ce même $y \in G$, l'hypothèse nous dit qu'il existe un élément $z \in G$ tel que $y \star z = e$.
Calculons $y \star x$ :
$$y \star x = (y \star x) \star e \quad \text{(car } e \text{ est neutre à droite)}$$
$$y \star x = (y \star x) \star (y \star z) \quad \text{(par définition de } z \text{)}$$
$$y \star x = y \star (x \star y) \star z \quad \text{(par associativité)}$$
$$y \star x = y \star e \star z \quad \text{(car } x \star y = e \text{)}$$
$$y \star x = (y \star e) \star z = y \star z \quad \text{(car } e \text{ est neutre à droite)}$$
$$y \star x = e \quad \text{(par définition de } z \text{)}$$
Ainsi, tout symétrique à droite est également un symétrique à gauche.

### 2. Preuve que le neutre à droite est un neutre à gauche
Soit $x \in G$. On sait qu'il existe $y \in G$ tel que $x \star y = e$ et, d'après le point précédent, $y \star x = e$.
Calculons $e \star x$ :
$$e \star x = (x \star y) \star x \quad \text{(car } e = x \star y \text{)}$$
$$e \star x = x \star (y \star x) \quad \text{(par associativité)}$$
$$e \star x = x \star e \quad \text{(car } y \star x = e \text{, prouvé ci-dessus)}$$
$$e \star x = x \quad \text{(car } e \text{ est neutre à droite)}$$
L'élément $e$ est donc également un neutre à gauche.

### Conclusion
La loi $\star$ est associative, possède un élément neutre $e$ ($e \star x = x \star e = x$) et tout élément $x$ possède un symétrique $y$ ($x \star y = y \star x = e$). 
$(G, \star)$ est donc un groupe.