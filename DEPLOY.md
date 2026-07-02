# Preview the site

## Open on a computer (easiest — no server needed)

The file `public/biscuit-and-brew-ipad.html` is a single, fully self-contained
page (catalog, images and the hero video are all embedded). On any computer it
just opens — no server, no internet:

1. Download it: open
   `https://github.com/mademoisellejulia4-svg/BB/raw/claude/biscuit-brew-website-gnwai3/public/biscuit-and-brew-ipad.html`
   (or grab the file from the repo).
2. **Double-click the downloaded file** — it opens in your default browser
   (Chrome, Edge, Firefox or Safari) and the hero video plays as you scroll.

> On a desktop browser everything works, including the embedded hero video —
> the data-URI video limitation only affects iPad/iOS Safari.

## Run the full served site on a computer

To run the real Express server (live `index.html`, hot data from
`data/products.json`):

```bash
npm install
npm start
```

Then open **http://localhost:3000** in your browser. Stop with `Ctrl-C`.

---

# Private preview — from an iPad, with no computer

The site is fully static (HTML + `data/products.json` + `Video.mp4`). You can
preview it privately on your iPad without a Mac or PC. Two good options:

---

## Option A — GitHub Codespaces (recommended: private, runs the real server)

A Codespace is a cloud computer that opens in iPad Safari. It runs `server.js`
for you, and the preview URL is **private by default** — only you, signed into
GitHub, can open it. Nothing is public.

1. In Safari, go to your repo: `https://github.com/mademoisellejulia4-svg/BB`
2. Switch to the branch **`claude/biscuit-brew-website-gnwai3`**.
3. Tap the green **`< > Code`** button → **Codespaces** tab →
   **Create codespace on this branch**. Wait ~1 minute for it to build
   (it auto-runs `npm install`).
4. When the editor loads, open a **Terminal** (menu ☰ → Terminal → New Terminal)
   and run:
   ```bash
   npm start
   ```
5. A popup says *"Application running on port 3000"* → tap **Open in Browser**.
   (Or open the **Ports** tab and tap the 🌐 globe next to port 3000.)
   The port is set to **Private** in `.devcontainer/devcontainer.json`, so the
   `*.app.github.dev` URL only works while you're signed into GitHub.

To stop: press `Ctrl-C` in the terminal, then stop the Codespace from the
Codespaces list so it doesn't use your free hours.

> Free GitHub accounts include a monthly allowance of Codespaces hours — plenty
> for testing. Stop the Codespace when you're done.

---

## Option B — Cloudflare Pages + Access (free, private, always-on URL)

Use this if you want a stable link you can revisit without starting anything.
It hosts the static files and gates them behind your email (one-time PIN), so
only you can view it — it is **not** public.

1. Create a free Cloudflare account at `dash.cloudflare.com` (works in Safari).
2. **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → authorize
   GitHub and pick this repo.
3. Build settings:
   - **Production branch:** `claude/biscuit-brew-website-gnwai3`
   - **Build command:** *(leave empty)*
   - **Build output directory:** `public`
   - Deploy. You'll get a `https://<name>.pages.dev` URL.
4. Make it private: go to **Zero Trust** → **Access** → **Applications** →
   **Add an application** → **Self-hosted**. Set the domain to your
   `<name>.pages.dev`. Add a **policy** → Action **Allow**, rule
   **Emails** = your email address.
5. Now visiting the URL on your iPad asks for your email and emails you a
   one-time code. Anyone without your inbox is blocked.

---

## Notes

- Always open the served URL (Codespaces port URL or the `.pages.dev` URL), not
  the raw `index.html` file — the page `fetch`es the catalog JSON and video,
  which browsers block from a `file://` path.
- To change prices/sizes/copy later, edit `public/data/products.json` only.
- Nothing here makes the GitHub repository itself public; keep the repo private.
