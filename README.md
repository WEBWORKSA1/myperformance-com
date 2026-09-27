# MyPerformance.com

Free tools, templates and guides to measure, review and improve performance at work and in life. Static site (HTML/CSS/JS), hosted on GitHub Pages (free plan), monetised via Google AdSense, sponsorships, affiliate leads, YouTube and reader donations.

**Live:** https://webworksa1.github.io/myperformance-com/ (custom domain: add a `CNAME` file containing `myperformance.com` and point DNS — see below).

**First-time activation:** see [`setup/README.md`](setup/README.md) — one file to add through the GitHub UI and the site deploys itself.

## Structure

```
build.py                 static generator: src/ → _site/
src/pages/**/*.html      page fragments with <!--META {...}--> front matter
src/guides/*.md          Markdown guides with JSON front matter
assets/css/main.css      single stylesheet (light/dark)
assets/js/main.js        runtime + CONFIG (ads, YouTube, donations, analytics, hidden contact address)
assets/data/phrases.json review phrase library
assets/data/search-index.json  generated
docs/                    phase-wise build prompts, competitor research
setup/pages.yml          GitHub Pages workflow — copy to .github/workflows/pages.yml
```

The GitHub Actions workflow builds `_site/` and deploys it to GitHub Pages on every push to `main`; generated output is not committed.

## Build

```
python3 -m pip install markdown
python3 build.py
cd _site && python3 -m http.server 8080   # preview
```

Set `SITE_URL` to build for a different host (the workflow sets it to the project Pages URL, or to the `CNAME` domain when that file exists).

## Configure (assets/js/main.js → CONFIG)

| Key | What |
|---|---|
| `contactEncoded` | base64 of the only contact address. Never write the address in plain text anywhere. |
| `adsenseClient` | `ca-pub-…` — activates every `.ad-slot`. Also update `ads.txt`. |
| `youtubeChannel`, `youtubeVideos` | Channel URL and video IDs for `/videos/` |
| `donate.*` | PayPal / Buy Me a Coffee / Ko-fi / Patreon URLs for `/support/` |
| `ga4` | Google Analytics 4 measurement ID |

Forms post via FormSubmit (AJAX) to the decoded address; the first submission triggers a one-time activation email. If the request fails, the visitor's mail client opens pre-filled.

## Custom domain

1. Add a file `CNAME` at the repo root containing `myperformance.com`.
2. DNS: `A` records for the apex to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `CNAME www → webworksa1.github.io`.
3. Repo → Settings → Pages → Custom domain → enforce HTTPS.
4. Push; the workflow rebuilds with the custom domain as the canonical URL.

## Content rules

- Tools run in the browser; nothing typed is uploaded.
- Every page shows the top bar linking to https://web.works/contact.
- Trademark/copyright disclosure is in the footer and at `/legal/trademark/`. "My Performance" is used descriptively; no ™/® claims.
- Sponsored content is labelled; see `/legal/editorial-policy/`.

## Roadmap

See `docs/PHASE-WISE-BUILD-PROMPTS.md` (Phases 7–10).
