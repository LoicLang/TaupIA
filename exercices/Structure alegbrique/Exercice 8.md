---
chapitre: "Structures algébriques"
difficulte: "★★★☆"
notions: ["Groupe abélien", "Sous-groupe", "Classes à gauche", "Dénombrement"]
---

# Énoncé
Soit $G$ un groupe tel que : $\forall g \in G, g^2 = e$.

1. Montrer que $G$ est abélien.
2. Montrer que si $H$ est un sous-groupe de $G$ et $a \in G \setminus H$, alors $H \cup aH$ est un sous-groupe de $G$ et $H \cap aH = \emptyset$.
3. Déduire de la question précédente que si $G$ est fini, alors son cardinal est une puissance de 2.

---

# Indications
- **Question 1 :** Par hypothèse, tout élément est son propre inverse ($g = g^{-1}$). Développez $(ab)^2 = e$.
- **Question 2 :** - Pour l'intersection vide, raisonnez par l'absurde : si $x \in H \cap aH$, alors $x = h_1 = a h_2$. Isolez $a$.
  - Pour la structure de sous-groupe, vérifiez les trois critères classiques. Utilisez le fait que $G$ est abélien pour simplifier les produits.
- **Question 3 :** Procédez par récurrence ou par construction successive. Si $G$ n'est pas encore épuisé par un sous-groupe $H_n$ de cardinal $2^n$, prenez un élément $a$ à l'extérieur et construisez $H_{n+1}$ avec la question 2.

---

# Correction

### 1. $G$ est abélien
Soit $(a, b) \in G^2$. Par hypothèse, $a^2 = e$, $b^2 = e$ et $(ab)^2 = e$.
L'égalité $(ab)^2 = e$ s'écrit $abab = e$. 
En multipliant à gauche par $a$ et à droite par $b$, on obtient :
$a(abab)b = aeb \implies (aa)ba(bb) = ab$.
Comme $a^2 = e$ et $b^2 = e$, il reste :
$eba e = ab \implies ba = ab$.
La loi est commutative, donc $G$ est abélien.

### 2. Étude de $H \cup aH$
Soit $H$ un sous-groupe de $G$ et $a \notin H$. 

**Intersection vide :**
Supposons qu'il existe $x \in H \cap aH$. Alors il existe $h_1, h_2 \in H$ tels que $x = h_1$ et $x = a h_2$.
On a donc $h_1 = a h_2 \implies a = h_1 h_2^{-1}$.
Puisque $H$ est un sous-groupe, $h_1 h_2^{-1} \in H$. 
Cela impliquerait $a \in H$, ce qui contredit l'hypothèse. Donc $H \cap aH = \emptyset$.

**Structure de sous-groupe :**
Posons $K = H \cup aH$.
- **Non-vacuité :** $e \in H \subset K$, donc $K \neq \emptyset$.
- **Stabilité par inverse :** Soit $x \in K$. Si $x \in H$, $x^{-1} \in H \subset K$. Si $x \in aH$, $x = ah$. Comme $G$ est abélien et que chaque élément est son propre inverse : $x^{-1} = x = ah \in aH \subset K$.
- **Stabilité par la loi :** Soient $x, y \in K$.
  - Si $x, y \in H$, $xy \in H \subset K$.
  - Si $x \in H$ et $y = ah \in aH$, alors $xy = x(ah) = a(xh) \in aH \subset K$ (par commutativité et stabilité de $H$).
  - Si $x = ah_1 \in aH$ et $y = ah_2 \in aH$, alors $xy = (ah_1)(ah_2) = a^2 h_1 h_2 = e h_1 h_2 = h_1 h_2 \in H \subset K$.
$K$ est donc un sous-groupe de $G$.

### 3. Cardinal de $G$
Notons $|X|$ le cardinal d'un ensemble $X$. Puisque $H \cap aH = \emptyset$ et que l'application $h \mapsto ah$ est bijective, on a $|aH| = |H|$. 
Ainsi, $|H \cup aH| = |H| + |aH| = 2|H|$.
On peut construire une suite de sous-groupes $(H_n)$ :
- $H_0 = \{e\}$, de cardinal $1 = 2^0$.
- Si $H_n \neq G$, il existe $a \in G \setminus H_n$. On pose $H_{n+1} = H_n \cup a H_n$. 
D'après la question 2, $H_{n+1}$ est un sous-groupe de cardinal $2|H_n| = 2 \times 2^n = 2^{n+1}$.
Comme $G$ est fini, ce processus s'arrête nécessairement quand $H_n = G$. 
Le cardinal de $G$ est donc de la forme $2^n$ pour un certain $n \in \mathbb{N}$.