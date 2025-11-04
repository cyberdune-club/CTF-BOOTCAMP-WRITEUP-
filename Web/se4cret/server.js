// Minimal CTF web challenge inspired by 'Secrets'
// Vulnerable message board + report-to-admin with headless bot.
// The flag is placed in the admin's non-HttpOnly cookie so an XSS can steal it.
// Port: process.env.PORT (default 31347).

const express = require("express");
const cookieParser = require("cookie-parser");
const { v4: uuidv4 } = require("uuid");
const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

const PORT = process.env.PORT || 31347;

// --- Flag source: ENV FLAG or /app/flag.txt ---
function getFlag() {
  const envFlag = process.env.FLAG;
  if (envFlag && /^CYBERDUNE\{.*\}$/.test(envFlag)) return envFlag;
  try {
    const p = path.join(process.cwd(), "flag.txt");
    const f = fs.readFileSync(p, "utf8").trim();
    if (/^CYBERDUNE\{.*\}$/.test(f)) return f;
  } catch(e) {}
  return "CYBERDUNE{set_me_with_ENV_FLAG_or_flag.txt}";
}

// In-memory stores (simple on purpose)
const messages = []; // {id, content, createdAt}
const reports = [];  // message ids
const logs = [];     // {time, ip, data}

// Very naive "sanitizer" (intentionally flawed for the challenge)
// Strips <script> blocks but allows event handlers and SVG/XML payloads.
function weakSanitize(input) {
  if (typeof input !== "string") return "";
  // Remove script tags
  let out = input.replace(/<\s*script[\s\S]*?>[\s\S]*?<\s*\/\s*script\s*>/gi, "");
  // Optionally limit length
  if (out.length > 2000) out = out.slice(0, 2000);
  return out;
}

// Simple pages
function pageTemplate(body) {
  return `<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>CYBERDUNE Board</title>
    <style>
      body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height:1.45; }}
      .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin: 1rem 0; }}
      input, textarea, button {{ font-size: 1rem; padding: 0.4rem; }}
      code {{ background: #f7f7f7; padding: 0.2rem 0.4rem; border-radius: 6px; }}
    </style>
  </head>
  <body>
    <h1>CYBERDUNE — Message Board</h1>
    <p>Submit a message below. An <em>admin bot</em> can review a message if you <strong>report</strong> it.
    Beware our "sanitizer" is… minimal.</p>
    <nav>
      <a href="/">Home</a> · 
      <a href="/logs">Logs</a> · 
      <a href="/health">Health</a>
    </nav>
    ${body}
    <footer style="margin-top:3rem;opacity:.7">Port <code>${PORT}</code></footer>
  </body>
</html>`;
}

// Home page: list + form
app.get("/", (req, res) => {
  const list = messages.map(m => {
    return `<div class="card">
      <div><strong>ID:</strong> ${m.id}</div>
      <div><strong>Content (rendered):</strong><br>${weakSanitize(m.content)}</div>
      <div><strong>Created:</strong> ${new Date(m.createdAt).toISOString()}</div>
      <form method="POST" action="/report/${m.id}" style="margin-top:.5rem">
        <button type="submit">Report to admin</button>
      </form>
      <div style="margin-top:.5rem"><a href="/message/${m.id}">Open isolated view</a></div>
    </div>`;
  }).join("\n");

  const body = `
    <div class="card">
      <form method="POST" action="/submit">
        <label>Message (HTML allowed):</label><br/>
        <textarea name="content" rows="5" cols="80" placeholder="Try some HTML…"></textarea><br/>
        <button type="submit">Post</button>
      </form>
    </div>
    <h2>Messages</h2>
    ${list || "<p>No messages yet.</p>"}
  `;
  res.send(pageTemplate(body));
});

// Isolated message view — often used by the admin to "review".
app.get("/message/:id", (req, res) => {
  const msg = messages.find(x => x.id === req.params.id);
  if (!msg) return res.status(404).send("No such message");
  const body = `<div class="card">
    <h2>Message ${msg.id}</h2>
    <div>${weakSanitize(msg.content)}</div>
    <div style="margin-top:1rem"><a href="/">Back</a></div>
  </div>`;
  res.send(pageTemplate(body));
});

// Submit
app.post("/submit", (req, res) => {
  const content = (req.body?.content ?? "").toString();
  const id = uuidv4().slice(0, 8);
  messages.unshift({ id, content, createdAt: Date.now() });
  res.redirect("/");
});

// Report
app.post("/report/:id", (req, res) => {
  const id = req.params.id;
  if (!messages.some(m => m.id === id)) return res.status(404).send("No such message");
  reports.push(id);
  res.send(pageTemplate(`<div class="card"><strong>Queued for admin review:</strong> ${id}</div><p><a href="/">Back</a></p>`));
});

// Exfiltration catch-all
app.get("/collect", (req, res) => {
  const data = (req.query.d || "").toString().slice(0, 5000);
  logs.unshift({ time: Date.now(), ip: req.ip, data });
  res.type("text").send("ok");
});

// Logs
app.get("/logs", (req, res) => {
  const items = logs.map(l => `<div class="card">
    <div><strong>Time:</strong> ${new Date(l.time).toISOString()}</div>
    <div><strong>IP:</strong> ${l.ip}</div>
    <div><strong>Data:</strong> <code>${(l.data || "").replace(/</g,"&lt;")}</code></div>
  </div>`).join("\n");
  res.send(pageTemplate(`<h2>Exfiltration Logs</h2>${items || "<p>No logs yet.</p>"}`));
});

// Health check
app.get("/health", (req, res) => res.send("OK"));

// Admin-only endpoint that sets the flag cookie.
// Only accessible from localhost to avoid trivial abuse.
app.get("/admin/seed", (req, res) => {
  const localIPs = new Set(["::1", "127.0.0.1", "::ffff:127.0.0.1"]);
  if (!localIPs.has(req.ip)) {
    return res.status(403).send("Forbidden");
  }
  const flag = getFlag();
  // Intentionally NOT HttpOnly (vulnerability)
  res.setHeader("Set-Cookie", [
    `flag=${encodeURIComponent(flag)}; Path=/; SameSite=Lax`,
    // Give admin a name cookie for flavor
    `name=admin; Path=/; SameSite=Lax`
  ]);
  res.send("Admin seeded");
});

// -------- Headless admin bot --------
async function adminWorker() {
  // Give the server a tiny bit of time to start
  await new Promise(r => setTimeout(r, 1000));
  const base = `http://127.0.0.1:${PORT}`;
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: "new",
      args: ["--no-sandbox","--disable-dev-shm-usage"]
    });
    const page = await browser.newPage();

    // Seed admin cookies by visiting the internal endpoint
    await page.goto(`${base}/admin/seed`, { waitUntil: "networkidle2" });

    // Poll the report queue forever
    while (true) {
      const id = reports.shift();
      if (id) {
        try {
          await page.goto(`${base}/message/${id}`, { waitUntil: "networkidle2", timeout: 15000 });
          // Give any JS a moment to run
          await page.waitForTimeout(1500);
        } catch (e) {
          logs.unshift({ time: Date.now(), ip: "admin-bot", data: `Error visiting ${id}: ${e}` });
        }
      } else {
        // Sleep briefly if no reports
        await new Promise(r => setTimeout(r, 750));
      }
    }
  } catch (e) {
    logs.unshift({ time: Date.now(), ip: "admin-bot", data: `Bot failed: ${e}` });
    if (browser) await browser.close().catch(()=>{});
  }
}

// Kick off the admin bot (fire-and-forget)
adminWorker();

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Challenge listening on 0.0.0.0:${PORT}`);
});
