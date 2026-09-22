# -*- coding: utf-8 -*-
"""Source de vérité unique : les 21 e-books TRUvector."""

# accents (issus de tokens.css)
MENTHE   = "#34f5c5"
MENTHE_S = "#8ff3d9"
VIOLET   = "#b14aed"
VIOLET_S = "#c98bf5"
VERT     = "#59e39a"
AMBRE    = "#f4c56b"
ACIER    = "#7fa8c9"   # bleu froid dérivé, pour le noir/polar
ROSE     = "#f2a0c0"   # rose tendre dérivé, pour la romance

# motif : type de trame procédurale dessinée sur la couverture
# "orbit" | "grid" | "rain" | "roots" | "stars" | "clock" | "wave" | "lines" | "bloom" | "maze"

BOOKS = [
    # --- SF / anticipation ---
    dict(n=1,  slug="le-dernier-octet", title="Le Dernier Octet",
         genre="SF · anticipation", accent=MENTHE, motif="grid",
         blurb="Un archiviste doit choisir quels souvenirs de l’humanité sauver avant l’effacement d’un monde.",
         words=1650),
    dict(n=2,  slug="signal-perdu", title="Signal Perdu",
         genre="SF · anticipation", accent=MENTHE, motif="orbit",
         blurb="Une sonde revient deux siècles trop tard, porteuse d’un message que plus personne ne sait lire.",
         words=1500),
    # --- Cyberpunk / techno-thriller ---
    dict(n=3,  slug="root-at-nuit", title="root@nuit",
         genre="Cyberpunk", accent=VIOLET, motif="rain",
         blurb="Une hackeuse découvre que son propre cerveau tourne sous licence — et qu’elle est en retard de paiement.",
         words=1700),
    dict(n=4,  slug="le-contrat-fantome", title="Le Contrat Fantôme",
         genre="Techno-thriller", accent=VIOLET, motif="lines",
         blurb="Un dev freelance accepte une mission trop bien payée, pour un client qui n’existe pas.",
         words=1600),
    # --- Polar / noir ---
    dict(n=5,  slug="chambre-404", title="Chambre 404",
         genre="Polar · noir", accent=ACIER, motif="maze",
         blurb="Une disparition dans un hôtel dont une chambre ne figure sur aucun plan.",
         words=1600),
    dict(n=6,  slug="encre-noire", title="Encre Noire",
         genre="Polar · noir", accent=ACIER, motif="lines",
         blurb="Un tatoueur reconnaît, sur la peau d’un client, le dessin d’un crime jamais résolu.",
         words=1550),
    # --- Fantastique / horreur ---
    dict(n=7,  slug="ce-qui-pousse-la-nuit", title="Ce qui pousse la nuit",
         genre="Fantastique", accent=VERT, motif="roots",
         blurb="Une plante offerte se met à réclamer bien plus que de l’eau.",
         words=1600),
    dict(n=8,  slug="le-treizieme-etage", title="Le Treizième Étage",
         genre="Horreur", accent=VERT, motif="grid",
         blurb="L’ascenseur s’arrête à un étage que l’immeuble ne possède pas.",
         words=1550),
    # --- Fantasy ---
    dict(n=9,  slug="la-forge-des-noms", title="La Forge des Noms",
         genre="Fantasy", accent=AMBRE, motif="bloom",
         blurb="Dans un royaume où nommer une chose la crée, un forgeron oublie son propre nom.",
         words=1750),
    dict(n=10, slug="le-cartographe-aveugle", title="Le Cartographe Aveugle",
         genre="Fantasy", accent=AMBRE, motif="maze",
         blurb="Il dessine des cartes de pays qu’il n’a jamais vus — et qui finissent par exister.",
         words=1700),
    # --- Conte / fable philosophique ---
    dict(n=11, slug="l-horloger-et-le-temps", title="L’Horloger et le Temps",
         genre="Conte philosophique", accent=MENTHE_S, motif="clock",
         blurb="Celui qui répare les montres du village n’a jamais eu le temps de vivre.",
         words=1450),
    dict(n=12, slug="la-fille-qui-comptait-les-etoiles", title="La Fille qui Comptait les Étoiles",
         genre="Conte poétique", accent=MENTHE_S, motif="stars",
         blurb="Sur ce qu’on cesse de voir, un à un, en grandissant.",
         words=1400),
    # --- Réalisme / tranche de vie ---
    dict(n=13, slug="cafe-table-3", title="Café, table 3",
         genre="Tranche de vie", accent="#9db2ae", motif="wave",
         blurb="Deux inconnus, le même café chaque matin, sans un mot — jusqu’au jour où l’un manque.",
         words=1500),
    dict(n=14, slug="vingt-minutes-de-retard", title="Vingt Minutes de Retard",
         genre="Réalisme", accent="#9db2ae", motif="lines",
         blurb="Comment un train raté redessine une vie entière.",
         words=1500),
    # --- Romance épistolaire ---
    dict(n=15, slug="correspondances", title="Correspondances",
         genre="Romance épistolaire", accent=ROSE, motif="wave",
         blurb="Deux personnes s’écrivent par erreur sur une vieille adresse — et n’arrêtent plus.",
         words=1650),
    # --- Humour / satire ---
    dict(n=16, slug="reunion-obligatoire", title="Réunion Obligatoire",
         genre="Satire", accent=AMBRE, motif="grid",
         blurb="La chronique d’une réunion qui ne finit jamais.",
         words=1400),
    dict(n=17, slug="mise-a-jour-requise", title="Mise à Jour Requise",
         genre="Humour", accent=AMBRE, motif="rain",
         blurb="Un homme dont la vie refuse de fonctionner tant qu’il n’a pas installé la v2.0.",
         words=1450),
    # --- Historique / uchronie ---
    dict(n=18, slug="lettre-de-1914", title="Lettre de 1914",
         genre="Historique", accent=AMBRE, motif="wave",
         blurb="Une lettre du front qui arrive à destination cent ans trop tard.",
         words=1600),
    dict(n=19, slug="si-ada-avait-continue", title="Si Ada Avait Continué",
         genre="Uchronie", accent=MENTHE, motif="orbit",
         blurb="Et si Ada Lovelace avait achevé sa machine à penser ?",
         words=1700),
    # --- Huis clos / psychologique ---
    dict(n=20, slug="le-dernier-wagon", title="Le Dernier Wagon",
         genre="Huis clos", accent=VIOLET, motif="rain",
         blurb="Un train qui ne s’arrête plus, des passagers qui ne se souviennent pas d’être montés.",
         words=1650),
    # --- Post-apocalyptique lumineux ---
    dict(n=21, slug="le-jardin-sous-la-cendre", title="Le Jardin sous la Cendre",
         genre="Post-apo lumineux", accent=VERT, motif="bloom",
         blurb="Après la fin du monde, une communauté fait éclore la première fleur.",
         words=1750),
]
