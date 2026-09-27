#!/usr/bin/env python3
"""Static site generator for MyPerformance.com.

Usage:  python3 build.py
Reads   src/pages/**/*.html  (HTML fragments with a leading <!--META {...}--> block)
        src/guides/*.md       (Markdown articles with a leading JSON front-matter block)
Writes  _site/ (deployable static site: pages, sitemap.xml, robots.txt, assets, search index)
Everything the site needs is plain HTML/CSS/JS, so it hosts on GitHub Pages' free plan.
"""
import json, os, re, glob, datetime, html
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")
# Canonical site URL. Override with SITE_URL env var (the Pages workflow does this).
SITE = os.environ.get("SITE_URL", "https://myperformance.com").rstrip("/")
from urllib.parse import urlparse as _up
BASE = _up(SITE).path.rstrip("/")   # "" for a custom domain, "/repo-name" for a project Pages site
SITE_NAME = "MyPerformance.com"
TODAY = datetime.date.today().isoformat()

NAV = [
    ("Tools", "/tools/", [
        ("Self-Evaluation Generator", "/tools/self-evaluation-generator/", "Write your self-appraisal in minutes"),
        ("Review Phrase Library", "/tools/performance-review-phrases/", "500+ phrases by competency & rating"),
        ("SMART Goal Builder", "/tools/smart-goal-builder/", "Turn vague goals into measurable ones"),
        ("Performance Score Quiz", "/tools/performance-score/", "Rate your performance across 8 dimensions"),
        ("Raise & Promotion Calculator", "/tools/raise-calculator/", "What your review is worth in dollars"),
        ("Productivity Calculator", "/tools/productivity-calculator/", "Find your real focus hours"),
        ("1:1 Meeting Agenda Builder", "/tools/one-on-one-agenda/", "Agendas managers and reports both like"),
        ("Habit & Streak Tracker", "/tools/habit-tracker/", "Weekly habit grid, saved in your browser"),
        ("Focus Timer (Pomodoro)", "/tools/focus-timer/", "Deep-work sessions with stats"),
    ]),
    ("Templates", "/templates/", [
        ("Performance Review Template", "/templates/performance-review/", "Manager review, ready to fill"),
        ("Self-Evaluation Template", "/templates/self-evaluation/", "Employee self-assessment form"),
        ("30-60-90 Day Plan", "/templates/30-60-90-day-plan/", "New role onboarding plan"),
        ("Goal-Setting Worksheet (OKR)", "/templates/okr-goal-setting/", "Quarterly objectives & key results"),
        ("Performance Improvement Plan", "/templates/performance-improvement-plan/", "Fair, documented PIP"),
        ("1:1 Meeting Template", "/templates/one-on-one-meeting/", "Weekly check-in format"),
    ]),
    ("Guides", "/guides/", None),
    ("Videos", "/videos/", None),
    ("Coaching", "/coaching/", None),
    ("Support", "/support/", None),
]

FOOTER_COLS = [
    ("Tools", [(t, u) for t, u, _ in NAV[0][2]]),
    ("Templates", [(t, u) for t, u, _ in NAV[1][2]]),
    ("Company", [("About", "/about/"), ("Contact", "/contact/"), ("Careers — we're hiring", "/careers/"), ("Advertise & Sponsor", "/advertise/"), ("Partnerships", "/advertise/#partnerships"), ("Support Us", "/support/"), ("Contests & Prizes", "/contests/"), ("Newsletter", "/newsletter/")]),
    ("Legal", [("Privacy Policy", "/legal/privacy/"), ("Terms of Use", "/legal/terms/"), ("Disclaimer", "/legal/disclaimer/"), ("Trademark & Copyright Notice", "/legal/trademark/"), ("Cookie Policy", "/legal/cookies/"), ("Editorial Policy", "/legal/editorial-policy/"), ("Sitemap", "/sitemap/")]),
]

def nav_html():
    out = []
    for label, url, sub in NAV:
        if sub:
            items = "".join(f'<li><a href="{u}">{html.escape(t)}<small>{html.escape(d)}</small></a></li>' for t, u, d in sub)
            items += f'<li><a href="{url}" style="font-weight:700;color:var(--brand)">All {label.lower()} →</a></li>'
            out.append(f'<li><a href="{url}" aria-haspopup="true">{label} ▾</a><ul class="sub">{items}</ul></li>')
        else:
            out.append(f'<li><a href="{url}">{label}</a></li>')
    return "".join(out)

def footer_html():
    cols = "".join(
        f'<div><h4>{h}</h4><ul>' + "".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in links) + "</ul></div>"
        for h, links in FOOTER_COLS)
    return f'''
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/"><span class="mark">MP</span><span>My<b>Performance</b><i class="dom">.com</i></span></a>
        <p class="muted small" style="margin-top:12px">Free tools, templates and guides to measure, review and improve your performance at work and in life. Independent, reader-supported, and built for people who want to get better on purpose.</p>
        <div class="share">
          <a class="btn btn-ghost btn-sm" data-youtube-channel href="#" target="_blank" rel="noopener">▶ YouTube</a>
          <a class="btn btn-ghost btn-sm" href="/newsletter/">✉ Newsletter</a>
          <a class="btn btn-ghost btn-sm" href="/support/">♥ Support</a>
        </div>
      </div>
      {cols}
    </div>
    <div class="footer-bottom">
      <p class="disclosure"><strong>Trademark &amp; copyright disclosure.</strong> MyPerformance.com is an independent educational publication. “My Performance” is used purely in its ordinary descriptive sense — <em>your</em> performance — and this website claims no exclusive rights to that phrase. MyPerformance.com is not affiliated with, endorsed by, or sponsored by any company, product, software or organisation that uses “MyPerformance”, “My Performance” or any similar name, in any country. All third-party trademarks, product names, logos and brands mentioned on this site are the property of their respective owners and are used for identification and reference only. Original content on this site is © <span data-year></span> MyPerformance.com. <a href="/legal/trademark/">Read the full notice</a>.</p>
      <p class="disclosure">Content on this site is for general informational and educational purposes and is not professional HR, legal, medical or financial advice. This site is reader-supported and may display advertising and affiliate links; see our <a href="/legal/disclaimer/">Disclaimer</a> and <a href="/legal/privacy/">Privacy Policy</a>.</p>
      <p>© <span data-year></span> MyPerformance.com · <a href="/legal/privacy/">Privacy</a> · <a href="/legal/terms/">Terms</a> · <a href="/legal/trademark/">Trademarks</a> · <a href="/contact/">Contact</a> · Domain, sponsorship &amp; partnership inquiries: <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a></p>
    </div>
  </div>
</footer>'''

NEWSLETTER_BAND = '''
<section class="tight newsletter-band">
  <div class="wrap">
    <div class="leadgen" style="padding:36px">
      <div class="grid g2" style="align-items:center">
        <div>
          <span class="eyebrow" style="color:#fde68a">The Performance Brief</span>
          <h2 style="font-size:1.7rem">One email a week. One idea that moves your performance.</h2>
          <p>Practical review tactics, goal frameworks and productivity systems — plus new tools and templates first. Free. Unsubscribe any time.</p>
        </div>
        <form class="form" data-form="newsletter">
          <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
          <div class="inline-form"><input type="email" name="email" placeholder="you@company.com" required aria-label="Email address"><button class="btn btn-accent" type="submit">Subscribe free</button></div>
          <p class="form-note" style="color:#cbd5e1">Join readers at companies of every size. No spam, ever.</p>
          <div class="form-success">You're in. Watch your inbox for a welcome email.</div>
        </form>
      </div>
    </div>
  </div>
</section>'''

MODAL = '''
<div class="modal" id="newsletter-modal" role="dialog" aria-modal="true" aria-label="Newsletter signup">
  <div class="modal-box">
    <button class="modal-close" aria-label="Close">×</button>
    <span class="eyebrow">Before you go</span>
    <h3>Get the free Performance Review Toolkit</h3>
    <p class="muted">Self-evaluation template, 100 review phrases, and a goal-setting worksheet — delivered instantly, plus our weekly brief.</p>
    <form class="form" data-form="toolkit-download">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
      <input type="email" name="email" placeholder="Your email address" required aria-label="Email">
      <button class="btn btn-primary btn-block" type="submit">Send me the toolkit</button>
      <p class="form-note">Free forever. Unsubscribe with one click.</p>
      <div class="form-success">Sent! Check your inbox (and spam folder) in a minute.</div>
    </form>
  </div>
</div>
<div class="cookie"><span>We use cookies for analytics and to show relevant ads. By using this site you agree to our <a href="/legal/cookies/">cookie policy</a>.</span><button class="btn btn-primary btn-sm" data-cookie-ok>OK, got it</button></div>
<button class="back-top" aria-label="Back to top">↑</button>'''

def layout(meta, body):
    title = meta.get("title", SITE_NAME)
    full_title = title if meta.get("raw_title") else f"{title} | {SITE_NAME}"
    desc = html.escape(meta.get("description", ""))
    url = SITE + meta["url"]
    schema = meta.get("schema")
    schema_html = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    org = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE,
           "potentialAction": {"@type": "SearchAction", "target": SITE + "/search/?q={search_term_string}", "query-input": "required name=search_term_string"}}
    band = "" if meta.get("no_band") else NEWSLETTER_BAND
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{meta.get('og_type','website')}"><meta property="og:site_name" content="{SITE_NAME}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/og-cover.svg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}/assets/img/og-cover.svg">
<meta name="theme-color" content="#1e3a8a">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css">
<script>window.MP_BASE="{BASE}";</script>
<script type="application/ld+json">{json.dumps(org)}</script>
{schema_html}
</head>
<body>
<div class="topbar">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership → <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a></div>
<header class="header">
  <div class="wrap nav">
    <a class="logo" href="/" aria-label="MyPerformance.com home"><span class="mark">MP</span><span>My<b>Performance</b><i class="dom">.com</i></span></a>
    <nav aria-label="Main"><ul class="menu">{nav_html()}</ul></nav>
    <div class="nav-actions">
      <a class="btn btn-ghost btn-sm" href="/search/" aria-label="Search">🔍</a>
      <button class="theme-toggle" data-theme-toggle aria-label="Toggle dark mode">◐</button>
      <a class="btn btn-primary btn-sm" href="/coaching/">Free performance audit</a>
      <button class="burger" data-burger aria-label="Menu" aria-expanded="false">☰</button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
{band}
{footer_html()}
{MODAL}
<script src="/assets/js/main.js" defer></script>
{meta.get("scripts","")}
</body>
</html>'''

def parse_meta(text):
    m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->", text, re.S)
    if not m:
        raise SystemExit("Missing META block")
    return json.loads(m.group(1)), text[m.end():]

def write(path, content):
    if BASE and path.endswith(".html"):
        content = (content.replace('href="/', f'href="{BASE}/').replace('src="/', f'src="{BASE}/')
                          .replace("href='/", f"href='{BASE}/").replace('action="/', f'action="{BASE}/'))
    elif BASE and path.endswith(".json"):
        content = content.replace('"url": "/', f'"url": "{BASE}/')
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def slugify_heading(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def guide_page(meta, md_text):
    md = markdown.Markdown(extensions=["tables", "toc", "fenced_code", "attr_list"], extension_configs={"toc": {"toc_depth": "2-2"}})
    body_html = md.convert(md_text)
    toc = md.toc if "<li>" in md.toc else ""
    toc_html = f'<div class="toc"><strong>In this guide</strong>{toc}</div>' if toc else ""
    # in-article ad after 3rd h2
    parts = body_html.split("<h2")
    if len(parts) > 3:
        rebuilt = [parts[0]]
        for i, p in enumerate(parts[1:], start=1):
            rebuilt.append(('<div class="ad-slot" data-slot="in-article">Advertisement</div>' if i == 3 else '') + "<h2" + p)
        body_html = "".join(rebuilt)
    words = len(re.findall(r"\w+", md_text))
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": meta["title"], "description": meta["description"],
              "author": {"@type": "Organization", "name": "MyPerformance.com Editorial Team"}, "publisher": {"@type": "Organization", "name": SITE_NAME},
              "datePublished": meta.get("date", TODAY), "dateModified": TODAY, "mainEntityOfPage": SITE + meta["url"]}
    meta["schema"] = schema; meta["og_type"] = "article"
    related = "".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in meta.get("related", []))
    body = f'''
<div class="wrap"><p class="breadcrumb"><a href="/">Home</a> › <a href="/guides/">Guides</a> › {html.escape(meta["title"])}</p></div>
<section class="tight"><div class="wrap with-side">
  <article class="prose">
    <span class="badge">{html.escape(meta.get("category","Guide"))}</span>
    <h1 style="margin-top:12px">{html.escape(meta["title"])}</h1>
    <p class="lead muted" style="font-size:1.15rem">{html.escape(meta["description"])}</p>
    <div class="meta"><span>By MyPerformance.com Editorial Team</span><span>Updated {TODAY}</span><span>{max(3, words // 220)} min read</span></div>
    <div class="ad-slot leader" data-slot="guide-top">Advertisement</div>
    {toc_html}
    {body_html}
    <div class="share"><strong style="align-self:center">Share:</strong> <a class="btn btn-ghost btn-sm" data-share="linkedin" href="#">LinkedIn</a><a class="btn btn-ghost btn-sm" data-share="x" href="#">X</a><a class="btn btn-ghost btn-sm" data-share="facebook" href="#">Facebook</a><a class="btn btn-ghost btn-sm" data-share="whatsapp" href="#">WhatsApp</a><a class="btn btn-ghost btn-sm" data-share="copy" href="#">Copy link</a></div>
    <div class="author"><div class="av">MP</div><div><strong>MyPerformance.com Editorial Team</strong><br><span class="muted small">We research, test and simplify the best thinking on workplace and personal performance. Our content is independent and reader-supported. <a href="/legal/editorial-policy/">Editorial policy</a>.</span></div></div>
    <div class="ad-slot leader" data-slot="guide-bottom">Advertisement</div>
  </article>
  <aside>
    <div class="card flat" style="margin-bottom:20px"><span class="eyebrow">Free toolkit</span><h3>Performance Review Toolkit</h3><p class="muted small">Self-evaluation template + 100 phrases + goal worksheet.</p>
      <form class="form" data-form="toolkit-download"><input type="text" name="_honey" class="hp" tabindex="-1"><input type="email" name="email" placeholder="Email address" required aria-label="Email"><button class="btn btn-primary btn-block" type="submit">Send it free</button><div class="form-success">Sent — check your inbox.</div></form></div>
    <div class="card flat" style="margin-bottom:20px"><h3>Try the tools</h3><ul class="list-check small"><li><a href="/tools/self-evaluation-generator/">Self-Evaluation Generator</a></li><li><a href="/tools/performance-review-phrases/">Review Phrase Library</a></li><li><a href="/tools/smart-goal-builder/">SMART Goal Builder</a></li><li><a href="/tools/performance-score/">Performance Score Quiz</a></li></ul></div>
    {"<div class='card flat' style='margin-bottom:20px'><h3>Related guides</h3><ul class='list-check small'>" + related + "</ul></div>" if related else ""}
    <div class="ad-slot rect sticky-side" data-slot="guide-side">Advertisement</div>
  </aside>
</div></section>'''
    return body

def main():
    import shutil
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for f in ("manifest.webmanifest", "ads.txt", ".nojekyll", "CNAME"):
        if os.path.exists(os.path.join(ROOT, f)):
            shutil.copy(os.path.join(ROOT, f), OUT)
    pages = []
    # HTML pages
    for f in sorted(glob.glob(os.path.join(ROOT, "src/pages/**/*.html"), recursive=True)):
        meta, body = parse_meta(open(f, encoding="utf-8").read())
        out = "index.html" if meta["url"] == "/" else (meta["url"].lstrip("/") if meta["url"].endswith(".html") else meta["url"].rstrip("/") + "/index.html")
        write(out, layout(meta, body))
        pages.append(meta)
    # Guides
    guides = []
    for f in sorted(glob.glob(os.path.join(ROOT, "src/guides/*.md"))):
        text = open(f, encoding="utf-8").read()
        m = re.match(r"\s*```json\s*(\{.*?\})\s*```", text, re.S)
        meta = json.loads(m.group(1)); md_text = text[m.end():]
        meta["section"] = "Guide"
        write(meta["url"].rstrip("/") + "/index.html", layout(meta, guide_page(meta, md_text)))
        pages.append(meta); guides.append(meta)
    # Guides index
    cards = "".join(f'<a class="card reveal" href="{g["url"]}"><span class="badge">{html.escape(g.get("category","Guide"))}</span><h3>{html.escape(g["title"])}</h3><p class="muted small">{html.escape(g["description"])}</p><span class="small" style="font-weight:700">Read guide →</span></a>' for g in guides)
    gmeta = {"title": "Guides — Performance Reviews, Goals & Productivity", "description": "In-depth, practical guides on performance reviews, self-evaluations, goal setting, feedback, promotions and productivity systems.", "url": "/guides/", "section": "Guides"}
    gbody = f'''<section class="hero"><div class="wrap"><span class="eyebrow">Guides</span><h1>Performance guides that actually get used</h1><p class="lead">Research-backed, plain-English playbooks for reviews, goals, feedback, promotions and focus. Every guide pairs with a free tool or template.</p></div></section>
<section class="tight"><div class="wrap"><div class="ad-slot leader" data-slot="guides-top">Advertisement</div><div class="grid g3">{cards}</div></div></section>'''
    write("guides/index.html", layout(gmeta, gbody)); pages.append(gmeta)
    # Search index
    idx = [{"title": p["title"], "description": p.get("description", ""), "url": p["url"], "section": p.get("section", "Page"), "tags": p.get("tags", "")} for p in pages if not p.get("noindex")]
    write("assets/data/search-index.json", json.dumps(idx, indent=0))
    # Sitemap + robots
    urls = "".join(f"<url><loc>{SITE}{p['url']}</loc><lastmod>{TODAY}</lastmod><changefreq>{'weekly' if p.get('section') in ('Guide','Tool') else 'monthly'}</changefreq><priority>{'1.0' if p['url']=='/' else '0.8' if p.get('section') in ('Tool','Template','Guide') else '0.5'}</priority></url>" for p in pages if not p.get("noindex"))
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    # HTML sitemap page
    groups = {}
    for p in pages:
        if p.get("noindex"): continue
        groups.setdefault(p.get("section", "Page"), []).append(p)
    smap = "".join(f'<div class="card flat"><h3>{s}</h3><ul class="list-check small">' + "".join(f'<li><a href="{p["url"]}">{html.escape(p["title"])}</a></li>' for p in sorted(ps, key=lambda x: x["title"])) + "</ul></div>" for s, ps in sorted(groups.items()))
    smeta = {"title": "Sitemap", "description": "Every page on MyPerformance.com.", "url": "/sitemap/", "section": "Page", "no_band": True}
    write("sitemap/index.html", layout(smeta, f'<section><div class="wrap"><h1>Sitemap</h1><div class="grid g3">{smap}</div></div></section>'))
    print(f"Built {len(pages)+1} pages.")

if __name__ == "__main__":
    main()
