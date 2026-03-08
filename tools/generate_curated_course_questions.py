from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "cours"
PROGRAMME_PATH = ROOT / "data" / "programme.json"
OUTPUT_DIR = ROOT / "data" / "questions_de_cours_curated"


def make_question(
    course_id: str,
    index: int,
    qtype: str,
    difficulty: int,
    question_latex: str,
    programme_notion: str,
    answer_latex: str,
) -> dict:
    return {
        "id": f"{course_id}__qc_{index:03d}",
        "type": qtype,
        "difficulty": difficulty,
        "question_latex": question_latex,
        "programme_notion": programme_notion,
        "answer_node_id": f"{course_id}__curated_{index:03d}",
        "answer_latex": answer_latex,
        "tags": ["curated", "qualite", "chapitre de cours"],
    }


COURSE_QUESTIONS = {
    "rudiments_de_logique_et_vocabulaire_ensembliste": [
        make_question(
            "rudiments_de_logique_et_vocabulaire_ensembliste",
            1,
            "definition",
            1,
            "Énoncer les règles de négation d'une proposition quantifiée.",
            "Négation d'une proposition avec quantificateurs",
            "Pour toute propriété $\\mathscr P$, on a :\\par "
            "$\\neg(\\forall x\\in E,\\ \\mathscr P(x))\\iff \\exists x\\in E,\\ \\neg\\mathscr P(x)$\\par "
            "et $\\neg(\\exists x\\in E,\\ \\mathscr P(x))\\iff \\forall x\\in E,\\ \\neg\\mathscr P(x)$.",
        ),
        make_question(
            "rudiments_de_logique_et_vocabulaire_ensembliste",
            2,
            "enonce",
            2,
            "Énoncer le principe de récurrence simple sur $\\mathbb N$.",
            "Raisonnement par récurrence",
            "Soit $\\mathscr P(n)$ une proposition dépendant de $n\\in\\mathbb N$. "
            "Si l'on montre d'une part l'initialisation, c'est-à-dire que $\\mathscr P(n_0)$ est vraie pour un certain rang initial $n_0$, "
            "et d'autre part l'hérédité, c'est-à-dire "
            "$\\forall n\\ge n_0,\\ \\mathscr P(n)\\Rightarrow \\mathscr P(n+1)$, "
            "alors $\\mathscr P(n)$ est vraie pour tout $n\\ge n_0$.",
        ),
    ],
    "relations_binaires_et_applications": [
        make_question(
            "relations_binaires_et_applications",
            1,
            "definition",
            1,
            "Définir une application injective, surjective et bijective.",
            "Injection, surjection, bijection",
            "Soit $f:E\\to F$.\\par "
            "$f$ est injective si $\\forall x,y\\in E$, $f(x)=f(y)\\Rightarrow x=y$.\\par "
            "$f$ est surjective si $\\forall y\\in F$, $\\exists x\\in E$ tel que $f(x)=y$.\\par "
            "$f$ est bijective si elle est à la fois injective et surjective.",
        ),
        make_question(
            "relations_binaires_et_applications",
            2,
            "enonce",
            2,
            "Énoncer la caractérisation d'une bijection par l'existence d'une application réciproque.",
            "Bijection réciproque",
            "Une application $f:E\\to F$ est bijective si et seulement si il existe une application "
            "$g:F\\to E$ telle que $g\\circ f=\\operatorname{Id}_E$ et $f\\circ g=\\operatorname{Id}_F$. "
            "Cette application $g$ est alors unique et s'appelle la réciproque de $f$, notée $f^{-1}$.",
        ),
    ],
    "calculs_algebriques_dans_R": [
        make_question(
            "calculs_algebriques_dans_R",
            1,
            "enonce",
            1,
            "Énoncer la formule du binôme de Newton.",
            "Formule du binôme de Newton",
            "Pour tout $n\\in\\mathbb N$ et tous $a,b\\in\\mathbb R$,\\par "
            "$$(a+b)^n=\\sum_{k=0}^n \\binom{n}{k}a^{n-k}b^k.$$",
        ),
        make_question(
            "calculs_algebriques_dans_R",
            2,
            "enonce",
            2,
            "Énoncer les formules d'addition pour le sinus, le cosinus et la tangente.",
            "Formules d'addition trigonométriques",
            "Pour tous réels $a,b$ tels que les expressions aient un sens,\\par "
            "$\\sin(a+b)=\\sin a\\cos b+\\cos a\\sin b$,\\par "
            "$\\cos(a+b)=\\cos a\\cos b-\\sin a\\sin b$,\\par "
            "$\\tan(a+b)=\\dfrac{\\tan a+\\tan b}{1-\\tan a\\tan b}$.",
        ),
    ],
    "nombres_complexes": [
        make_question(
            "nombres_complexes",
            1,
            "definition",
            1,
            "Définir le conjugué et le module d'un nombre complexe.",
            "Conjugaison et module",
            "Si $z=x+iy$ avec $(x,y)\\in\\mathbb R^2$, le conjugué de $z$ est "
            "$\\overline z=x-iy$ et son module est $|z|=\\sqrt{x^2+y^2}$. "
            "On a en particulier $z\\overline z=|z|^2$.",
        ),
        make_question(
            "nombres_complexes",
            2,
            "enonce",
            2,
            "Énoncer la forme des racines $n$-ièmes d'un complexe non nul.",
            "Racines n-ièmes d'un complexe",
            "Si $a=\\rho e^{i\\theta}$ avec $\\rho>0$ et $n\\ge1$, les racines $n$-ièmes de $a$ sont\\par "
            "$$z_k=\\rho^{1/n}e^{i(\\theta+2k\\pi)/n},\\qquad k=0,1,\\dots,n-1.$$ "
            "Elles sont deux à deux distinctes et réparties régulièrement sur un cercle de centre $0$.",
        ),
    ],
    "rappels_et_complements_sur_les_fonctions_reelles": [
        make_question(
            "rappels_et_complements_sur_les_fonctions_reelles",
            1,
            "definition",
            1,
            "Définir la parité, l'imparité et la périodicité d'une fonction.",
            "Parité, imparité, périodicité",
            "Soit $f:E\\to\\mathbb R$ avec $E$ stable par opposition.\\par "
            "$f$ est paire si $\\forall x\\in E$, $f(-x)=f(x)$.\\par "
            "$f$ est impaire si $\\forall x\\in E$, $f(-x)=-f(x)$.\\par "
            "Si $T>0$ et si $E$ est stable par translation de vecteur $T$, on dit que $f$ est $T$-périodique si "
            "$\\forall x\\in E$, $f(x+T)=f(x)$.",
        ),
        make_question(
            "rappels_et_complements_sur_les_fonctions_reelles",
            2,
            "definition",
            2,
            "Définir le maximum et le minimum d'une fonction sur un ensemble.",
            "Maximum et minimum",
            "Soit $f:E\\to\\mathbb R$ et $a\\in E$.\\par "
            "$f(a)$ est le maximum de $f$ sur $E$ si $\\forall x\\in E$, $f(x)\\le f(a)$.\\par "
            "$f(a)$ est le minimum de $f$ sur $E$ si $\\forall x\\in E$, $f(x)\\ge f(a)$.\\par "
            "Un extremum est donc une valeur de la fonction qui est à la fois atteinte et extrémale.",
        ),
    ],
    "techniques_elementaires_de_calcul_integral": [
        make_question(
            "techniques_elementaires_de_calcul_integral",
            1,
            "enonce",
            2,
            "Énoncer la formule d'intégration par parties sur un segment.",
            "Intégration par parties",
            "Si $u$ et $v$ sont de classe $\\mathcal C^1$ sur $[a,b]$, alors\\par "
            "$$\\int_a^b u(t)v'(t)\\,dt=[u(t)v(t)]_a^b-\\int_a^b u'(t)v(t)\\,dt.$$",
        ),
        make_question(
            "techniques_elementaires_de_calcul_integral",
            2,
            "enonce",
            2,
            "Énoncer la formule de changement de variable dans une intégrale sur un segment.",
            "Changement de variable",
            "Si $\\varphi:[\\alpha,\\beta]\\to[a,b]$ est de classe $\\mathcal C^1$, bijective et monotone, "
            "et si $f$ est continue sur $[a,b]$, alors\\par "
            "$$\\int_a^b f(x)\\,dx=\\int_\\alpha^\\beta f(\\varphi(t))\\varphi'(t)\\,dt.$$",
        ),
    ],
    "equations_differentielles_lineaires": [
        make_question(
            "equations_differentielles_lineaires",
            1,
            "enonce",
            2,
            "Énoncer la forme générale des solutions de $y'+a(x)y=b(x)$ sur un intervalle.",
            "Équation différentielle linéaire du premier ordre",
            "Si $a$ et $b$ sont continues sur un intervalle $I$, alors l'équation "
            "$y'+a(x)y=b(x)$ admet sur $I$ une unique solution pour toute condition initiale. "
            "En posant $A$ une primitive de $a$, on obtient\\par "
            "$$(e^{A}y)'=be^{A},\\qquad y(x)=e^{-A(x)}\\left(C+\\int_{x_0}^x b(t)e^{A(t)}\\,dt\\right).$$",
        ),
        make_question(
            "equations_differentielles_lineaires",
            2,
            "enonce",
            3,
            "Énoncer les formes des solutions de $y''+ay'+by=0$ à coefficients constants réels.",
            "Équation linéaire d'ordre 2 à coefficients constants",
            "On considère le polynôme caractéristique $r^2+ar+b$.\\par "
            "Si ses racines sont réelles distinctes $r_1,r_2$, alors les solutions sont "
            "$y(x)=\\lambda e^{r_1x}+\\mu e^{r_2x}$.\\par "
            "Si la racine réelle $r$ est double, alors "
            "$y(x)=(\\lambda+\\mu x)e^{rx}$.\\par "
            "Si les racines sont complexes conjuguées $\\alpha\\pm i\\beta$ avec $\\beta\\ne0$, alors "
            "$y(x)=e^{\\alpha x}(\\lambda\\cos(\\beta x)+\\mu\\sin(\\beta x))$.",
        ),
    ],
    "topologie_de_r_et_c": [
        make_question(
            "topologie_de_r_et_c",
            1,
            "definition",
            1,
            "Définir l'adhérence d'une partie d'un espace métrique.",
            "Adhérence",
            "L'adhérence d'une partie $A$ est l'ensemble des points $x$ tels que tout voisinage de $x$ rencontre $A$. "
            "De manière équivalente, $x\\in\\overline A$ si et seulement si il existe une suite d'éléments de $A$ qui converge vers $x$.",
        ),
        make_question(
            "topologie_de_r_et_c",
            2,
            "enonce",
            2,
            "Énoncer le théorème de Bolzano-Weierstrass dans $\\mathbb R^n$ ou $\\mathbb C$.",
            "Compacité séquentielle",
            "Toute suite bornée de $\\mathbb R^n$ admet une sous-suite convergente. "
            "En particulier, toute suite bornée de $\\mathbb C$ admet une sous-suite convergente.",
        ),
    ],
    "suites_reelles": [
        make_question(
            "suites_reelles",
            1,
            "definition",
            1,
            "Définir la convergence d'une suite réelle vers un réel $\\ell$.",
            "Convergence d'une suite",
            "La suite réelle $(u_n)$ converge vers $\\ell\\in\\mathbb R$ si "
            "$\\forall \\varepsilon>0$, $\\exists N\\in\\mathbb N$ tel que "
            "$\\forall n\\ge N$, $|u_n-\\ell|<\\varepsilon$.",
        ),
        make_question(
            "suites_reelles",
            2,
            "enonce",
            2,
            "Énoncer le théorème de convergence monotone pour les suites réelles.",
            "Suites monotones",
            "Toute suite réelle croissante et majorée converge dans $\\mathbb R$. "
            "Toute suite réelle décroissante et minorée converge dans $\\mathbb R$.",
        ),
    ],
    "limites_et_continuite": [
        make_question(
            "limites_et_continuite",
            1,
            "definition",
            1,
            "Définir la continuité d'une fonction en un point.",
            "Continuité en un point",
            "Soit $f:E\\to\\mathbb R$ et $a\\in E$ adhérent à $E$. "
            "La fonction $f$ est continue en $a$ si $\\lim_{x\\to a}f(x)=f(a)$.",
        ),
        make_question(
            "limites_et_continuite",
            2,
            "enonce",
            2,
            "Énoncer le théorème des valeurs intermédiaires.",
            "Théorème des valeurs intermédiaires",
            "Si $f$ est continue sur un intervalle $I$, alors pour tous $a,b\\in I$ avec $a<b$ et tout réel "
            "$y$ compris entre $f(a)$ et $f(b)$, il existe $c\\in[a,b]$ tel que $f(c)=y$. "
            "En particulier, si $f(a)f(b)<0$, il existe $c\\in(a,b)$ tel que $f(c)=0$.",
        ),
    ],
    "derivabilite_et_convexite": [
        make_question(
            "derivabilite_et_convexite",
            1,
            "enonce",
            2,
            "Énoncer le théorème de Rolle et l'inégalité des accroissements finis.",
            "Rolle et accroissements finis",
            "Si $f$ est continue sur $[a,b]$, dérivable sur $]a,b[$ et vérifie $f(a)=f(b)$, "
            "alors il existe $c\\in]a,b[$ tel que $f'(c)=0$.\\par "
            "Si $f$ est continue sur $[a,b]$ et dérivable sur $]a,b[$, alors il existe $c\\in]a,b[$ tel que "
            "$f(b)-f(a)=f'(c)(b-a)$.",
        ),
        make_question(
            "derivabilite_et_convexite",
            2,
            "enonce",
            2,
            "Donner une caractérisation d'une fonction convexe dérivable sur un intervalle.",
            "Convexité",
            "Si $f$ est dérivable sur un intervalle $I$, alors $f$ est convexe sur $I$ si et seulement si $f'$ est croissante sur $I$. "
            "Équivalemment, pour tous $x,a\\in I$, on a "
            "$f(x)\\ge f(a)+f'(a)(x-a)$, c'est-à-dire que le graphe est au-dessus de chacune de ses tangentes.",
        ),
    ],
    "arithmetique_des_entiers": [
        make_question(
            "arithmetique_des_entiers",
            1,
            "enonce",
            1,
            "Énoncer le théorème de division euclidienne dans $\\mathbb Z$.",
            "Division euclidienne",
            "Pour tous entiers $a\\in\\mathbb Z$ et $b\\in\\mathbb N^*$, il existe un unique couple "
            "$(q,r)\\in\\mathbb Z\\times\\mathbb N$ tel que $a=bq+r$ et $0\\le r<b$.",
        ),
        make_question(
            "arithmetique_des_entiers",
            2,
            "enonce",
            2,
            "Énoncer le théorème de Bézout et le critère de coprimalité associé.",
            "Bézout",
            "Pour tous entiers $a,b$ non tous deux nuls, il existe des entiers $u,v$ tels que "
            "$au+bv=\\gcd(a,b)$. En particulier, $a$ et $b$ sont premiers entre eux si et seulement si il existe "
            "$u,v\\in\\mathbb Z$ tels que $au+bv=1$.",
        ),
    ],
    "groupes_et_anneaux": [
        make_question(
            "groupes_et_anneaux",
            1,
            "enonce",
            1,
            "Énoncer le critère de sous-groupe.",
            "Sous-groupe",
            "Une partie non vide $H$ d'un groupe $G$ est un sous-groupe de $G$ si et seulement si "
            "$\\forall x,y\\in H$, $xy^{-1}\\in H$. "
            "Dans le cas additif, cela s'écrit : $\\forall x,y\\in H$, $x-y\\in H$.",
        ),
        make_question(
            "groupes_et_anneaux",
            2,
            "enonce",
            2,
            "Énoncer les propriétés du noyau et de l'image d'un morphisme de groupes.",
            "Morphisme de groupes",
            "Si $f:G\\to H$ est un morphisme de groupes, alors son noyau "
            "$\\ker f=\\{x\\in G\\mid f(x)=e_H\\}$ est un sous-groupe distingué de $G$ et son image "
            "$\\operatorname{Im}f=f(G)$ est un sous-groupe de $H$. "
            "De plus, $f$ est injectif si et seulement si $\\ker f=\\{e_G\\}$.",
        ),
    ],
    "matrices_et_systemes_lineaires": [
        make_question(
            "matrices_et_systemes_lineaires",
            1,
            "enonce",
            2,
            "Énoncer des critères équivalents d'inversibilité d'une matrice carrée.",
            "Inversibilité d'une matrice",
            "Pour $A\\in\\mathcal M_n(\\mathbb K)$, les propriétés suivantes sont équivalentes :\\par "
            "$A$ est inversible ; le système $AX=B$ admet une solution unique pour tout $B$ ; "
            "$AX=0$ n'admet que la solution nulle ; les colonnes de $A$ forment une base de $\\mathbb K^n$ ; "
            "les lignes de $A$ forment une base de $\\mathbb K^n$.",
        ),
        make_question(
            "matrices_et_systemes_lineaires",
            2,
            "enonce",
            2,
            "Énoncer le principe du pivot de Gauss pour résoudre un système linéaire.",
            "Pivot de Gauss",
            "Les opérations élémentaires sur les lignes d'une matrice augmentée conservent l'ensemble des solutions du système associé. "
            "En échelonnant la matrice, on ramène donc la résolution d'un système linéaire à une lecture directe par remontée.",
        ),
    ],
    "polynomes_et_racines": [
        make_question(
            "polynomes_et_racines",
            1,
            "enonce",
            1,
            "Énoncer le théorème de factorisation par une racine.",
            "Racine d'un polynôme",
            "Soit $P\\in\\mathbb K[X]$ et $a\\in\\mathbb K$. Alors $a$ est racine de $P$ si et seulement si "
            "$(X-a)$ divise $P$. Plus généralement, $a$ est racine de multiplicité $m$ si et seulement si "
            "$(X-a)^m$ divise $P$ et $(X-a)^{m+1}$ ne divise pas $P$.",
        ),
        make_question(
            "polynomes_et_racines",
            2,
            "enonce",
            2,
            "Énoncer le théorème de d'Alembert-Gauss et sa conséquence pour les polynômes réels.",
            "Racines complexes et conjugaison",
            "Tout polynôme non constant à coefficients complexes admet au moins une racine complexe ; par conséquent, "
            "un polynôme de degré $n$ se scinde sur $\\mathbb C$ en produit de $n$ facteurs du premier degré, comptés avec multiplicité. "
            "Si les coefficients sont réels, toute racine complexe non réelle apparaît avec sa conjuguée et de même multiplicité.",
        ),
    ],
    "arithmetique_des_polynomes_et_fractions_rationnelles": [
        make_question(
            "arithmetique_des_polynomes_et_fractions_rationnelles",
            1,
            "enonce",
            2,
            "Énoncer le théorème de division euclidienne dans $\\mathbb K[X]$.",
            "Division euclidienne dans K[X]",
            "Pour tous polynômes $A,B\\in\\mathbb K[X]$ avec $B\\neq0$, il existe un unique couple $(Q,R)$ de polynômes tel que "
            "$A=BQ+R$ et $\\deg R<\\deg B$ ou $R=0$.",
        ),
        make_question(
            "arithmetique_des_polynomes_et_fractions_rationnelles",
            2,
            "enonce",
            2,
            "Énoncer le théorème de Bézout dans $\\mathbb K[X]$.",
            "Bézout dans K[X]",
            "Si $A,B\\in\\mathbb K[X]$ ne sont pas tous deux nuls et si $D$ est leur pgcd unitaire, alors il existe "
            "$U,V\\in\\mathbb K[X]$ tels que $AU+BV=D$. En particulier, $A$ et $B$ sont premiers entre eux si et seulement si "
            "il existe $U,V\\in\\mathbb K[X]$ tels que $AU+BV=1$.",
        ),
    ],
    "analyse_asymptotique_de_niveau_1": [
        make_question(
            "analyse_asymptotique_de_niveau_1",
            1,
            "definition",
            1,
            "Définir les notations $o$, $O$ et l'équivalence asymptotique.",
            "Petits o, grands O, équivalents",
            "Au voisinage d'un point $a$, on écrit $f=o(g)$ si $\\dfrac{f}{g}\\to0$ lorsque ce quotient a un sens localement.\\par "
            "On écrit $f=O(g)$ s'il existe un voisinage de $a$ et une constante $C>0$ tels que $|f|\\le C|g|$ sur ce voisinage.\\par "
            "On écrit $f\\sim g$ si $\\dfrac{f}{g}\\to1$.",
        ),
        make_question(
            "analyse_asymptotique_de_niveau_1",
            2,
            "enonce",
            2,
            "Énoncer les croissances comparées usuelles en $+\\infty$.",
            "Croissances comparées",
            "Pour tous $\\alpha>0$, $\\beta\\in\\mathbb R$ et $a>1$, lorsque $x\\to+\\infty$, on a\\par "
            "$$(\\ln x)^\\beta=o(x^\\alpha)\\qquad\\text{et}\\qquad x^\\alpha=o(a^x).$$",
        ),
    ],
    "analyse_asymptotique_de_niveau_2": [
        make_question(
            "analyse_asymptotique_de_niveau_2",
            1,
            "definition",
            2,
            "Définir un développement limité d'ordre $n$ en un point $a$.",
            "Développement limité",
            "On dit que $f$ admet en $a$ un développement limité d'ordre $n$ s'il existe des réels "
            "$c_0,\\dots,c_n$ tels que\\par "
            "$$f(x)=c_0+c_1(x-a)+\\cdots+c_n(x-a)^n+o((x-a)^n)\\quad (x\\to a).$$",
        ),
        make_question(
            "analyse_asymptotique_de_niveau_2",
            2,
            "enonce",
            3,
            "Énoncer la formule de Taylor-Young à l'ordre $n$ en un point $a$.",
            "Taylor-Young",
            "Si $f$ est de classe $\\mathcal C^n$ au voisinage de $a$, alors\\par "
            "$$f(x)=\\sum_{k=0}^n \\frac{f^{(k)}(a)}{k!}(x-a)^k+o((x-a)^n)\\quad (x\\to a).$$",
        ),
    ],
    "espaces_vectoriels": [
        make_question(
            "espaces_vectoriels",
            1,
            "definition",
            1,
            "Définir une famille libre, une famille génératrice et une base.",
            "Liberté, génération, base",
            "Une famille $(x_i)_{i\\in I}$ est libre si toute combinaison linéaire finie nulle est triviale. "
            "Elle est génératrice de $E$ si tout vecteur de $E$ est combinaison linéaire finie des $x_i$. "
            "Une base est une famille à la fois libre et génératrice.",
        ),
        make_question(
            "espaces_vectoriels",
            2,
            "enonce",
            2,
            "Énoncer le théorème de la base incomplète en dimension finie.",
            "Base incomplète",
            "Dans un espace vectoriel de dimension finie, toute famille libre peut être complétée en une base et toute famille génératrice contient une base extraite de cette famille.",
        ),
    ],
    "applications_lineaires": [
        make_question(
            "applications_lineaires",
            1,
            "definition",
            1,
            "Définir le noyau et l'image d'une application linéaire.",
            "Noyau et image",
            "Si $u:E\\to F$ est linéaire, son noyau est "
            "$\\ker u=\\{x\\in E\\mid u(x)=0\\}$ et son image est "
            "$\\operatorname{Im}u=u(E)=\\{u(x)\\mid x\\in E\\}$. "
            "Ce sont des sous-espaces vectoriels de $E$ et de $F$ respectivement.",
        ),
        make_question(
            "applications_lineaires",
            2,
            "enonce",
            2,
            "Énoncer le théorème du rang.",
            "Théorème du rang",
            "Si $E$ est de dimension finie et $u:E\\to F$ est linéaire, alors\\par "
            "$$\\dim E=\\dim(\\ker u)+\\dim(\\operatorname{Im}u).$$",
        ),
    ],
    "representation_matricielle_applications_lineaires": [
        make_question(
            "representation_matricielle_applications_lineaires",
            1,
            "definition",
            2,
            "Définir la matrice d'une application linéaire dans deux bases données.",
            "Matrice d'une application linéaire",
            "Si $u:E\\to F$, $\\mathcal B=(e_1,\\dots,e_n)$ est une base de $E$ et "
            "$\\mathcal C=(f_1,\\dots,f_p)$ une base de $F$, la matrice de $u$ dans ces bases est l'unique matrice "
            "$A=(a_{ij})\\in\\mathcal M_{p,n}(\\mathbb K)$ telle que pour tout $j$, "
            "$u(e_j)=\\sum_{i=1}^p a_{ij}f_i$.",
        ),
        make_question(
            "representation_matricielle_applications_lineaires",
            2,
            "enonce",
            3,
            "Énoncer la formule de changement de base pour la matrice d'un endomorphisme.",
            "Changement de base",
            "Si $u\\in\\mathcal L(E)$ et si $A=[u]_{\\mathcal B}$, $A'=[u]_{\\mathcal B'}$, alors\\par "
            "$$A'=P^{-1}AP,$$ "
            "où $P$ est la matrice de passage de la base $\\mathcal B'$ vers la base $\\mathcal B$. "
            "Les matrices $A$ et $A'$ sont donc semblables.",
        ),
    ],
    "determinants": [
        make_question(
            "determinants",
            1,
            "enonce",
            2,
            "Énoncer les propriétés fondamentales du déterminant.",
            "Déterminant",
            "Le déterminant est l'unique forme multilinéaire alternée des colonnes sur $\\mathcal M_n(\\mathbb K)$ "
            "qui vaut $1$ sur l'identité. Il vérifie en particulier "
            "$\\det(AB)=\\det(A)\\det(B)$ et $\\det(A^\\top)=\\det(A)$.",
        ),
        make_question(
            "determinants",
            2,
            "enonce",
            2,
            "Énoncer le critère d'inversibilité par le déterminant.",
            "Inversibilité et déterminant",
            "Une matrice carrée $A\\in\\mathcal M_n(\\mathbb K)$ est inversible si et seulement si "
            "$\\det(A)\\ne0$.",
        ),
    ],
    "denombrement": [
        make_question(
            "denombrement",
            1,
            "enonce",
            1,
            "Énoncer la formule donnant le nombre de parties à $k$ éléments d'un ensemble à $n$ éléments.",
            "Coefficient binomial",
            "Le nombre de parties à $k$ éléments d'un ensemble à $n$ éléments est le coefficient binomial\\par "
            "$$\\binom nk=\\frac{n!}{k!(n-k)!}$$ "
            "pour $0\\le k\\le n$.",
        ),
        make_question(
            "denombrement",
            2,
            "enonce",
            2,
            "Énoncer la formule d'inclusion-exclusion pour deux et trois ensembles finis.",
            "Inclusion-exclusion",
            "Pour deux ensembles finis $A,B$,\\par "
            "$$|A\\cup B|=|A|+|B|-|A\\cap B|.$$\\par "
            "Pour trois ensembles finis $A,B,C$,\\par "
            "$$|A\\cup B\\cup C|=|A|+|B|+|C|-|A\\cap B|-|A\\cap C|-|B\\cap C|+|A\\cap B\\cap C|.$$",
        ),
    ],
    "probabilites_sur_un_univers_fini": [
        make_question(
            "probabilites_sur_un_univers_fini",
            1,
            "enonce",
            2,
            "Énoncer la formule des probabilités totales et la formule de Bayes.",
            "Probabilités totales et Bayes",
            "Si $(A_i)_{i=1}^n$ est un système complet d'événements avec $P(A_i)>0$, alors pour tout événement $B$,\\par "
            "$$P(B)=\\sum_{i=1}^n P(B\\mid A_i)P(A_i).$$\\par "
            "Si de plus $P(B)>0$, alors\\par "
            "$$P(A_k\\mid B)=\\frac{P(B\\mid A_k)P(A_k)}{\\sum_{i=1}^n P(B\\mid A_i)P(A_i)}.$$",
        ),
        make_question(
            "probabilites_sur_un_univers_fini",
            2,
            "definition",
            2,
            "Définir l'indépendance de deux événements.",
            "Indépendance",
            "Deux événements $A$ et $B$ sont indépendants si "
            "$P(A\\cap B)=P(A)P(B)$. Si $P(B)>0$, cela équivaut à $P(A\\mid B)=P(A)$.",
        ),
    ],
    "complements_probabilistes": [
        make_question(
            "complements_probabilistes",
            1,
            "definition",
            2,
            "Définir l'espérance et la variance d'une variable aléatoire réelle discrète finie.",
            "Espérance et variance",
            "Si $X$ prend un nombre fini de valeurs $(x_i)$ avec probabilités $(p_i)$, alors\\par "
            "$$E(X)=\\sum_i x_ip_i,\\qquad V(X)=E\\bigl((X-E(X))^2\\bigr)=E(X^2)-E(X)^2.$$",
        ),
        make_question(
            "complements_probabilistes",
            2,
            "enonce",
            3,
            "Énoncer l'inégalité de Bienaymé-Tchebychev.",
            "Inégalité de Bienaymé-Tchebychev",
            "Si $X$ admet une variance finie, alors pour tout $\\varepsilon>0$,\\par "
            "$$P\\bigl(|X-E(X)|\\ge\\varepsilon\\bigr)\\le \\frac{V(X)}{\\varepsilon^2}.$$",
        ),
    ],
    "espaces_prehilbertiens_reels": [
        make_question(
            "espaces_prehilbertiens_reels",
            1,
            "enonce",
            2,
            "Énoncer l'inégalité de Cauchy-Schwarz.",
            "Cauchy-Schwarz",
            "Dans un espace préhilbertien réel, pour tous $x,y$,\\par "
            "$$|\\langle x,y\\rangle|\\le \\|x\\|\\,\\|y\\|,$$ "
            "avec égalité si et seulement si $x$ et $y$ sont liés.",
        ),
        make_question(
            "espaces_prehilbertiens_reels",
            2,
            "enonce",
            3,
            "Énoncer le théorème de projection orthogonale sur un sous-espace de dimension finie.",
            "Projection orthogonale",
            "Si $F$ est un sous-espace vectoriel de dimension finie d'un espace préhilbertien réel $E$, "
            "alors tout vecteur $x\\in E$ s'écrit de façon unique "
            "$x=p_F(x)+u$ avec $p_F(x)\\in F$ et $u\\in F^\\perp$. "
            "Le vecteur $p_F(x)$ est appelé projection orthogonale de $x$ sur $F$.",
        ),
    ],
    "series_et_familles_sommables": [
        make_question(
            "series_et_familles_sommables",
            1,
            "definition",
            1,
            "Définir la convergence d'une série numérique et rappeler une condition nécessaire.",
            "Convergence d'une série",
            "La série $\\sum u_n$ converge si la suite de ses sommes partielles "
            "$S_n=\\sum_{k=0}^n u_k$ converge. Une condition nécessaire de convergence est "
            "$u_n\\to0$.",
        ),
        make_question(
            "series_et_familles_sommables",
            2,
            "enonce",
            2,
            "Énoncer le critère de comparaison pour les séries à termes positifs.",
            "Comparaison des séries positives",
            "Si $0\\le u_n\\le v_n$ à partir d'un certain rang, alors\\par "
            "si $\\sum v_n$ converge, la série $\\sum u_n$ converge ;\\par "
            "si $\\sum u_n$ diverge, la série $\\sum v_n$ diverge.",
        ),
    ],
    "fonctions_de_deux_variables": [
        make_question(
            "fonctions_de_deux_variables",
            1,
            "definition",
            2,
            "Définir la différentiabilité d'une fonction de deux variables en un point.",
            "Différentiabilité",
            "Une fonction $f:\\mathbb R^2\\to\\mathbb R$ est différentiable en $a=(a_1,a_2)$ si il existe une application linéaire "
            "$L:\\mathbb R^2\\to\\mathbb R$ telle que\\par "
            "$$f(a+h)=f(a)+L(h)+o(\\|h\\|)\\quad (h\\to0).$$ "
            "La forme linéaire $L$ est la différentielle de $f$ en $a$.",
        ),
        make_question(
            "fonctions_de_deux_variables",
            2,
            "enonce",
            3,
            "Énoncer la forme de l'équation du plan tangent au graphe d'une fonction différentiable.",
            "Plan tangent",
            "Si $f$ est différentiable en $(a,b)$, alors le graphe $z=f(x,y)$ admet en "
            "$(a,b,f(a,b))$ pour plan tangent\\par "
            "$$z=f(a,b)+\\partial_x f(a,b)(x-a)+\\partial_y f(a,b)(y-b).$$",
        ),
    ],
    "integration_sur_un_segment": [
        make_question(
            "integration_sur_un_segment",
            1,
            "enonce",
            2,
            "Énoncer les propriétés de base de l'intégrale sur un segment : linéarité, positivité, croissance.",
            "Propriétés de l'intégrale",
            "Pour des fonctions intégrables sur $[a,b]$, l'intégrale est linéaire.\\par "
            "Si $f\\ge0$ sur $[a,b]$, alors $\\int_a^b f(t)\\,dt\\ge0$.\\par "
            "Si $f\\le g$ sur $[a,b]$, alors $\\int_a^b f(t)\\,dt\\le\\int_a^b g(t)\\,dt$.",
        ),
        make_question(
            "integration_sur_un_segment",
            2,
            "enonce",
            3,
            "Énoncer le théorème fondamental de l'analyse sur un segment.",
            "Théorème fondamental de l'analyse",
            "Si $f$ est continue sur $[a,b]$ et si l'on pose "
            "$F(x)=\\int_a^x f(t)\\,dt$, alors $F$ est de classe $\\mathcal C^1$ sur $[a,b]$ et "
            "$F'(x)=f(x)$ pour tout $x\\in[a,b]$. En particulier, si $G$ est une primitive de $f$ sur $[a,b]$, alors "
            "$\\int_a^b f(t)\\,dt=G(b)-G(a)$.",
        ),
    ],
}

ADDITIONAL_COURSE_QUESTIONS = {
    "rudiments_de_logique_et_vocabulaire_ensembliste": [
        make_question(
            "rudiments_de_logique_et_vocabulaire_ensembliste",
            3,
            "definition",
            1,
            "Définir l'implication, la réciproque, la contraposée et l'équivalence de deux propositions.",
            "Connecteurs logiques élémentaires",
            "Pour deux propositions $P$ et $Q$, l'implication $P\\Rightarrow Q$ signifie que $P$ vraie entraîne $Q$ vraie. "
            "Sa réciproque est $Q\\Rightarrow P$. Sa contraposée est $\\neg Q\\Rightarrow\\neg P$. "
            "On dit que $P$ et $Q$ sont équivalentes si $P\\Rightarrow Q$ et $Q\\Rightarrow P$, ce qui se note $P\\Leftrightarrow Q$.",
        ),
        make_question(
            "rudiments_de_logique_et_vocabulaire_ensembliste",
            4,
            "enonce",
            2,
            "Énoncer le principe de récurrence forte sur $\\mathbb N$.",
            "Récurrence forte",
            "Soit $\\mathscr P(n)$ une proposition définie pour $n\\ge n_0$. "
            "Si l'on montre d'une part l'initialisation au rang $n_0$, "
            "et d'autre part que, pour tout $n\\ge n_0$, l'hypothèse "
            "$\\mathscr P(n_0),\\dots,\\mathscr P(n)$ vraie entraîne $\\mathscr P(n+1)$, "
            "alors $\\mathscr P(n)$ est vraie pour tout $n\\ge n_0$.",
        ),
    ],
    "relations_binaires_et_applications": [
        make_question(
            "relations_binaires_et_applications",
            3,
            "definition",
            2,
            "Définir une relation d'équivalence et une classe d'équivalence.",
            "Relation d'équivalence",
            "Une relation $\\mathcal R$ sur un ensemble $E$ est une relation d'équivalence si elle est réflexive, symétrique et transitive. "
            "Pour $x\\in E$, la classe d'équivalence de $x$ est "
            "$[x]=\\{y\\in E\\mid y\\mathcal R x\\}$.",
        ),
        make_question(
            "relations_binaires_et_applications",
            4,
            "enonce",
            2,
            "Énoncer les propriétés de l'image directe et de l'image réciproque pour l'union et l'intersection.",
            "Images directe et réciproque",
            "Soit $f:E\\to F$. Pour toutes parties $A,B\\subset E$ et $C,D\\subset F$, on a\\par "
            "$f(A\\cup B)=f(A)\\cup f(B)$,\\quad $f(A\\cap B)\\subset f(A)\\cap f(B)$,\\par "
            "$f^{-1}(C\\cup D)=f^{-1}(C)\\cup f^{-1}(D)$,\\quad "
            "$f^{-1}(C\\cap D)=f^{-1}(C)\\cap f^{-1}(D)$.",
        ),
    ],
    "calculs_algebriques_dans_R": [
        make_question(
            "calculs_algebriques_dans_R",
            3,
            "enonce",
            1,
            "Énoncer la formule de la somme géométrique finie.",
            "Somme géométrique",
            "Pour tout $q\\in\\mathbb R$ avec $q\\ne1$ et tout $n\\in\\mathbb N$,\\par "
            "$$\\sum_{k=0}^n q^k=\\frac{1-q^{n+1}}{1-q}.$$ "
            "Si $q=1$, la somme vaut $n+1$.",
        ),
        make_question(
            "calculs_algebriques_dans_R",
            4,
            "enonce",
            2,
            "Énoncer les formules de linéarisation de $\\cos^2 x$, $\\sin^2 x$ et $\\sin x\\cos x$.",
            "Linéarisation trigonométrique",
            "$$\\cos^2 x=\\frac{1+\\cos(2x)}{2},\\qquad "
            "\\sin^2 x=\\frac{1-\\cos(2x)}{2},\\qquad "
            "\\sin x\\cos x=\\frac{\\sin(2x)}{2}.$$",
        ),
    ],
    "nombres_complexes": [
        make_question(
            "nombres_complexes",
            3,
            "definition",
            1,
            "Définir un argument d'un complexe non nul et sa forme exponentielle.",
            "Argument et forme exponentielle",
            "Si $z\\in\\mathbb C^*$, un réel $\\theta$ est un argument de $z$ si "
            "$z=|z|(\\cos\\theta+i\\sin\\theta)$. "
            "On écrit alors aussi $z=|z|e^{i\\theta}$. "
            "Les arguments de $z$ sont définis modulo $2\\pi$.",
        ),
        make_question(
            "nombres_complexes",
            4,
            "enonce",
            2,
            "Énoncer la formule de Moivre.",
            "Formule de Moivre",
            "Pour tout $\\theta\\in\\mathbb R$ et tout $n\\in\\mathbb Z$,\\par "
            "$$(\\cos\\theta+i\\sin\\theta)^n=\\cos(n\\theta)+i\\sin(n\\theta).$$ "
            "En particulier, $(re^{i\\theta})^n=r^n e^{in\\theta}$ pour tout $r\\ge0$.",
        ),
    ],
    "rappels_et_complements_sur_les_fonctions_reelles": [
        make_question(
            "rappels_et_complements_sur_les_fonctions_reelles",
            3,
            "definition",
            1,
            "Définir ce que signifie qu'une fonction est croissante, décroissante ou monotone sur un intervalle.",
            "Monotonie",
            "Soit $f:I\\to\\mathbb R$ avec $I$ intervalle. "
            "$f$ est croissante si $\\forall x,y\\in I$, $x\\le y\\Rightarrow f(x)\\le f(y)$. "
            "Elle est décroissante si $x\\le y\\Rightarrow f(x)\\ge f(y)$. "
            "Elle est monotone si elle est croissante ou décroissante.",
        ),
        make_question(
            "rappels_et_complements_sur_les_fonctions_reelles",
            4,
            "definition",
            1,
            "Définir ce que signifie qu'une fonction est majorée, minorée ou bornée sur un ensemble.",
            "Bornitude d'une fonction",
            "Soit $f:E\\to\\mathbb R$. "
            "$f$ est majorée sur $E$ s'il existe $M\\in\\mathbb R$ tel que $\\forall x\\in E$, $f(x)\\le M$. "
            "Elle est minorée s'il existe $m\\in\\mathbb R$ tel que $\\forall x\\in E$, $f(x)\\ge m$. "
            "Elle est bornée si elle est à la fois majorée et minorée.",
        ),
    ],
    "techniques_elementaires_de_calcul_integral": [
        make_question(
            "techniques_elementaires_de_calcul_integral",
            3,
            "definition",
            1,
            "Définir une primitive d'une fonction sur un intervalle.",
            "Primitive",
            "Soit $f:I\\to\\mathbb R$ et $F:I\\to\\mathbb R$ dérivable sur l'intervalle $I$. "
            "On dit que $F$ est une primitive de $f$ sur $I$ si $F'(x)=f(x)$ pour tout $x\\in I$.",
        ),
        make_question(
            "techniques_elementaires_de_calcul_integral",
            4,
            "enonce",
            1,
            "Énoncer la linéarité et l'additivité de l'intégrale sur un segment.",
            "Propriétés algébriques de l'intégrale",
            "Pour des fonctions continues $f,g$ sur $[a,b]$ et des scalaires $\\lambda,\\mu$,\\par "
            "$$\\int_a^b (\\lambda f+\\mu g)(t)\\,dt=\\lambda\\int_a^b f(t)\\,dt+\\mu\\int_a^b g(t)\\,dt.$$ "
            "Si $c\\in[a,b]$, alors\\par "
            "$$\\int_a^b f(t)\\,dt=\\int_a^c f(t)\\,dt+\\int_c^b f(t)\\,dt.$$",
        ),
    ],
    "equations_differentielles_lineaires": [
        make_question(
            "equations_differentielles_lineaires",
            3,
            "enonce",
            1,
            "Énoncer la forme générale des solutions de l'équation $y'=ay$ avec $a\\in\\mathbb R$ constant.",
            "Équation différentielle homogène simple",
            "Les solutions de l'équation $y'=ay$ sur $\\mathbb R$ sont exactement les fonctions\\par "
            "$$x\\longmapsto Ce^{ax},\\qquad C\\in\\mathbb R.$$",
        ),
        make_question(
            "equations_differentielles_lineaires",
            4,
            "enonce",
            2,
            "Énoncer le principe de superposition pour une équation linéaire.",
            "Superposition",
            "Pour une équation linéaire, l'ensemble des solutions de l'équation homogène associée est un espace vectoriel. "
            "Si $y_p$ est une solution particulière de l'équation avec second membre, alors l'ensemble des solutions de cette équation est "
            "$y_p+\\mathcal S_h$, où $\\mathcal S_h$ désigne l'ensemble des solutions de l'équation homogène associée.",
        ),
    ],
    "topologie_de_r_et_c": [
        make_question(
            "topologie_de_r_et_c",
            3,
            "definition",
            1,
            "Définir un ouvert, un fermé et un voisinage dans un espace métrique.",
            "Ouverts, fermés, voisinages",
            "Une partie $U$ est ouverte si tout point de $U$ possède une boule ouverte contenue dans $U$. "
            "Une partie $F$ est fermée si son complémentaire est ouvert. "
            "Un voisinage d'un point $x$ est toute partie contenant une boule ouverte centrée en $x$.",
        ),
        make_question(
            "topologie_de_r_et_c",
            4,
            "enonce",
            2,
            "Énoncer le théorème de Heine-Borel dans $\\mathbb R$ ou $\\mathbb C$.",
            "Compacité dans R et C",
            "Une partie de $\\mathbb R$ ou de $\\mathbb C$ est compacte si et seulement si elle est fermée et bornée.",
        ),
    ],
    "suites_reelles": [
        make_question(
            "suites_reelles",
            3,
            "enonce",
            2,
            "Énoncer le théorème des suites adjacentes.",
            "Suites adjacentes",
            "Si $(u_n)$ est croissante, $(v_n)$ est décroissante et si $u_n\\le v_n$ pour tout $n$, "
            "avec $v_n-u_n\\to0$, alors les suites $(u_n)$ et $(v_n)$ convergent et ont la même limite.",
        ),
        make_question(
            "suites_reelles",
            4,
            "enonce",
            1,
            "Énoncer le théorème d'encadrement pour les suites réelles.",
            "Théorème des gendarmes",
            "Si, à partir d'un certain rang, $u_n\\le v_n\\le w_n$ et si "
            "$u_n\\to \\ell$ et $w_n\\to \\ell$, alors $v_n\\to \\ell$.",
        ),
    ],
    "limites_et_continuite": [
        make_question(
            "limites_et_continuite",
            3,
            "definition",
            1,
            "Définir la limite finie d'une fonction en un point.",
            "Limite finie en un point",
            "Soit $f:E\\to\\mathbb R$, $a$ adhérent à $E$ et $\\ell\\in\\mathbb R$. "
            "On dit que $f(x)\\to \\ell$ lorsque $x\\to a$ si "
            "$\\forall \\varepsilon>0$, $\\exists \\eta>0$ tel que pour tout $x\\in E$, "
            "$0<|x-a|<\\eta\\Rightarrow |f(x)-\\ell|<\\varepsilon$.",
        ),
        make_question(
            "limites_et_continuite",
            4,
            "enonce",
            2,
            "Énoncer le théorème des bornes atteintes sur un segment.",
            "Bornes atteintes",
            "Toute fonction continue sur un segment $[a,b]$ est bornée et atteint ses bornes : "
            "il existe donc $x_m,x_M\\in[a,b]$ tels que "
            "$f(x_m)\\le f(x)\\le f(x_M)$ pour tout $x\\in[a,b]$.",
        ),
    ],
    "derivabilite_et_convexite": [
        make_question(
            "derivabilite_et_convexite",
            3,
            "definition",
            1,
            "Définir la dérivabilité d'une fonction en un point et rappeler sa conséquence immédiate sur la continuité.",
            "Dérivabilité",
            "Une fonction $f$ est dérivable en $a$ si la limite\\par "
            "$$\\lim_{x\\to a}\\frac{f(x)-f(a)}{x-a}$$ "
            "existe et est finie ; cette limite est alors notée $f'(a)$. "
            "Toute fonction dérivable en un point est continue en ce point.",
        ),
        make_question(
            "derivabilite_et_convexite",
            4,
            "enonce",
            2,
            "Énoncer la caractérisation d'une fonction convexe de classe $\\mathcal C^2$ par le signe de sa dérivée seconde.",
            "Convexité et dérivée seconde",
            "Si $f$ est de classe $\\mathcal C^2$ sur un intervalle $I$, alors "
            "$f$ est convexe sur $I$ si et seulement si $f''\\ge0$ sur $I$. "
            "De même, $f$ est concave sur $I$ si et seulement si $f''\\le0$ sur $I$.",
        ),
    ],
    "arithmetique_des_entiers": [
        make_question(
            "arithmetique_des_entiers",
            3,
            "definition",
            1,
            "Définir la congruence modulo $n$.",
            "Congruence",
            "Soient $a,b\\in\\mathbb Z$ et $n\\in\\mathbb N^*$. "
            "On dit que $a$ est congru à $b$ modulo $n$, ce qui se note "
            "$a\\equiv b\\ [n]$, si $n$ divise $a-b$.",
        ),
        make_question(
            "arithmetique_des_entiers",
            4,
            "enonce",
            2,
            "Énoncer le théorème fondamental de l'arithmétique.",
            "Factorisation première",
            "Tout entier $n\\ge2$ se décompose en produit de nombres premiers. "
            "Cette décomposition est unique à l'ordre des facteurs près.",
        ),
    ],
    "groupes_et_anneaux": [
        make_question(
            "groupes_et_anneaux",
            3,
            "definition",
            1,
            "Définir un groupe, un anneau et un corps.",
            "Structures algébriques",
            "Un groupe est un ensemble muni d'une loi interne associative, possédant un élément neutre et dans lequel tout élément est inversible. "
            "Un anneau est un ensemble muni de deux lois $+$ et $\\times$, tel que $(A,+)$ est un groupe abélien, "
            "$\\times$ est associative et distributive par rapport à $+$. "
            "Un corps est un anneau commutatif unitaire dans lequel tout élément non nul est inversible pour la multiplication.",
        ),
        make_question(
            "groupes_et_anneaux",
            4,
            "definition",
            2,
            "Définir un morphisme de groupes et rappeler ses propriétés élémentaires sur le neutre et les inverses.",
            "Morphisme de groupes",
            "Une application $f:G\\to H$ est un morphisme de groupes si "
            "$\\forall x,y\\in G$, $f(xy)=f(x)f(y)$. "
            "Alors nécessairement $f(e_G)=e_H$ et, pour tout $x\\in G$, "
            "$f(x^{-1})=f(x)^{-1}$.",
        ),
    ],
    "matrices_et_systemes_lineaires": [
        make_question(
            "matrices_et_systemes_lineaires",
            3,
            "enonce",
            1,
            "Énoncer la formule de transposition d'un produit et définir une matrice symétrique.",
            "Transposition",
            "Pour toutes matrices $A$ et $B$ de tailles compatibles,\\par "
            "$$(AB)^\\top=B^\\top A^\\top.$$ "
            "Une matrice carrée $A$ est dite symétrique si $A^\\top=A$.",
        ),
        make_question(
            "matrices_et_systemes_lineaires",
            4,
            "definition",
            2,
            "Définir une matrice élémentaire et expliquer son rôle pour les opérations élémentaires sur les lignes.",
            "Matrices élémentaires",
            "Une matrice élémentaire est obtenue à partir de l'identité par une unique opération élémentaire sur les lignes. "
            "Multiplier à gauche une matrice par une matrice élémentaire revient à effectuer cette opération élémentaire sur ses lignes.",
        ),
    ],
    "polynomes_et_racines": [
        make_question(
            "polynomes_et_racines",
            3,
            "enonce",
            2,
            "Énoncer les relations entre coefficients et racines pour un polynôme scindé.",
            "Relations coefficients-racines",
            "Si $P(X)=a_n\\prod_{i=1}^n (X-r_i)$, alors\\par "
            "$$\\sum_{i=1}^n r_i=-\\frac{a_{n-1}}{a_n},\\qquad "
            "\\prod_{i=1}^n r_i=(-1)^n\\frac{a_0}{a_n},$$ "
            "et plus généralement les coefficients sont, au signe près, les fonctions symétriques élémentaires des racines.",
        ),
        make_question(
            "polynomes_et_racines",
            4,
            "enonce",
            3,
            "Énoncer la formule d'interpolation de Lagrange pour des points deux à deux distincts.",
            "Interpolation de Lagrange",
            "Si $a_1,\\dots,a_n$ sont deux à deux distincts et si $b_1,\\dots,b_n\\in\\mathbb K$, "
            "il existe un unique polynôme $P\\in\\mathbb K_{n-1}[X]$ tel que $P(a_i)=b_i$ pour tout $i$, et\\par "
            "$$P(X)=\\sum_{i=1}^n b_i\\prod_{j\\ne i}\\frac{X-a_j}{a_i-a_j}.$$",
        ),
    ],
    "arithmetique_des_polynomes_et_fractions_rationnelles": [
        make_question(
            "arithmetique_des_polynomes_et_fractions_rationnelles",
            3,
            "definition",
            2,
            "Définir le pgcd de deux polynômes et la notion de polynômes premiers entre eux.",
            "PGCD dans K[X]",
            "Si $A,B\\in\\mathbb K[X]$ ne sont pas tous deux nuls, leur pgcd est l'unique polynôme unitaire $D$ qui divise $A$ et $B$ "
            "et qui est divisible par tout diviseur commun de $A$ et $B$. "
            "On dit que $A$ et $B$ sont premiers entre eux si leur pgcd vaut $1$.",
        ),
        make_question(
            "arithmetique_des_polynomes_et_fractions_rationnelles",
            4,
            "enonce",
            3,
            "Énoncer le principe de la décomposition en éléments simples sur $\\mathbb C$.",
            "Décomposition en éléments simples",
            "Toute fraction rationnelle propre à coefficients complexes se décompose en somme d'éléments simples de la forme\\par "
            "$$\\frac{\\lambda}{(X-a)^k}$$ "
            "où $a$ parcourt les pôles de la fraction rationnelle et $1\\le k\\le m_a$, avec $m_a$ l'ordre du pôle $a$. "
            "Cette décomposition est unique.",
        ),
    ],
    "analyse_asymptotique_de_niveau_1": [
        make_question(
            "analyse_asymptotique_de_niveau_1",
            3,
            "enonce",
            2,
            "Donner quatre équivalents usuels au voisinage de $0$.",
            "Équivalents usuels en 0",
            "Lorsque $x\\to0$, on a\\par "
            "$$\\sin x\\sim x,\\qquad \\tan x\\sim x,\\qquad \\ln(1+x)\\sim x,\\qquad e^x-1\\sim x.$$ "
            "On a aussi $1-\\cos x\\sim \\dfrac{x^2}{2}$.",
        ),
        make_question(
            "analyse_asymptotique_de_niveau_1",
            4,
            "enonce",
            2,
            "Énoncer les règles de calcul usuelles avec les équivalents pour le produit, le quotient et la puissance.",
            "Calcul sur les équivalents",
            "Si $f\\sim g$ et $u\\sim v$ au voisinage d'un point où les expressions ont un sens, alors\\par "
            "$fu\\sim gv$,\\quad $\\dfrac{f}{u}\\sim\\dfrac{g}{v}$ si $v$ ne s'annule pas localement,\\par "
            "et, pour tout entier $n$, $f^n\\sim g^n$ lorsque ces puissances ont un sens. "
            "En revanche, on n'additionne pas des équivalents en général.",
        ),
    ],
    "analyse_asymptotique_de_niveau_2": [
        make_question(
            "analyse_asymptotique_de_niveau_2",
            3,
            "enonce",
            2,
            "Donner les développements limités usuels en $0$ de $e^x$, $\\sin x$, $\\cos x$, $\\ln(1+x)$ et $\\dfrac{1}{1+x}$ à l'ordre 2.",
            "DL usuels en 0",
            "Lorsque $x\\to0$,\\par "
            "$$e^x=1+x+\\frac{x^2}{2}+o(x^2),\\qquad "
            "\\sin x=x+o(x^2),\\qquad "
            "\\cos x=1-\\frac{x^2}{2}+o(x^2),$$\\par "
            "$$\\ln(1+x)=x-\\frac{x^2}{2}+o(x^2),\\qquad "
            "\\frac{1}{1+x}=1-x+x^2+o(x^2).$$",
        ),
        make_question(
            "analyse_asymptotique_de_niveau_2",
            4,
            "enonce",
            3,
            "Énoncer comment un développement limité d'ordre 2 permet d'obtenir la tangente et la position relative d'une courbe.",
            "Étude locale par DL",
            "Si, au voisinage de $a$, on a\\par "
            "$$f(x)=f(a)+f'(a)(x-a)+\\alpha(x-a)^2+o((x-a)^2),$$ "
            "alors la tangente au graphe en $a$ a pour équation "
            "$y=f(a)+f'(a)(x-a)$. "
            "De plus, le signe de $f(x)-\\bigl(f(a)+f'(a)(x-a)\\bigr)$ est, au voisinage de $a$, celui de $\\alpha(x-a)^2$ ; "
            "il permet donc de déterminer la position relative de la courbe par rapport à sa tangente.",
        ),
    ],
    "espaces_vectoriels": [
        make_question(
            "espaces_vectoriels",
            3,
            "definition",
            2,
            "Définir une somme directe et un supplémentaire de sous-espaces vectoriels.",
            "Somme directe",
            "Pour deux sous-espaces $F$ et $G$ d'un espace vectoriel $E$, on dit que la somme $F+G$ est directe si "
            "$F\\cap G=\\{0\\}$. On écrit alors $F\\oplus G$. "
            "On dit que $G$ est un supplémentaire de $F$ dans $E$ si $E=F\\oplus G$.",
        ),
        make_question(
            "espaces_vectoriels",
            4,
            "enonce",
            2,
            "Énoncer la formule de Grassmann.",
            "Formule de Grassmann",
            "Si $F$ et $G$ sont deux sous-espaces d'un espace vectoriel de dimension finie, alors\\par "
            "$$\\dim(F+G)=\\dim F+\\dim G-\\dim(F\\cap G).$$",
        ),
    ],
    "applications_lineaires": [
        make_question(
            "applications_lineaires",
            3,
            "enonce",
            1,
            "Énoncer la caractérisation de l'injectivité d'une application linéaire par son noyau.",
            "Injectivité et noyau",
            "Une application linéaire $u:E\\to F$ est injective si et seulement si "
            "$\\ker u=\\{0_E\\}$.",
        ),
        make_question(
            "applications_lineaires",
            4,
            "enonce",
            2,
            "Énoncer la stabilité des sous-espaces par image et image réciproque.",
            "Image et image réciproque de sous-espace",
            "Si $u:E\\to F$ est linéaire et si $F_0$ est un sous-espace de $F$, alors "
            "$u^{-1}(F_0)$ est un sous-espace de $E$. "
            "Si $E_0$ est un sous-espace de $E$, alors $u(E_0)$ est un sous-espace de $F$.",
        ),
    ],
    "representation_matricielle_applications_lineaires": [
        make_question(
            "representation_matricielle_applications_lineaires",
            3,
            "enonce",
            2,
            "Énoncer le lien entre composition d'applications linéaires et produit matriciel.",
            "Composition et matrices",
            "Si $u:E\\to F$ et $v:F\\to G$ sont linéaires, alors dans des bases compatibles on a\\par "
            "$$[v\\circ u]=[v][u].$$",
        ),
        make_question(
            "representation_matricielle_applications_lineaires",
            4,
            "definition",
            2,
            "Définir deux matrices équivalentes et deux matrices semblables.",
            "Équivalence et similitude",
            "Deux matrices $A,B\\in\\mathcal M_{p,n}(\\mathbb K)$ sont équivalentes s'il existe "
            "$P\\in GL_p(\\mathbb K)$ et $Q\\in GL_n(\\mathbb K)$ tels que $B=PAQ$. "
            "Deux matrices carrées $A,B\\in\\mathcal M_n(\\mathbb K)$ sont semblables s'il existe "
            "$P\\in GL_n(\\mathbb K)$ tel que $B=P^{-1}AP$.",
        ),
    ],
    "determinants": [
        make_question(
            "determinants",
            3,
            "enonce",
            2,
            "Énoncer l'effet des opérations élémentaires sur les lignes ou les colonnes sur le déterminant.",
            "Opérations élémentaires et déterminant",
            "Échanger deux lignes ou deux colonnes multiplie le déterminant par $-1$. "
            "Multiplier une ligne ou une colonne par $\\lambda$ multiplie le déterminant par $\\lambda$. "
            "Ajouter à une ligne ou une colonne un multiple d'une autre ne change pas le déterminant.",
        ),
        make_question(
            "determinants",
            4,
            "enonce",
            3,
            "Énoncer la formule donnant l'inverse d'une matrice inversible à l'aide de la comatrice.",
            "Comatrice",
            "Si $A\\in\\mathcal M_n(\\mathbb K)$ est inversible, alors\\par "
            "$$A^{-1}=\\frac{1}{\\det(A)}\\,{}^\\top\\!\\operatorname{Com}(A),$$ "
            "où $\\operatorname{Com}(A)$ désigne la comatrice de $A$.",
        ),
    ],
    "denombrement": [
        make_question(
            "denombrement",
            3,
            "enonce",
            2,
            "Donner le nombre d'applications, d'injections et de bijections d'un ensemble à $n$ éléments vers un ensemble à $p$ éléments.",
            "Cardinaux classiques",
            "Le nombre d'applications d'un ensemble à $n$ éléments vers un ensemble à $p$ éléments est $p^n$. "
            "Si $n\\le p$, le nombre d'injections est "
            "$p(p-1)\\cdots(p-n+1)=\\dfrac{p!}{(p-n)!}$. "
            "Si $n=p$, le nombre de bijections est $n!$.",
        ),
        make_question(
            "denombrement",
            4,
            "enonce",
            1,
            "Énoncer la relation de Pascal et la somme des coefficients binomiaux.",
            "Identités binomiales",
            "Pour $0<k<n$, on a\\par "
            "$$\\binom{n}{k}=\\binom{n-1}{k-1}+\\binom{n-1}{k}.$$ "
            "De plus,\\par "
            "$$\\sum_{k=0}^n \\binom{n}{k}=2^n.$$",
        ),
    ],
    "probabilites_sur_un_univers_fini": [
        make_question(
            "probabilites_sur_un_univers_fini",
            3,
            "definition",
            1,
            "Définir une variable aléatoire réelle discrète finie et sa loi.",
            "Variable aléatoire et loi",
            "Sur un univers fini $\\Omega$, une variable aléatoire réelle discrète finie est une application "
            "$X:\\Omega\\to\\mathbb R$ prenant un nombre fini de valeurs. "
            "Sa loi est la donnée des probabilités "
            "$P(X=x)$ pour chacune des valeurs $x$ prises par $X$.",
        ),
        make_question(
            "probabilites_sur_un_univers_fini",
            4,
            "enonce",
            2,
            "Énoncer les formules de l'espérance et de la variance d'une variable affine en une autre.",
            "Transformation affine d'une variable",
            "Si $X$ est une variable aléatoire réelle de variance finie et si $a,b\\in\\mathbb R$, alors\\par "
            "$$E(aX+b)=aE(X)+b,\\qquad V(aX+b)=a^2V(X).$$",
        ),
    ],
    "complements_probabilistes": [
        make_question(
            "complements_probabilistes",
            3,
            "definition",
            2,
            "Définir la loi binomiale de paramètres $n$ et $p$.",
            "Loi binomiale",
            "Une variable aléatoire $X$ suit la loi binomiale de paramètres $n\\in\\mathbb N$ et $p\\in[0,1]$ si, pour tout "
            "$k\\in\\{0,\\dots,n\\}$,\\par "
            "$$P(X=k)=\\binom{n}{k}p^k(1-p)^{n-k}.$$",
        ),
        make_question(
            "complements_probabilistes",
            4,
            "enonce",
            3,
            "Énoncer les formules de l'espérance et de la variance d'une somme de variables aléatoires indépendantes.",
            "Somme de variables indépendantes",
            "Si $X_1,\\dots,X_n$ admettent une espérance et sont indépendantes, alors\\par "
            "$$E\\left(\\sum_{i=1}^n X_i\\right)=\\sum_{i=1}^n E(X_i).$$ "
            "Si elles admettent en plus une variance finie, alors\\par "
            "$$V\\left(\\sum_{i=1}^n X_i\\right)=\\sum_{i=1}^n V(X_i).$$",
        ),
    ],
    "espaces_prehilbertiens_reels": [
        make_question(
            "espaces_prehilbertiens_reels",
            3,
            "definition",
            1,
            "Définir l'orthogonalité, une famille orthonormée et l'orthogonal d'une partie.",
            "Orthogonalité",
            "Dans un espace préhilbertien réel, deux vecteurs $x$ et $y$ sont orthogonaux si "
            "$\\langle x,y\\rangle=0$. "
            "Une famille est orthonormée si ses vecteurs sont unitaires et deux à deux orthogonaux. "
            "Pour une partie $A$, l'orthogonal de $A$ est "
            "$A^\\perp=\\{x\\in E\\mid \\forall a\\in A,\\ \\langle x,a\\rangle=0\\}$.",
        ),
        make_question(
            "espaces_prehilbertiens_reels",
            4,
            "enonce",
            2,
            "Énoncer le théorème de Pythagore et la formule du projeté orthogonal sur une droite vectorielle.",
            "Pythagore et projeté",
            "Si $x\\perp y$, alors\\par "
            "$$\\|x+y\\|^2=\\|x\\|^2+\\|y\\|^2.$$ "
            "Si $u\\ne0$, le projeté orthogonal de $x$ sur la droite $\\mathbb Ru$ est\\par "
            "$$\\operatorname{proj}_{\\mathbb Ru}(x)=\\frac{\\langle x,u\\rangle}{\\|u\\|^2}u.$$",
        ),
    ],
    "series_et_familles_sommables": [
        make_question(
            "series_et_familles_sommables",
            3,
            "enonce",
            1,
            "Énoncer le critère de convergence d'une série géométrique.",
            "Série géométrique",
            "Pour $q\\in\\mathbb R$, la série $\\sum_{n=0}^{+\\infty} q^n$ converge si et seulement si $|q|<1$, "
            "et dans ce cas sa somme vaut\\par "
            "$$\\sum_{n=0}^{+\\infty} q^n=\\frac{1}{1-q}.$$",
        ),
        make_question(
            "series_et_familles_sommables",
            4,
            "enonce",
            2,
            "Énoncer le critère spécial des séries alternées.",
            "Séries alternées",
            "Si $(u_n)$ est une suite décroissante de réels positifs telle que $u_n\\to0$, alors la série alternée "
            "$\\sum (-1)^n u_n$ converge. "
            "De plus, le reste après sommation partielle est du signe du premier terme négligé et son module est majoré par ce terme.",
        ),
    ],
    "fonctions_de_deux_variables": [
        make_question(
            "fonctions_de_deux_variables",
            3,
            "definition",
            2,
            "Définir le gradient d'une fonction de deux variables et un point critique.",
            "Gradient et point critique",
            "Si $f$ admet des dérivées partielles en $(a,b)$, son gradient en ce point est\\par "
            "$$\\nabla f(a,b)=\\bigl(\\partial_x f(a,b),\\partial_y f(a,b)\\bigr).$$ "
            "Le point $(a,b)$ est critique si $\\nabla f(a,b)=(0,0)$.",
        ),
        make_question(
            "fonctions_de_deux_variables",
            4,
            "enonce",
            3,
            "Énoncer un critère suffisant d'extremum local à l'aide de la hessienne en dimension 2.",
            "Critère hessien",
            "Soit $f\\in\\mathcal C^2$ au voisinage d'un point critique $(a,b)$. "
            "On pose $D=f_{xx}(a,b)f_{yy}(a,b)-f_{xy}(a,b)^2$. "
            "Si $D>0$ et $f_{xx}(a,b)>0$, alors $f$ admet un minimum local en $(a,b)$. "
            "Si $D>0$ et $f_{xx}(a,b)<0$, alors $f$ admet un maximum local en $(a,b)$. "
            "Si $D<0$, le point critique est un point selle.",
        ),
    ],
    "integration_sur_un_segment": [
        make_question(
            "integration_sur_un_segment",
            3,
            "enonce",
            2,
            "Énoncer la convergence des sommes de Riemann pour une fonction continue sur un segment.",
            "Sommes de Riemann",
            "Si $f$ est continue sur $[a,b]$, alors\\par "
            "$$\\frac{b-a}{n}\\sum_{k=0}^{n-1} f\\left(a+k\\frac{b-a}{n}\\right)\\xrightarrow[n\\to+\\infty]{}\\int_a^b f(t)\\,dt.$$",
        ),
        make_question(
            "integration_sur_un_segment",
            4,
            "enonce",
            3,
            "Énoncer la formule de Taylor avec reste intégral.",
            "Taylor avec reste intégral",
            "Si $f$ est de classe $\\mathcal C^{n+1}$ sur un intervalle contenant $a$ et $x$, alors\\par "
            "$$f(x)=\\sum_{k=0}^{n}\\frac{f^{(k)}(a)}{k!}(x-a)^k+\\int_a^x \\frac{(x-t)^n}{n!}f^{(n+1)}(t)\\,dt.$$",
        ),
    ],
}

for course_id, questions in ADDITIONAL_COURSE_QUESTIONS.items():
    COURSE_QUESTIONS[course_id].extend(questions)


def main() -> None:
    cours_titles = {}
    for path in COURSE_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        cours_titles[data["chapter_official_id"]] = data["chapter_name"]

    expected_course_ids = set(cours_titles)
    curated_course_ids = set(COURSE_QUESTIONS)
    missing_course_ids = sorted(expected_course_ids - curated_course_ids)
    extra_course_ids = sorted(curated_course_ids - expected_course_ids)
    if missing_course_ids or extra_course_ids:
        raise ValueError(
            "Curated question bank is out of sync with course chapters: "
            f"missing={missing_course_ids}, extra={extra_course_ids}"
        )

    programme = json.loads(PROGRAMME_PATH.read_text(encoding="utf-8"))["referentiel_mpsi"]
    course_to_programme = {}
    course_to_semester = {}
    for prog_id, prog in programme.items():
        if prog_id == "metadata":
            continue
        for course_id in prog.get("linked_course_chapters", []):
            course_to_programme[course_id] = prog["titre"]
            course_to_semester[course_id] = prog["semestre"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*.json"):
        old_file.unlink()

    for course_id, questions in COURSE_QUESTIONS.items():
        if len(questions) != 4:
            raise ValueError(
                f"{course_id} should define exactly 4 curated questions, found {len(questions)}"
            )
        payload = {
            "programme_chapter_id": course_id,
            "programme_chapter_title": course_to_programme.get(course_id, cours_titles[course_id]),
            "course_chapter_id": course_id,
            "course_chapter_title": cours_titles[course_id],
            "semestre": course_to_semester.get(course_id, 1),
            "linked_course_chapters": [course_id],
            "source_document": "Banque de questions de cours curated",
            "questions": questions,
        }
        output_path = OUTPUT_DIR / f"{course_id}.json"
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
