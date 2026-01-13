# 19 Structures algébriques

THÉORÈME. Soit une équation donnée, dont \( a, b, c, \dots \) sont les \( m \) racines. Il y aura toujours un groupe de permutations des lettres \( a, b, c, \dots \) qui jouira de la propriété suivante :
1. Que toute fonction des racines, invariable par les substitutions de ce groupe, soit rationnellement connue ;
2. Réciproquement, que toute fonction des racines, déterminable rationnellement, soit invariable par les substitutions.
[...] Nous appellerons groupe de l’équation le groupe en question.
(Évariste Galois)

**Note Historique 19.0.1**
Il est fréquent de trouver des propriétés communes dans des situations qui au départ semblent totalement sans rapport. Une des grandes découvertes (et réussites) des mathématiques du 19e siècle a été de parvenir à unifier ces problèmes en apparence distincts, en faisant ressortir de ces différents problèmes des structures ensemblistes et opératoires ayant des propriétés similaires.
C’est Évariste Galois le premier à mettre en avant ces études de structure à l’occasion de ses travaux visant à étudier la résolubilité des équations polynomiales par radicaux. Il y parle de groupes de permutations des solutions d’une équation, et est amené à étudier des propriétés de certains sous-ensembles de ces groupes de permutations. C’est lui qui introduit la terminologie de « groupe », même si la formalisation précise de cette notion est beaucoup plus tardive.
Le groupe des permutations d’un ensemble avait déjà été étudié auparavant par Lagrange (mais sans en faire ressortir cette structure bien particulière de groupe). Il a notamment établi à cette occasion un résultat important, généralisé plus tard pour tout groupe sous le nom de « théorème de Lagrange ».

La notion de structure algébrique repose de façon essentielle sur la notion de loi de composition (c’est-à-dire d’opération définie sur un ensemble, comme l’addition ou la multiplication) et sur les différentes propriétés que ces lois de composition peuvent vérifier. Nous commençons donc notre étude par l’examen de ces propriétés, après avoir défini de façon précise ce qu’est une loi de composition.

## I Lois de composition

### I.1 Définitions

Dans ce qui suit, \( E \) est un ensemble quelconque.

**Définition 19.1.1 (Lois de composition)**
On distingue deux types de lois de compositions (opérations), suivant que la loi décrit une opération entre deux éléments de l’ensemble \( E \), ou entre un élément de \( E \) et un élément d’un ensemble externe \( \Omega \), appelé domaine d’opérateur.
* Une loi de composition interne est une application de \( \phi : E \times E \to E \), souvent notée de façon opérationnelle plutôt que fonctionnelle (par exemple \( x + y \) au lieu de \( \phi(x, y) \) pour désigner une addition).
* Une loi de composition externe à gauche sur \( E \), d’ensemble d’opérateurs \( \Omega \), est une application de \( \Omega \times E \to E \), également notée de façon opérationnelle le plus souvent (par exemple \( \lambda \cdot x \) au lieu de \( \phi(\lambda, x) \)).
* De même, une loi de composition externe à droite sur \( E \) d’ensemble d’opérateurs \( \Omega \) est une application \( E \times \Omega \to E \).

**Exemples 19.1.2**
* Les lois \( + \) et \( \times \) sont des lois de composition internes sur \( \mathbb{N}, \mathbb{Z}, \mathbb{R} \) ou \( \mathbb{C} \).
* La loi \( + \) est une loi de composition interne sur \( \mathbb{R}^n \) ou \( \mathbb{C}^n \).
* \( (\lambda, X) \mapsto \lambda X \) (multiplication d’un vecteur par un scalaire) est une loi de composition externe sur \( \mathbb{R}^n \) (ou \( \mathbb{C}^n \)), d’ensemble d’opérateurs \( \mathbb{R} \) (ou \( \mathbb{C} \)).
* De même pour la multiplication des polynômes par des scalaires.
* La composition \( \circ \) définit une loi de composition interne sur \( E^E \).
* Le produit scalaire sur \( \mathbb{R}^n \) n’est pas une loi de composition (interne ou externe), car le résultat de l’opération n’est pas un élément de \( \mathbb{R}^n \).

### I.2 Propriétés d’une loi de composition

Soit \( E \) un ensemble, muni d’une loi de composition interne que nous noterons \( \star \). Nous étudions ici quelques propriétés pouvant être vérifiées par la loi \( \star \).

**Définition 19.1.3 (Associativité, commutativité)**
* On dit que \( \star \) est associative ssi : \( \forall(x, y, z) \in E^3, (x \star y) \star z = x \star (y \star z) \)
* On dit que \( \star \) est commutative ssi : \( \forall(x, y) \in E^2, x \star y = y \star x \).

Ainsi, lorsque \( E \) est muni d’une loi associative, on peut effectuer les opérations dans l’ordre que l’on veut, à condition de respecter la position respective des éléments les uns par rapport aux autres. Si la loi est commutative, on peut échanger la position respective des éléments (mais pas nécessairement faire les opérations dans l’ordre qu’on veut si la loi n’est pas associative). Pour énoncer cette propriété d’associativité généralisée, on commence par définir ce qu’est un parenthésage admissible.

**Définition 19.1.4 (Parenthésage admissible)**
Un parenthésage admissible d’une expression formée de produits \( \star \) d’éléments \( x_1, \dots, x_n \) de \( E \) est un parenthésage qui permet de regrouper 2 par 2 des éléments \( x_1, \dots, x_n \), ou des termes calculés à partir de ceux-ci par un parenthésage plus fin. De façon plus rigoureuse, on définit cette notion par induction structurelle :
* (initialisation) les expressions \( x \) constitués d’un unique élément sont munis d’un parenthésage admissible ;
* si \( A_1 \) et \( A_2 \) sont deux expressions en \( x_1, \dots, x_k \) et \( x_{k+1}, \dots, x_n \) munis d’un parenthésage admissible, alors \( (A_1 \star A_2) \) est muni d’un parenthésage admissible.

**Remarque 19.1.5**
Le parenthésage le plus externe n’est pas complètement utile, et ne sert qu’à continuer la construction si d’autres termes doivent s’ajouter à l’expression. Ainsi, dans une expression munie d’un parenthésage admissible, on omet souvent le jeu de parenthèses externes. Par exemple, l’expression \( (x_1 \star x_2) \) est munie d’un parenthésage admissible, mais on écrira plutôt \( x_1 \star x_2 \). De même, on écrira \( x_1 \star (x_2 \star x_3) \) plutôt que \( (x_1 \star (x_2 \star x_3)) \).

**Exemples 19.1.6**
En utilisant la convention de la remarque précédente, lesquelles des expressions ci-dessous sont munies d’un parenthésage admissible ?
* \( (x_1 \star x_2) \star (x_3 \star x_4) \star x_5 \)
* \( (x_1 \star x_2) \star ((x_3 \star x_4) \star x_5) \)
* \( (x_1 \star x_2) \star x_3) \star ((x_4 \star x_5) \)

**Théorème 19.1.7 (Associativité généralisée)**
Soit \( \star \) une loi associative sur \( E \), et \( x_1, \dots, x_n \) des éléments de \( E \). Alors la valeur de \( x_1 \star x_2 \star \dots \star x_n \) ne dépend pas du parenthésage admissible choisi sur cette expression (donc de l’ordre dans lequel on effectue ces opérations).

**Démonstration**
Ce résultat qui paraît évident intuitivement n’est pas si évident que cela à démontrer. Une démonstration consiste à montrer par récurrence forte sur \( n \) (en se servant de la structure inductive), toute expression convenable parenthésée est égale à l’expression munie d’un parenthésage croissant, dans lequel les opérations sont faits dans l’ordre de lecture. La démonstration consiste alors à décomposer une expression en deux, écrire l’expression de droite avec un parenthésage croissant en utilisant l’hypothèse de récurrence, utiliser l’associativité pour isoler \( x_n \) puis réutiliser l’hypothèse de récurrence sur l’expression de gauche constituée maintenant de \( n - 1 \) termes.

**Notation 19.1.8 (Suppression des parenthèses)**
Lorsque \( \star \) est associative, nous nous permettons d’omettre le parenthésage, en notant \( x \star y \star z \) au lieu de \( (x \star y) \star z \) ou \( x \star (y \star z) \), la propriété d’associativité levant toute ambiguïté sur l’interprétation de cette expression. Plus généralement, d’après la propriété d’associativité généralisée, on peut omettre le parenthésage dans des opérations portant sur un nombre quelconque de termes.

On peut aussi donner une propriété de commutativité généralisée, lorsqu’on a à la fois l’associativité et la commutativité. Dans le cas d’une structure commutative non associative, la description est plus délicate.

**Théorème 19.1.9 (Commutativité généralisée)**
Soit \( \star \) une loi commutative et associative sur \( E \), et \( x_1, \dots, x_n \) des éléments de \( E \). Alors, pour tout \( \sigma \in \mathfrak{S}_n \),
\[ x_1 \star x_2 \star \dots \star x_n = x_{\sigma(1)} \star x_{\sigma(2)} \star \dots \star x_{\sigma(n)}. \]

**Démonstration**
Ici encore, le théorème semble assez évident. Mais une démonstration rigoureuse nécessite un petit effort de réflexion, et l’utilisation de quelques propriétés des permutations. On peut montrer que toute permutation s’écrit comme composée de permutations très simples consistant simplement à échanger 2 termes consécutifs, en laissant les autres fixes. C’est ce qu’on fait par exemple lorsqu’on effectue un tri à bulles, ou un tri par insertion, si on remonte les éléments au fur et à mesure. En admettant ce résultat, on passe donc de l’expression de gauche à l’expression de droite en faisant une succession d’échanges de deux termes consécutifs. Par associativité généralisée, on peut trouver un parenthésage associé qui regroupe ces deux termes, et donc l’échange de ces deux termes ne change pas la valeur de l’expression (par commutativité).
En attendant de disposer de ce résultat, on peut montrer à la main que l’échange de deux termes quelconques non nécessairement consécutifs ne change pas la valeur de l’expression, ce qui permet d’échanger \( x_n \) et \( x_{\phi(n)} \) dans l’expression de droite (si \( n \neq \phi(n) \)), puis on termine par récurrence, en considérant l’expression formée des \( n - 1 \) premiers termes.

**Exemples 19.1.10 (Lois commutatives, associatives)**
1. Les lois \( + \) et \( \times \) définies sur \( \mathbb{N}, \mathbb{Z}, \mathbb{R} \) et \( \mathbb{C} \) sont associatives et commutatives.
2. Le produit matriciel définit une loi associative sur \( \mathcal{M}_n(\mathbb{R}) \) (ensemble des matrices carrées d’ordre \( n \)), mais pas commutative.
3. La composition définit une loi associative sur \( E^E \) mais pas commutative.
4. La soustraction dans \( \mathbb{Z} \) est non associative et non commutative.
5. La loi définie sur \( \mathbb{R} \) par \( (a, b) \mapsto (a + b)^2 \) est commutative mais non associative.

**Avertissement 19.1.11**
Attention à toujours bien indiquer le parenthésage lorsque la loi n’est pas associative, ou lorsque plusieurs lois sont en jeu sans qu’il n’ait été défini de façon explicite de relation de priorité sur les opérations.

**Convention 19.1.12 (Commutativité d’une loi d’addition, usage)**
Nous réserverons la notation additive (signe opératoire \( + \)) pour des lois de composition commutatives. Cela n’empêche pas en revanche de considérer des lois commutatives notées différemment (par exemple multiplicativement).

**Convention 19.1.13 (Omission du signe d’opération)**
Il est fréquent d’omettre certains signes d’opérations (généralement les multiplications), si l’usage qui est fait de cette suppression est suffisamment clair et ne provoque pas d’ambiguïté.
Ainsi, vous avez déjà l’habitude d’écrire \( ab \) au lieu de \( a \times b \) ou \( a \cdot b \). Cet usage, courant dans \( \mathbb{R} \) ou \( \mathbb{C} \), est aussi fréquent pour les opérations matricielles, à la fois pour le produit interne que le produit externe (multiplication d’une matrice par un scalaire). De façon peut-être plus troublante, il est fréquent d’omettre le \( \circ \) de la composition, en particulier lorsqu’on compose des applications linéaires (il n’y a alors pas d’ambiguïté sur le sens de ce produit, les éléments de l’espace d’arrivée ne pouvant en général pas se multiplier entre eux).

**Notation 19.1.14 (Itération d’une loi)**
Soit \( \star \) une loi associative sur \( E \), \( n \) un élément de \( \mathbb{N}^* \) et \( x \) un élément de \( E \). On note \( x^{\star n} \), ou plus simplement \( x^n \) lorsqu’il n’y a pas d’ambiguïté (lorsqu’il n’y a qu’une loi en jeu par exemple), l’itération de la loi \( \star \), c’est à dire :
\[ x^{\star n} = x \star x \star \dots \star x, \]
le nombre de termes \( x \) étant égal à \( n \). Pour une définition plus rigoureuse, par récurrence, \( x^{\star 1} = x \), et pour tout \( n \in \mathbb{N}^* \), \( x^{\star(n+1)} = x^{\star n} \star x \).
Si \( E \) admet un élément neutre \( e \) pour la loi \( \star \) (voir ci-dessous), on note par convention \( x^{\star 0} = e \). Remarquez qu’alors, la définition par récurrence est aussi valable pour passer de l’exposant 0 à l’exposant 1.
Dans le cas où plusieurs lois sont en jeu, la notation \( x^n \) peut prêter à confusion. En général, dans les structures faisant intervenir deux lois dont une commutative, on utilise la multiplication \( \times \) (loi multiplicative) et l’addition \( + \) (loi additive). On distingue les itérations des lois sans introduire de lourdeur d’écriture en utilisant une notation particulière pour l’itération de l’addition, calquée sur ce qu’il se passe dans \( \mathbb{R} \) :

**Notation 19.1.15 (Itération d’une loi additive)**
Si \( E \) est muni d’une loi notée additivement \( + \), on note \( n \cdot x \) au lieu de \( x^{+n} \) l’itération de la loi \( + \).
Attention au fait que généralement, \( n \) n’étant pas élément de \( E \), la notation \( \cdot \) est à distinguer d’une éventuelle multiplication dans \( E \) (cela définit une loi externe à opérateurs dans \( \mathbb{N} \)). Si \( \mathbb{N} \subset E \), la loi externe \( \cdot \) peut coïncider avec le produit, si \( E \) est muni d’une structure suffisamment riche. C’est ce qui se produit dans la plupart des structures qui contiendront \( \mathbb{N} \) que nous aurons l’occasion de considérer.

**Définition 19.1.16 (Élément neutre)**
Soit \( e \) un élément de \( E \). On dit que \( e \) est un élément neutre pour la loi \( \star \) si pour tout \( x \in E \), \( e \star x = x = x \star e \).
On trouve aussi la notion de neutre à gauche ou à droite si une seule de ces deux égalités est satisfaite. Pour une loi commutative, \( e \) est neutre ssi \( e \) est neutre à droite ssi \( e \) est neutre à gauche.

**Exemple 19.1.17 (Éléments neutres)**
1. 0 est élément neutre pour \( + \) dans \( \mathbb{N}, \mathbb{Z}, \mathbb{R}, \mathbb{C} \). C’est le seul élément neutre pour \( + \).
2. 1 est élément neutre pour \( \times \) dans \( \mathbb{N}, \mathbb{Z}, \mathbb{R}, \mathbb{C} \). C’est le seul élément neutre pour \( \times \).
3. \( I_n \) est élément neutre pour \( \times \) sur \( \mathcal{M}_n(\mathbb{R}) \), \( 0_n \) est élément neutre pour \( + \) sur \( \mathcal{M}_n(\mathbb{R}) \).
4. \( \text{id}_E \) est élément neutre pour \( \circ \) sur \( E^E \).
5. Sur un ensemble \( E \) de cardinal supérieur ou égal à 2, la loi \( (x, y) \mapsto y \) admet plusieurs neutres à gauche (tout \( x \in E \) est neutre à gauche). En revanche, il n’y a pas de neutre à droite.

Une loi ne peut pas admettre plusieurs éléments neutres, comme le montre la propriété suivante.

**Proposition 19.1.18 (Unicité du neutre)**
L’élément neutre, s’il existe, est unique.

**Démonstration**
Considérer \( e_1 \star e_2 \).

**Notation 19.1.19 (\( 0_E, 1_E \))**
* On note généralement \( 0_E \) (ou 0 s’il n’y a pas de risque d’ambiguïté) le neutre (s’il existe) d’une loi notée additivement \( + \).
* On note généralement \( 1_E \) (ou 1 s’il n’y a pas de risque d’ambiguïté) le neutre (s’il existe) d’une loi notée multiplicativement \( \times \).

**Définition 19.1.20 (Élément symétrique)**
Supposons que \( E \) admet un élément neutre \( e \) pour la loi \( \star \). Soit \( x \in E \).
* On dit que \( y \) est un symétrique à gauche de \( x \) pour la loi \( \star \) si \( y \star x = e \).
* On dit que \( y \) est un symétrique à droite de \( x \) pour la loi \( \star \) si \( x \star y = e \).
* On dit que \( y \) est un symétrique de \( x \) pour la loi \( \star \) si et seulement si \( y \) est un symétrique à droite et à gauche de \( x \).
* On dit que \( x \) est symétrisable (resp. symétrisable à gauche, resp. symétrisable à droite) si \( x \) admet au moins un symétrique (resp. un symétrique à gauche, resp. un symétrique à droite).

**Terminologie 19.1.21 (Opposé, inverse)**
* Dans le cas d’une loi notée additivement, on parle plutôt d’opposé, et en cas d’unicité, on note \( -x \) l’opposé de \( x \).
* Dans le cas d’une loi notée multiplicativement, on parle plutôt d’inversibilité (inversibilité à droite, à gauche), et en cas d’unicité, on note \( x^{-1} \) l’inverse de \( x \).

Dans une situation plus générale, on trouve souvent la notation \( x^s \) pour désigner le symétrique.

**Proposition 19.1.22 (Unicité du symétrique)**
Si \( \star \) est associative, alors, en cas d’existence, le symétrique est unique.

**Démonstration**
Si \( y \) et \( z \) sont deux symétriques de \( x \), considérer \( y \star x \star z \).

**Exemples 19.1.23**
1. Dans \( \mathbb{N} \) seul 0 admet un opposé pour \( + \).
2. Dans \( \mathbb{Z}, \mathbb{R}, \mathbb{Q}, \mathbb{C} \), tout élément admet un opposé pour \( + \).
3. Dans \( \mathbb{N} \) seul 1 admet un inverse, dans \( \mathbb{Z} \), seuls 1 et \( -1 \) admettent un inverse. Dans \( \mathbb{R}, \mathbb{Q} \) et \( \mathbb{C} \) tous les éléments non nuls admettent un inverse.
4. Dans \( E^E \) muni de \( \circ \), sous réserve de l’axiome du choix, les éléments symétrisables à gauche sont les injections, les éléments symétrisables à droite sont les surjections, les éléments symétrisables sont les bijections. Une injection non surjective admet plusieurs symétriques à gauche ; une surjection non injective admet plusieurs symétriques à droite.

**Proposition 19.1.24 (Symétrique de \( x \star y \))**
Supposons \( \star \) associative. Soit \( (x, y) \in E^2 \). Si \( x \) et \( y \) sont symétrisables, de symétriques \( x^s \) et \( y^s \), alors \( x \star y \) est symétrisable de symétrique \( y^s \star x^s \). Notez l’inversion !

Traduisons pour une loi multiplicative : si \( x \) et \( y \) sont inversibles, d’inverses \( x^{-1} \) et \( y^{-1} \), alors \( xy \) aussi, et \( (xy)^{-1} = y^{-1}x^{-1} \).
Dans le cas d’une loi additive commutative, on obtient
\[ -(x + y) = (-y) + (-x) = (-x) + (-y), \]
ce qu’on note plus simplement \( -x - y \), comme dans \( \mathbb{R} \).

**Définition 19.1.25 (Élément absorbant)**
Soit \( x \in E \).
* On dit que \( x \) est un élément absorbant à gauche pour \( \star \) ssi : \( \forall y \in E, x \star y = x \).
* On dit que \( x \) est absorbant à droite pour \( \star \) ssi : \( \forall y \in E, y \star x = x \).
* On dit que \( x \) est absorbant s’il est à la fois absorbant à gauche et à droite.

**Exemples 19.1.26**
1. 0 est absorbant pour \( \times \) dans \( \mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C} \).
2. Pour la loi \( (x, y) \mapsto y \), tout élément \( y \) de \( E \) est absorbant à droite. Il n’y a pas d’élément absorbant à gauche si \( E \) est de cardinal au moins 2.
3. \( +\infty \) est absorbant dans \( (\mathbb{R} \cup \{+\infty\}, +) \).

**Définition 19.1.27 (Élément régulier ou simplifiable)**
* Un élément \( x \) est dit régulier (ou simplifiable) à gauche ssi :
\[ \forall(y, z) \in E^2, x \star y = x \star z \implies y = z. \]
* Un élément \( x \) est dit régulier (ou simplifiable) à droite ssi :
\[ \forall(y, z) \in E^2, y \star x = z \star x \implies y = z. \]
* Un élément \( x \) est dit régulier (ou simplifiable) s’il est à la fois régulier à gauche et à droite.

**Proposition 19.1.28 (Régularité des éléments symétrisables)**
Supposons que \( E \) soit muni d’une loi \( \star \) associative.
* Soit \( x \) un élément admettant un symétrique à gauche. Alors \( x \) est régulier à gauche.
* Soit \( x \) un élément admettant un symétrique à droite. Alors \( x \) est régulier à droite.
* Soit \( x \) un élément admettant un symétrique. Alors \( x \) est régulier.

**Démonstration**
Pour simplifier, multiplier par le symétrique !

Ainsi, le fait de pouvoir simplifier une égalité par un réel ou complexe non nul \( x \) ne vient pas tant de la non-nullité que de l’inversibilité de \( x \). Par exemple, la non-nullité n’est pas un critère suffisant de régularité dans \( \mathcal{M}_n(\mathbb{R}) \) : il est nécessaire d’avoir l’inversibilité de la matrice que l’on veut simplifier. Il convient toutefois de noter que la condition d’inversibilité, si elle est suffisante, n’est en général pas nécessaire.

**Exemple 19.1.29**
Donnez des exemples de structures algébriques simples dans lesquelles certains éléments sont réguliers sans être inversibles.

### I.3 Ensembles munis de plusieurs lois

Soit \( E \) un ensemble muni de deux lois de composition \( \star \) et \( \diamond \).

**Définition 19.1.30 (Distributivité)**
* On dit que la loi \( \star \) est distributive à gauche sur \( \diamond \) ssi : \( \forall(x, y, z) \in E^3, x \star (y \diamond z) = (x \star y) \diamond (x \star z) \).
* On dit que la loi \( \star \) est distributive à droite sur \( \diamond \) ssi : \( \forall(x, y, z) \in E^3, (y \diamond z) \star x = (y \star x) \diamond (z \star x) \).
* On dit que la loi \( \star \) est distributive sur \( \diamond \) ssi elle est distributive à droite et à gauche.

**Exemples 19.1.31**
1. La loi \( \times \) est distributive sur \( + \) dans \( \mathbb{N}, \mathbb{Z}, \mathbb{R}, \mathbb{C}, \mathcal{M}_n(\mathbb{R}) \dots \)
2. La loi \( \cap \) est distributive sur \( \cup \) sur \( \mathcal{P}(X) \). Inversement, la loi \( \cup \) est distributive sur \( \cap \).
3. Que peut-on dire de la loi \( \cap \) par rapport à elle-même ? De la loi \( \cup \) ?

**Remarque 19.1.32**
La première relation \( x \star (y \diamond z) = (x \star y) \diamond (x \star z) \) a également un sens lorsque \( \star \) est une loi externe. Ainsi, dans \( \mathbb{R}^n \), muni de l’addition en loi interne, et de la multiplication des scalaires en loi externe, on a \( \lambda(X + Y) = \lambda X + \lambda Y \) : la loi externe est distributive sur la loi interne.

**Théorème 19.1.33 (Distributivité généralisée)**
Soit \( E \) muni de deux lois \( \times \) et \( + \) associatives, et \( + \) commutative. On suppose que \( \times \) est distributive sur \( + \). On a alors, pour tout \( n \in \mathbb{N}^* \) et tous ensembles finis \( J_1, \dots, J_n \) non vides, les \( x_{i,j} \) étant des éléments de \( E \), on a :
\[ \prod_{i=1}^n \sum_{j \in J_i} x_{i,j} = \sum_{(j_1, \dots, j_n) \in J_1 \times \dots \times J_n} \prod_{i=1}^n x_{i,j_i}. \]
La loi \( \times \) n’étant pas supposée commutative, les produits \( \prod \) sont à comprendre dans l’ordre croissant des indices.

**Exemple 19.1.34**
Comprendre la formule ci-dessus pour l’expression \( (x_1 + x_2) \times (y_1 + y_2 + y_3) \times (z_1 + z_3) \).

**Définition 19.1.35 (associativité externe)**
Soit \( E \) un ensemble muni d’une loi de composition externe \( \diamond \) sur \( \mathbb{K} \), lui même muni d’une loi de composition interne \( \star \). On dit que les lois \( \star \) et \( \diamond \) vérifient une propriété d’associativité externe si pour tout \( (\lambda, \mu) \in \mathbb{K}^2 \) et \( x \in E \)
\[ (\lambda \star \mu) \diamond x = \lambda \diamond (\mu \diamond x). \]
Cette propriété est par exemple satisfaite sur \( \mathbb{R}^n \) pour la multiplication par un scalaire : \( (\lambda\mu)X = \lambda(\mu X) \).
Plus généralement, un espace vectoriel vérifiera cette propriété d’associativité externe.
De la même manière, si \( E \) est muni d’une loi interne \( \times \) et d’une loi externe \( \diamond \) à opérateurs dans \( \mathbb{K} \), on dispose d’une autre propriété de distributivité externe s’exprimant par la relation :
\[ \lambda \diamond (x \times y) = (\lambda \diamond x) \times y. \]
Dans cette situation, qu’on retrouve notamment dans la définition des \( \mathbb{K} \)-algèbres, on pourra éventuellement avoir en plus l’égalité avec \( x \times (\lambda \diamond y) \). C’est une propriété qu’on retrouve par exemple pour l’ensemble des matrices carrées d’ordre \( n \), muni de la loi interne \( \times \) (produit matriciel) et de la loi externe correspondant au produit d’une matrice par un scalaire.

### I.4 Stabilité

**Définition 19.1.36**
1. Soit \( E \) un ensemble muni d’une loi de composition interne \( \star \) et \( F \subset E \) un sous-ensemble de \( E \). On dit que \( F \) est stable par \( \star \), si la restriction de la loi de \( E \) à \( F \times F \) peut se corestreindre à \( F \), autrement dit si :
\[ \forall(x, y) \in F^2, x \star y \in F. \]
Dans ce cas, la l.c.i. de \( E \) se restreint en une l.c.i. \( \star_F : F \times F \to F \), appelée loi induite sur \( F \) par \( \star \).
2. Soit \( E \) un ensemble muni d’une loi de composition externe \( \cdot \) à opérateurs dans \( \Omega \), et \( F \subset E \). On dit que \( E \) est stable par \( \cdot \) :
\[ \forall \omega \in \Omega, \forall x \in F, \omega \cdot x \in F. \]
Dans ce cas, la l.c.e. de \( E \) se restreint en une l.c.e. sur \( F \), à opérateurs dans \( \Omega \).

## II Structures

### II.1 Généralités

**Définition 19.2.1**
* Une structure de « truc » est la donnée d’un certain nombre d’axiomes (définissant ce qu’on appelle un « truc ») portant sur un ensemble fini de lois de composition (internes et/ou externes).
* On dit qu’un ensemble \( E \) est muni d’une structure de truc ssi \( E \) est muni d’un nombre fini de lois de composition vérifiant les axiomes de structure de truc.

**Exemples 19.2.2**
1. Une structure de magma se définit comme la donnée d’une loi de composition, et un ensemble vide d’axiomes. Ainsi, tout ensemble \( E \) muni d’une loi de composition est muni d’une structure de magma.
2. Une structure de monoïde se définit comme la donnée d’une loi de composition, et de deux axiomes : l’associativité de la loi et l’existence d’un élément neutre. Par exemple \( (\mathbb{N}, +) \) est muni d’une structure de monoïde (on dit plus simplement que \( (\mathbb{N}, +) \) est un monoïde). L’ensemble des mots sur un alphabet \( \mathcal{A} \), muni de l’opération de concaténation est aussi un monoïde (appelé monoïde libre sur l’alphabet \( \mathcal{A} \)). Contrairement à \( \mathbb{N} \), le monoïde libre n’est pas commutatif.
3. Ainsi, la structure de monoïde est plus riche que celle de magma : tout monoïde est aussi un magma ; un monoïde peut être défini comme un magma dont la loi est associative et possède un élément neutre.
4. Une structure de groupe est une structure de monoïde à laquelle on rajoute l’axiome d’existence de symétriques. Par exemple \( (\mathbb{Z}, +) \) est un groupe, mais pas \( (\mathbb{N}, +) \).

**Définition 19.2.3 (Structure induite)**
Soit \( E \) un ensemble muni d’une structure de truc, et \( F \) un sous-ensemble de \( E \). Si \( F \) est stable pour chacune des lois de \( E \), l’ensemble \( F \) muni des lois induites sur \( F \) par les lois de \( E \) est muni d’une structure appelée structure induite sur \( F \) par la structure de \( E \).

**Avertissement 19.2.4**
En général, \( F \) ne peut pas être muni d’une structure de truc, mais seulement d’une structure moins riche, certains des axiomes de la structure de truc pouvant ne pas être préservés par restriction.

**Exemple 19.2.5**
\( (\mathbb{N}, +) \) est la structure induite sur \( \mathbb{N} \) par la structure de groupe additif de \( (\mathbb{Z}, +) \). En revanche, \( (\mathbb{N}, +) \) n’est pas un groupe. On a perdu l’existence des opposés par restriction.

**Définition 19.2.6 (Sous-truc)**
Soit \( E \) un ensemble muni d’une structure de truc et \( F \) un sous-ensemble de \( E \). On dit que \( F \) est un sous-truc de \( E \) si \( F \) est stable par les lois de \( E \), si \( F \) contient les neutres imposés de \( E \), et si les lois induites sur \( F \) par les lois de \( E \) vérifient les axiomes de la structure de truc.

**Remarque 19.2.7 (Restriction des propriétés universelles)**
Toutes les propriétés universelles (quantifiées par \( \forall \)) passent bien aux structures induites. Ainsi, la commutativité, l’associativité, la distributivité, la régularité passent aux structures induites.

### II.2 Morphismes

Lorsqu’on dispose d’une structure de truc, on est souvent amené à considérer des applications entre ensembles munis de la structure de truc. Cependant seules nous intéressent les applications compatibles dans un certain sens avec la structure de truc.

**Définition 19.2.8 (Homomorphisme)**
Soit \( E \) et \( F \) deux ensembles munis d’une structure de truc, \( E \) étant muni des lois de composition interne \( (\star_1, \dots, \star_n) \) et \( F \) des lois \( (\diamond_1, \dots, \diamond_n) \), et des lois de composition externes \( (\top_1, \dots, \top_m) \) et \( (\perp_1, \dots, \perp_m) \) sur \( K_1, \dots, K_m \) respectivement. On dit qu’une application \( f : E \to F \) est un homomorphisme de trucs ssi :
* L’application \( f \) est compatible avec les lois internes :
\[ \forall k \in \llbracket 1, n \rrbracket, \forall (x, y) \in E^2, f(x \star_k y) = f(x) \diamond_k f(y). \]
* L’application \( f \) est compatible avec les lois externes :
\[ \forall \ell \in \llbracket 1, m \rrbracket, \forall \lambda \in K_\ell, \forall x \in E, f(\lambda \top_\ell x) = \lambda \perp_\ell f(x). \]
* Si l’existence du neutre \( e_i \) pour la loi \( \star_i \) est imposée dans les axiomes (et donc le neutre \( e'_i \) pour la loi \( \diamond_i \) existe aussi), \( f \) doit être compatible avec le neutre : \( f(e_i) = e'_i \).

**Proposition 19.2.9 (Composition d’homomorphismes)**
Soit \( f : E \to F \) et \( g : F \to G \) deux morphismes de trucs. Alors \( g \circ f \) est un morphisme de trucs.

**Terminologie 19.2.10**
* Un isomorphisme de trucs est un homomorphisme de truc bijectif.
* Un endomorphisme de truc est un homomorphisme de truc de \( E \) dans lui-même.
* Un automorphisme de truc est un endomorphisme qui est également un isomorphisme.

**Proposition 19.2.11**
Si \( f : E \to F \) est un isomorphisme de trucs, alors \( f^{-1} \) est un isomorphisme de trucs.

## III Groupes

### III.1 Axiomatique de la structure groupes

**Définition 19.3.1 (Groupe)**
Soit \( G \) un ensemble. On dit que \( G \) est muni d’une structure de groupe si \( G \) est muni d’une loi de composition \( \star \) telle que :
* \( \star \) est associative ;
* il existe un élément neutre \( e \) pour la loi \( \star \) ;
* tout élément \( x \) admet un symétrique \( x^s \).

**Proposition 19.3.2 (Unicité du neutre et des symétriques)**
Soit \( (G, \star) \) un groupe. Alors :
* \( G \) admet un unique élément neutre pour \( \star \)
* Pour tout \( x \in G \), il existe un unique symétrique \( x^s \) de \( x \).

**Corollaire 19.3.3 (régularité des éléments d’un groupe)**
Tous les éléments d’un groupe sont réguliers pour la loi du groupe.

**Définition 19.3.4 (Groupe abélien ou commutatif)**
On dit qu’un groupe \( (G, \star) \) est abélien (ou commutatif) si la loi de \( G \) est commutative.

**Notation 19.3.5 (Notation additive, notation multiplicative)**
* loi multiplicative : \( x \times \dots \times x \) (avec \( n \) occurrences) est noté \( x^n \); le neutre est noté 1 ; par convention, \( x^0 = 1 \);
* loi additive : \( x + \dots + x \) (avec \( n \) occurrences) est noté \( n \cdot x \) ou \( nx \); le neutre est noté 0 ; par convention \( 0x = 0 \).

**Notation 19.3.6 (Simplifications d’écriture pour la notation additive)**
Soit \( (G, +) \) un groupe commutatif. L’opposé d’un élément \( x \) est noté \( -x \). On note alors \( x - y \) au lieu de \( x + (-y) \).
* \( \forall(x, y, z) \in G^3, x - (y + z) = x - y - z \)
* \( \forall(x, y, z) \in G^3, x - (y - z) = x - y + z \).

**Définition 19.3.7 (Homomorphisme de groupes)**
Soit \( (G, \star) \) et \( (H, \diamond) \) deux groupes.
* On dit qu’une application \( f : G \to H \) est un homomorphisme de groupes si pour tout \( (x, y) \in G, f(x \star y) = f(x) \diamond f(y) \). On note \( \text{Hom}(G, H) \) l’ensemble des homomorphismes de \( G \) dans \( H \).
* Un homomorphisme bijectif est appelé isomorphisme.
* Un endomorphisme bijectif est appelé automorphisme. On note \( \text{Aut}(G) \) l’ensemble des automorphismes de \( G \).

**Proposition 19.3.8 (Image du neutre par un morphisme)**
Soit \( f : G \to H \) un morphisme de groupes. Alors \( f(e_G) = e_H \).

**Proposition 19.3.9 (Image par un morphisme d’un inverse)**
Soit \( G, H \) deux groupes (notés multiplicativement), et \( f \) un morphisme de \( G \) dans \( H \). Alors \( f(x^{-1}) = f(x)^{-1} \).

**Proposition 19.3.10 (Structure de (\( \text{Aut}(G), \circ \)))**
Soit \( G \) un groupe. Alors, \( (\text{Aut}(G), \circ) \) est un groupe.

### III.3 Sous-groupes

**Définition 19.3.12 (Sous-groupe)**
Soit \( (G, \star) \) un groupe. Un sous-ensemble \( H \) de \( G \) est appelé sous-groupe de \( G \) si \( H \) est stable pour la loi de \( G \) et si la loi induite définit sur \( H \) une structure de groupe.

**Proposition 19.3.13 (Appartenance de l’élément neutre à \( H \))**
Soit \( H \) un sous-groupe de \( G \). Alors l’élément neutre \( e \) de \( G \) est dans \( H \) et est l’élément neutre du groupe \( H \).

**Théorème 19.3.14 (Caractérisation des sous-groupes)**
Un sous-ensemble \( H \) d’un groupe \( (G, \star) \) est un sous-groupe de \( G \) si et seulement si :
(i) \( H \) est non vide,
(ii) \( H \) est stable pour \( \star : \forall(x, y) \in H^2, x \star y \in H \),
(iii) \( H \) est stable par prise de symétrique : \( \forall x \in H, x^s \in H \).

**Théorème 19.3.15 (Caractérisation, version condensée)**
\( H \subset G \) est un sous-groupe ssi :
(i) \( H \) est non vide,
(ii) \( \forall(x, y) \in H^2, x \star y^s \in H \).

**Proposition 19.3.18 (Intersection de sous-groupes)**
Soit \( G \) un groupe, et \( (H_i)_{i \in I} \) une famille de sous-groupes de \( G \). Alors \( \bigcap_{i \in I} H_i \) est un sous-groupe de \( G \).

**Définition 19.3.21 (Noyau)**
Le noyau de \( f \in \text{Hom}(G, H) \) est le sous-groupe de \( G \) défini par :
\[ \text{Ker}(f) = f^{-1}(\{e_H\}) = \{y \in G \mid f(y) = e_H \}. \]

**Théorème 19.3.22 (Caractérisation de l’injectivité)**
Soit \( f \in \text{Hom}(G, H) \). Le morphisme \( f \) est injectif si et seulement si \( \text{Ker}(f) = \{e_G\} \).

### III.4 Sous-groupes engendrés par une partie, sous-groupes monogènes

**Définition 19.3.25 (Sous-groupe engendré par une partie)**
Soit \( (G, \times) \) un groupe, et \( X \) une partie de \( G \). Le sous-groupe \( \langle X \rangle \) de \( G \) engendré par \( X \) est le plus petit sous-groupe de \( G \) contenant \( X \).

**Définition 19.3.28 (Sous-groupe monogène)**
1. Si \( X = \{x\} \), \( \langle x \rangle \) est appelé sous-groupe monogène engendré par \( x \).
2. Concrètement : \( \langle x \rangle = \{x^n, n \in \mathbb{Z}\} \) (notation multiplicative) ou \( \{nx, n \in \mathbb{Z}\} \) (notation additive).
5. Un groupe est dit cyclique s’il est monogène et fini.

### III.6 Congruences modulo un sous-groupe

**Définition 19.3.34 (Classes à droite et à gauche modulo \( H \))**
* Les classes à droite modulo \( H \) sont les ensembles \( Ha, a \in G \).
* Les classes à gauche modulo \( H \) sont les ensembles \( aH, a \in G \).

**Théorème 19.3.40 (Lagrange, Spé)**
Soit \( G \) un groupe fini, et \( H \) un sous-groupe de \( G \). Alors l’ordre de \( H \) divise l’ordre de \( G \).

**Proposition/Définition 19.3.43 (Sous-groupe distingué, HP)**
Un sous-groupe \( H \) est dit distingué (ou normal) si :
\[ \forall a \in G, aH = Ha \quad \iff \quad \forall a \in G, \forall h \in H, aha^{-1} \in H. \]

## IV Anneaux et corps

### IV.1 Axiomatiques de la structure d’anneau

**Définition 19.4.1 (Anneau)**
\( (A, +, \times) \) est un anneau si :
(i) \( (A, +) \) est un groupe abélien ;
(ii) \( (A, \times) \) est un monoïde (associative avec neutre 1) ;
(iii) \( \times \) est distributive sur \( + \).

**Théorème 19.4.17 (Formule du binôme)**
Soit \( a \) et \( b \) deux éléments d’un anneau tels que \( ab = ba \). Alors, pour tout \( n \in \mathbb{N} \),
\[ (a + b)^n = \sum_{k=0}^n \begin{pmatrix} n \\ k \end{pmatrix} a^k b^{n-k}. \]

**Définition 19.4.23 (anneau intègre, HP)**
Un anneau intègre \( A \) est un anneau commutatif non réduit à \( \{0\} \) et sans diviseur de 0 (c’est-à-dire \( ab = 0 \implies a = 0 \text{ ou } b = 0 \)).

### IV.5 Corps

**Définition 19.4.26 (Corps)**
On dit que \( (K, +, \times) \) est un corps si \( K \) est un anneau commutatif tel que \( (K \setminus \{0\}, \times) \) soit un groupe.

**Théorème 19.4.29 (Le corps \( \mathbb{F}_p \))**
L’anneau \( (\mathbb{Z}/p\mathbb{Z}, +, \times) \) est un corps si et seulement si \( p \) est premier.

**Théorème 19.4.40 (Primalité de la caractéristique d’un corps)**
Soit \( K \) un corps de caractéristique non nulle. Alors sa caractéristique \( p \) est un nombre premier.

