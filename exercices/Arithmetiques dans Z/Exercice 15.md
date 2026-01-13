---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["Irrationalité", "Arithmétique élémentaire", "Raisonnement par l'absurde"]
---

# Énoncé
Soient $a, b \in \mathbb{N} \setminus \{0, 1\}$. Montrer que si $a$ et $b$ sont premiers entre eux, alors $\frac{\ln(a)}{\ln(b)} \in \mathbb{R} \setminus \mathbb{Q}$.

# Indications
- Raisonnez par l'absurde en posant $\frac{\ln(a)}{\ln(b)} = \frac{p}{q}$.
- Transformez l'égalité pour obtenir une relation entre puissances de $a$ et $b$.
- Utilisez la décomposition en facteurs premiers ou le Lemme de Gauss.

# Correction
Supposons par l'absurde que $\frac{\ln(a)}{\ln(b)} = \frac{p}{q}$ avec $p, q \in \mathbb{N}^*$.
Alors $q \ln(a) = p \ln(b) \iff \ln(a^q) = \ln(b^p) \iff a^q = b^p$.
Cela implique que $a$ divise $b^p$.
Comme $a \wedge b = 1$, d'après le lemme de Gauss (ou par unicité de la décomposition en facteurs premiers), $a$ n'a aucun facteur premier en commun avec $b$, donc avec $b^p$.
La seule possibilité pour que $a$ divise $b^p$ est que $a=1$.
Or l'énoncé précise $a \in \mathbb{N} \setminus \{0, 1\}$. C'est une contradiction.
[cite_start]Donc $\frac{\ln(a)}{\ln(b)}$ est irrationnel [cite: 331-335].