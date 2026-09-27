# MyPerformance.com — Phase-wise Build Prompts

Use these prompts, in order, with any capable AI coding assistant (or a developer) to build, extend and operate MyPerformance.com. Each phase is self-contained, states its inputs, and ends with an acceptance checklist. The current repository already implements Phases 0–6; Phases 7–10 are the growth roadmap.

Global constraints that apply to **every** prompt:

- Static site only (HTML/CSS/JS, no server code) so it hosts on the GitHub Pages free plan.
- The only contact email is the one stored base64-encoded in `assets/js/main.js` (`CONFIG.contactEncoded`). It must never appear in plain text anywhere in the repo or rendered output. All forms and mail links resolve it at runtime.
- Every page carries the top bar: *"Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership → web.works/contact"* linking to `https://web.works/contact`.
- "My Performance" is used descriptively; no ™/® claims; the trademark/copyright disclosure stays in the footer and at `/legal/trademark/`.
- Mobile-first, accessible (labels, contrast, keyboard), no horizontal overflow at 360px.
- Ads only via `.ad-slot` placeholders activated by `CONFIG.adsenseClient`; never above the primary tool on a tool page.

---

## Phase 0 — Positioning & information architecture

**Prompt.** "You are building MyPerformance.com, an independent, ad-supported, reader-supported website about workplace and personal performance: performance reviews, self-evaluations, goal setting (SMART/OKR), raises and promotions, feedback, 1:1s, productivity and focus. Audience: employees preparing for reviews, managers, HR/People teams, founders. Monetisation: Google AdSense display, sponsorships, HR-software/coaching affiliate leads, YouTube, donations. Produce: (1) a one-sentence positioning statement; (2) a sitemap with these top-level sections — Tools, Templates, Guides, Videos, Coaching (lead-gen), Support (donations), Advertise, Careers, Contests, About, Contact, Newsletter, Search, Legal; (3) the primary keyword cluster for each section; (4) a conversion map: which pages feed the newsletter, the toolkit download, the free performance audit form, and the advertiser inquiry form."

**Accept when:** sitemap has ≤ 6 primary nav items; every tool and template page has an assigned target keyword; every page has exactly one primary CTA.

## Phase 1 — Design system & shell

**Prompt.** "Create a single stylesheet `assets/css/main.css` with CSS variables for light and dark themes (`data-theme` on `<html>`), Inter from Google Fonts, an 1180px container, card/button/badge/form/table primitives, a sticky translucent header with a mega-menu for Tools and Templates and a hamburger under 1000px, a gradient hero, a `.leadgen` dark panel, `.ad-slot` placeholders (leaderboard, rectangle, sticky sidebar), FAQ `<details>`, modal, cookie notice, back-to-top, and print styles that hide chrome and ads. Create `build.py`, a Python generator that wraps HTML fragments in `src/pages/**` and Markdown in `src/guides/*.md` with the shared layout, emits `sitemap.xml`, `robots.txt`, an HTML sitemap and `assets/data/search-index.json`. The layout must include: the web.works/contact top bar, header, footer with five link columns, the trademark/copyright disclosure paragraph, affiliate/ads disclosure, a newsletter band, an exit-intent newsletter modal, JSON-LD WebSite schema, Open Graph/Twitter meta, canonical URLs, favicon and web manifest."

**Accept when:** `python3 build.py` regenerates the whole site; Lighthouse accessibility ≥ 95 on the home page; no plain-text email in any output file (`grep -r` returns nothing).

## Phase 2 — Runtime (`assets/js/main.js`)

**Prompt.** "Write one dependency-free JS file with a `CONFIG` block (site name, base64 contact address, AdSense client, YouTube channel and video IDs, donation URLs, GA4 ID). Implement: theme toggle with `localStorage`; hamburger nav; `[data-mail]` links that build a `mailto:` from the decoded address only on hover/focus/click; `form[data-form]` handling that POSTs JSON to `https://formsubmit.co/ajax/<decoded address>` with a honeypot field, a table template and a subject prefix, falling back to a pre-filled `mailto:` if the request fails, then shows the sibling `.form-success`; `[data-multistep]` forms with `.fstep` panels, `.choice` tiles and a progress bar; AdSense injection into `.ad-slot` when `CONFIG.adsenseClient` is set; optional GA4 loader and `mpTrack(event, params)`; YouTube grid rendering from `CONFIG.youtubeVideos` (privacy-enhanced embeds) with a 'subscribe' fallback; `[data-donate]` buttons that take their href from `CONFIG.donate` or degrade to a mail link; share buttons; `mpCopy`, `mpDownload`, `mpPrint` helpers; scroll reveal with a 2.5s fallback; animated counters; cookie notice; exit-intent + 45s newsletter modal shown once; client-side site search over the JSON index."

**Accept when:** submitting any form with the network blocked opens the mail client with the fields in the body; hovering a contact link produces a `mailto:` containing `@` while the page source contains none.

## Phase 3 — Interactive tools (9)

**Prompt.** "Build the following as self-contained pages under `/tools/<slug>/`, each with the tool at the top, a leaderboard ad slot below it, 400–600 words of explanatory SEO content, a sticky sidebar ad, related links, and JSON-LD via the layout. All state stays in the browser.
1. **Self-Evaluation Generator** — six inputs (name, role, period, tone, 3 achievements, challenge, strengths, development areas, goals, support) → five-section self-appraisal; live preview; copy / download .txt / print; 'load example'.
2. **Performance Review Phrase Library** — loads `assets/data/phrases.json` (12 competencies × 3 rating levels × 7 phrases with `{N} {n} {o} {p} {X}` placeholders); filters by competency and rating; search; manager mode with name and pronouns, self-evaluation mode that converts to first person (conjugating the verb after 'I' and an optional adverb); per-phrase copy and copy-all.
3. **SMART Goal Builder** — S/M/A/R/T inputs with baseline→target, deadline, owner, cadence → goal statement, % change, 25/50/75/100% milestones with dates and interpolated targets, scoring rubric.
4. **Performance Score Quiz** — 24 Likert statements across 8 dimensions; progress bar; results ring, per-dimension bars coloured by band, three priority actions with links, hidden score fields feeding an email-capture form for the full report; share and copy summary; non-diagnostic disclaimer.
5. **Raise & Promotion Calculator** — salary, ask %, default %, inflation, future raises, optional promotion salary → new salary, monthly delta, real change vs inflation, 1/3/5/10-year cumulative gap table, promotion comparison notice.
6. **Productivity Calculator** — hours, meetings, comms, admin, interruptions/hour, skippable-meeting % , optional salary → real focus hours and ratio, recoverable hours/week and /year, stacked bars, meeting cost, recovery plan.
7. **1:1 Agenda Builder** — role (manager/report), length, meeting type (weekly/monthly/pre-review/first/skip-level), focus chips → timed agenda with questions and commitments.
8. **Habit & Streak Tracker** — up to 8 habits, 7-day grid with week navigation, completion %, longest streak, total check-ins, JSON export, reset; `localStorage` key `mp-habits`.
9. **Focus Timer** — presets 25/5, 52/17, 90/20, 45/15; task name; tab-title countdown; sound and optional notification; today's focused minutes, sessions, all-time hours in `localStorage`."

**Accept when:** each tool produces a copy-able result with no console errors on desktop and 390px mobile; a Playwright run completes the quiz and reads a score.

## Phase 4 — Templates (6) and guides (12)

**Prompt.** "Under `/templates/<slug>/`, create editable-in-browser templates (a monospace `<textarea>` pre-filled from a JS string, with Copy / Download .txt / Download .md / Print / Reset, filling instructions and 300–500 words of guidance): Performance Review (8 competencies with evidence, development plan, sign-off), Self-Evaluation (5 sections), 30-60-90 Day Plan, OKR Worksheet (scored KRs, 12-week log, retrospective), Performance Improvement Plan (with a legal-review notice), 1:1 Meeting (structure, question bank, log). Under `src/guides/`, write twelve 900–1,300-word Markdown guides with JSON front matter (`title, description, url, category, tags, related`): how to write a self-evaluation; 150 review phrases by competency; 30 SMART goal examples by department; how to ask for a raise (script, data, timing); the deep work schedule; 12 personal KPIs; how to give feedback; how to get promoted (12-month playbook); OKRs for individuals; the 20-minute weekly review; how to run a performance review meeting; what to do after a bad review. Every guide links to at least two tools/templates and has a TOC, author box, share row and an in-article ad after the third H2."

**Accept when:** all internal links resolve (automated check reports 0 broken); every guide renders a table of contents; templates download with the correct filename.

## Phase 5 — Monetisation, lead-gen and community pages

**Prompt.** "Build: `/coaching/` — a dedicated, high-converting lead-generation page: five-step multi-step form (role → goal → timeline → team size → contact + consent), benefits, individual vs manager/HR sections, three-step process, FAQ, sticky CTA; `/support/` — donation page with one-time/monthly toggle, $5/$15/$30/$100 presets plus custom, impact copy that updates, PayPal / Buy Me a Coffee / Ko-fi / Patreon buttons driven by `CONFIG.donate`, transparency allocation, non-monetary support options, supporter wall; `/advertise/` — sponsored tool, newsletter sponsorship, display, content partnerships, affiliate, domain acquisition, media-kit request form, audience and standards; `/careers/` — open roles cards and a two-minute application form; `/contests/` — monthly Performance Challenge with prize tiers, four-step process, registration form with age/rules consent, and full contest rules including platform non-affiliation; `/videos/` — YouTube grid from config, upcoming series, video-request form; `/newsletter/`, `/about/`, `/contact/` (form + hidden mail link + web.works/contact pointer), `/search/`, `/404.html`."

**Accept when:** every form posts through the shared handler; the coaching form cannot be submitted without consent; donation buttons degrade gracefully when URLs are blank.

## Phase 6 — Legal, SEO and deployment

**Prompt.** "Write `/legal/privacy/` (GDPR/UK GDPR/CCPA/PIPEDA/Quebec Law 25, AdSense cookie disclosure and opt-out links, local-storage disclosure), `/legal/terms/` (template licence, donations, contests, limitation of liability), `/legal/disclaimer/` (no professional advice, assessment limits, affiliate disclosure), `/legal/cookies/` (table of cookies and local-storage keys), `/legal/editorial-policy/`, `/legal/trademark/` (descriptive use of 'My Performance', no affiliation, third-party marks, copyright licence, takedown process). Add `ads.txt` placeholder, `.nojekyll`, `manifest.webmanifest`, SVG favicon and OG image, `robots.txt`, `sitemap.xml`. Add `.github/workflows/pages.yml` that installs `markdown`, runs `python3 build.py` with `SITE_URL` set to the custom domain (from `CNAME`) or the project Pages URL, uses `actions/configure-pages@v5` with `enablement: true`, `upload-pages-artifact` (path `_site`) and `deploy-pages` so a push to `main` publishes the site. Push to `github.com/webworksa1/myperformance-com`."

**Accept when:** the workflow is green and the site is served at `https://webworksa1.github.io/myperformance-com/` (or the custom domain once `CNAME` + DNS are set).

---

## Phase 7 — Activation (first week after launch)

**Prompt.** "Fill `CONFIG` in `assets/js/main.js`: AdSense publisher ID (after approval; also replace `ads.txt`), GA4 ID, YouTube channel URL and 6–12 video IDs, donation URLs. Activate the FormSubmit endpoint by submitting the contact form once and clicking the confirmation email. Add a `CNAME` file containing `myperformance.com` and point DNS (A records to GitHub Pages IPs and `www` CNAME to `webworksa1.github.io`), then enable 'Enforce HTTPS'. Submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools. Verify all `.ad-slot` positions render responsive units and none appear above the primary tool."

## Phase 8 — Content engine (months 1–3)

**Prompt.** "Produce a 12-week editorial calendar: two guides per week targeting long-tail queries in the clusters 'performance review phrases for <competency>', 'self evaluation examples for <role>', 'SMART goals for <department>', '30-60-90 day plan for <role>'. For each guide, generate the Markdown with front matter in the house style (numbers in every example, action→result→impact, links to two tools), plus a 60-second video script and three social posts. Add one new template per month (e.g. peer review form, career development plan, meeting audit sheet)."

## Phase 9 — Conversion optimisation (months 2–6)

**Prompt.** "Instrument events with `mpTrack`: tool completion, copy/download, quiz score bands, form submissions by type, modal opens. Build a weekly report from GA4. Run A/B variants on: hero CTA wording, quiz result email-capture copy, coaching form step order, donation presets. Add a results-page sponsorship slot in the Performance Score quiz and the Raise Calculator (highest-intent moments) sold via `/advertise/`. Implement the 'Performance Review Toolkit' PDF (six templates + 100 phrases + checklist) delivered by autoresponder."

## Phase 10 — Expansion

**Prompt.** "Add: (a) role-specific tool variants (self-evaluation for nurses, engineers, teachers, sales) as thin pages sharing the generator; (b) a 'Compare HR software' affiliate hub with honest comparison tables; (c) a community submission flow for contest write-ups with moderation; (d) multi-language versions (FR, ES, HI) of the top five tools using the same generator; (e) a lightweight Progressive Web App install prompt for the tools. Keep the static-only constraint: any feature needing a backend goes through a free-tier third-party service (FormSubmit, Buttondown/MailerLite, Ko-fi) configured in `CONFIG`."
