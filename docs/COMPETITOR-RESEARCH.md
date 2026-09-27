# Competitor & Reference Research — 36 sites

Research conducted September 2026 to define the feature set for MyPerformance.com. Sites were fetched live (homepage plus one key inner page); four were blocked by the fetch proxy and are marked *(public knowledge)*.

## Sites surveyed

**HR / performance-management publishers & SaaS:** Indeed Career Guide, BetterUp, Lattice Library, Culture Amp, 15Five, Leapsome, The Muse, Asana Resources, Atlassian Work Life, MindTools, HBR Managing Yourself, SHRM, PerformYard, Effy AI, AIHR, Smartsheet templates, HubSpot Resources.
**Productivity & personal performance:** James Clear, Todoist Productivity Methods, Zapier Blog, Tony Robbins, Coursera Personal Development, 16Personalities, Psychology Today Tests.
**Calculator / tool aggregators (ad-monetised models):** Calculator.net, Omni Calculator, NerdWallet, Forbes Advisor, Investopedia *(public knowledge)*, wikiHow *(public knowledge)*, Template.net.
**Health & fitness performance (ad + affiliate models):** Healthline Fitness, Verywell Mind *(public knowledge)*, Strava, MyFitnessPal Blog.
**Donation UX benchmark:** Wikipedia / Wikimedia fundraising *(public knowledge; donate pages blocked)*.

## Feature matrix → what MyPerformance.com implements

| # | Feature (prevalence across sites) | Revenue impact | Implemented as |
|---|---|---|---|
| 1 | Free interactive tools with results panel (Calculator.net, Omni, Todoist quiz, PerformYard grader, 16Personalities) | High — traffic + ad inventory | 9 tools under `/tools/` |
| 2 | Ungated templates in multiple formats (Smartsheet, Template.net, Lattice) | High — SEO + trust | 6 editable templates, copy/.txt/.md/print |
| 3 | Long-form educational content around each tool (Omni, Healthline, Investopedia) | High — ad inventory | 400–600 words on every tool/template page |
| 4 | Persistent newsletter capture: nav, inline, exit-intent (16/18 sites) | High | Newsletter band on every page, exit-intent modal, sidebar form, `/newsletter/` |
| 5 | Gated flagship asset (HubSpot, Lattice, Leapsome reports) | High — leads | "Performance Review Toolkit" email capture |
| 6 | Result-page upsell at peak engagement (16Personalities, Psychology Today) | High | Quiz result → "full report" email form; sponsorship slot planned |
| 7 | Demo / consultation CTA, sticky (14+ sites) | High | "Free performance audit" header CTA + `/coaching/` multi-step form |
| 8 | Ad slots beside results and between content blocks, never above the tool | High | `.ad-slot` leader/rect/sticky-side placements |
| 9 | Category mega-menu with descriptions (Healthline, Asana, HubSpot) | Medium | Tools/Templates mega-menus |
| 10 | Related-tool / related-guide cross-links (12 sites) | Medium — session depth | Sidebar and in-body links on every page |
| 11 | Author bylines, updated dates, editorial policy (10 sites) | Medium — E-E-A-T | Author box, dates, `/legal/editorial-policy/` |
| 12 | Trust bar of frameworks/logos (14 sites) | Medium | Frameworks strip on home |
| 13 | Non-diagnostic disclaimer + privacy note on assessments (Psychology Today) | Medium — completion rate | On quiz page and `/legal/disclaimer/` |
| 14 | Low-friction donation: presets, one-time/monthly, minimal fields (Wikimedia) | Medium | `/support/` |
| 15 | Advertise-with-us / media kit page (Investopedia, Forbes) | Medium | `/advertise/` with inquiry form |
| 16 | Careers page (8 sites) | Low — legitimacy | `/careers/` with application form |
| 17 | Contests / community programmes (Strava challenges, HubSpot community) | Medium — retention, email | `/contests/` monthly challenge |
| 18 | Video module (10 sites) | Medium — YouTube revenue | `/videos/` + config-driven embeds |
| 19 | Site search + JSON index (12 sites) | Low | `/search/` client-side |
| 20 | Dark mode, mobile-first nav, print styles | Low — UX | Global |
| 21 | Legal cluster: privacy, terms, cookies, disclaimer, trademark (12 sites) | Low — AdSense approval requirement | `/legal/*` |
| 22 | Comparison / "best X software" pages (Forbes, NerdWallet, Effy) | High — affiliate | Roadmap Phase 10 |
| 23 | Role- and industry-specific landing pages (PerformYard, 15Five) | Medium — SEO | Roadmap Phase 10 |
| 24 | Community forum / UGC (Healthline Bezzy) | Low–Medium | Roadmap Phase 10 |

## Niche economics used for the decision

- AdSense RPM bands (2026 industry estimates): Business $20–40, B2B services $25–50, Software/SaaS $30–65, Career & jobs $12–25, Education $15–30, Health $18–35, Fitness $10–22.
- YouTube typical US RPM: Business $18, Education $12, Health $14, Careers $11, Self-help $7.50.
- The performance-review / goal-setting cluster is served by HR SaaS publishers (Lattice, 15Five, Leapsome, Culture Amp, PerformYard, Effy) whose demo-request economics support high CPCs and paid referral partnerships — the ad pool MyPerformance.com sits in.

## Sources

adstimate.com (AdSense RPM by category), fluxnote.io (YouTube RPM by niche 2026), and the 36 sites above.
