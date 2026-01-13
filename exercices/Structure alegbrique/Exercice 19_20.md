---
chapitre: "Structures algébriques"
difficulte: "★★★☆"
notions: ["Produit de sous-groupes", "Sous-groupe", "Commutativité", "Élément inverse"]
---

# Énoncé
Soit $(G, \times)$ un groupe, et $H, K$ deux sous-groupes de $G$. Les questions sont indépendantes.

1. Montrer que si $G$ est abélien, alors $HK = \{hk \mid h \in H, k \in K\}$ est un groupe, et que c'est le plus petit sous-groupe de $G$ contenant $H \cup K$.
2. Dans le cas général, montrer que les propriétés suivantes sont équivalentes :
   (i) $HK$ est un sous-groupe de $G$
   (ii) $KH$ est un sous-groupe de $G$
   (iii) $HK \subset KH$
   (iv) $KH \subset HK$
3. Soit $H, K, L$ trois sous-groupes de $G$ tels que $HK = KH$ et $H \subset L$. Montrer que :
   $H(K \cap L) = (K \cap L)H = (HK) \cap L$.

---

# Indications
1. **Structure de groupe :** Vérifiez les critères de caractérisation habituels (non-vacuité, stabilité par la loi et l'inverse). Pour la minimalité, montrez que tout sous-groupe contenant $H$ et $K$ contient nécessairement tous les produits $hk$.
2. **Équivalences :** Utilisez le fait que $(HK)^{-1} = KH$. Pour montrer $(i) \implies (iii)$, utilisez l'inversibilité dans le sous-groupe $HK$.
3. **Double inclusion :** Pour $(HK) \cap L = H(K \cap L)$, utilisez l'inclusion $H \subset L$ pour justifier qu'un produit $hk$ appartient à $L$ si et seulement si $k$ appartient à $L$.

---

# Correction

### 1. Cas abélien
Supposons $G$ abélien.
- **LCI et stabilité :** Soient $x, y \in HK$. On peut écrire $x = h_1 k_1$ et $y = h_2 k_2$ avec $(h_1, h_2) \in H^2$ et $(k_1, k_2) \in K^2$.
  $x \cdot y = h_1 k_1 h_2 k_2 = (h_1 h_2)(k_1 k_2)$ par commutativité.
  Puisque $H$ et $K$ sont des sous-groupes, $h_1 h_2 \in H$ et $k_1 k_2 \in K$. Donc $xy \in HK$. La loi est stable.
- **Élément neutre :** $e = e \cdot e \in HK$ car $e \in H$ et $e \in K$.
- **Symétrique :** $x^{-1} = (h_1 k_1)^{-1} = k_1^{-1} h_1^{-1} = h_1^{-1} k_1^{-1}$ par commutativité. $x^{-1} \in HK$ car $h_1^{-1} \in H$ et $k_1^{-1} \in K$.
- **Minimalité :** Soit $G'$ un sous-groupe contenant $H \cup K$. Alors $\forall h \in H, \forall k \in K$, on a $(h, k) \in (G')^2$. Par stabilité de $G'$, le produit $hk \in G'$. Donc $HK \subset G'$. Comme $H \subset HK$ (en prenant $k=e$) et $K \subset HK$ (en prenant $h=e$), $HK$ est bien le plus petit sous-groupe contenant $H \cup K$.

### 2. Équivalences dans le cas général
Remarquons que pour toutes parties $A, B$ d'un groupe, $(AB)^{-1} = B^{-1}A^{-1}$. Puisque $H$ et $K$ sont des sous-groupes, $H^{-1} = H$ et $K^{-1} = K$. Donc $(HK)^{-1} = KH$.

- **$(i) \iff (iv)$ :** Un sous-ensemble $S$ est un sous-groupe ssi $S \neq \emptyset$ et $S = S^{-1}$ et $SS \subset S$. Ici, $HK$ est un sous-groupe ssi $HK = (HK)^{-1} = KH$ (ce qui implique $KH \subset HK$).
- **$(iii) \iff (iv)$ :** En passant à l'inverse, $HK \subset KH \iff (HK)^{-1} \subset (KH)^{-1} \iff KH \subset HK$.
Les quatre propriétés sont en réalité équivalentes à la condition de "commutation" des ensembles : $HK = KH$.

### 3. Identité modulaire
Supposons $HK = KH$ et $H \subset L$.
- **Montrons $H(K \cap L) = (HK) \cap L$ :**
  - ($\subset$) Soit $x \in H(K \cap L)$. $x = h k$ avec $h \in H$ et $k \in K \cap L$.
    $hk \in HK$ par définition. Comme $H \subset L$ et $k \in L$, alors $hk \in L$ par stabilité de $L$. Donc $x \in (HK) \cap L$.
  - ($\supset$) Soit $x \in (HK) \cap L$. $x = hk$ avec $h \in H, k \in K$. Comme $x \in L$ et $h \in H \subset L$, alors $k = h^{-1} x \in L$ par stabilité de $L$.
    Ainsi $k \in K \cap L$, d'où $x \in H(K \cap L)$.
- **Égalité avec $(K \cap L)H$ :**
  Puisque $HK=KH$, on peut appliquer le même raisonnement par symétrie (ou en passant à l'inverse) pour obtenir l'égalité bilatérale.