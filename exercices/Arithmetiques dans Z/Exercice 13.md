---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["PGCD", "Théorème de Bézout", "Lemme de Gauss", "Coefficients binomiaux"]
---

# Énoncé
1. Montrer que, pour tout entier naturel $n$, les nombres $n+1$ et $2n+1$ sont premiers entre eux.
2. En considérant le coefficient binomial $\binom{2n+1}{n+1}$, montrer que $\binom{2n}{n}$ est divisible par $n+1$.

# Indications
- **Q1 :** Trouvez une relation de Bézout simple entre $n+1$ et $2n+1$.
- **Q2 :** Exprimez $\binom{2n+1}{n+1}$ en fonction de $\binom{2n}{n}$ et utilisez le lemme de Gauss.

# Correction
1.  On cherche une combinaison linéaire valant 1 :
    $2(n+1) - 1(2n+1) = 2n + 2 - 2n - 1 = 1$.
    [cite_start]D'après le théorème de Bézout, $(n+1) \wedge (2n+1) = 1$ [cite: 300-301].

2.  On utilise la formule du pion (ou absorbtion) :
    $\binom{2n+1}{n+1} = \frac{2n+1}{n+1} \binom{2n}{n}$.
    En chassant le dénominateur :
    $(n+1) \binom{2n+1}{n+1} = (2n+1) \binom{2n}{n}$.
    Cela signifie que $n+1$ divise le produit $(2n+1) \binom{2n}{n}$.
    Or, d'après la question 1, $(n+1)$ et $(2n+1)$ sont premiers entre eux.
    [cite_start]D'après le **Lemme de Gauss**, $n+1$ doit diviser l'autre facteur $\binom{2n}{n}$ [cite: 312-316].