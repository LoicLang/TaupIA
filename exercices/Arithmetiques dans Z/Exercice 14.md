---
chapitre: "Arithmétique dans Z"
difficulte: "★★★☆"
notions: ["Nombres premiers", "Coefficients binomiaux", "Congruences", "Formule de Pascal"]
---

# Énoncé
Soit $p$ un nombre premier.
1. Montrer que, pour tout entier $k \in [\![1, p-1]\!]$, le nombre premier $p$ divise $\binom{p}{k}$.
2. En déduire que : $\forall k \in [\![0, p-1]\!], \quad \binom{p-1}{k} \equiv (-1)^k [p]$.

# Indications
- **Q1 :** Utilisez la "formule sans nom" (ou du pion) : $k \binom{p}{k} = p \binom{p-1}{k-1}$. Pensez au Lemme de Gauss.
- **Q2 :** Raisonnez par récurrence finie sur $k$ en utilisant la formule du triangle de Pascal : $\binom{p}{k+1} = \binom{p-1}{k} + \binom{p-1}{k+1}$.

# Correction
1.  **Divisibilité de $\binom{p}{k}$ :**
    On sait que $k \binom{p}{k} = p \binom{p-1}{k-1}$.
    Donc $p$ divise le produit $k \binom{p}{k}$.
    Comme $p$ est premier et que $1 \le k \le p-1$, $p$ ne divise pas $k$ (donc $p \wedge k = 1$).
    [cite_start]D'après le **Lemme de Gauss**, $p$ divise nécessairement $\binom{p}{k}$ [cite: 318-322].

2.  **Congruence de $\binom{p-1}{k}$ :**
    On procède par récurrence finie sur $k \in [\![0, p-1]\!]$.
    * **Initialisation ($k=0$) :** $\binom{p-1}{0} = 1 \equiv (-1)^0 [p]$. C'est vrai.
    * **Hérédité :** Supposons $\binom{p-1}{k} \equiv (-1)^k [p]$ pour un $k < p-1$.
        D'après la formule de Pascal : $\binom{p-1}{k} + \binom{p-1}{k+1} = \binom{p}{k+1}$.
        Or, d'après la question 1, comme $k+1 \in [\![1, p-1]\!]$, on a $\binom{p}{k+1} \equiv 0 [p]$.
        Donc $\binom{p-1}{k+1} \equiv -\binom{p-1}{k} [p]$.
        Par hypothèse de récurrence : $\binom{p-1}{k+1} \equiv -(-1)^k \equiv (-1)^{k+1} [p]$.
    * [cite_start]**Conclusion :** La propriété est vraie pour tout $k \in [\![0, p-1]\!]$ [cite: 324-330].