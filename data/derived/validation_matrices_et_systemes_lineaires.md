# Validation des prérequis — matrices_et_systemes_lineaires

**47 arêtes retenues** (proposées 58, réfutées 11). `[<-chapitre]` = prérequis amont d'un autre chapitre.

## Arêtes RETENUES (vérifier la précision)

### Définition : Addition matricielle et multiplication par un scalaire
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.99
      Must know what a matrix is before operating on matrices (addition and scalar multiplication)

### Définition : Matrices élémentaires
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.99
      Elementary matrices are matrices with specific structure; need to understand matrix definition
- **Définition : Addition matricielle et multiplication par un scalaire** · conf 0.95
      Statement shows any matrix as linear combination of elementary matrices - requires understanding linear combinations

### Définition : Produit matriciel
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.99
      Product operation only makes sense after understanding matrix definition and indexing

### Théorème : Lignes et colonnes d'un produit
- **Définition : Produit matriciel** · conf 0.99
      Theorem characterizes result of matrix product via rows and columns - cannot state without product definition
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.95
      Statement uses row/column terminology requiring matrix definition

### Théorème : Propriétés du produit matriciel
- **Définition : Produit matriciel** · conf 0.99
      Theorem states properties of product - cannot understand without product definition
- **Définition : Addition matricielle et multiplication par un scalaire** · conf 0.98
      Bilinearity property involves scalar multiplication and addition operations

### Définition : Puissances d'une matrice carrée
- **Définition : Produit matriciel** · conf 0.99
      Matrix power A^k is defined via repeated matrix multiplication
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.85
      Identity matrix I_n referenced in definition - need to understand matrices

### Définition : Matrice nilpotente
- **Définition : Puissances d'une matrice carrée** · conf 0.99
      Nilpotent defined as A^p = 0 for some p - directly requires understanding powers
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.8
      Statement references square matrices M_n - need matrix definition

### Théorème : Formule du binôme et $A^k - B^k$
- **Définition : Puissances d'une matrice carrée** · conf 0.99
      Binomial formula uses A^k and B^k notation
- **Définition : Addition matricielle et multiplication par un scalaire** · conf 0.98
      Formula involves (A+B) and sums of terms - need addition/combination operations
- **Définition : Produit matriciel** · conf 0.95
      Commutativity condition AB=BA and products appear throughout

### Théorème : Produit par blocs
- **Définition : Produit matriciel** · conf 0.99
      Theorem shows block matrix product works like scalar product - requires knowing matrix product

### Définition : Transposée
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.99
      Transpose swaps rows and columns - need to understand matrix structure and indexing

### Théorème : Propriétés de la transposition
- **Définition : Transposée** · conf 0.99
      Theorem characterizes properties of transpose operation - cannot state without transpose definition
- **Définition : Addition matricielle et multiplication par un scalaire** · conf 0.95
      Linearity property states (lambda*A + mu*B)^T = ... - requires understanding linear combinations
- **Définition : Produit matriciel** · conf 0.92
      Statement includes (AB)^T = B^T A^T involving matrix product

### Définition : Matrice symétrique / antisymétrique
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 1
      Requires understanding what a square matrix is
- **Définition : Transposée** · conf 1
      Definition uses A^T = A (symmetric) and A^T = -A (antisymmetric)

### Définition : Diagonale, scalaire, triangulaire
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 1
      Requires understanding matrix structure, coefficients, diagonal positions

### Théorème : Opérations sur les matrices triangulaires
- **Définition : Diagonale, scalaire, triangulaire** · conf 1
      Statement defines and works with triangular matrices
- **Définition : Addition matricielle et multiplication par un scalaire** · conf 1
      Theorem involves scalar multiplication and addition (λA + μB)
- **Définition : Produit matriciel** · conf 1
      Theorem claims AB remains triangular - must know matrix product

### Définition-théorème : Trace d'une matrice carrée
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 1
      Trace is sum of diagonal elements - requires understanding diagonal
- **Définition : Addition matricielle et multiplication par un scalaire** · conf 1
      Linearity property: tr(λA + μB) = λtr(A) + μtr(B)
- **Définition : Produit matriciel** · conf 0.9
      Trace properties involve relationships with matrix product

### Définition : Notation Vect
- **Définition : Addition matricielle et multiplication par un scalaire** · conf 1
      Vect notation requires understanding linear combinations (scalars + vectors)

### Méthode : Algorithme du pivot
- **Définition-théorème : Opérations élémentaires sur les lignes** · conf 1
      Pivot algorithm uses elementary row operations (L_i <-> L_j, etc.)

### Définition-théorème : Matrice inversible, inverse, groupe linéaire
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 1
      Definition applies to square matrices in M_n(K)
- **Définition : Produit matriciel** · conf 1
      Invertibility requires AB = BA = I_n (matrix product and identity)

### Définition-théorème : Système de Cramer
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire** · conf 1
      Cramer system requires invertible matrix (A ∈ GL_n(K))

### Théorème : Une condition suffisante de non-inversibilité
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire** · conf 1
      Theorem states condition for non-invertibility

### Théorème : Caractérisation de l'inversibilité en termes de systèmes linéaires
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire** · conf 1
      Theorem characterizes when A is invertible

### Définition-théorème : Déterminant d'une matrice carrée de taille 2
- **Définition : Matrice, coefficients, lignes, colonnes** · conf 0.95
      Indispensable pour comprendre la notion de matrice 2x2 dont on définit le déterminant
- **Définition : Produit matriciel** · conf 0.9
      Nécessaire pour comprendre l'énoncé (ii) sur l'effet du déterminant sur le produit det(MN)=det(M)det(N)
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire** · conf 0.85
      Important pour le contexte de l'énoncé (i) sur l'inversibilité iff déterminant non nul

### Théorème : Formules de Cramer pour les systèmes $2\times 2$
- **Définition-théorème : Déterminant d'une matrice carrée de taille 2** · conf 0.98
      Pivot du théorème: les formules de Cramer utilisent explicitement les déterminants 2x2 au numérateur et dénominateur

### Théorème : Opérations sur les matrices inversibles
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire** · conf 0.98
      Indispensable: énoncé porte sur GL_n(K), l'ensemble des matrices inversibles
- **Définition : Produit matriciel** · conf 0.95
      Indispensable pour comprendre (ii) sur (AB)⁻¹=B⁻¹A⁻¹ et la composition de produits
- **Définition : Transposée** · conf 0.95
      Indispensable pour la partie (iii) sur (A^T)⁻¹=(A⁻¹)^T
- **Définition : Puissances d'une matrice carrée** · conf 0.95
      Indispensable pour la partie (ii) sur A^k et (A^k)⁻¹=(A⁻¹)^k

### Théorème : Inversibilité et inverse d'une matrice triangulaire
- **Définition : Diagonale, scalaire, triangulaire** · conf 0.98
      Indispensable pour définir les matrices triangulaires dont on étudie l'inversibilité
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire** · conf 0.95
      Indispensable pour le contexte global du théorème sur l'inversibilité

### Théorème : Système triangulaire à coefficients diagonaux non nuls
- **Définition : Diagonale, scalaire, triangulaire** · conf 0.98
      Indispensable pour définir ce qu'est un système triangulaire

## Arêtes RÉFUTÉES (vérifier si le filtre est trop strict)

### Définition : Produit matriciel
- ~~Définition : Addition matricielle et multiplication par un scalaire~~ — La formule (AB)_{ij} = \sum a_{ik}b_{kj} utilise une somme de produits de scalaires du corps K, pas d'opérations sur des matrices. La def_addition_scalaire (combinaison linéaire de matrices) n'est pas requise pour énoncer le produit matriciel.

### Théorème : Structure de l'ensemble des solutions d'un système linéaire
- ~~Définition : Notation Vect~~ — L'énoncé exact ne mentionne jamais Vect(...) — il dit seulement 'solution quelconque = solution particulière + solution quelconque du système homogène'. La notation Vect n'apparaît pas dans cet énoncé.

### Définition-théorème : Opérations élémentaires sur les lignes
- ~~Définition : Matrice, coefficients, lignes, colonnes~~ — L'énoncé définit des opérations sur des lignes (Li ↔ Lj, Li ← λLi, Li ← Li+λLj) sans référence à la structure de matrice — les opérations sont définies purement en termes de lignes indexées par i,j ∈ N*, sans utiliser la notation a_{ij} ou M_{n,p}(K).
- ~~Définition : Matrices élémentaires~~ — L'énoncé ne mentionne pas du tout les matrices élémentaires E_{ij} — les opérations élémentaires sont définies indépendamment via la notation Li ← ... sans référence à E_{ij}.

### Définition-théorème : Matrice inversible, inverse, groupe linéaire
- ~~Définition : Matrices élémentaires~~ — L'énoncé ne mentionne pas les matrices élémentaires E_{ij} — la définition d'inversibilité ne fait référence qu'à AB = BA = I_n, sans E_{ij}.

### Théorème : Une condition suffisante de non-inversibilité
- ~~Définition : Addition matricielle et multiplication par un scalaire~~ — L'énoncé dit 'si une colonne est combinaison linéaire des autres colonnes' — la notion de combinaison linéaire est utilisée, mais def_addition_scalaire définit λA+μB pour des matrices entières, pas des combinaisons de vecteurs colonnes. La notion est implicite dans le contexte mais def_addition_scalaire n'est pas ce qui la définit directement dans l'énoncé.

### Théorème : Caractérisation de l'inversibilité en termes de systèmes linéaires
- ~~Théorème : Structure de l'ensemble des solutions d'un système linéaire~~ — L'énoncé dit seulement que le système Y=AX possède 'une et une seule solution' — il n'invoque pas le théorème de structure (solution particulière + homogène). La caractérisation est autonome et ne nécessite pas de connaître thm_structure_solutions_systeme pour être lue.

### Théorème : Formules de Cramer pour les systèmes $2\times 2$
- ~~Définition-théorème : Système de Cramer~~ — L'énoncé du théorème écrit le système explicitement sous forme de deux équations scalaires (ax+by=c, a'x+b'y=c') et n'invoque pas la définition abstraite 'AX=B avec A inversible'. La notion de 'système de Cramer' n'est pas strictement nécessaire pour comprendre l'énoncé tel qu'il est rédigé ; elle est contextuelle mais non constitutive.

### Théorème : Inversibilité et inverse d'une matrice triangulaire
- ~~Théorème : Opérations sur les matrices inversibles~~ — L'énoncé de thm_inv_triangulaire ne mentionne ni produit d'inverses, ni puissances, ni transposée. thm_op_matrices_inv n'est pas requis pour comprendre cet énoncé ; il peut être utile dans une preuve mais n'apparaît pas dans le statement.

### Théorème : Système triangulaire à coefficients diagonaux non nuls
- ~~Théorème : Structure de l'ensemble des solutions d'un système linéaire~~ — L'énoncé de thm_systeme_triangulaire est autonome : 'possède une et une seule solution'. Il ne fait aucune référence à la décomposition solution particulière + solution homogène de thm_structure_solutions_systeme. Ce dernier n'est pas requis pour comprendre l'énoncé.
- ~~Définition-théorème : Système de Cramer~~ — L'énoncé ne mentionne pas les systèmes de Cramer ni la matrice inversible. Un système triangulaire à diagonale non nulle est certes un cas particulier de système de Cramer, mais cela n'apparaît pas dans le statement ; cette arête est contextuelle, non constitutive.