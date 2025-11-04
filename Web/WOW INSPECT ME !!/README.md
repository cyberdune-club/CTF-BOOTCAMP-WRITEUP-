# CYBERDUNE — Inspect Me (Static Web Challenge)

A static, Netlify-friendly web challenge inspired by classic "Inspect" tasks.
The flag is split across **three places**:
1. An HTML comment in `index.html`
2. A CSS comment in `css/style.css`
3. A JavaScript comment in `js/app.js`

## Host on Netlify
- **Netlify Drop**: drag the whole folder (or the ZIP) into https://app.netlify.com/drop
- **Or via Git**: push these files to a repo and connect the repo on Netlify. No build step required.
- **Or via CLI**:
  ```bash
  npm i -g netlify-cli
  netlify deploy --dir .
  # then netlify deploy --dir . --prod
  ```

## Local preview
Open `index.html` directly, or serve with any static server:
```bash
python3 -m http.server 8080
```
