# Validation des prérequis — determinants

**29 arêtes retenues** (proposées 45, réfutées 16). `[<-chapitre]` = prérequis amont d'un autre chapitre.

## Arêtes RETENUES (vérifier la précision)

### Définition : Forme multilinéaire alternée
- **Définition : Application multilinéaire** · conf 0.95
      Forme n-linéaire est un cas spécial d'application n-linéaire; la définition de forme alternée suppose déjà compris ce qu'est une application multilinéaire

### Théorème : Propriétés des formes multilinéaires alternées
- **Définition : Forme multilinéaire alternée** · conf 0.95
      Énonce les propriétés d'une forme qui doit déjà être alternée par définition

### Théorème : Engendrement par les transpositions
- **Définition-théorème : Permutation, groupe symétrique**  [<-groupes_et_anneaux] · conf 0.95
      Les transpositions sont les générateurs fondamentaux du groupe symétrique S_n

### Définition-théorème : Signature
- **Théorème : Engendrement par les transpositions** · conf 0.95
      La signature d'une permutation est définie via sa décomposition unique en transpositions

### Théorème : Signature d'un cycle
- **Définition-théorème : Signature** · conf 0.95
      Applique la définition générale de signature au cas particulier des cycles

### Théorème : Effet d'une permutation sur une forme multilinéaire alternée
- **Définition : Forme multilinéaire alternée** · conf 0.95
      Énonce comment une permutation agit sur une forme multilinéaire alternée
- **Définition-théorème : Signature** · conf 0.95
      L'effet est multiplié par la signature de la permutation; c'est le résultat central

### Théorème : Toute forme multilinéaire alternée est un multiple du déterminant dans une base donnée
- **Définition-théorème : Déterminant d'une famille de vecteurs dans une base** · conf 0.95
      Énonce que toute forme alternée est un multiple de cet déterminant-ci dans une base fixée

### Théorème : Déterminants en dimensions 2 et 3
- **Définition-théorème : Déterminant d'une famille de vecteurs dans une base** · conf 0.95
      Applique la définition générale du déterminant aux cas concrets dim 2 et 3

### Théorème : Propriétés du déterminant d'une famille de vecteurs dans une base
- **Définition-théorème : Déterminant d'une famille de vecteurs dans une base** · conf 0.95
      Énonce les propriétés du déterminant qui vient d'être défini

### Définition-théorème : Orientation d'un $\mathbb{R}$-espace vectoriel de dimension finie
- **Définition-théorème : Déterminant d'une famille de vecteurs dans une base** · conf 0.95
      L'orientation est basée sur le signe du déterminant d'une base

### Définition : Déterminant d'une matrice carrée
- **Définition-théorème : Déterminant d'une famille de vecteurs dans une base** · conf 0.95
      Determinant of matrices is defined as determinant of column family

### Théorème : Lien entre le déterminant d'une matrice carrée et celui d'une famille de vecteurs dans une base
- **Définition-théorème : Déterminant d'une famille de vecteurs dans une base** · conf 0.95
      Provides definition of determinant for family of vectors
- **Définition : Déterminant d'une matrice carrée** · conf 0.9
      States the link between matrix determinant and family determinant

### Théorème : Premières propriétés du déterminant d'une matrice carrée
- **Définition : Déterminant d'une matrice carrée** · conf 0.98
      Defines determinant of matrix needed for its properties

### Théorème : Déterminant d'une matrice triangulaire par blocs
- **Définition : Déterminant d'une matrice carrée** · conf 0.95
      Applies to square matrices and their determinants

### Théorème : Déterminant d'une matrice et opérations élémentaires
- **Définition : Déterminant d'une matrice carrée** · conf 0.95
      Describes behavior of determinant under operations

### Définition : Mineurs, cofacteurs, comatrice
- **Définition : Déterminant d'une matrice carrée** · conf 0.98
      Minors and cofactors are determinants of submatrices

### Théorème : Développement par rapport à une ligne ou une colonne
- **Définition : Déterminant d'une matrice carrée** · conf 0.98
      Provides formula for computing determinant via expansion
- **Définition : Mineurs, cofacteurs, comatrice** · conf 0.95
      Uses definition of minors and cofactors in expansion formula

### Théorème : Formule d'inversion
- **Définition : Déterminant d'une matrice carrée** · conf 0.98
      Describes inverse in terms of determinant and cofactors
- **Définition : Mineurs, cofacteurs, comatrice** · conf 0.95
      Uses cofactor matrix in inverse formula

### Théorème : Polynôme caractéristique d'une matrice carrée
- **Définition : Déterminant d'une matrice carrée** · conf 0.98
      Characteristic polynomial is defined as det(A - λI)

### Définition-théorème : Déterminant d'un endomorphisme
- **Définition : Déterminant d'une matrice carrée** · conf 0.95
      Determinant of endomorphism extends matrix determinant via matrix representation

### Théorème : Déterminant de l'endomorphisme canoniquement associé à une matrice carrée
- **Définition-théorème : Déterminant d'un endomorphisme** · conf 0.95
      Establishes that determinant of endomorphism is well-defined

### Théorème : Propriétés du déterminant d'un endomorphisme
- **Définition-théorème : Déterminant d'un endomorphisme** · conf 0.98
      Requires definition of determinant of endomorphisms

### Théorème : Polynôme caractéristique d'un endomorphisme
- **Théorème : Polynôme caractéristique d'une matrice carrée** · conf 0.95
      Le théorème pour matrices précède directement la définition pour endomorphismes; l'énoncé introduit le polynôme caractéristique de u en le définissant comme celui de sa matrice
- **Définition : Matrice d'une application linéaire dans des bases finies**  [<-representation_matricielle_applications_lineaires] · conf 0.92
      Notion préalable: tout endomorphisme est représenté par une matrice dans une base donnée, fondamental pour définir le polynôme caractéristique
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)**  [<-representation_matricielle_applications_lineaires] · conf 0.88
      L'énoncé affirme que les racines du polynôme caractéristique sont exactement les valeurs propres de u, preuve-clé du théorème

## Arêtes RÉFUTÉES (vérifier si le filtre est trop strict)

### Théorème : Propriétés des formes multilinéaires alternées
- ~~Définition : Application multilinéaire~~ — La notion de multilinéarité est déjà contenue dans definition_forme_multilineaire_alternee (prérequis direct). L'énoncé du théorème ne fait pas référence à la définition générale d'application n-linéaire indépendamment de la forme alternée; le prérequis est redondant via la chaîne.

### Définition-théorème : Déterminant d'une famille de vecteurs dans une base
- ~~Théorème : Effet d'une permutation sur une forme multilinéaire alternée~~ — L'énoncé définit det_B directement par la formule sommatoire Σ ε(σ) Π a_{σ(i)i}, puis affirme que c'est une forme n-linéaire alternée avec det_B(B)=1. Theorem_effet_permutation n'apparaît pas dans l'énoncé; seuls ε(σ) (signature) et la formule explicite sont nécessaires pour lire l'énoncé.
- ~~Définition : Application multilinéaire~~ — L'énoncé affirme que det_B 'est une forme n-linéaire alternée' mais cette assertion est dans la conclusion, pas dans l'hypothèse requise pour comprendre l'énoncé. La notion de forme n-linéaire alternée est déjà encapsulée dans definition_forme_multilineaire_alternee qui est un prérequis naturel; definition_application_multilineaire est redondant ici.

### Théorème : Toute forme multilinéaire alternée est un multiple du déterminant dans une base donnée
- ~~Théorème : Propriétés des formes multilinéaires alternées~~ — L'énoncé se lit entièrement en termes de 'forme n-alternée' et de det_B. theorem_proprietes_formes_multilineaires_alternees intervient dans la preuve mais pas dans la compréhension de l'énoncé lui-même; l'objet 'forme n-alternée' est déjà défini dans definition_forme_multilineaire_alternee.

### Théorème : Propriétés du déterminant d'une famille de vecteurs dans une base
- ~~Théorème : Effet d'une permutation sur une forme multilinéaire alternée~~ — L'énoncé (formule de changement de base + caractérisation des bases) ne mentionne pas la signature ni la permutation d'arguments; theorem_effet_permutation n'apparaît pas dans l'énoncé et n'est requis que pour la preuve.

### Définition-théorème : Orientation d'un $\mathbb{R}$-espace vectoriel de dimension finie
- ~~Théorème : Propriétés du déterminant d'une famille de vecteurs dans une base~~ — L'énoncé définit l'orientation à partir de det_B(B') > 0 et affirme que c'est une relation d'équivalence à deux classes. theorem_proprietes_determinant_famille_vecteurs (changement de base, caractérisation des bases) n'est pas requis pour comprendre l'énoncé; il intervient seulement dans la vérification que la relation est bien d'équivalence.

### Théorème : Premières propriétés du déterminant d'une matrice carrée
- ~~Définition : Forme multilinéaire alternée~~ — L'énoncé mentionne la 'multilinéarité par rapport aux colonnes' comme propriété, mais n'utilise pas la définition formelle de forme multilinéaire alternée pour énoncer les résultats. Les propriétés sont énoncées directement sans référence à cette définition abstraite. C'est une propriété caractéristique, pas un prérequis de l'énoncé.

### Théorème : Déterminant d'une matrice triangulaire par blocs
- ~~Théorème : Premières propriétés du déterminant d'une matrice carrée~~ — L'énoncé du théorème se lit directement comme une formule de calcul de déterminant par blocs. Il n'est pas nécessaire de connaître les propriétés de multilinéarité pour comprendre l'énoncé; ces propriétés interviennent dans la preuve, pas dans l'énoncé.

### Théorème : Déterminant d'une matrice et opérations élémentaires
- ~~Théorème : Premières propriétés du déterminant d'une matrice carrée~~ — L'énoncé se formule directement en termes d'opérations élémentaires et de leur effet sur le déterminant, sans nécessiter de référence aux propriétés de multilinéarité pour être compris. La multilinéarité sert à prouver le résultat, pas à l'énoncer.

### Théorème : Formule d'inversion
- ~~Théorème : Premières propriétés du déterminant d'une matrice carrée~~ — L'énoncé est A com(A)^T = com(A)^T A = det(A) I_n, et si A inversible alors A^{-1} = (1/det(A)) com(A)^T. La condition 'A inversible' est mentionnée mais ne requiert pas de connaître le théorème sur l'inversibilité pour comprendre l'énoncé — c'est une hypothèse standard. Le théorème des premières propriétés n'est pas nécessaire à l'énoncé lui-même.

### Théorème : Polynôme caractéristique d'une matrice carrée
- ~~Théorème : Premières propriétés du déterminant d'une matrice carrée~~ — L'énoncé définit χ_A et en énonce les propriétés (degré, racines = valeurs propres, invariance par similitude). Aucune de ces propriétés n'exige de référencer le théorème des premières propriétés pour être comprise — elles sont autoportantes. L'invariance par similitude est une conséquence mais pas un prérequis de l'énoncé.

### Définition-théorème : Déterminant d'un endomorphisme
- ~~Définition : Matrices semblables~~ — L'énoncé affirme que det(Mat_B(u)) ne dépend pas de B, sans mentionner les matrices semblables explicitement. La notion de matrices semblables n'apparaît pas dans l'énoncé — elle intervient dans la preuve (changement de base donne une matrice semblable), pas dans l'énoncé. On peut comprendre l'énoncé sans connaître la définition formelle de matrices semblables.

### Théorème : Déterminant de l'endomorphisme canoniquement associé à une matrice carrée
- ~~Théorème : Matrice dans les bases canoniques de l'application linéaire canoniquement associée~~ — L'énoncé dit que det(Ã) = det(A) où Ã est l'endomorphisme canoniquement associé à A. Pour comprendre cet énoncé, il suffit de savoir ce qu'est l'endomorphisme canoniquement associé à une matrice (notion élémentaire). Le théorème formel sur la matrice dans la base canonique est utilisé dans la preuve, pas requis pour comprendre l'énoncé lui-même.

### Théorème : Propriétés du déterminant d'un endomorphisme
- ~~Théorème : Premières propriétés du déterminant d'une matrice carrée~~ — Les propriétés énoncées (det(u∘v)=det(u)det(v), det(λu)=λ^n det(u), caractérisation des automorphismes) sont formulées directement pour les endomorphismes. Elles n'exigent pas de connaître le théorème analogue pour les matrices pour être comprises — même si la preuve s'y ramène. L'énoncé est autoportant.

### Théorème : Polynôme caractéristique d'un endomorphisme
- ~~Théorème : Changement de bases pour une application linéaire~~ — La formule A' = Q⁻¹AP sert à prouver l'indépendance en base, pas à l'énoncer. L'énoncé affirme simplement que le polynôme ne dépend pas de la base ; comprendre cette assertion ne requiert pas de connaître la formule de changement de base.
- ~~Théorème : Invariance du rang et de la trace~~ — Ce théorème porte sur la trace et le rang des matrices semblables — des propriétés absentes de l'énoncé du polynôme caractéristique d'un endomorphisme. C'est un résultat voisin, non requis pour lire ou comprendre l'énoncé.