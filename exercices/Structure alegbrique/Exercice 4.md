---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Groupe abélien", "Différence symétrique", "Ensemble des parties", "Élément neutre", "Auto-symétrique"]
---

# Énoncé
Soit $E$ un ensemble non vide. On définit la loi $\Delta$ sur $\mathcal{P}(E)$ par :
$$A \Delta B = (A \setminus B) \cup (B \setminus A)$$

1. Montrer que $(\mathcal{P}(E), \Delta)$ est un groupe abélien.

---

# Indications
- **Commutativité :** Observez la symétrie de la définition par rapport à $A$ et $B$.
- **Associativité :** C'est le point technique. Une méthode rigoureuse consiste à passer par les fonctions caractéristiques : $\mathbb{1}_{A \Delta B} \equiv \mathbb{1}_A + \mathbb{1}_B \pmod 2$.
- **Élément neutre :** Cherchez un ensemble $X \in \mathcal{P}(E)$ tel que $A \Delta X = A$. Testez l'ensemble vide.
- **Symétrique :** Calculez $A \Delta A$. Dans ce groupe, chaque élément est son propre symétrique.

---

# Correction

### 1. $(\mathcal{P}(E), \Delta)$ est un groupe abélien

**LCI et caractère bien défini :**
Par définition des opérations de base (différence et réunion), si $A$ et $B$ sont des parties de $E$, alors $A \Delta B$ est également une partie de $E$. La loi $\Delta$ est donc une LCI sur $\mathcal{P}(E)$.

**Commutativité :**
Pour tout $(A, B) \in \mathcal{P}(E)^2$ :
$$A \Delta B = (A \setminus B) \cup (B \setminus A)$$
$$B \Delta A = (B \setminus A) \cup (A \setminus B)$$
Par commutativité de la réunion dans $\mathcal{P}(E)$, on a $A \Delta B = B \Delta A$. La loi est commutative.

**Associativité :**
Démontrons que $(A \Delta B) \Delta C = A \Delta (B \Delta C)$. Utilisons les fonctions caractéristiques $\mathbb{1}_X$ pour tout $X \subset E$. On sait que :
$$\mathbb{1}_{A \Delta B} = \mathbb{1}_A + \mathbb{1}_B - 2\mathbb{1}_{A \cap B}$$
Modulo 2, cela devient : $\mathbb{1}_{A \Delta B} \equiv \mathbb{1}_A + \mathbb{1}_B \pmod 2$.
Dès lors :
- $\mathbb{1}_{(A \Delta B) \Delta C} \equiv (\mathbb{1}_A + \mathbb{1}_B) + \mathbb{1}_C \pmod 2$
- $\mathbb{1}_{A \Delta (B \Delta C)} \equiv \mathbb{1}_A + (\mathbb{1}_B + \mathbb{1}_C) \pmod 2$
Par associativité de l'addition dans $\mathbb{Z}/2\mathbb{Z}$, les deux fonctions caractéristiques sont égales, donc les ensembles sont égaux. La loi $\Delta$ est associative.

**Élément neutre :**
Cherchons un ensemble neutre $e$. Testons l'ensemble vide $\emptyset \in \mathcal{P}(E)$ :
$$A \Delta \emptyset = (A \setminus \emptyset) \cup (\emptyset \setminus A) = A \cup \emptyset = A$$
Par commutativité, on a aussi $\emptyset \Delta A = A$. L'ensemble vide $\emptyset$ est donc le neutre unique.

**Symétrisabilité :**
Soit $A \in \mathcal{P}(E)$. Cherchons son symétrique en calculant $A \Delta A$ :
$$A \Delta A = (A \setminus A) \cup (A \setminus A) = \emptyset \cup \emptyset = \emptyset$$
Ainsi, tout élément $A$ est son propre symétrique (on dit qu'il est auto-symétrique ou involutif). L'existence du symétrique est assurée pour tout élément.

**Conclusion :** $(\mathcal{P}(E), \Delta)$ est un groupe abélien.