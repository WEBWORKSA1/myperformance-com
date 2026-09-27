# Activating GitHub Pages (one-time, ~1 minute)

The site builds and deploys itself through GitHub Actions, but GitHub does not allow API integrations to create workflow files, so the workflow must be added once through the GitHub web UI:

1. Open https://github.com/webworksa1/myperformance-com → **Add file** → **Create new file**.
2. File name: `.github/workflows/pages.yml`
3. Paste the full contents of `setup/pages.yml` (the comment lines at the top are fine to keep or remove).
4. **Commit changes** to `main`.

The workflow runs immediately: it installs the Markdown library, runs `build.py`, enables GitHub Pages for the repository (`enablement: true`), and deploys `_site/`. Within about two minutes the site is live at:

**https://webworksa1.github.io/myperformance-com/**

Every later push to `main` redeploys automatically. Progress and the live URL appear under the **Actions** tab.

## Custom domain (when ready)

1. Add a file `CNAME` at the repo root containing `myperformance.com`.
2. DNS at the registrar: `A` records for the apex → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `CNAME www` → `webworksa1.github.io`.
3. Settings → Pages → Custom domain → `myperformance.com` → Enforce HTTPS.

The build reads `CNAME` and switches every canonical URL, sitemap entry and internal link to the custom domain automatically.
