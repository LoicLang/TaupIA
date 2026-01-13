---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Nombres complexes", "Racines de l'unité", "PGCD", "Groupes"]
---

# Énoncé
Soient $a, b \in \mathbb{N}^*$. Montrer que $\mathbb{U}_a \cap \mathbb{U}_b = \mathbb{U}_{a \wedge b}$.

# Indications
- Procédez par double inclusion.
- Pour $\subset$, utilisez le théorème de Bézout ($au + bv = a \wedge b$).
- Pour $\supset$, utilisez la définition de la divisibilité ($d | a \implies a = kd$).

# Correction
1.  **Sens $\supset$ :**
    Soit $z \in \mathbb{U}_{a \wedge b}$. Alors $z^{a \wedge b} = 1$.
    Comme $a \wedge b$ divise $a$, il existe $k$ tel que $a = k(a \wedge b)$.
    Donc $z^a = (z^{a \wedge b})^k = 1^k = 1$. Donc $z \in \mathbb{U}_a$.
    De même, $z \in \mathbb{U}_b$.
    [cite_start]Donc $\mathbb{U}_{a \wedge b} \subset \mathbb{U}_a \cap \mathbb{U}_b$ [cite: 340-343].

2.  **Sens $\subset$ :**
    Soit $z \in \mathbb{U}_a \cap \mathbb{U}_b$. On a $z^a = 1$ et $z^b = 1$.
    D'après le **théorème de Bézout**, il existe $u, v \in \mathbb{Z}$ tels que $au + bv = a \wedge b$.
    Alors $z^{a \wedge b} = z^{au + bv} = (z^a)^u \times (z^b)^v$.
    Comme $z^a = 1$ et $z^b = 1$, on a $z^{a \wedge b} = 1^u \times 1^v = 1$.
    [cite_start]Donc $z \in \mathbb{U}_{a \wedge b}$ [cite: 348-351].

[cite_start]**Conclusion :** $\mathbb{U}_a \cap \mathbb{U}_b = \mathbb{U}_{a \wedge b}$[cite: 361].