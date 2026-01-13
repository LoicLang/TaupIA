---
chapitre: "Structures algébriques"
difficulte: "★★★☆"
notions: ["Relation d'équivalence", "Classes d'équivalence", "Théorème de Lagrange", "Partition"]
---

# Énoncé
Soit $G$ un groupe fini et $H$ un sous-groupe de $G$.

1. On définit la relation binaire $\mathcal{R}$ sur l'ensemble $G$ par :
   $$\forall(x, y) \in G^2, \quad x\mathcal{R}y \iff x^{-1}y \in H$$
2. Montrer que $\mathcal{R}$ est une relation d'équivalence sur $G$.
3. Pour $x \in G$, on définit $cl(x) = \{g \in G \mid x\mathcal{R}g\}$. Montrer que :
   $$\forall x, y \in G, \quad cl(x) = cl(y) \iff x\mathcal{R}y$$
4. Montrer également que :
   $$\forall x, y \in G, \quad x \not\mathcal{R} y \iff cl(x) \cap cl(y) = \emptyset$$
5. On considère l'ensemble $X = \{cl(x) \mid x \in G\}$. Montrer que $X$ est un ensemble fini.
6. On note $X = \{P_1, \dots, P_n\}$. Montrer que les $(P_i)_{1 \le i \le n}$ forment une partition de $G$, en parties non vides.
7. Montrer que pour tout $i \in \llbracket 1, n \rrbracket$, $P_i$ est un ensemble fini et $|P_i| = |H|$.
8. En déduire que $|G| = |X| \times |H|$.
9. Que vient-on de démontrer ?

---

# Indications
- **Question 2 :** Vérifiez la réflexivité ($x^{-1}x \in H$), la symétrie (si $x^{-1}y \in H$ alors $(x^{-1}y)^{-1} \in H$) et la transitivité.
- **Question 4 :** C'est une propriété générale des relations d'équivalence : deux classes sont soit égales, soit disjointes.
- **Question 7 :** Pour une classe $P = cl(x)$, considérez l'application $\phi : H \to cl(x)$ définie par $\phi(h) = xh$. Montrez qu'elle est bijective.
- **Question 8 :** Utilisez le fait qu'une partition d'un ensemble fini permet de sommer les cardinaux des parties.

---

# Correction

### 1 & 2. Relation d'équivalence
Soit $H$ un sous-groupe de $G$.
- **Réflexivité :** Pour tout $x \in G$, $x^{-1}x = e \in H$ car $H$ est un sous-groupe. Donc $x\mathcal{R}x$.
- **Symétrie :** Soient $x, y \in G$ tels que $x\mathcal{R}y$. On a $x^{-1}y \in H$. Puisque $H$ est un sous-groupe, l'inverse $(x^{-1}y)^{-1}$ appartient à $H$. Or $(x^{-1}y)^{-1} = y^{-1}(x^{-1})^{-1} = y^{-1}x$. Donc $y\mathcal{R}x$.
- **Transitivité :** Soient $x, y, z \in G$ tels que $x\mathcal{R}y$ et $y\mathcal{R}z$. Alors $x^{-1}y \in H$ et $y^{-1}z \in H$. Par stabilité de $H$, le produit $(x^{-1}y)(y^{-1}z) = x^{-1}(yy^{-1})z = x^{-1}z$ appartient à $H$. Donc $x\mathcal{R}z$.
$\mathcal{R}$ est donc une relation d'équivalence.

### 3 & 4. Propriétés des classes
Ce sont des propriétés structurelles des classes d'équivalence :
- Si $x\mathcal{R}y$, alors pour tout $g \in cl(x)$, $x\mathcal{R}g \implies y\mathcal{R}x\mathcal{R}g \implies g \in cl(y)$ par transitivité. L'inclusion réciproque est identique.
- Deux classes sont disjointes si et seulement si leurs représentants ne sont pas en relation. S'il existait $z \in cl(x) \cap cl(y)$, on aurait $x\mathcal{R}z$ et $y\mathcal{R}z$, d'où $x\mathcal{R}y$ par symétrie et transitivité, ce qui impliquerait $cl(x) = cl(y)$.

### 5 & 6. Partition de $G$
- Comme $G$ est fini, l'ensemble de ses parties $\mathcal{P}(G)$ est fini, donc $X \subset \mathcal{P}(G)$ est fini.
- Tout élément $x \in G$ appartient à sa propre classe $cl(x)$ (réflexivité), donc la réunion des $P_i$ couvre $G$.
- Comme les $P_i$ sont deux à deux disjoints (question 4) et non vides, ils forment une **partition** de $G$.

### 7. Cardinal des classes
Soit $P_i = cl(x)$ une classe. Par définition, $g \in cl(x) \iff x^{-1}g \in H \iff \exists h \in H, g = xh$.
Considérons $\phi : H \to cl(x)$ telle que $\phi(h) = xh$.
- **Surjectivité :** Vient de la définition ci-dessus.
- **Injectivité :** Si $xh_1 = xh_2$, par régularité dans un groupe, $h_1 = h_2$.
$\phi$ est une bijection, donc $|P_i| = |H|$ pour tout $i$.

### 8. Conclusion numérique
Puisque $(P_1, \dots, P_n)$ est une partition de $G$ :
$$|G| = \sum_{i=1}^n |P_i| = \sum_{i=1}^n |H| = n \times |H|$$
Ici, $n = |X|$ est le nombre de classes (appelé indice de $H$ dans $G$). On a bien $|G| = |X| \times |H|$.

### 9. Théorème de Lagrange
Nous venons de démontrer le **théorème de Lagrange** : dans un groupe fini, l'ordre d'un sous-groupe divise l'ordre du groupe.