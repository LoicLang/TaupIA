---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Anneau", "Élément nilpotent", "Inversibilité", "Série géométrique"]
---

# Énoncé
Soit $A$ un anneau et $a$ un élément nilpotent de $A$. [cite_start]Montrer que $1 - a$ est inversible, et exprimer son inverse en fonction des puissances successives de $a$.

---

# Indications
Comment exprimer, dans $\mathbb{R}$, $\frac{1}{1-x}$ sous forme d'une somme (infinie) ? Analogisez en tenant compte du fait que pour un élément nilpotent, cette somme devient finie.

---

# Correction

### 1. Définition de la nilpotence
[cite_start]Un élément $a \in A$ est dit nilpotent s'il existe un entier $n \in \mathbb{N}^*$ tel que $a^n = 0_A$[cite: 167]. On suppose ici un tel $n$ fixé.

### 2. Candidat pour l'inverse
En s'inspirant de la série géométrique réelle $\sum x^k$, on pose comme candidat pour l'inverse l'élément $b$ suivant :
$$b = \sum_{k=0}^{n-1} a^k = 1 + a + a^2 + \dots + a^{n-1}$$

### 3. Vérification de l'inversibilité bilatérale
Pour prouver que $1-a$ est inversible, nous devons vérifier que $(1-a)b = 1$ et $b(1-a) = 1$.

* **Calcul de $(1-a)b$ :**
  En utilisant la distributivité de la multiplication sur l'addition dans l'anneau $A$ :
  $$(1 - a) \sum_{k=0}^{n-1} a^k = \sum_{k=0}^{n-1} a^k - a \sum_{k=0}^{n-1} a^k$$
  $$(1 - a)b = (1 + a + a^2 + \dots + a^{n-1}) - (a + a^2 + a^3 + \dots + a^n)$$
  Par télescopage, tous les termes intermédiaires s'annulent :
  $$(1 - a)b = 1 - a^n$$
  Puisque $a^n = 0_A$ par hypothèse de nilpotence, on obtient : $(1-a)b = 1$.

* **Calcul de $b(1-a)$ :**
  De la même manière, ou en remarquant que $a$ commute avec toutes ses puissances :
  $$b(1 - a) = \sum_{k=0}^{n-1} a^k - \left(\sum_{k=0}^{n-1} a^k\right)a = \sum_{k=0}^{n-1} a^k - \sum_{k=1}^{n} a^k = 1 - a^n = 1$$

### Conclusion
[cite_start]L'élément $1 - a$ est donc inversible dans $A$. Son inverse est donné par la somme finie des puissances de $a$ :
$$(1 - a)^{-1} = \sum_{k=0}^{n-1} a^k$$