---
chapitre: "Arithmétique dans Z"
difficulte: "★★★☆"
notions: ["Récurrence", "Congruences", "Parité"]
---

# Énoncé
Soient $a$ un entier relatif impair et $n \in \mathbb{N}$. Montrer que $a^{2^n} \equiv 1 [2^{n+1}]$.

# Indications
- Procédez par récurrence sur $n$.
- Pour l'hérédité, factorisez $a^{2^{n+1}} - 1$ comme une différence de carrés : $(a^{2^n})^2 - 1$.
- Utilisez le fait que si $x$ est impair, $x+1$ est pair.

# Correction
**Initialisation ($n=0$) :**
On doit montrer $a^{2^0} \equiv 1 [2^1]$, soit $a \equiv 1 [2]$.
[cite_start]C'est vrai car $a$ est supposé impair[cite: 276].

**Hérédité :**
Supposons que $a^{2^n} \equiv 1 [2^{n+1}]$. Cela signifie que $a^{2^n} - 1 = k \cdot 2^{n+1}$ pour un certain $k$.
Calculons pour $n+1$ :
$a^{2^{n+1}} - 1 = (a^{2^n})^2 - 1 = (a^{2^n} - 1)(a^{2^n} + 1)$.
- Le premier facteur $(a^{2^n} - 1)$ est divisible par $2^{n+1}$ par hypothèse de récurrence.
- Le second facteur $(a^{2^n} + 1)$ est un entier **pair**. En effet, $a$ est impair, donc toute puissance de $a$ est impaire, et impair + 1 = pair. Donc $(a^{2^n} + 1)$ est divisible par 2.
Le produit est donc divisible par $2^{n+1} \times 2 = 2^{n+2}$.
[cite_start]Conclusion : $a^{2^{n+1}} \equiv 1 [2^{n+2}]$ [cite: 277-280].