# Validation des prérequis — representation_matricielle_applications_lineaires

**40 arêtes retenues** (proposées 56, réfutées 16). `[<-chapitre]` = prérequis amont d'un autre chapitre.

## Arêtes RETENUES (vérifier la précision)

### Définition : Matrice d'une application linéaire dans des bases finies
- **Définition : Application linéaire**  [<-applications_lineaires] · conf 0.95
      Notion fondamentale: définir ce qu'est une application linéaire u ∈ L(E,F)
- **Définition : Matrice, coefficients, lignes, colonnes**  [<-matrices_et_systemes_lineaires] · conf 0.95
      Définition de base: comprendre qu'est-ce qu'une matrice et ses coefficients

### Théorème : Matrice dans les bases canoniques de l'application linéaire canoniquement associée
- **Définition : Matrice d'une application linéaire dans des bases finies** · conf 0.95
      Énoncé utilise Mat(u) et ses bases associées
- **Définition-théorème : Application linéaire canoniquement associée à une matrice**  [<-applications_lineaires] · conf 0.9
      Notion d'application linéaire canoniquement associée à une matrice A

### Théorème : Rang d'une application linéaire, rang d'une matrice associée
- **Définition : Matrice d'une application linéaire dans des bases finies** · conf 0.95
      Énoncé établit l'égalité rg(u) = rg(Mat(u))
- **Définition : Application linéaire de rang fini, rang**  [<-applications_lineaires] · conf 0.95
      Notion de rang d'une application linéaire u
- **Définition : Rang d'une matrice**  [<-applications_lineaires] · conf 0.95
      Notion de rang d'une matrice

### Théorème : Calcul matriciel de l'image d'un vecteur
- **Définition : Matrice d'une application linéaire dans des bases finies** · conf 0.95
      Utilise Mat(u) et ses coordonnées
- **Définition : Produit matriciel**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Énoncé: Mat(u(x)) = Mat(u) × Mat(x) utilise la multiplication matricielle

### Théorème : Dictionnaire entre les points de vue vectoriel et matriciel
- **Définition : Matrice d'une application linéaire dans des bases finies** · conf 0.95
      Énoncé porte sur l'isomorphisme u ↦ Mat(u)
- **Définition : Isomorphisme, espaces vectoriels isomorphes**  [<-applications_lineaires] · conf 0.9
      Énoncé parle d'isomorphisme de L(E,F) sur M(n,p)(K)
- **Définition : Produit matriciel**  [<-matrices_et_systemes_lineaires] · conf 0.8
      Point (ii) utilise le produit matriciel pour exprimer composition

### Définition-théorème : Matrice de Vandermonde
- **Définition : Matrice, coefficients, lignes, colonnes**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Définition basique: comprendre la notation matricielle (x_i^(j-1))
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Critère d'inversibilité: matrice de Vandermonde inversible ssi scalaires distincts

### Définition-théorème : Matrice de passage
- **Définition : Matrice d'une application linéaire dans des bases finies** · conf 0.95
      Définition utilise P = Mat(Id_E) dans les bases B' et B
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Propriété (i): matrice de passage est inversible

### Théorème : Changement de base pour un vecteur
- **Définition-théorème : Matrice de passage** · conf 0.95
      Énoncé utilise P = P_B^(B') matrice de passage
- **Définition : Produit matriciel**  [<-matrices_et_systemes_lineaires] · conf 0.85
      Relation X = PX' est une multiplication matricielle

### Théorème : Changement de bases pour une application linéaire
- **Définition-théorème : Matrice de passage** · conf 0.95
      Énoncé utilise P = P_B^(B') et Q = P_C^(C')
- **Définition : Produit matriciel**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Formule A' = Q^(-1)AP utilise multiplicaton et inversion matricielle

### Théorème : Changement de bases et matrice $J_r$
- **Théorème : Rang d'une application linéaire, rang d'une matrice associée** · conf 0.85
      Le paramètre r du théorème est le rang de u

### Définition : Matrices équivalentes
- **Définition-théorème : Matrice inversible, inverse, groupe linéaire**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Définition requiert P ∈ GL_p et Q ∈ GL_n (matrices inversibles)

### Théorème : Caractérisation par le rang
- **Définition : Matrices équivalentes** · conf 0.95
      Defines matrix equivalence
- **Théorème : Changement de bases et matrice $J_r$** · conf 0.95
      Establishes J_r canonical form

### Définition : Matrices semblables
- **Définition : Produit matriciel**  [<-matrices_et_systemes_lineaires] · conf 0.9
      Matrix multiplication

### Théorème : Invariance du rang et de la trace
- **Définition : Matrices semblables** · conf 0.95
      Definition of similarity
- **Définition-théorème : Trace d'une matrice carrée**  [<-matrices_et_systemes_lineaires] · conf 0.95
      Trace definition and properties

### Définition : Trace d'un endomorphisme
- **Définition : Matrice d'une application linéaire dans des bases finies** · conf 0.95
      Matrices of endomorphisms

### Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Matrices carrées)
- **Définition : Matrice, coefficients, lignes, colonnes**  [<-matrices_et_systemes_lineaires] · conf 0.95
      Matrix definition
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)** · conf 0.8
      Parallel definition for endomorphisms

### Théorème : Éléments propres et similitude
- **Définition : Matrices semblables** · conf 0.95
      Similar matrices
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Matrices carrées)** · conf 0.95
      Eigenvalues and eigenspaces

### Théorème : Valeurs propres et polynômes annulateurs
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)** · conf 0.95
      Eigenvalues of endomorphisms

### Théorème : Non-vacuité du spectre sur $\mathbb{C}$
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)** · conf 0.95
      Spectrum defined as eigenvalue set

### Théorème : Finitude du spectre et liberté des vecteurs propres
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)** · conf 0.95
      Eigenspaces definition

### Définition-théorème : Endomorphisme et matrice diagonalisable
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)** · conf 0.95
      Eigenvalues and eigenvectors

### Théorème : Condition suffisante de diagonalisabilité
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Matrices carrées)** · conf 0.95
      Eigenvalues and eigenspaces of matrices

### Théorème : Caractérisations de la diagonalisabilité
- **Définition-théorème : Endomorphisme et matrice diagonalisable** · conf 1
      Définit la notion de diagonalisabilité qui est l'équivalent (i) du théorème
- **Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)** · conf 1
      Définit les sous-espaces propres E_λ(u) qui apparaissent explicitement dans la caractérisation (ii)
- **Définition-théorème : Polynômes annulateurs d'un endomorphisme**  [<-applications_lineaires] · conf 0.95
      Définit formellement les polynômes annulateurs, notion fondamentale pour les équivalences (iii) et (iv)

## Arêtes RÉFUTÉES (vérifier si le filtre est trop strict)

### Théorème : Dictionnaire entre les points de vue vectoriel et matriciel
- ~~Théorème : Composition d'applications linéaires, réciproque d'un isomorphisme~~ — Le point (ii) utilise la composition v∘u, mais la composition de deux applications linéaires est une notion élémentaire ne nécessitant pas de connaître le théorème sur la composition des applications linéaires. Ce théorème porte sur la stabilité/clôture de la composition et l'inversibilité, qui ne sont pas requises pour comprendre l'énoncé du point (ii). La notation v∘u suffit à comprendre l'énoncé.

### Théorème : Commutation et sous-espaces stables
- ~~Théorème : Image d'un sous-espace vectoriel par une application linéaire~~ — L'énoncé utilise Im(g) comme sous-espace vectoriel stable, mais la notion de Im(g) est une conséquence immédiate de la définition d'une application linéaire, pas du théorème sur l'image d'un SEV. Ce théorème porte sur f(A) pour A sous-espace quelconque, ce qui n'est pas nécessaire pour comprendre l'énoncé qui mentionne seulement Im g et Ker g comme objets nommés.
- ~~Théorème : Image réciproque d'un sous-espace vectoriel par une application linéaire et noyau~~ — L'énoncé utilise Ker(g) mais la définition du noyau est contenue dans ce même théorème. Cependant, la notion Ker(g) est une définition élémentaire (souvent donnée comme définition et non comme théorème). Le théorème theoreme_image_reciproque_noyau porte sur les images réciproques de sous-espaces, ce qui dépasse la simple notion de Ker(g) utilisée dans l'énoncé. La préreq n'est pas indéniablement nécessaire pour comprendre l'énoncé.

### Théorème : Changement de base pour un vecteur
- ~~Définition-théorème : Formes coordonnées relativement à une base~~ — L'énoncé parle de 'coordonnées X dans B et X' dans B''. La notion de coordonnées d'un vecteur dans une base est une notion basique d'algèbre linéaire liée à la définition d'une base, pas spécifiquement au théorème sur les formes coordonnées (qui concerne les applications linéaires e_i* associées aux coordonnées). L'énoncé se comprend sans connaître ce théorème.

### Théorème : Changement de bases pour une application linéaire
- ~~Théorème : Changement de base pour un vecteur~~ — L'énoncé du théorème de changement de base pour les applications linéaires se comprend directement à partir des notations Mat et des matrices de passage, sans nécessiter de connaître le théorème de changement de base pour les vecteurs. C'est une généralisation conceptuellement indépendante dans son énoncé ; la preuve peut l'utiliser, mais pas l'énoncé lui-même.

### Théorème : Changement de bases et matrice $J_r$
- ~~Théorème : Changement de bases pour une application linéaire~~ — L'énoncé dit qu'il existe des bases B, C telles que Mat_{B,C}(u) = J_r. Il utilise la notion de Mat_{B,C}(u) (définie dans def_matrice_app_lin) et la notion de rang, mais pas la formule A' = Q^{-1}AP du théorème de changement de base. Ce théorème est utilisé dans la preuve, pas dans l'énoncé.

### Définition : Matrices équivalentes
- ~~Théorème : Changement de bases pour une application linéaire~~ — La définition de matrices équivalentes est B = Q^{-1}AP avec P ∈ GL_p et Q ∈ GL_n. C'est une définition purement algébrique qui ne fait pas référence à la formule du changement de base ni à des applications linéaires dans son énoncé. Le théorème de changement de base explique pourquoi cette notion est pertinente, mais n'est pas nécessaire pour comprendre l'énoncé de la définition.

### Théorème : Caractérisation par le rang
- ~~Théorème : Rang d'une application linéaire, rang d'une matrice associée~~ — Le rang apparaît dans l'énoncé comme notion (même rang), mais le théorème liant rg(u) et rg(Mat) est un outil de preuve, pas nécessaire pour comprendre l'énoncé lui-même.

### Définition : Matrices semblables
- ~~Définition : Matrice d'une application linéaire dans des bases finies~~ — La définition de similitude (B = P^{-1}AP avec P inversible) n'invoque que le produit matriciel et l'inversibilité — pas la notion de matrice d'une application linéaire dans des bases.

### Théorème : Invariance du rang et de la trace
- ~~Théorème : Rang d'une application linéaire, rang d'une matrice associée~~ — Le rang apparaît dans l'énoncé ('même rang') comme notion, mais le théorème liant rang d'un endomorphisme et rang de sa matrice est un outil de preuve, pas nécessaire pour comprendre l'énoncé.

### Définition : Trace d'un endomorphisme
- ~~Théorème : Changement de bases pour une application linéaire~~ — L'indépendance par rapport à la base est mentionnée dans l'énoncé, mais le théorème de changement de base est un outil justificatif, pas une notion dont l'énoncé dépend pour être compris.

### Définition : Valeurs propres, vecteurs propres, sous-espaces propres (Endomorphismes)
- ~~Définition : Matrice d'une application linéaire dans des bases finies~~ — La définition des éléments propres d'un endomorphisme (E_lambda(u) = Ker(u - lambda Id)) ne fait aucune référence à une matrice — elle est purement intrinsèque.

### Définition-théorème : Endomorphisme et matrice diagonalisable
- ~~Définition-théorème : Matrice de passage~~ — L'énoncé pour les matrices écrit A = P diag P^{-1} avec P inversible, mais ne nomme pas P 'matrice de passage' — la définition formelle de matrice de passage n'est pas nécessaire pour comprendre l'énoncé.

### Théorème : Condition suffisante de diagonalisabilité
- ~~Théorème : Finitude du spectre et liberté des vecteurs propres~~ — Ce théorème (indépendance des vecteurs propres pour des vp distinctes) est l'outil clé de la preuve, pas une notion dont l'énoncé dépend pour être compris.

### Théorème : Caractérisations de la diagonalisabilité
- ~~Théorème : Valeurs propres et polynômes annulateurs~~ — Ce théorème (P(u)(x)=P(λ)x, racines des annulateurs) sert à prouver les équivalences, mais n'apparaît nulle part dans l'énoncé lui-même ; l'énoncé reste lisible sans lui.
- ~~Théorème : Lemme de décomposition des noyaux~~ — Le lemme des noyaux est un outil de démonstration ; l'énoncé du théorème n'y fait aucune référence — (ii) parle de somme directe de sous-espaces propres, pas de noyaux de polynômes.