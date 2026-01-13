---
chapitre: "Arithmétique dans Z"
difficulte: "★★☆☆"
notions: ["PGCD", "Propriétés élémentaires"]
---

# Énoncé
Soient $a$ et $b$ deux entiers naturels non nuls premiers entre eux. Montrer que $(a+b) \wedge ab = 1$.

# Indications
- Montrez séparément que $(a+b) \wedge a = 1$ et $(a+b) \wedge b = 1$.
- Utilisez la propriété : si $d | u$ et $d | v$, alors $d | u+v$ (ou $u-v$).

# Correction
Posons $d = (a+b) \wedge a$.
$d$ divise la combinaison linéaire $(a+b) - a = b$.
Donc $d$ divise $a$ et $d$ divise $b$.
Comme $a \wedge b = 1$, alors $d=1$.
On a donc $(a+b)$ premier avec $a$.
[cite_start]Par symétrie, $(a+b)$ est premier avec $b$ [cite: 292-295].
Si un nombre est premier avec $a$ et avec $b$, il est premier avec leur produit $ab$.
[cite_start]Donc $(a+b) \wedge ab = 1$[cite: 296].