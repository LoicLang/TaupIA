---
chapitre: "Structures algébriques"
difficulte: "★★☆☆"
notions: ["Automorphisme", "Morphismes de groupes", "Noyau et Image", "Automorphismes intérieurs"]
---

# Énoncé
Soit $G$ un groupe. Pour tout $a \in G$, on définit :
$$f_a : \begin{cases} G \to G \\ g \mapsto aga^{-1} \end{cases}$$

1. Démontrer que $f_a$ est un automorphisme de $G$. On note $\text{Int}(G)$ l'ensemble des applications $f_a$ lorsque $a$ décrit $G$.
2. Montrer que $\varphi : \begin{cases} G \to \text{Aut}(G) \\ a \mapsto f_a \end{cases}$ est un morphisme de groupes.
3. Quel est le noyau de $\varphi$ ? Quel est son image ?
4. En déduire que $(\text{Int}(G), \circ)$ est un groupe.

---

# Indications
- **Question 1 :** Pour montrer qu'il s'agit d'un automorphisme, vérifiez d'abord que $f_a$ est un morphisme de $G$ dans $G$. Prouvez ensuite sa bijectivité en montrant que $f_{a^{-1}}$ est son application réciproque.
- **Question 2 :** Appliquez la définition du morphisme : vérifiez que $\varphi(ab) = \varphi(a) \circ \varphi(b)$ pour tous $a, b \in G$.
- **Question 3 :** Le noyau est l'ensemble des éléments $a$ tels que $f_a = \text{id}_G$. L'image est donnée par définition dans l'énoncé.
- **Question 4 :** Utilisez la propriété selon laquelle l'image d'un groupe par un morphisme est un sous-groupe du groupe d'arrivée.

---

# Correction

### 1. $f_a$ est un automorphisme de $G$
- **Morphisme :** Soient $(g, h) \in G^2$.
  $f_a(gh) = a(gh)a^{-1}$. Par associativité et en insérant $e = a^{-1}a$ :
  $f_a(gh) = (aga^{-1})(aha^{-1}) = f_a(g)f_a(h)$.
  Donc $f_a$ est un endomorphisme de $G$.
- **Bijectivité :** Soit $g \in G$. On a $f_a \circ f_{a^{-1}}(g) = f_a(a^{-1}ga) = a(a^{-1}ga)a^{-1} = g$.
  De même, $f_{a^{-1}} \circ f_a(g) = g$.
  Ainsi, $f_a$ est bijective de réciproque $f_{a^{-1}}$.
C'est donc un automorphisme de $G$.

### 2. $\varphi$ est un morphisme de groupes
Soient $(a, b) \in G^2$. On veut montrer que $\varphi(ab) = f_{ab} = f_a \circ f_b$.
Pour tout $g \in G$ :
$f_{ab}(g) = (ab)g(ab)^{-1} = abgb^{-1}a^{-1}$ car $(ab)^{-1} = b^{-1}a^{-1}$.
Or $f_a(f_b(g)) = f_a(bgb^{-1}) = a(bgb^{-1})a^{-1} = abgb^{-1}a^{-1}$.
On a bien $f_{ab} = f_a \circ f_b$, donc $\varphi$ est un morphisme de $(G, \cdot)$ dans $(\text{Aut}(G), \circ)$.

### 3. Noyau et Image
- **Noyau :** $a \in \text{Ker}(\varphi) \iff f_a = \text{id}_G$.
  Ceci signifie $\forall g \in G, aga^{-1} = g$, soit $\forall g \in G, ag = ga$.
  Le noyau est donc l'ensemble des éléments de $G$ qui commutent avec tous les autres : **$\text{Ker}(\varphi) = Z(G)$** (le centre de $G$).
- **Image :** Par définition de l'énoncé, $\text{Im}(\varphi)$ est l'ensemble des $f_a$ pour $a \in G$. Donc **$\text{Im}(\varphi) = \text{Int}(G)$**.

### 4. Structure de $(\text{Int}(G), \circ)$
On sait que $(\text{Aut}(G), \circ)$ est un groupe.
Puisque $\text{Int}(G)$ est l'image du groupe $G$ par le morphisme $\varphi$, c'est un sous-groupe de $(\text{Aut}(G), \circ)$.
En tant que sous-groupe, $(\text{Int}(G), \circ)$ est lui-même un groupe.