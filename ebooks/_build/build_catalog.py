# -*- coding: utf-8 -*-
import json, html, datetime
from data import BOOKS

GH_USER = "clode666"
REPO    = "truvector-assets"
CDN     = f"https://cdn.jsdelivr.net/gh/{GH_USER}/{REPO}@main/ebooks"
# Fenêtre de disponibilité par défaut (modifiable) : lancement -> échéance
UNTIL_DEFAULT = "2026-11-30"     # <-- change cette date globale ici
FROM_DEFAULT  = "2026-09-22"

def esc(s): return html.escape(s, quote=True)

# ---------- manifest.json (pour truvector-assets) ----------
manifest = {
    "version": 1,
    "generated": datetime.date.today().isoformat(),
    "cdn": CDN,
    "window": {"from": FROM_DEFAULT, "until": UNTIL_DEFAULT},
    "books": [
        {
            "n": b["n"],
            "slug": b["slug"],
            "title": b["title"],
            "genre": b["genre"],
            "blurb": b["blurb"],
            "cover": f'covers/{b["slug"]}.svg',
            "trubook": f'{b["slug"]}.trubook',
            "words_target": b["words"],
            "window": {"from": FROM_DEFAULT, "until": UNTIL_DEFAULT},
            "passphrase_public": "truvector"
        } for b in BOOKS
    ]
}
with open("/home/claude/build/truvector-assets/ebooks/manifest.json","w",encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# ---------- cartes ----------
cards = []
avail_map = {}
for b in BOOKS:
    slug=b["slug"]
    cover=f'{CDN}/covers/{slug}.svg'
    reader=f'lecteur.html?src={CDN}/{slug}.trubook'
    avail_map[slug]=UNTIL_DEFAULT
    cards.append(f'''      <article class="eb-card" data-slug="{slug}">
        <a class="eb-cover" href="{reader}" aria-label="Lire : {esc(b["title"])}">
          <img src="{cover}" alt="Couverture de {esc(b["title"])}" loading="lazy" width="320" height="480">
          <span class="eb-badge">{esc(b["genre"])}</span>
        </a>
        <div class="eb-body">
          <h3>{esc(b["title"])}</h3>
          <p>{esc(b["blurb"])}</p>
          <div class="eb-foot">
            <a class="btn eb-read" href="{reader}">Lire</a>
            <span class="eb-until" data-until="{UNTIL_DEFAULT}"></span>
          </div>
        </div>
      </article>''')

cards_html = "\n".join(cards)
avail_json = json.dumps(avail_map, ensure_ascii=False)

PAGE = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>E-books — TRUvector.dev</title>
<meta name="robots" content="noindex">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/tokens.css?v=5">
<style>
.cta-row{{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin:6px 0 30px}}
.cta-row .btn{{min-width:220px;justify-content:center}}
.sec-h{{font-family:var(--mono);font-size:12px;letter-spacing:2px;color:var(--menthe);text-transform:uppercase;margin:26px 0 6px}}
.sec-h small{{color:var(--texte-3);letter-spacing:1px;text-transform:none;margin-left:8px}}
.eb-note{{font-family:var(--mono);font-size:12.5px;color:var(--texte-2);background:var(--panneau-2);border:1px solid var(--bord);border-radius:12px;padding:12px 14px;margin:0 0 20px;display:flex;gap:10px;align-items:flex-start}}
.eb-note .ic{{color:var(--menthe)}}
.eb-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:20px;margin:8px 0 40px}}
.eb-card{{background:var(--panneau-2);border:1px solid var(--bord);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;transition:transform .18s,border-color .2s,box-shadow .2s}}
.eb-card:hover{{transform:translateY(-3px);border-color:var(--bord-fort);box-shadow:0 10px 34px rgba(0,0,0,.4)}}
.eb-card.eb-expired{{opacity:.5;filter:grayscale(.5)}}
.eb-card.eb-expired .eb-read{{pointer-events:none;opacity:.4;filter:grayscale(.3);box-shadow:none}}
.eb-cover{{position:relative;display:block;aspect-ratio:2/3;background:#05080d}}
.eb-cover img{{width:100%;height:100%;object-fit:cover}}
.eb-badge{{position:absolute;left:10px;top:10px;font-family:var(--mono);font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--menthe);background:rgba(5,8,13,.72);border:1px solid var(--bord-fort);border-radius:999px;padding:4px 9px;backdrop-filter:blur(4px)}}
.eb-body{{padding:14px 15px 16px;display:flex;flex-direction:column;gap:8px;flex:1}}
.eb-body h3{{margin:0;font-size:17px;font-weight:600;letter-spacing:-.2px;line-height:1.25}}
.eb-body p{{margin:0;color:var(--texte-2);font-size:13.5px;line-height:1.5;flex:1}}
.eb-foot{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:4px}}
.eb-read{{padding:9px 18px;font-size:13px}}
.eb-until{{font-family:var(--mono);font-size:11px;color:var(--texte-3);text-align:right;line-height:1.3}}
.eb-until.soon{{color:var(--ambre)}}
</style>
<script src="../assets/js/assets.js?v=1"></script>
</head>
<body>
<nav class="site-nav"><div class="wrap row">
  <a class="brand" href="../index.html" aria-label="Accueil TRUvector"><svg class="triskele" viewBox="0 0 200 200" aria-hidden="true"><g fill="none" stroke="#34f5c5" stroke-width="7" stroke-linecap="round"><path d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/><path transform="rotate(120 100 100)" d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/><path transform="rotate(240 100 100)" d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/></g><circle cx="100" cy="100" r="5" fill="#34f5c5"/></svg><span><span class="tru">TRU</span><span class="vec">vector</span><span class="dev">.dev</span></span></a>
  <div class="nav-links"><a href="../index.html">Accueil</a><a href="../mentions-legales/">Légal</a></div>
</div></nav>
<header class="section-hero"><div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>
  <div class="wrap in"><svg class="triskele" viewBox="0 0 200 200" aria-hidden="true"><g fill="none" stroke="#34f5c5" stroke-width="7" stroke-linecap="round"><path d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/><path transform="rotate(120 100 100)" d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/><path transform="rotate(240 100 100)" d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/></g><circle cx="100" cy="100" r="5" fill="#34f5c5"/></svg><h1>E-books</h1><p>Vingt et une nouvelles, dix-huit styles. Lues dans la visionneuse maison : durée, pages, filigrane — sans jamais exposer le fichier.</p></div>
</header>

<main class="wrap">
  <div class="cta-row">
    <a class="btn" href="lecteur.html">📖 Ouvrir la visionneuse</a>
    <a class="btn btn-ghost" href="proteger.html">🔒 Protéger un e-book</a>
  </div>

  <p class="eb-note"><span class="ic">⏳</span><span>Édition à durée limitée — ces nouvelles restent disponibles jusqu’au <strong id="eb-globaldate"></strong>. Passé cette date, l’accès se verrouille automatiquement.</span></p>

  <p class="sec-h">Catalogue <small>{len(BOOKS)} nouvelles</small></p>
  <div class="eb-grid">
{cards_html}
  </div>
</main>

<footer class="site-foot"><div class="wrap"><div class="hr" style="margin-bottom:26px"></div>
  <p class="fm">$ truvector serve --section ebooks --public</p>
  <p>© 2026 TRUvector.dev — Tristan Ruard</p>
  <p class="foot-legal"><a href="../mentions-legales/">Mentions légales</a> · <a href="../cgv/">CGV</a> · <a href="../confidentialite/">Confidentialité</a> · <a href="../cookies/">Cookies</a> · <a href="../securite/">Sécurité</a></p>
</div></footer>
<script src="../assets/js/nav.js?v=4"></script>
<script>
/* Disponibilité limitée : verrouille les cartes expirées et affiche l'échéance. */
(function(){{
  var GLOBAL_UNTIL = "{UNTIL_DEFAULT}";
  var g=document.getElementById('eb-globaldate');
  if(g) g.textContent = new Date(GLOBAL_UNTIL+'T23:59:59').toLocaleDateString('fr-FR',{{day:'2-digit',month:'long',year:'numeric'}});
  var now=new Date();
  document.querySelectorAll('.eb-card').forEach(function(card){{
    var el=card.querySelector('.eb-until'); if(!el) return;
    var until=el.getAttribute('data-until'); var d=new Date(until+'T23:59:59');
    var days=Math.ceil((d-now)/86400000);
    if(days<0){{ card.classList.add('eb-expired'); el.textContent='Terminé'; }}
    else if(days<=7){{ el.classList.add('soon'); el.textContent='Plus que '+days+' j'; }}
    else {{ el.textContent='Jusqu’au '+d.toLocaleDateString('fr-FR',{{day:'2-digit',month:'2-digit'}}); }}
  }});
}})();
</script>
</body>
</html>'''

with open("/home/claude/build/site-patch/ebooks/index.html","w",encoding="utf-8") as f:
    f.write(PAGE)

print("manifest.json + index.html générés.")
print("cartes:", len(cards))
