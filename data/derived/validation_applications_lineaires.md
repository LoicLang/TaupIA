# Validation des prérequis — chapitre *applications linéaires*

**174 arêtes retenues** (sur 212 proposées, 38 réfutées par le vérificateur adversarial).

Pour chaque concept, ses prérequis directs retenus. La mention `[<-espaces_vectoriels]` signale un prérequis venant d'un chapitre amont. Coche/marque celles qui te semblent FAUSSES, et dans la section réfutées, celles qui auraient dû être GARDÉES.

---
## Arêtes RETENUES (à vérifier : précision)

### [1] Définition : Application linéaire  _( definition )_
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.98
      L'énoncé suppose connus les $\mathbb{K}$-espaces vectoriels $E$ et $F$, objets de départ et d'arrivée de l'application.

### [2] Propriété : Image du vecteur nul  _( property )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé porte sur une application linéaire $f \in \mathcal{L}(E,F)$, objet central dont la définition doit être maîtrisée.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé mobilise les espaces vectoriels $E$ et $F$ et leurs vecteurs nuls $0_E$, $0_F$, qui n'ont de sens que via cette définition.

### [4] Propriété : Critère simplifié de linéarité  _( property )_
- [ ] **Définition : Application linéaire**  · conf 0.99
      Le critère sert précisément à vérifier la linéarité, donc l'énoncé n'a aucun sens sans la définition d'application linéaire.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé mobilise des espaces vectoriels E, F sur K, leurs vecteurs, scalaires et le vecteur nul, structures qui doivent être déjà connues.

### [5] Définition : Morphisme d'algèbres  _( definition )_
- [ ] **Définition : Algèbre**  [<-espaces_vectoriels]  · conf 0.97
      L'énoncé porte sur des morphismes entre deux K-algèbres, donc la notion d'algèbre doit être maîtrisée pour comprendre les objets A et B.
- [ ] **Définition : Application linéaire**  · conf 0.95
      Un morphisme d'algèbres est par définition une application linéaire (en plus d'être un morphisme d'anneaux), notion explicitement mobilisée par l'énoncé.

### [6] Définition : Homothétie  _( definition )_
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.95
      L'énoncé débute par « Soient E un K-espace vectoriel et λ ∈ K », donc la notion d'espace vectoriel et de scalaire est indispensable.
- [ ] **Définition : Application linéaire**  · conf 0.92
      L'énoncé affirme que λId_E est un endomorphisme et que Id_E ∈ L(E), ce qui suppose de connaître la définition d'application linéaire/endomorphisme.

### [12] Définition-théorème : Application linéaire canoniquement associée à une matrice  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé affirme que X ↦ AX est 'linéaire', notion qui suppose de connaître la définition d'une application linéaire.

### [14] Définition-théorème : Formes coordonnées relativement à une base  _( theorem )_
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.98
      L'énoncé repose entièrement sur la notion de base et de coordonnée d'un vecteur dans cette base, qui est précisément ce que chaque forme coordonnée extrait.
- [ ] **Définition : Application linéaire**  · conf 0.92
      Le théorème affirme que chaque forme coordonnée est une forme linéaire (application linéaire à valeurs dans K), notion indispensable pour comprendre l'énoncé.

### [16] Définition : Isomorphisme, espaces vectoriels isomorphes  _( definition )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      Un isomorphisme est défini comme une application linéaire bijective, donc la notion d'application linéaire est indispensable pour comprendre l'énoncé.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.92
      L'énoncé porte sur des applications entre deux K-espaces vectoriels E et F, dont la définition doit être maîtrisée.

### [19] Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé manipule des éléments de $\mathcal{L}(E,F)$ et $\mathcal{L}(F,G)$, donc la notion d'application linéaire doit être maîtrisée.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.97
      L'énoncé parle d'isomorphismes, d'automorphisme et de la réciproque d'un isomorphisme, notions définies par ce concept.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.85
      L'énoncé porte sur trois $\mathbb{K}$-espaces vectoriels $E$, $F$, $G$, objet fondamental sans lequel il n'a pas de sens.

### [21] Théorème : Traduction de l'inversibilité en termes d'application linéaire canoniquement associée  _( theorem )_
- [ ] **Définition-théorème : Application linéaire canoniquement associée à une matrice**  · conf 0.97
      L'énoncé porte sur l'application linéaire canoniquement associée à A, objet central défini par ce concept.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.9
      Un automorphisme est un isomorphisme d'un espace dans lui-même, notion sans laquelle l'énoncé n'a pas de sens.
- [ ] **Définition : Application linéaire**  · conf 0.8
      L'énoncé manipule une application linéaire, dont la définition est indispensable.

### [23] Théorème : Combinaisons linéaires d'applications linéaires  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé porte sur l'ensemble L(E,F) des applications linéaires, dont la définition est indispensable.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.95
      L'énoncé affirme que L(E,F) est un K-espace vectoriel, notion qui doit être connue.
- [ ] **Définition : Sous-espace vectoriel**  [<-espaces_vectoriels]  · conf 0.95
      L'énoncé qualifie L(E,F) de sous-espace vectoriel de F^E, notion centrale de la conclusion.
- [ ] **Théorème : Espaces vectoriels d'applications**  [<-espaces_vectoriels]  · conf 0.88
      L'énoncé suppose connue la structure d'espace vectoriel de F^E (ensemble d'applications de E dans F).
- [ ] **Définition : Combinaisons linéaires d'un nombre fini de vecteurs**  [<-espaces_vectoriels]  · conf 0.82
      L'énoncé parle de toute combinaison linéaire d'applications linéaires, notion à maîtriser pour comprendre la formulation.

### [26] Théorème : Algèbre $\mathcal{L}(E)$  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé porte sur L(E), l'ensemble des endomorphismes (applications linéaires de E dans E), notion sans laquelle l'énoncé n'a aucun sens.
- [ ] **Définition : Algèbre**  [<-espaces_vectoriels]  · conf 0.95
      Le théorème affirme que L(E) est une K-algèbre, donc la structure d'algèbre doit déjà être maîtrisée pour comprendre l'énoncé.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.8
      GL(E) est le groupe des automorphismes (isomorphismes de E dans E), notion nécessaire pour comprendre l'identification des inversibles de l'anneau L(E).
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.75
      L'énoncé débute par 'soit E un K-espace vectoriel', objet de base sur lequel tout repose.

### [28] Définition : Endomorphisme nilpotent  _( definition )_
- [ ] **Définition : Application linéaire**  · conf 0.95
      L'énoncé porte sur f ∈ L(E), donc sur un endomorphisme, ce qui suppose la notion d'application linéaire.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.85
      L'énoncé débute par 'Soit E un K-espace vectoriel', notion sans laquelle f ∈ L(E) n'a pas de sens.

### [30] Théorème : Image d'un sous-espace vectoriel par une application linéaire  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé porte sur f ∈ L(E,F) : il faut savoir ce qu'est une application linéaire pour comprendre l'objet f(A) et Im f.
- [ ] **Définition : Sous-espace vectoriel**  [<-espaces_vectoriels]  · conf 0.97
      L'énoncé affirme que f(A) et Im f sont des sous-espaces vectoriels, notion centrale qu'il faut déjà maîtriser.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.8
      E et F sont des K-espaces vectoriels et f(E)=Im f ⊂ F : la notion d'espace vectoriel sous-tend tout l'énoncé.

### [32] Théorème : Image d'un Vect par une application linéaire  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé porte sur f ∈ L(E,F), donc la notion d'application linéaire est indispensable pour comprendre l'objet f.
- [ ] **Définition : Sous-espace vectoriel engendré par une partie**  [<-espaces_vectoriels]  · conf 0.98
      L'énoncé manipule Vect(X) et Vect(f(X)), donc le sous-espace engendré par une partie est central à la compréhension.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.9
      Le cas particulier de l'énoncé suppose que E possède une base (e_i), notion nécessaire à sa formulation.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.82
      L'énoncé met en jeu deux K-espaces vectoriels E et F, cadre de base sans lequel l'énoncé n'a pas de sens.

### [35] Définition-théorème : Image d'une matrice  _( theorem )_
- [ ] **Définition-théorème : Application linéaire canoniquement associée à une matrice**  · conf 0.97
      L'énoncé définit Im A via l'application linéaire canoniquement associée X↦AX, objet directement mobilisé.
- [ ] **Définition : Sous-espace vectoriel engendré par une partie**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé exprime Im A comme le Vect(C_1,…,C_p), donc le sous-espace engendré par une partie est indispensable.
- [ ] **Définition : Application linéaire**  · conf 0.85
      Im A est l'image d'une application linéaire, notion fondamentale sans laquelle l'énoncé n'a pas de sens.

### [38] Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé porte sur f ∈ L(E,F) : la notion d'application linéaire est l'objet central manipulé.
- [ ] **Définition : Sous-espace vectoriel**  [<-espaces_vectoriels]  · conf 0.97
      L'énoncé affirme que f^{-1}(B) et Ker f sont des sous-espaces vectoriels, notion indispensable à sa formulation.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.85
      E et F sont des K-espaces vectoriels, cadre de base sans lequel l'énoncé n'a pas de sens.

### [44] Théorème : Solutions d'une équation linéaire  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé porte sur f \in \mathcal{L}(E,F), donc la notion d'application linéaire est indispensable.
- [ ] **Définition : Sous-espace affine et direction**  [<-espaces_vectoriels]  · conf 0.92
      La conclusion x_0 + Ker f est un sous-espace affine de direction Ker f, notion directement utilisée dans l'énoncé.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.9
      L'énoncé mobilise le noyau Ker f, défini comme image réciproque de {0} par une application linéaire.
- [ ] **Théorème : Image d'un sous-espace vectoriel par une application linéaire**  · conf 0.82
      L'énoncé utilise Im f (condition y_0 \in Im f), notion d'image d'une application linéaire.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.75
      E et F sont des K-espaces vectoriels, cadre de base de l'énoncé.

### [46] Définition-théorème : Noyau d'une matrice  _( theorem )_
- [ ] **Définition-théorème : Application linéaire canoniquement associée à une matrice**  · conf 0.97
      L'énoncé définit Ker A via l'application linéaire canoniquement associée X ↦ AX, notion explicitement mobilisée.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.9
      L'énoncé définit le noyau d'une matrice comme le noyau de son application linéaire, donc la notion de noyau d'une application linéaire doit être déjà connue.
- [ ] **Définition : Application linéaire**  · conf 0.7
      La notion d'application linéaire est nécessaire pour donner un sens à l'application canoniquement associée invoquée dans l'énoncé.

### [49] Théorème : Caractérisation d'une application linéaire par l'image d'une base  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.99
      L'énoncé affirme l'existence et l'unicité d'une application linéaire, notion centrale qu'il faut maîtriser pour comprendre le théorème.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.98
      Le théorème repose entièrement sur l'existence d'une base $(e_i)$ de E et sur l'image qu'on en donne.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé suppose E et F deux K-espaces vectoriels, notion sans laquelle l'énoncé n'a pas de sens.

### [50] Théorème : Caractérisation d'une application linéaire par ses restrictions sur une somme directe  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé porte sur des applications linéaires u_i et u (éléments de L(E_i,F) et L(E,F)), notion sans laquelle il n'a aucun sens.
- [ ] **Définition : Sous-espaces vectoriels en somme directe**  [<-espaces_vectoriels]  · conf 0.97
      L'hypothèse centrale E = E_1 ⊕ ... ⊕ E_p est la décomposition en somme directe que l'on doit déjà maîtriser.
- [ ] **Définition : Sous-espace vectoriel**  [<-espaces_vectoriels]  · conf 0.92
      Les E_1,...,E_p sont des sous-espaces vectoriels de E, objets explicitement mobilisés par l'énoncé.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé manipule deux K-espaces vectoriels E et F qui constituent le cadre de base du théorème.

### [52] Théorème : Caractérisation de l'injectivité/surjectivité d'une application linéaire par l'image d'une base  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé porte sur une application linéaire f de L(E,F), notion qu'il faut connaître pour comprendre le théorème.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.96
      L'énoncé suppose que E possède une base (e_i), objet central du théorème.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.95
      Le point (iii) caractérise f comme isomorphisme, notion explicitement mobilisée dans l'énoncé.
- [ ] **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs**  [<-espaces_vectoriels]  · conf 0.95
      Le point (ii) caractérise l'injectivité par la liberté de la famille (f(e_i)).
- [ ] **Définition : Partie/famille génératrice**  [<-espaces_vectoriels]  · conf 0.94
      Le point (i) repose sur le fait que (f(e_i)) engendre F, c'est-à-dire qu'elle est génératrice.

### [54] Théorème : Effet d'un isomorphisme sur la dimension  _( theorem )_
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.99
      L'énoncé porte entièrement sur l'existence d'un isomorphisme entre E et F, notion centrale qui doit être déjà connue.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.98
      La conclusion compare dim E et dim F, donc la notion de dimension d'un espace vectoriel doit être maîtrisée.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.95
      L'hypothèse et la conclusion reposent sur le fait que les espaces sont de dimension finie.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé manipule des K-espaces vectoriels E, F et K^n, objets fondamentaux du théorème.

### [57] Théorème : Dimension d'un espace vectoriel d'applications linéaires  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'objet de l'énoncé est l'ensemble L(E,F) des applications linéaires, dont il faut connaître la définition.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.93
      Le résultat porte sur la valeur dim L(E,F) = dim E x dim F, ce qui exige la notion de dimension.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.92
      L'énoncé exhibe une base de L(E,F) et utilise des bases de E et F, notion centrale de la conclusion.
- [ ] **Théorème : Combinaisons linéaires d'applications linéaires**  · conf 0.9
      Parler de la dimension et d'une base de L(E,F) suppose de savoir que les applications linéaires forment un espace vectoriel via leurs combinaisons linéaires.
- [ ] **Définition-théorème : Formes coordonnées relativement à une base**  · conf 0.9
      L'énoncé construit la base à l'aide des formes coordonnées e_i^star relativement à une base.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.85
      L'énoncé suppose E et F de dimension finie et conclut que L(E,F) l'est aussi.

### [58] Définition : Application linéaire de rang fini, rang  _( definition )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé porte sur f ∈ L(E,F), il faut donc savoir ce qu'est une application linéaire.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.95
      L'énoncé repose sur la condition « Im f est de dimension finie » pour définir le rang fini.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.95
      Le rang est l'entier dim Im f, ce qui nécessite la notion de dimension d'un espace vectoriel.

### [59] Théorème : Inégalités sur le rang et cas d'égalité  _( theorem )_
- [ ] **Définition : Application linéaire de rang fini, rang**  · conf 0.98
      L'énoncé porte entièrement sur rg(f) ; sans la définition du rang d'une application linéaire, l'inégalité et le cas d'égalité n'ont pas de sens.
- [ ] **Définition : Application linéaire**  · conf 0.95
      L'énoncé manipule f ∈ L(E,F), donc la notion d'application linéaire est indispensable.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.95
      Les quantités dim E et dim F figurent explicitement dans les inégalités, ce qui exige la notion de dimension.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.9
      L'hypothèse centrale « E (ou F) de dimension finie » repose sur la définition d'espace vectoriel de dimension finie.

### [60] Théorème : Applications linéaires entre espaces vectoriels de mêmes dimensions finies  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé porte sur f appartenant à L(E,F), donc la notion d'application linéaire est mobilisée d'emblée.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.95
      L'hypothèse centrale est que E et F sont de dimensions finies égales, ce qui suppose la notion de dimension finie.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.9
      L'égalité des dimensions est l'hypothèse clé, donc la définition de dimension est nécessaire pour comprendre l'énoncé.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.85
      L'équivalence bijective/injective/surjective et la notion de GL(E) reposent sur celle d'isomorphisme (application linéaire bijective).

### [63] Théorème : Forme géométrique du théorème du rang  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé porte sur f ∈ L(E,F), donc requiert la notion d'application linéaire.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.97
      La conclusion affirme que f|I est un isomorphisme de I sur Im f, notion indispensable à l'énoncé.
- [ ] **Définition : Sous-espaces vectoriels supplémentaires**  [<-espaces_vectoriels]  · conf 0.95
      L'hypothèse repose sur l'existence d'un supplémentaire I de Ker f dans E.
- [ ] **Définition : Sous-espaces vectoriels en somme directe**  [<-espaces_vectoriels]  · conf 0.85
      L'égalité E = I ⊕ Ker f utilise la notion de somme directe.

### [64] Théorème : Théorème du rang  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      L'énoncé porte sur f appartenant à L(E,F), donc la notion d'application linéaire est indispensable.
- [ ] **Définition : Application linéaire de rang fini, rang**  · conf 0.97
      Le terme rg(f) apparaît explicitement dans la formule et c'est précisément cette définition.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.95
      La formule égalise des dimensions (dim E, dim Ker f), notion centrale de l'énoncé.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.9
      L'hypothèse 'E de dimension finie' conditionne tout l'énoncé et doit être maîtrisée.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.85
      L'énoncé fait intervenir Ker f, dont la définition est introduite dans ce théorème sur l'image réciproque et le noyau.

### [68] Définition : Rang d'une matrice  _( definition )_
- [ ] **Définition : Application linéaire de rang fini, rang**  · conf 0.95
      L'énoncé définit le rang d'une matrice comme le rang de l'application linéaire associée, ce qui suppose de connaître la définition du rang d'une application linéaire.
- [ ] **Définition : Rang d'une famille finie de vecteurs**  [<-espaces_vectoriels]  · conf 0.95
      L'énoncé identifie le rang de A au rang de la famille des colonnes de A, notion qui doit être déjà maîtrisée.
- [ ] **Définition-théorème : Application linéaire canoniquement associée à une matrice**  · conf 0.93
      L'énoncé invoque l'application linéaire canoniquement associée à A, objet central de la définition.

### [69] Théorème : Rang d'une famille de vecteurs, rang d'une matrice associée  _( theorem )_
- [ ] **Définition : Rang d'une famille finie de vecteurs**  [<-espaces_vectoriels]  · conf 0.98
      L'énoncé pose rg(𝒳), le rang d'une famille finie de vecteurs, qui doit être défini au préalable.
- [ ] **Définition : Rang d'une matrice**  · conf 0.97
      L'énoncé pose rg(Mat_𝓑(𝒳)), le rang d'une matrice, dont la définition est indispensable.
- [ ] **Définition : Matrice d'une famille finie de vecteurs dans une base finie**  [<-espaces_vectoriels]  · conf 0.97
      L'énoncé utilise Mat_𝓑(𝒳), la matrice d'une famille de vecteurs dans une base, objet central de l'égalité.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.85
      L'énoncé fixe une base 𝓑 de E, notion nécessaire pour former la matrice des coordonnées de la famille.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.8
      L'énoncé suppose E de dimension finie, hypothèse indispensable à la formulation du théorème.

### [71] Théorème : Rang d'une composée  _( theorem )_
- [ ] **Définition : Application linéaire de rang fini, rang**  · conf 0.98
      L'énoncé porte entièrement sur la notion de rang rg(f), rg(f∘φ), rg(ψ∘f).
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.95
      Les cas d'égalité sont conditionnés par le fait que φ ou ψ soit un isomorphisme.
- [ ] **Définition : Application linéaire**  · conf 0.92
      L'énoncé manipule des éléments de L(E,F), L(E',E), L(F,F'), donc la notion d'application linéaire.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.8
      L'énoncé se place explicitement dans des K-espaces vectoriels de dimension finie, condition d'existence du rang.

### [72] Théorème : Les opérations élémentaires préservent le rang  _( theorem )_
- [ ] **Définition : Rang d'une matrice**  · conf 0.97
      L'énoncé affirme qu'une opération préserve le rang : sans la définition du rang d'une matrice, l'énoncé n'a aucun sens.

### [73] Méthode : Algorithme de calcul du rang d'une matrice  _( method )_
- [ ] **Définition : Rang d'une matrice**  · conf 0.95
      L'algorithme calcule rg(A), donc l'énoncé n'a de sens que si l'on sait ce qu'est le rang d'une matrice.
- [ ] **Théorème : Les opérations élémentaires préservent le rang**  · conf 0.9
      L'algorithme du pivot fonctionne précisément parce que les opérations élémentaires préservent le rang, théorème directement mobilisé par l'énoncé.

### [75] Définition-théorème : Matrices extraites  _( theorem )_
- [ ] **Définition : Rang d'une matrice**  · conf 0.95
      L'énoncé compare les rangs rg(B) et rg(A), ce qui suppose connue la définition du rang d'une matrice.

### [78] Théorème : Invariance du rang par transposition et caractérisation par les matrices extraites inversibles  _( theorem )_
- [ ] **Définition : Rang d'une matrice**  · conf 0.97
      L'énoncé porte entièrement sur le rang d'une matrice (rg(A), rg(A^T)), notion qui doit être déjà définie pour avoir un sens.
- [ ] **Définition-théorème : Matrices extraites**  · conf 0.92
      L'assertion (ii) parle des matrices qu'on peut extraire de A, donc la notion de matrice extraite est mobilisée dans l'énoncé.

### [80] Théorème : Deux petits résultats bien utiles  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.98
      L'énoncé manipule des applications linéaires f et g de L(E,F) et L(F,G), notion centrale dont dépend tout le théorème.
- [ ] **Théorème : Image d'un sous-espace vectoriel par une application linéaire**  · conf 0.85
      Le théorème utilise Im f, l'image d'un (sous-)espace par une application linéaire, qui doit être connue.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.85
      Le théorème mobilise Ker g, le noyau d'une application linéaire, défini dans ce théorème.
- [ ] **Définition : Sous-espace vectoriel**  [<-espaces_vectoriels]  · conf 0.8
      L'énoncé parle d'inclusion Im f ⊂ Ker g et de sous-espaces stables, ce qui suppose la notion de sous-espace vectoriel.

### [83] Théorème : Noyaux itérés, images itérées et décomposition de Fitting  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.9
      L'énoncé porte sur un endomorphisme f de L(E), notion qui suppose de connaître ce qu'est une application linéaire.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.88
      L'énoncé manipule les noyaux itérés Ker f^k, qui supposent la notion de noyau d'une application linéaire.
- [ ] **Théorème : Image d'un sous-espace vectoriel par une application linéaire**  · conf 0.85
      L'énoncé manipule les images itérées Im f^k comme sous-espaces vectoriels, ce qui suppose la notion d'image d'une application linéaire.
- [ ] **Définition : Sous-espaces vectoriels en somme directe**  [<-espaces_vectoriels]  · conf 0.83
      La décomposition de Fitting (iii) exprime E comme somme directe Ker f^p ⊕ Im f^p, notion centrale de l'énoncé.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.8
      L'énoncé suppose E de dimension finie, hypothèse indispensable à la stationnarité des suites.

### [85] Théorème : Deux propriétés des endomorphismes nilpotents  _( theorem )_
- [ ] **Définition : Endomorphisme nilpotent**  · conf 0.98
      L'énoncé porte sur un endomorphisme nilpotent et son indice de nilpotence, notion centrale qu'il faut connaître pour le comprendre.
- [ ] **Théorème : Noyaux itérés, images itérées et décomposition de Fitting**  · conf 0.95
      Le point (ii) parle explicitement de l'indice au sens de la décomposition de Fitting, défini dans ce théorème.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.85
      L'énoncé mobilise Ker f, dont la définition et le statut de sous-espace vectoriel proviennent de ce théorème.
- [ ] **Théorème : Image d'un sous-espace vectoriel par une application linéaire**  · conf 0.82
      L'énoncé mobilise Im f, dont la définition et la nature de sous-espace vectoriel sont fixées par ce théorème.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.8
      Le point (ii) suppose E de dimension finie n et compare l'indice à n, ce qui requiert la notion de dimension.

### [87] Définition : Projecteur et symétrie  _( definition )_
- [ ] **Définition : Sous-espaces vectoriels supplémentaires**  [<-espaces_vectoriels]  · conf 0.97
      L'énoncé suppose explicitement que F et G sont des sous-espaces supplémentaires, dont la décomposition unique x = f + g est la propriété fondatrice utilisée pour définir le projecteur et la symétrie.
- [ ] **Définition : Sous-espace vectoriel**  [<-espaces_vectoriels]  · conf 0.9
      F et G sont introduits comme des sous-espaces vectoriels de E, notion indispensable pour comprendre l'énoncé.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.85
      E est un K-espace vectoriel, structure de base sur laquelle reposent tous les objets de l'énoncé.

### [89] Théorème : Propriétés des projecteurs et des symétries  _( theorem )_
- [ ] **Définition : Projecteur et symétrie**  · conf 0.98
      L'énoncé porte directement sur la projection et la symétrie associées à des supplémentaires, dont la définition est ici établie.
- [ ] **Définition : Sous-espaces vectoriels supplémentaires**  [<-espaces_vectoriels]  · conf 0.95
      L'énoncé suppose F et G supplémentaires de E, notion indispensable pour définir p et s.
- [ ] **Définition : Application linéaire**  · conf 0.9
      Le théorème affirme que p est un endomorphisme et s un automorphisme, ce qui exige la notion d'application linéaire.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.8
      Dire que s est un automorphisme avec s^{-1}=s mobilise la notion d'isomorphisme/automorphisme.

### [91] Théorème : Caractérisation algébrique des projecteurs  _( theorem )_
- [ ] **Définition : Projecteur et symétrie**  · conf 0.97
      Le théorème caractérise un projecteur, dont la définition géométrique (projection sur un sous-espace parallèlement à un autre) doit être déjà connue.
- [ ] **Définition : Application linéaire**  · conf 0.95
      L'énoncé affirme que p doit être linéaire, ce qui suppose maîtrisée la notion d'application linéaire.
- [ ] **Définition : Sous-espaces vectoriels supplémentaires**  [<-espaces_vectoriels]  · conf 0.9
      Le théorème conclut que Im p et Ker p sont supplémentaires, notion qui doit déjà être comprise.

### [93] Théorème : Caractérisation algébrique des symétries  _( theorem )_
- [ ] **Définition : Projecteur et symétrie**  · conf 0.97
      L'énoncé caractérise la notion de symétrie, qui doit donc être définie au préalable.
- [ ] **Définition : Application linéaire**  · conf 0.95
      L'énoncé affirme que s est linéaire, notion centrale de la caractérisation.
- [ ] **Définition : Sous-espaces vectoriels supplémentaires**  [<-espaces_vectoriels]  · conf 0.93
      La conclusion porte sur le fait que Ker(s-Id) et Ker(s+Id) sont supplémentaires dans E.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.85
      L'énoncé utilise les noyaux Ker(s-Id) et Ker(s+Id), notion de noyau d'une application linéaire.

### [96] Théorème : Lien projecteur/symétrie  _( theorem )_
- [ ] **Définition : Projecteur et symétrie**  · conf 0.99
      L'énoncé porte directement sur la projection sur F parallèlement à G et la symétrie par rapport à F, notions définies par ce concept.
- [ ] **Définition : Sous-espaces vectoriels supplémentaires**  [<-espaces_vectoriels]  · conf 0.97
      L'énoncé suppose F et G sous-espaces vectoriels supplémentaires de E, notion indispensable pour définir projection et symétrie.

### [97] Définition-théorème : Polynômes annulateurs d'un endomorphisme  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.95
      L'énoncé porte sur un endomorphisme f de L(E), donc la notion d'application linéaire est indispensable.
- [ ] **Théorème : Algèbre $\mathcal{L}(E)$**  · conf 0.9
      Écrire P(f) et 0_{L(E)} suppose la structure d'algèbre L(E) (puissances f^k par composition et combinaisons linéaires).

### [99] Théorème : Lemme de décomposition des noyaux  _( theorem )_
- [ ] **Définition-théorème : Polynômes annulateurs d'un endomorphisme**  · conf 0.95
      L'énoncé utilise l'évaluation d'un polynôme en un endomorphisme P_i(f) et la notion de polynôme annulateur, objets définis par ce concept.
- [ ] **Définition : Sous-espaces vectoriels en somme directe**  [<-espaces_vectoriels]  · conf 0.95
      La conclusion exprime une décomposition en somme directe (le symbole oplus), notion centrale de l'énoncé.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.9
      L'énoncé parle de Ker P_i(f), donc suppose maîtrisée la notion de noyau d'une application linéaire.
- [ ] **Définition : Application linéaire**  · conf 0.8
      L'objet f appartient à L(E), espace des endomorphismes, ce qui suppose la notion d'application linéaire.

### [102] Définition-théorème : Dual d'un espace vectoriel  _( theorem )_
- [ ] **Définition : Application linéaire**  · conf 0.97
      Une forme linéaire est une application linéaire de E dans K ; sans cette notion l'énoncé du dual n'a pas de sens.
- [ ] **Définition-théorème : Formes coordonnées relativement à une base**  · conf 0.95
      La base duale est précisément la famille des formes coordonnées associées à une base, objet directement mobilisé par l'énoncé.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé manipule des bases (e_1,...,e_n) de E et affirme que la base duale est une base de E*.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.85
      L'énoncé parle du K-espace vectoriel E et de la structure d'espace vectoriel de L(E,K), notion de base requise.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.85
      L'énoncé suppose E de dimension finie n et conclut sur dim E* = dim E, ce qui nécessite la notion de dimension.

### [105] Définition : Hyperplan  _( definition )_
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.9
      Un hyperplan est défini comme le noyau d'une forme linéaire, notion introduite et caractérisée ici.
- [ ] **Définition : Application linéaire**  · conf 0.85
      Une forme linéaire est une application linéaire vers le corps des scalaires, donc cette définition fonde la notion mobilisée.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.8
      L'énoncé suppose un K-espace vectoriel E comme cadre ambiant de l'hyperplan.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.7
      La caractérisation en dimension finie décrit l'hyperplan par une équation linéaire sur les coordonnées dans une base fixée.

### [107] Théorème : Caractérisation géométrique des hyperplans  _( theorem )_
- [ ] **Définition : Hyperplan**  · conf 0.98
      L'enonce caracterise les hyperplans, donc la definition d'hyperplan est indispensable pour comprendre l'objet etudie.
- [ ] **Définition : Sous-espaces vectoriels supplémentaires**  [<-espaces_vectoriels]  · conf 0.95
      L'assertion (ii) parle de H 'supplementaire d'une droite', notion qui exige la definition de sous-espaces supplementaires.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.9
      L'enonce utilise la dimension finie n et la dimension n-1, ainsi que la notion de droite (dimension 1).

### [110] Théorème : Comparaison des équations d'un hyperplan  _( theorem )_
- [ ] **Définition : Hyperplan**  · conf 0.98
      L'énoncé porte sur un hyperplan H de E, notion qui doit être définie au préalable.
- [ ] **Définition : Application linéaire**  · conf 0.8
      Une forme linéaire est une application linéaire à valeurs dans K, dont la définition est nécessaire pour comprendre l'énoncé.
- [ ] **Définition : Espace vectoriel**  [<-espaces_vectoriels]  · conf 0.75
      L'énoncé se place dans un K-espace vectoriel E, structure de base mobilisée.

### [111] Théorème : Intersections d'hyperplans  _( theorem )_
- [ ] **Définition : Hyperplan**  · conf 0.99
      L'énoncé porte entièrement sur des intersections d'hyperplans, notion qui doit être définie au préalable.
- [ ] **Définition : Sous-espace vectoriel**  [<-espaces_vectoriels]  · conf 0.95
      L'énoncé affirme que l'intersection est un sous-espace vectoriel et parle de sous-espaces vectoriels de E.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.93
      L'hypothèse suppose E de dimension finie n, notion indispensable pour comprendre l'énoncé.

### [113] Théorème : Dimension d'une intersection d'hyperplans  _( theorem )_
- [ ] **Définition-théorème : Dual d'un espace vectoriel**  · conf 0.95
      L'énoncé fait des phi_i des éléments du dual E* (formes linéaires), notion sans laquelle l'énoncé n'a pas de sens.
- [ ] **Définition : Application linéaire de rang fini, rang**  · conf 0.9
      Le terme rg(phi_1,...,phi_p) est le rang de la famille de formes linéaires, mobilisé directement dans la formule.
- [ ] **Définition / Théorème : Dimension**  [<-espaces_vectoriels]  · conf 0.9
      La dimension dim(...) et l'entier n sont au cœur de l'égalité énoncée.
- [ ] **Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau**  · conf 0.85
      Les Ker phi_i (noyaux des formes linéaires) figurent explicitement dans l'énoncé.

### [114] Théorème : Rudiments de dualité  _( theorem )_
- [ ] **Définition-théorème : Dual d'un espace vectoriel**  · conf 0.98
      L'énoncé manipule le dual E* = L(E,K) et en forme le bidual E**, donc la notion de dual est indispensable.
- [ ] **Définition : Isomorphisme, espaces vectoriels isomorphes**  · conf 0.95
      Le point (i) affirme que x ↦ ev_x est un isomorphisme de E sur E**, notion centrale de l'énoncé.
- [ ] **Définition : Base et coordonnées**  [<-espaces_vectoriels]  · conf 0.92
      Le point (ii) parle de bases F de E* et B de E, donc la notion de base est mobilisée directement.
- [ ] **Définition : Espace vectoriel de dimension finie**  [<-espaces_vectoriels]  · conf 0.9
      L'énoncé suppose explicitement E de dimension finie, hypothèse sans laquelle le théorème n'a pas de sens.

---
## Arêtes RÉFUTÉES par le vérificateur (à vérifier : le filtre est-il trop strict ?)

### Définition : Application linéaire
- [ ] ~~Définition : Combinaisons linéaires d'un nombre fini de vecteurs~~  — L'énoncé n'utilise qu'une combinaison de DEUX vecteurs (lambda x + mu y), directement lisible à partir des opérations + et · de l'espace vectoriel. La notion formalisée de combinaison linéaire FINIE de n vecteurs (somme de 1 à n) n'apparaît pas dans l'énoncé ; c'est un vocabulaire voisin/co-utilisé, pas un prérequis logique pour comprendre l'énoncé. Réfutée.

### Propriété : Critère simplifié de linéarité
- [ ] ~~Propriété : Image du vecteur nul~~  — f(0_E)=0_F n'est utilise que comme etape interne de la PREUVE, pas pour comprendre l'ENONCE du critere. De plus image_zero est une consequence aval de la linearite, donc co-usee/downstream, non un prerequis amont.

### Définition-théorème : Application linéaire canoniquement associée à une matrice
- [ ] ~~Définition : Espace vectoriel~~  — C mentionne K^p et K^n, mais ce sont des espaces de coordonnées concrets ; comprendre l'énoncé ne requiert pas de dérouler les axiomes abstraits d'espace vectoriel. Cette structure est le substrat de la définition d'application linéaire (P1), donc la dépendance est médiée par P1, pas un prérequis amont direct de l'énoncé de C.

### Définition-théorème : Formes coordonnées relativement à une base
- [ ] ~~Définition : Espace vectoriel~~  — Le K-espace vectoriel E est le cadre ambiant, mais l'enonce de C ne mobilise pas la definition axiomatique de l'EV (groupe commutatif + loi externe). Cette notion est deja entierement encapsulee en amont par 'base et coordonnees', qui presuppose l'EV. Prerequis trop fondamental/indirect : voisin de cadre, pas prerequis logique direct de l'enonce de C. Refute.
- [ ] ~~Définition : Combinaisons linéaires d'un nombre fini de vecteurs~~  — Ce prereq definit la combinaison lineaire FINIE (x_1,...,x_n), or l'enonce de C utilise une somme sur un ensemble d'indices I quelconque (famille presque nulle), pas une somme finie indexee. La notion de combinaison lineaire necessaire est deja portee par la definition de base/coordonnees. Lien co-utilise, pas prerequis amont strict de l'enonce. Refute.

### Théorème : Traduction de l'inversibilité en termes d'application linéaire canoniquement associée
- [ ] ~~Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme~~  — Ce theoreme (reciproque/composition d'isomorphismes) sert dans la PREUVE de l'egalite finale mais n'est pas requis pour comprendre l'ENONCE; il est co-utilise, pas un prerequis logique amont.

### Théorème : Algèbre $\mathcal{L}(E)$
- [ ] ~~Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme~~  — Ce théorème (g∘f linéaire, réciproque d'isomorphisme) est un résultat amont qui justifie pourquoi L(E) est stable par composition, mais l'ÉNONCÉ de C n'a pas besoin de ce théorème pour être compris : il suffit de connaître la composition d'applications. C'est un prérequis de la PREUVE, pas de la compréhension de l'énoncé. Réfutable.

### Définition : Endomorphisme nilpotent
- [ ] ~~Théorème : Algèbre $\mathcal{L}(E)$~~  — Pour comprendre l'énoncé il suffit que f^p soit une composée itérée et 0_{L(E)} l'application nulle; le théorème complet de structure d'algèbre (GL(E), inversibles, non-commutativité) est un contexte aval co-utilisé, pas un prérequis logique amont de l'énoncé.
- [ ] ~~Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme~~  — L'énoncé n'a besoin que de l'opération de composition pour donner sens à f^p; ce théorème (clôture de g∘f entre E,F,G, isomorphismes, relation d'équivalence) a un contenu plus large non requis pour comprendre la nilpotence. Relié, non indéniablement nécessaire.

### Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau
- [ ] ~~Théorème : Ensemble des solutions d'un système linéaire homogène~~  — P porte sur le cas matriciel AX=0 (A ∈ M_{m,p}). C mentionne l'équation générale f(x)=0_F, pas le système matriciel de P. P est un résultat frère/aval (instance matricielle), pas un prérequis logique amont pour comprendre l'énoncé de C.

### Définition-théorème : Noyau d'une matrice
- [ ] ~~Théorème : Ensemble des solutions d'un système linéaire homogène~~  — L'identification de Ker A a l'ensemble des solutions de AX=0 est presentee dans C comme une consequence/caracterisation pratique, pas comme support de la definition (qui repose sur l'application canonique). P est co-mentionne/voisin, non un prerequis logique amont pour comprendre l'enonce. Refutee.

### Définition : Application linéaire de rang fini, rang
- [ ] ~~Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau~~  — Ce théorème porte sur l'image RÉCIPROQUE f^{-1}(B) et le noyau Ker f, pas sur l'image directe Im f. L'énoncé de C utilise Im f (image directe), notion absente de ce théorème. Aucun lien logique amont : confusion entre image et image réciproque.
- [ ] ~~Définition : Rang d'une famille finie de vecteurs~~  — Le rang de la famille n'apparaît que dans la remarque finale (rg(f) = rg(f(B))), comme rapprochement/conséquence, non comme support de la définition principale de rg(f) = dim Im f. C'est une notion co-utilisée et reliée, pas un prérequis amont de l'énoncé du rang d'une application linéaire.

### Théorème : Forme géométrique du théorème du rang
- [ ] ~~Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau~~  — L'énoncé ne mobilise Ker f que comme un sous-ensemble admettant un supplémentaire ; le contenu propre de ce théorème (Ker est un s.e.v., injectivité ⟺ Ker={0}) n'est pas requis pour LIRE l'énoncé de C. Lien amont de contenu, pas prérequis logique de l'énoncé.

### Définition : Rang d'une matrice
- [ ] ~~Théorème : Traduction de l'inversibilité en termes d'application linéaire canoniquement associée~~  — Le point (ii) de C énonce 'A inversible ssi rg(A)=n' de façon autonome, en termes de rang déjà défini. Le théorème caractérisant l'inversibilité via l'automorphisme est un résultat parallèle/co-utilisé (utile en preuve), non nécessaire pour comprendre l'ÉNONCÉ de C. Réfutée.

### Théorème : Rang d'une composée
- [ ] ~~Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme~~  — L'enonce mentionne les composees f∘φ et ψ∘f, mais comprendre l'enonce ne requiert que la notion de composition de fonctions, pas le THEOREME affirmant que la composee de deux applications lineaires est lineaire ni la stabilite de l'isomorphisme. C'est un resultat co-utilise/amont pour la preuve, pas necessaire a la comprehension de l'enonce.

### Théorème : Les opérations élémentaires préservent le rang
- [ ] ~~Théorème : Rang d'une famille de vecteurs, rang d'une matrice associée~~  — L'énoncé de C ne parle que du rang d'une matrice, pleinement compris via la seule définition du rang matriciel. Le lien rg(X)=rg(Mat_B(X)) est une technique de preuve/notion co-utilisée, pas requise pour comprendre l'énoncé. Voisin, non prérequis amont.

### Définition-théorème : Matrices extraites
- [ ] ~~Définition : Matrice d'une famille finie de vecteurs dans une base finie~~  — Ce P definit la matrice d'une famille de vecteurs dans une base (Mat_B(X)), construction specifique non utilisee par C. C ne requiert que la notion generique de matrice A dans M_{n,p}(K) et l'extraction de lignes/colonnes, sans aucun vecteur ni base. Concept voisin/co-utilise, pas un prerequis logique amont de l'enonce.

### Théorème : Deux petits résultats bien utiles
- [ ] ~~Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme~~  — L'enonce utilise seulement l'operation de composition g o f comme notation. Le theoreme (la composee est lineaire, transfert d'isomorphismes) n'est pas requis pour comprendre l'enonce (i). Co-utilise mais pas prerequis amont de l'enonce.

### Théorème : Noyaux itérés, images itérées et décomposition de Fitting
- [ ] ~~Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme~~  — Les itérées f^k reposent sur la composition d'un endomorphisme avec lui-même (g∘f), notion déjà couverte par la définition d'application linéaire et la composition usuelle d'applications. Ce théorème porte sur la stabilité de la composition d'isomorphismes/applications linéaires distincts, ce qui n'est pas requis pour comprendre l'énoncé de Fitting : co-utilisé au plus, pas prérequis amont indéniable.

### Définition : Projecteur et symétrie
- [ ] ~~Définition : Application linéaire~~  — L'enonce ne parle que d'« applications de E dans E », sans aucune mention de linearite ni de combinaisons lineaires. Projecteur et symetrie sont definis comme de simples applications via la decomposition x=f+g; leur linearite est une propriete ulterieure, pas un prerequis pour comprendre l'enonce. Voisin co-utilise dans le chapitre, pas prerequis logique amont.

### Théorème : Propriétés des projecteurs et des symétries
- [ ] ~~Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau~~  — C n'utilise que la NOTATION Ker (ensemble {x | f(x)=0}), notion définitionnelle. Le CONTENU de ce théorème (l'image réciproque/noyau est un sev, injectivité ssi noyau trivial) n'est nullement requis pour comprendre l'ÉNONCÉ de C, qui se contente de nommer ces noyaux comme des ensembles. Résultat co-utilisé/voisin, pas prérequis logique amont.

### Théorème : Caractérisation algébrique des projecteurs
- [ ] ~~Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau~~  — L'énoncé utilise Ker p mais la simple notation/définition Ker p = {x | p(x)=0} suffit ; ce théorème (image réciproque d'un sev est un sev, critère d'injectivité) n'est pas requis pour comprendre l'énoncé. Au mieux la définition du noyau, pas ce théorème entier. Réfutée.
- [ ] ~~Théorème : Image d'un sous-espace vectoriel par une application linéaire~~  — L'énoncé fait intervenir Im p mais seule la notation/définition de l'image suffit à le comprendre ; le théorème (image d'un sev est un sev, critère de surjectivité) n'est pas nécessaire pour saisir l'énoncé. Voisin/co-utilisé, pas prérequis amont indispensable. Réfutée.

### Théorème : Caractérisation algébrique des symétries
- [ ] ~~Définition : Espace vectoriel~~  — Le K-espace vectoriel E n'est que le cadre ambiant. La definition axiomatique complete (groupe commutatif, axiomes de la loi externe) n'est pas un prerequis logique amont indeniable pour saisir le SENS de l'enonce de caracterisation; c'est une structure de fond co-presente partout. Refute par defaut sceptique.

### Théorème : Lien projecteur/symétrie
- [ ] ~~Théorème : Algèbre $\mathcal{L}(E)$~~  — L'énoncé utilise la notation 0_{L(E)} et la composition ∘, mais la simple notation de l'endomorphisme nul et de la composée ne nécessite pas le théorème de structure d'algèbre de L(E) (algèbre, GL(E), inversibles). Comprendre l'ÉNONCÉ de C ne demande que de savoir composer des endomorphismes et l'existence de l'application nulle, pas la structure d'algèbre. Concept co-utilisé/voisin, pas prérequis logique amont de l'énoncé.
- [ ] ~~Définition : Espace vectoriel~~  — E est un K-espace vectoriel, cadre de fond très général. La définition axiomatique de l'espace vectoriel n'est pas un prérequis spécifique à l'énoncé de C : elle est présupposée partout et n'éclaire en rien le contenu propre de C (lien projecteur/symétrie). Trop amont/transverse pour être un prérequis indéniable de cet énoncé précis.

### Définition-théorème : Polynômes annulateurs d'un endomorphisme
- [ ] ~~Définition : Projecteur et symétrie~~  — Projecteurs et symétries n'apparaissent que comme exemples illustratifs dans le 2e paragraphe. La DÉFINITION elle-même (P(f)=0_{L(E)}) se comprend sans eux. Illustration co-utilisée, pas prérequis logique amont de l'énoncé.
- [ ] ~~Définition : Espace vectoriel~~  — E est mentionné comme K-espace vectoriel mais sert seulement de cadre ambiant. La notion centrale est l'endomorphisme f et P(f) ; la définition d'espace vectoriel est déjà absorbée en amont par la définition d'application linéaire (qui la suppose), donc arête redondante/non indispensable à l'énoncé propre de C.

### Définition : Hyperplan
- [ ] ~~Définition-théorème : Dual d'un espace vectoriel~~  — C mentionne « forme linéaire » mais ne suppose PAS la notion de dual E* ni de base duale pour énoncer la définition d'hyperplan. Le théorème du dual est un objet voisin/co-utilisé, pas un prérequis logique amont de l'énoncé. La notion fondatrice (forme linéaire = application linéaire vers K) vient d'ailleurs.

### Théorème : Caractérisation géométrique des hyperplans
- [ ] ~~Théorème : Dimension d'un sous-espace vectoriel~~  — Le theoreme dim F <= dim E (egalite ssi F=E) est un outil de la PREUVE, non un element requis pour comprendre l'ENONCE de la caracterisation. Reduction des prerequis: arete eliminee.
- [ ] ~~Définition : Espace vectoriel~~  — Cadre ambiant trop fondamental, co-utilise par tout le chapitre sans etre un prerequis amont specifique de CET enonce. Les notions porteuses (hyperplan, supplementaire, dimension) le presupposent deja. Arete refutee.

### Théorème : Comparaison des équations d'un hyperplan
- [ ] ~~Définition-théorème : Dual d'un espace vectoriel~~  — C parle de 'formes lineaires', pas du dual E* ni de la base duale. La notion de forme lineaire se comprend via l'application lineaire a valeurs dans K, sans la construction du dual. Concept co-utilise, non prerequis logique amont.
- [ ] ~~Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau~~  — C utilise la notion de 'noyau', mais ce P est le THEOREME affirmant que l'image reciproque/le noyau est un sous-espace, pas la definition du noyau. Ce resultat n'est pas necessaire pour comprendre l'enonce de C.

### Théorème : Intersections d'hyperplans
- [ ] ~~Théorème : Dimension d'un sous-espace vectoriel~~  — Ce theoreme (dim F <= dim E avec egalite ssi F=E) n'apparait pas dans la formulation de C. L'enonce de C utilise la notion de 'dimension d'un sev' mais pas ce theoreme particulier; il s'agit d'un resultat connexe utile pour la preuve, non d'un prerequis pour comprendre l'enonce. Refutable.
- [ ] ~~Théorème : Intersection de sous-espaces vectoriels~~  — Que 'toute intersection de sev est un sev' sert a JUSTIFIER (preuve) le (i) de C, mais l'enonce de C affirme deja directement que l'intersection est un sev sans presupposer ce theoreme general pour etre compris. Co-utilise/voisin pour la demonstration, pas prerequis amont pour l'enonce. Refutable.

### Théorème : Dimension d'une intersection d'hyperplans
- [ ] ~~Théorème : Intersection de sous-espaces vectoriels~~  — Ce théorème (toute intersection de sev est un sev) sert à justifier la bonne définition dans la preuve, pas à comprendre l'énoncé. Parser 'dim de l'intersection des noyaux' n'exige que la notion d'intersection et le fait que chaque Ker est un sev (déjà couvert) — fait amont co-utilisé, non prérequis indéniable de l'énoncé.

### Théorème : Rudiments de dualité
- [ ] ~~Définition-théorème : Formes coordonnées relativement à une base~~  — L'énoncé de C n'invoque pas les formes coordonnées : il parle de base duale/antéduale, notions encapsulées par definition_theoreme_dual. Les formes coordonnées sont en amont du *dual*, pas un prérequis direct de l'énoncé de C. Dépendance médiée, donc co-utilisé plutôt que requis.
