# Validation des prérequis — espaces_vectoriels

**109 arêtes retenues** (proposées 130, réfutées 21). `[<-chapitre]` = prérequis amont d'un autre chapitre.

## Arêtes RETENUES (vérifier la précision)

### Définition : Espace vectoriel
- **Définition : Groupe**  [<-groupes_et_anneaux] · conf 0.95
      Vector space definition explicitly requires (E,+) to be a commutative group; this is the foundational algebraic structure for the vector space.

### Théorème : Règles de calcul dans un espace vectoriel
- **Définition : Espace vectoriel** · conf 0.99
      Theorem about calculation rules in vector spaces presupposes understanding the definition of vector space and its axioms.

### Théorème : Espace vectoriel produit
- **Définition : Espace vectoriel** · conf 0.99
      Product theorem must first establish what a vector space is in order to prove the product structure is a vector space.

### Théorème : Espaces vectoriels d'applications
- **Définition : Espace vectoriel** · conf 0.99
      Theorem requires understanding vector space definition to prove the function space E^X with pointwise operations is a vector space.

### Définition : Algèbre
- **Définition : Espace vectoriel** · conf 0.99
      Algebra definition explicitly requires (A,+,·) to be a K-vector space as part of its structure.
- **Définition : Anneau**  [<-groupes_et_anneaux] · conf 0.99
      Algebra definition explicitly requires (A,+,×) to be a ring; understanding ring structure is essential to the definition.

### Définition : Combinaisons linéaires d'un nombre fini de vecteurs
- **Définition : Espace vectoriel** · conf 0.99
      Finite linear combination requires vector space context: understanding how scalar multiplication and addition work in E.

### Définition : Combinaisons linéaires d'un nombre quelconque de vecteurs
- **Définition : Famille presque nulle de scalaires** · conf 0.99
      Definition of infinite linear combination explicitly uses 'almost null family' to define well-formed infinite sums.

### Définition : Sous-espace vectoriel
- **Définition : Espace vectoriel** · conf 0.99
      Subspace definition requires understanding vector space structure; F must inherit the vector space axioms from E.

### Théorème : Caractérisation des sous-espaces vectoriels
- **Définition : Sous-espace vectoriel** · conf 0.99
      Characterization theorem directly characterizes what it means to be a subspace; requires the definition.

### Théorème : Ensemble des solutions d'un système linéaire homogène
- **Définition : Sous-espace vectoriel** · conf 0.99
      Theorem proves solution set is a subspace; requires understanding what subspace definition means.

### Théorème : Intersection de sous-espaces vectoriels
- **Définition : Sous-espace vectoriel** · conf 0.99
      Intersection theorem requires definition of subspace; proves intersection of subspaces is closed.

### Définition / Théorème : Sous-algèbre
- **Définition : Algèbre** · conf 0.95
      Defines what an algebra is; a subalgebra is a subset that is itself an algebra

### Définition : Sous-espace affine et direction
- **Définition : Espace vectoriel** · conf 0.98
      Affine subspace is defined as a special form within a vector space
- **Définition : Sous-espace vectoriel** · conf 0.95
      Affine subspace direction F must be a vector subspace of E

### Théorème : Ensemble des solutions d'un système linéaire
- **Définition : Sous-espace affine et direction** · conf 0.96
      Theorem states solution set is an affine subspace
- **Théorème : Ensemble des solutions d'un système linéaire homogène** · conf 0.93
      Direction of solution affine subspace is the homogeneous system solution set

### Théorème : Caractérisation des sous-espaces affines
- **Définition : Sous-espace affine et direction** · conf 0.97
      Characterizes affine subspaces; needs to understand what they are first

### Théorème : Intersection de sous-espaces affines
- **Définition : Sous-espace affine et direction** · conf 0.98
      Theorem is about intersection of affine subspaces

### Définition : Sous-espace vectoriel engendré par une partie
- **Définition : Sous-espace vectoriel** · conf 0.96
      Vect(X) is defined as the smallest subspace containing X
- **Définition : Combinaisons linéaires d'un nombre quelconque de vecteurs** · conf 0.92
      Vect(X) is the set of all linear combinations of elements of X

### Théorème : Propriétés des Vect
- **Définition : Sous-espace vectoriel engendré par une partie** · conf 0.97
      Theorem lists properties of Vect operator
- **Définition : Combinaisons linéaires d'un nombre fini de vecteurs** · conf 0.85
      Definitions of being a linear combination are used throughout

### Définition : Partie/famille génératrice
- **Définition : Sous-espace vectoriel engendré par une partie** · conf 0.98
      Generating set X means E = Vect(X)
- **Définition : Combinaisons linéaires d'un nombre quelconque de vecteurs** · conf 0.9
      Need to understand what it means for every element to be a linear combination

### Théorème : Propriétés des parties génératrices
- **Définition : Partie/famille génératrice** · conf 0.98
      Theorem states properties of generating sets

### Méthode : Trouver une partie génératrice
- **Définition : Partie/famille génératrice** · conf 0.97
      Method is about finding generating sets; must know what they are first
- **Définition : Sous-espace vectoriel engendré par une partie** · conf 0.92
      Finding a generating set means writing space as Vect(X)

### Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs
- **Définition : Combinaisons linéaires d'un nombre fini de vecteurs** · conf 0.96
      Free families use finite linear combinations in their definition

### Définition : Partie/famille liée d'un nombre fini de vecteurs
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.98
      Linked family is exactly the negation of a free family
- **Définition : Combinaisons linéaires d'un nombre fini de vecteurs** · conf 0.88
      Linked if one vector is a linear combination of others

### Théorème : Liberté des familles de polynômes échelonnées en degré
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.95
      notion de liberté testée par le théorème

### Définition : Partie/famille libre/liée d'un nombre quelconque de vecteurs
- **Définition : Famille presque nulle de scalaires** · conf 0.98
      condition essentielle 'presque nulle' dans la définition
- **Définition : Espace vectoriel** · conf 0.95
      fondement pour les familles de vecteurs

### Théorème : Propriétés des parties libres/liées
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.98
      la propriété porte sur les familles libres
- **Définition : Partie/famille liée d'un nombre fini de vecteurs** · conf 0.95
      équivalence libre <==> non liée
- **Définition : Combinaisons linéaires d'un nombre fini de vecteurs** · conf 0.85
      comprendre 'y n'est pas combinaison linéaire'

### Définition : Base et coordonnées
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.98
      une base doit être libre
- **Définition : Partie/famille génératrice** · conf 0.98
      une base doit être génératrice
- **Définition : Espace vectoriel** · conf 0.9
      contexte: E est un K-ev

### Définition / Théorème : Bases canoniques
- **Définition : Base et coordonnées** · conf 0.98
      montre des exemples concrets de bases

### Méthode : Trouver une base
- **Définition : Base et coordonnées** · conf 0.98
      définition de ce qu'on cherche
- **Définition : Partie/famille génératrice** · conf 0.95
      trouver une génératrice d'abord
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.95
      vérifier que c'est libre

### Théorème : Caractérisation des matrices inversibles (lignes/colonnes)
- **Définition : Base et coordonnées** · conf 0.98
      les colonnes/lignes forment une base

### Définition : Espace vectoriel de dimension finie
- **Définition : Partie/famille génératrice** · conf 0.98
      notion de génératrice
- **Définition : Espace vectoriel** · conf 0.95
      contexte EV

### Théorème : Nombre maximal de vecteurs linéairement indépendants
- **Définition : Espace vectoriel de dimension finie** · conf 0.98
      précondition: dim finie
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.95
      compter les vecteurs libres
- **Définition : Partie/famille génératrice** · conf 0.9
      comparaison avec génératrice

### Théorème : Algorithme de la base incomplète
- **Définition : Espace vectoriel de dimension finie** · conf 0.98
      contexte: dim finie requise
- **Définition : Base et coordonnées** · conf 0.95
      but: obtenir une base
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.95
      partir d'une partie libre
- **Définition : Partie/famille génératrice** · conf 0.85
      à partir d'une génératrice

### Théorème : Théorèmes de la base incomplète/extraite et existence de bases finies
- **Définition : Base et coordonnées** · conf 0.98
      notion de base
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.95
      compléter une partie libre
- **Définition : Partie/famille génératrice** · conf 0.95
      extraire d'une génératrice
- **Définition : Espace vectoriel de dimension finie** · conf 0.9
      contexte: dim finie

### Définition / Théorème : Dimension
- **Définition : Espace vectoriel de dimension finie** · conf 0.98
      précondition: dim finie
- **Définition : Base et coordonnées** · conf 0.98
      cardinal de base

### Théorème : Quelques dimensions usuelles
- **Définition / Théorème : Dimension** · conf 0.95
      Must know what dimension means
- **Définition : Espace vectoriel** · conf 0.8
      K^n and K_n[X] are vector spaces

### Théorème : Dimension et cardinal d'une partie libre/génératrice
- **Définition : Espace vectoriel de dimension finie** · conf 0.95
      References 'dimension finie' explicitly
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.95
      Free/independent family is the main subject
- **Définition : Partie/famille génératrice** · conf 0.95
      Generating family is the main subject
- **Définition / Théorème : Dimension** · conf 0.9
      Dimension concept is fundamental

### Théorème : Caractérisation des bases en dimension finie
- **Définition : Espace vectoriel de dimension finie** · conf 0.95
      Requires finite dimension hypothesis
- **Définition : Base et coordonnées** · conf 0.95
      Basis is main topic
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.9
      Characterization uses linearly independent
- **Définition : Partie/famille génératrice** · conf 0.9
      Characterization uses generating family

### Théorème : Caractérisations diverses de l'inversibilité
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire**  [<-matrices_et_systemes_lineaires] · conf 0.95
      Invertibility of matrices is the topic

### Définition : Rang d'une famille finie de vecteurs
- **Définition / Théorème : Dimension** · conf 0.95
      Rank IS a dimension of a subspace
- **Définition : Sous-espace vectoriel engendré par une partie** · conf 0.95
      Vect(x1,...,xn) is the span of vectors

### Théorème : Dimension d'un sous-espace vectoriel
- **Définition : Espace vectoriel de dimension finie** · conf 0.95
      Hypothesis: E finite-dimensional
- **Définition : Sous-espace vectoriel** · conf 0.95
      F is a subspace of E
- **Définition / Théorème : Dimension** · conf 0.9
      Conclusion is about dimensions

### Définition : Dimension d'un sous-espace affine
- **Définition : Sous-espace affine et direction** · conf 0.95
      F is an affine subspace (has direction)
- **Définition / Théorème : Dimension** · conf 0.9
      Dimension of direction is dimension of F
- **Définition : Espace vectoriel de dimension finie** · conf 0.8
      Finiteness condition

### Théorème : Dimension d'un espace vectoriel produit
- **Théorème : Espace vectoriel produit** · conf 0.95
      E×F is a vector space (product space)
- **Définition : Espace vectoriel de dimension finie** · conf 0.9
      Assumes finite dimensions
- **Définition / Théorème : Dimension** · conf 0.9
      Conclusion about dimensions

### Définition : Matrice d'une famille finie de vecteurs dans une base finie
- **Définition : Base et coordonnées** · conf 0.95
      Coordinates in a basis B
- **Définition : Matrice, coefficients, lignes, colonnes**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Matrix definition and notation

### Théorème : Matrice des colonnes dans la base canonique
- **Définition : Matrice d'une famille finie de vecteurs dans une base finie** · conf 0.95
      Uses Mat_B notation
- **Définition / Théorème : Bases canoniques** · conf 0.9
      B_n is canonical basis of K^n

### Théorème : Interprétation vectorielle de l'inversibilité
- **Définition : Matrice d'une famille finie de vecteurs dans une base finie** · conf 0.95
      Uses Mat_B(F) notation
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Invertibility of matrices
- **Définition : Base et coordonnées** · conf 0.85
      F is a basis of E

### Définition : Somme de sous-espaces vectoriels
- **Définition : Sous-espace vectoriel** · conf 0.95
      F_1,...,F_p are subspaces

### Théorème : Parties génératrices d'une somme
- **Définition : Somme de sous-espaces vectoriels** · conf 0.95
      Définit la somme de sous-espaces vectoriels nécessaire pour comprendre l'énoncé
- **Définition : Partie/famille génératrice** · conf 0.95
      Définit les parties génératrices mentionnées dans l'énoncé
- **Définition : Sous-espace vectoriel engendré par une partie** · conf 0.95
      Définit Vect(X) utilisé dans la formule principale

### Définition : Sous-espaces vectoriels en somme directe
- **Définition : Somme de sous-espaces vectoriels** · conf 0.95
      Définit la somme de sous-espaces dont la somme directe est un cas particulier
- **Définition : Sous-espace vectoriel** · conf 0.9
      Concept fondamental de sous-espace utilisé dans la définition

### Théorème : Caractérisation de la somme directe pour deux sous-espaces vectoriels
- **Définition : Sous-espaces vectoriels en somme directe** · conf 0.95
      Énonce la définition dont ce théorème donne la caractérisation

### Théorème : Somme directe et liberté
- **Définition : Sous-espaces vectoriels en somme directe** · conf 0.95
      Énoncé qui établit le lien avec la liberté des familles
- **Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs** · conf 0.95
      Concept de liberté utilisé dans la caractérisation

### Théorème : Base adaptée et dimension d'une somme
- **Définition : Base et coordonnées** · conf 0.95
      Concept de base utilisé dans la notion de base adaptée
- **Définition : Sous-espaces vectoriels en somme directe** · conf 0.9
      Somme directe pour laquelle on construit la base adaptée
- **Définition / Théorème : Dimension** · conf 0.9
      Notion de dimension utilisée dans la formule

### Définition : Sous-espaces vectoriels supplémentaires
- **Définition : Sous-espaces vectoriels en somme directe** · conf 0.95
      Les supplémentaires sont caractérisés par la somme directe
- **Définition : Somme de sous-espaces vectoriels** · conf 0.9
      Notion de somme E = F + G dans la définition

### Théorème : Existence de supplémentaires en dimension finie
- **Définition : Sous-espaces vectoriels supplémentaires** · conf 0.95
      Énonce l'existence de supplémentaires dont ce théorème affirme l'existence
- **Définition : Espace vectoriel de dimension finie** · conf 0.9
      Hypothèse essentielle du théorème

### Théorème : Formule de Grassmann
- **Définition / Théorème : Dimension** · conf 0.95
      Concept de dimension utilisé dans la formule
- **Définition : Somme de sous-espaces vectoriels** · conf 0.9
      Somme F + G dont on calcule la dimension

### Théorème : Caractérisation de la supplémentarité en dimension finie
- **Définition : Sous-espaces vectoriels supplémentaires** · conf 0.95
      Énoncé qu'on caractérise dans l'assertion (ii)
- **Définition / Théorème : Dimension** · conf 0.95
      Relation dim F + dim G = dim E dans l'énoncé

## Arêtes RÉFUTÉES (vérifier si le filtre est trop strict)

### Définition : Combinaisons linéaires d'un nombre quelconque de vecteurs
- ~~Définition : Combinaisons linéaires d'un nombre fini de vecteurs~~ — L'énoncé ne fait aucune référence à la combinaison linéaire finie ; il se définit directement via une famille presque nulle de scalaires. Le cas fini est intuitivement antérieur mais n'apparaît pas dans l'énoncé.

### Définition / Théorème : Sous-algèbre
- ~~Définition : Sous-espace vectoriel~~ — L'énoncé ne mentionne pas explicitement 'sous-espace vectoriel'. La stabilité par combinaison linéaire est citée directement dans la caractérisation sans référence au concept de SEV. Le prérequis est utile mais pas indispensable pour lire l'énoncé.

### Théorème : Intersection de sous-espaces affines
- ~~Théorème : Intersection de sous-espaces vectoriels~~ — L'énoncé dit que la direction de l'intersection est l'intersection des directions (qui sont des SEV), mais ne cite pas explicitement le théorème sur l'intersection des SEV. Ce théorème justifie que cette intersection est bien un SEV, mais sa connaissance n'est pas requise pour lire l'énoncé du théorème sur les sous-espaces affines.

### Théorème : Propriétés des parties génératrices
- ~~Théorème : Propriétés des Vect~~ — L'énoncé du théorème ne fait aucune référence au théorème sur les propriétés de Vect. Les propriétés sont énoncées directement en termes de 'engendre' sans citer l'opérateur Vect ni ce théorème. Ce lien est justificatif (preuve), pas nécessaire pour comprendre l'énoncé.

### Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs
- ~~Définition : Espace vectoriel~~ — L'énoncé commence par 'Soient E un K-espace vectoriel', mais ce prérequis est commun à toutes les définitions de ce chapitre. La compréhension de l'énoncé de famille libre ne requiert pas de connaître les axiomes détaillés d'un espace vectoriel, seulement le cadre formel. Ce lien est trop générique.

### Théorème : Liberté des familles de polynômes échelonnées en degré
- ~~Définition : Combinaisons linéaires d'un nombre fini de vecteurs~~ — L'énoncé dit 'une telle famille est toujours libre' — il utilise le mot 'libre' mais pas explicitement 'combinaison linéaire'. La preuve en use, mais l'énoncé seul ne convoque pas la définition de CL.

### Définition : Partie/famille libre/liée d'un nombre quelconque de vecteurs
- ~~Définition : Combinaisons linéaires d'un nombre quelconque de vecteurs~~ — L'énoncé utilise la notation Σ_{i∈I} λ_i x_i mais ne fait pas référence au terme 'combinaison linéaire infinie' explicitement. La somme est directement posée dans l'énoncé sans renvoyer à cette définition nommée.
- ~~Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs~~ — Cette définition généralise la version finie, mais l'énoncé est auto-suffisant — il redéfinit entièrement le concept sans référer à la version finie. La version finie n'est pas nécessaire pour comprendre l'énoncé.

### Définition / Théorème : Bases canoniques
- ~~Théorème : Espace vectoriel produit~~ — L'énoncé mentionne K^n et K_n[X] comme espaces, mais ne fait pas référence au théorème 'EV produit' — K^n est compris directement comme espace de n-uplets sans invoquer ce théorème dans l'énoncé.
- ~~Définition : Algèbre~~ — L'énoncé mentionne K[X] mais ne le qualifie pas d'algèbre — l'énoncé traite K[X] comme EV directement, sans que la définition d'algèbre soit nécessaire à sa compréhension.

### Théorème : Caractérisation des matrices inversibles (lignes/colonnes)
- ~~Théorème : Espace vectoriel produit~~ — K^n est mentionné mais le théorème EV produit n'est pas nécessaire pour comprendre l'énoncé — K^n est un espace familier dont la structure n'a pas besoin d'être rappelée via ce théorème.

### Définition / Théorème : Dimension
- ~~Théorème : Théorèmes de la base incomplète/extraite et existence de bases finies~~ — Ce théorème justifie l'existence de bases, mais l'énoncé de la définition de dimension n'y fait pas référence explicitement — c'est un prérequis de la preuve du bien-fondé, pas de la lecture de l'énoncé.

### Théorème : Quelques dimensions usuelles
- ~~Définition : Base et coordonnées~~ — L'énoncé donne seulement des valeurs numériques de dimensions. La notion de base est utilisée dans la preuve (on exhibe une base), pas dans l'énoncé lui-même. Il suffit de connaître 'dim' (definition_dimension) pour lire l'énoncé.

### Théorème : Caractérisations diverses de l'inversibilité
- ~~Définition-théorème : Système de Cramer~~ — L'énoncé parle d'un 'système linéaire Y=AX' et de 'l'unique solution' — ces notions relèvent de la définition générale de système linéaire, pas spécifiquement du système de Cramer. La définition de système de Cramer n'est pas nécessaire pour comprendre l'énoncé des équivalences (iv) et (v) ; ce sont des assertions sur des systèmes linéaires quelconques avec A donnée.

### Définition : Rang d'une famille finie de vecteurs
- ~~Définition / Théorème : Partie/famille libre d'un nombre fini de vecteurs~~ — La propriété 'rg = n ssi la famille est libre' est une remarque/conséquence annexée à la définition, mais elle n'est pas nécessaire pour comprendre ce qu'est le rang. Le rang est défini indépendamment par la dimension de Vect(x1,...,xn). La notion de famille libre n'est pas indispensable à la lecture de l'énoncé principal de la définition.

### Définition : Matrice d'une famille finie de vecteurs dans une base finie
- ~~Définition : Espace vectoriel de dimension finie~~ — L'énoncé dit 'E un K-espace vectoriel de dimension finie n ≥ 1' mais la notion de 'dimension finie' en tant que définition formelle n'est pas requise pour comprendre l'énoncé — il suffira de savoir que E a une base finie de cardinal n. C'est definition_base_coordonnees qui est réellement nécessaire. La notion 'dimension finie' n'apparaît que comme contexte, et n pourrait être introduit directement via la base.

### Définition : Somme de sous-espaces vectoriels
- ~~Définition : Espace vectoriel~~ — L'énoncé définit la somme de sous-espaces vectoriels. Il fait référence à E un espace vectoriel, mais la structure de l'espace vectoriel lui-même n'est pas ce dont on a besoin pour comprendre l'énoncé : c'est la notion de sous-espace vectoriel (definition_sous_espace_vectoriel) qui est indispensable. La définition d'espace vectoriel est un prérequis transitif de sous-espace vectoriel, pas direct de cet énoncé.

### Théorème : Caractérisation de la somme directe pour deux sous-espaces vectoriels
- ~~Théorème : Intersection de sous-espaces vectoriels~~ — L'énoncé mentionne F∩G = {0_E}, mais la notion d'intersection de SEV n'a pas besoin d'être un théorème pour comprendre l'énoncé — F∩G est une notation ensembliste évidente. theorem_intersection_sev affirme que cette intersection est un SEV, ce qui est utile pour la preuve mais pas pour comprendre l'énoncé.

### Théorème : Existence de supplémentaires en dimension finie
- ~~Théorème : Théorèmes de la base incomplète/extraite et existence de bases finies~~ — theorem_base_incomplete_extraite est utilisé dans la preuve de l'existence, mais n'apparaît pas dans l'énoncé. L'énoncé ne mentionne ni base, ni complément de base. C'est un outil de démonstration, pas un prérequis de compréhension de l'énoncé.

### Théorème : Formule de Grassmann
- ~~Théorème : Intersection de sous-espaces vectoriels~~ — F∩G apparaît dans la formule, mais comprendre l'énoncé ne requiert que de savoir ce qu'est l'intersection ensembliste de deux SEV (c'est un SEV, certes, mais ce fait n'est pas nécessaire pour lire la formule). theorem_intersection_sev est utile pour la preuve, pas pour comprendre l'énoncé.

### Théorème : Caractérisation de la supplémentarité en dimension finie
- ~~Théorème : Intersection de sous-espaces vectoriels~~ — L'assertion (ii) est F∩G = {0_E}, ce qui nécessite de savoir ce qu'est F∩G, mais pas que c'est un SEV (ce que theorem_intersection_sev affirme). La notation F∩G est ensembliste et compréhensible sans ce théorème.