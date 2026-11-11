// Local dev server: serves public/ and runs api/*.js like Vercel does. In-memory storage with MASAKJE_MEMORY=1.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PORT = Number(process.env.PORT || 3000);
const TYPES = { ".js": "text/javascript; charset=utf-8", ".html": "text/html; charset=utf-8", ".json": "application/json", ".svg": "image/svg+xml", ".webmanifest": "application/manifest+json" };

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (url.pathname.startsWith("/api/")) {
    const name = url.pathname.slice(5).replace(/[^a-z]/g, "");
    const file = path.join(ROOT, "api", `${name}.js`);
    if (!fs.existsSync(file)) { res.statusCode = 404; return res.end("{}"); }
    const mod = await import(file);
    return mod.default(req, res);
  }
  let p = path.join(ROOT, "public", url.pathname === "/" ? "index.html" : url.pathname);
  if (!p.startsWith(path.join(ROOT, "public")) || !fs.existsSync(p)) { res.statusCode = 404; return res.end("Not found"); }
  res.setHeader("Content-Type", TYPES[path.extname(p)] || "application/octet-stream");
  fs.createReadStream(p).pipe(res);
}).listen(PORT, () => console.log(`MasakJe dev server on http://localhost:${PORT}`));
