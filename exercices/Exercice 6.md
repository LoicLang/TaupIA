---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Sous-groupe", "Réunion de sous-groupes", "Raisonnement par l'absurde"]
---

# Énoncé
Soient $G$ un groupe et $H, K$ deux sous-groupes de $G$. Montrer que $H \cup K$ est un sous-groupe de $G$ si et seulement si $K \subset H$ ou $H \subset K$.

---

# Indications
L'énoncé est une équivalence ($\iff$). Procédez par double implication :
1. **Sens $(\Leftarrow)$ :** Ce sens est immédiat. Si l'un est inclus dans l'autre, que vaut $H \cup K$ ? Est-ce alors un sous-groupe ?
2. **Sens $(\Rightarrow)$ :** Utilisez un raisonnement par l'absurde (ou par contraposée). Supposez que $H \cup K$ est un sous-groupe mais que $H \not\subset K$ et $K \not\subset H$. 
   - Traduisez ces non-inclusions par l'existence d'éléments $h \in H \setminus K$ et $k \in K \setminus H$.
   - Considérez l'élément $x = h \star k$. Comme $H \cup K$ est un sous-groupe, où doit se trouver $x$ ?
   - Concluez en montrant que la présence de $x$ dans $H$ ou dans $K$ mène à une contradiction.

---

# Correction

### 1. Condition suffisante $(\Leftarrow)$
Supposons que $H \subset K$. Alors $H \cup K = K$. Comme $K$ est un sous-groupe de $G$, alors $H \cup K$ est un sous-groupe de $G$. 
Le raisonnement est identique si $K \subset H$, car alors $H \cup K = H$.

### 2. Condition nécessaire $(\Rightarrow)$
Supposons que $H \cup K$ est un sous-groupe de $G$. Montrons par l'absurde que $H \subset K$ ou $K \subset H$.
Supposons que $H \not\subset K$ et $K \not\subset H$. 
* Comme $H \not\subset K$, il existe un élément $h \in H$ tel que $h \notin K$.
* Comme $K \not\subset H$, il existe un élément $k \in K$ tel que $k \notin H$.

Puisque $h \in H$ et $k \in K$, ces deux éléments appartiennent à la réunion $H \cup K$. 
Par hypothèse, $H \cup K$ est un sous-groupe, il est donc stable par la loi de composition interne. 
Posons $x = h \star k$. On doit avoir $x \in H \cup K$.
Deux cas se présentent alors :

* **Cas 1 : $x \in H$**
  Comme $h \in H$ et que $H$ est un sous-groupe, $h^{-1} \in H$.
  Par stabilité de $H$ : $k = h^{-1} \star x \in H$.
  Ceci contredit notre hypothèse de départ ($k \notin H$).

* **Cas 2 : $x \in K$**
  Comme $k \in K$ et que $K$ est un sous-groupe, $k^{-1} \in K$.
  Par stabilité de $K$ : $h = x \star k^{-1} \in K$.
  Ceci contredit notre hypothèse de départ ($h \notin K$).

Dans les deux cas, nous aboutissons à une contradiction. Par conséquent, l'hypothèse de départ est fausse : on a nécessairement $H \subset K$ ou $K \subset H$.

**Conclusion :** La réunion de deux sous-groupes est un sous-groupe si et seulement si l'un des deux est inclus dans l'autre.