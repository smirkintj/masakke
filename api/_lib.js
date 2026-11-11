// Shared helpers for MasakJe's API (Vercel Node functions).
// Storage: Upstash Redis over its REST API (Vercel Marketplace sets KV_REST_API_URL / KV_REST_API_TOKEN).
// Without those variables and with MASAKJE_MEMORY=1, an in-memory store is used for local testing.
import crypto from "node:crypto";

const URL_ = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const MEMORY = !URL_ && process.env.MASAKJE_MEMORY === "1";

export const storageReady = () => Boolean((URL_ && TOKEN) || MEMORY);

// ---- in-memory fallback (local tests only) ----
const mem = (globalThis.__masakjeMem ||= { kv: new Map(), hash: new Map(), exp: new Map() });
function alive(k) { const e = mem.exp.get(k); if (e && e < Date.now()) { mem.kv.delete(k); mem.hash.delete(k); mem.exp.delete(k); } }
function memExec([cmd, ...a]) {
  const c = cmd.toUpperCase(); if (a[0] !== undefined) alive(a[0]);
  switch (c) {
    case "GET": return mem.kv.has(a[0]) ? mem.kv.get(a[0]) : null;
    case "SET": { if (a.includes("NX") && mem.kv.has(a[0])) return null; mem.kv.set(a[0], String(a[1])); return "OK"; }
    case "DEL": { const n = a.filter(k => mem.kv.delete(k) | mem.hash.delete(k)).length; return n; }
    case "INCR": { const v = Number(mem.kv.get(a[0]) || 0) + 1; mem.kv.set(a[0], String(v)); return v; }
    case "EXPIRE": mem.exp.set(a[0], Date.now() + Number(a[1]) * 1000); return 1;
    case "HSET": { const h = mem.hash.get(a[0]) || new Map(); for (let i = 1; i < a.length; i += 2) h.set(a[i], String(a[i + 1])); mem.hash.set(a[0], h); return (a.length - 1) / 2; }
    case "HDEL": { const h = mem.hash.get(a[0]); if (!h) return 0; return a.slice(1).filter(f => h.delete(f)).length; }
    case "HGETALL": { const h = mem.hash.get(a[0]); return h ? [...h.entries()].flat() : []; }
    default: throw new Error("memory store: unsupported " + c);
  }
}

export async function redis(cmds) {
  if (MEMORY) return cmds.map(memExec);
  const r = await fetch(`${URL_}/pipeline`, {
    method: "POST",
    headers: { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify(cmds),
  });
  if (!r.ok) throw new Error(`storage error ${r.status}`);
  return (await r.json()).map(x => { if (x.error) throw new Error(x.error); return x.result; });
}

export const sha256 = s => crypto.createHash("sha256").update(s).digest("hex");
export const newToken = () => crypto.randomBytes(24).toString("base64url");
export const newId = () => crypto.randomUUID();
export const newPin = () => String(crypto.randomInt(0, 1_000_000)).padStart(6, "0");
export const hashToObj = arr => { const o = {}; for (let i = 0; i < (arr || []).length; i += 2) o[arr[i]] = arr[i + 1]; return o; };

export function send(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(body));
}

export async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") { try { return JSON.parse(req.body); } catch { return {}; } }
  const chunks = []; let size = 0;
  for await (const c of req) { size += c.length; if (size > 256 * 1024) throw Object.assign(new Error("Too large"), { status: 413 }); chunks.push(c); }
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}"); } catch { return {}; }
}

export const cleanName = s => String(s || "").replace(/\s+/g, " ").trim().slice(0, 40);
export const clientIp = req => String(req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "unknown").split(",")[0].trim();

// Create a member + device token inside a household.
// One person can sign in on several devices: each device has its own token, all pointing at the same member.
// dev:<hh> maps token hash -> member id, so leaving removes one device and the person only when it was their last.
export async function addDevice(hh, id, name) {
  const token = newToken(), th = sha256(token);
  await redis([["SET", `tok:${th}`, JSON.stringify({ hh, id, name })], ["HSET", `dev:${hh}`, th, id], ["INCR", `ver:${hh}`]]);
  return token;
}
export async function addMember(hh, name) {
  const id = newId();
  await redis([["HSET", `members:${hh}`, id, JSON.stringify({ name, joinedAt: Date.now() })]]);
  return { id, token: await addDevice(hh, id, name) };
}
export const sameName = (a, b) => String(a).trim().toLowerCase().replace(/\s+/g, " ") === String(b).trim().toLowerCase().replace(/\s+/g, " ");

export async function auth(req) {
  const h = String(req.headers.authorization || "");
  const token = h.startsWith("Bearer ") ? h.slice(7) : "";
  if (!token) return null;
  const [raw] = await redis([["GET", `tok:${sha256(token)}`]]);
  return raw ? { ...JSON.parse(raw), token } : null;
}

export function guard(res) {
  if (!storageReady()) { send(res, 503, { error: "Storage isn't connected yet. Add Upstash Redis to this Vercel project." }); return false; }
  return true;
}
