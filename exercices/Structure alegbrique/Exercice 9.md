---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Groupe fini", "Ordre d'un élément", "Involutions", "Dénombrement"]
---

# Énoncé
Soit $G$ un groupe fini de cardinal pair. On veut montrer qu'il existe un élément $x$ de $G$ distinct de $1$ et égal à son propre inverse. Pour cela, on pose :
$$A = \{g \in G \mid g \neq 1 \text{ et } g^{-1} = g\} \quad \text{et} \quad B = \{g \in G \mid g \neq 1 \text{ et } g^{-1} \neq g\}$$

1. $A$ et $B$ sont-ils des sous-groupes de $G$ ?
2. Justifier que $A$ et $B$ sont des ensembles finis puis exprimer $|G|$ en fonction de $|A|$ et de $|B|$.
3. Montrer que $|B|$ est pair et conclure.

---

# Indications
- **Question 1 :** Un sous-groupe doit impérativement contenir l'élément neutre.
- **Question 2 :** Observez que $\{1\}$, $A$ et $B$ forment une partition de $G$.
- **Question 3 :** Dans $B$, si un élément $g$ s'y trouve, son inverse $g^{-1}$ s'y trouve aussi. Sont-ils distincts ? Regroupez les éléments de $B$ par paires.

---

# Correction

### 1. Structure de $A$ et $B$
Par définition, l'élément neutre $1_G$ n'appartient ni à $A$ ni à $B$ car la condition $g \neq 1$ est explicitement requise. 
Or, tout sous-groupe d'un groupe $G$ doit contenir l'élément neutre. 
Par conséquent, **ni $A$ ni $B$ ne sont des sous-groupes de $G$**.

### 2. Cardinalité et Partition
Comme $G$ est un ensemble fini, tous ses sous-ensembles sont finis.
Analysons la structure de $G$. Tout élément $g \in G$ vérifie l'une et une seule des conditions suivantes :
* $g = 1$ (l'élément neutre).
* $g \neq 1$ et $g = g^{-1}$ (éléments de $A$).
* $g \neq 1$ et $g \neq g^{-1}$ (éléments de $B$).

L'ensemble $G$ est la réunion disjointe : $G = \{1\} \cup A \cup B$.
D'après les propriétés du cardinal d'une réunion disjointe :
$$|G| = |\{1\}| + |A| + |B| = 1 + |A| + |B|$$

### 3. Parité de $|B|$ et conclusion
Considérons l'application $\phi : B \to B$ définie par $\phi(g) = g^{-1}$.
* **Bien définie :** Si $g \in B$, alors $g \neq 1$ et $g^{-1} \neq g$. L'inverse $(g^{-1})^{-1}$ est égal à $g$. Comme $g \neq 1$, alors $g^{-1} \neq 1$. De plus, comme $g \neq g^{-1}$, alors $g^{-1} \neq (g^{-1})^{-1}$. Donc $g^{-1} \in B$.
* **Appariement :** Pour tout $g \in B$, $g \neq \phi(g)$ par définition de $B$. De plus $\phi(\phi(g)) = g$. 
On peut donc regrouper les éléments de $B$ par paires de la forme $\{g, g^{-1}\}$. 
Le cardinal $|B|$ est donc la somme de cardinaux d'ensembles à 2 éléments : **$|B|$ est pair**.

**Conclusion :**
On sait que $|G| = 1 + |A| + |B|$. On nous donne $|G|$ pair.
On peut écrire : $|A| = |G| - |B| - 1$.
* $|G|$ est pair.
* $|B|$ est pair.
* Donc $|G| - |B|$ est pair.
* Ainsi, $|A| = (\text{pair}) - 1$ est **impair**.

Comme $|A|$ est impair, il est au moins égal à $1$. Il existe donc au moins un élément $x \in A$.
Par définition de $A$, cet élément $x$ est distinct de $1$ et vérifie $x = x^{-1}$ (ou $x^2 = 1$).