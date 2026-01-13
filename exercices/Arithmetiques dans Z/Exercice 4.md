---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Équations algébriques", "Rationnels", "Analyse-Synthèse", "Divisibilité"]
---

# Énoncé
[cite_start]L'équation $x^3 + x^2 + 2x + 1 = 0$ admet-elle des solutions rationnelles ? [cite: 23]

# Indications
- Raisonnez par **Analyse-Synthèse**.
- Posez $x = \frac{p}{q}$ sous forme irréductible ($p \wedge q = 1$).
- Réduisez au même dénominateur pour obtenir une équation dans $\mathbb{Z}$.
- Utilisez des arguments de divisibilité (Lemme de Gauss) pour montrer que $p$ doit diviser le terme constant et $q$ le coefficient dominant.

# Correction
**Analyse :**
Supposons qu'il existe une solution $x = \frac{p}{q}$ avec $p \in \mathbb{Z}, q \in \mathbb{N}^*$ et $p \wedge q = 1$.
L'équation devient $\frac{p^3}{q^3} + \frac{p^2}{q^2} + \frac{2p}{q} + 1 = 0$.
[cite_start]En multipliant par $q^3$ : $p^3 + p^2q + 2pq^2 + q^3 = 0$[cite: 174, 176].

1. $p(p^2 + pq + 2q^2) = -q^3 \implies p | q^3$. Comme $p \wedge q = 1$, alors $p | [cite_start]1 \implies p \in \{-1, 1\}$[cite: 177].
2. $q(p^2 + 2pq + q^2) = -p^3 \implies q | p^3$. Comme $p \wedge q = 1$, alors $q | [cite_start]1 \implies q = 1$[cite: 178].

Les seules solutions rationnelles possibles sont donc entières : $x = 1$ ou $x = -1$.

**Synthèse :**
- Si $x = 1$ : $1 + 1 + 2 + 1 = 5 \neq 0$.
- [cite_start]Si $x = -1$ : $-1 + 1 - 2 + 1 = -1 \neq 0$[cite: 180].

[cite_start]**Conclusion :** L'équation n'admet aucune solution rationnelle[cite: 181].