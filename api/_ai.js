// DeepSeek helpers for "find a dish": web search, page reading and JSON chat.
// The key lives only in Vercel (DEEPSEEK_API_KEY). Nothing personal is sent: only the dish
// text someone typed and public recipe pages.
import { redis } from "./_lib.js";

const BASE = (process.env.MASAKJE_MEMORY === "1" && process.env.MASAKJE_AI_BASE) || "https://api.deepseek.com";   // a stand-in server only for local tests
export const MODEL = process.env.MASAKJE_AI_MODEL || "deepseek-flash";
export const DAILY = Number(process.env.MASAKJE_FIND_PER_DAY || 3);

export const aiReady = () => !!process.env.DEEPSEEK_API_KEY;

async function call(path, body, ms = 25000) {
  const ctl = new AbortController(), t = setTimeout(() => ctl.abort(), ms);
  try {
    const r = await fetch(BASE + path, {
      method: "POST", signal: ctl.signal,
      headers: { Authorization: `Bearer ${process.env.DEEPSEEK_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) {
      const msg = r.status === 402 ? "The recipe finder is out of credit. Top up the DeepSeek account"
        : r.status === 429 ? "The recipe finder is busy. Try again in a minute"
        : r.status === 404 && path.includes("fetch") ? "That page couldn't be read" : "The recipe finder isn't answering right now";
      throw Object.assign(new Error(msg), { status: r.status === 404 ? 422 : 502, upstream: r.status });
    }
    return j;
  } catch (e) {
    if (e.name === "AbortError") throw Object.assign(new Error("The recipe finder took too long. Try again"), { status: 504 });
    throw e;
  } finally { clearTimeout(t); }
}

export const webSearch = (query, count = 8) => call("/v1/tools/search", { query: query.slice(0, 128), count });
export const webFetch = url => call("/v1/tools/fetch", { url }, 20000);

// JSON-mode chat. Thinking off: these are extraction jobs, and it keeps replies fast.
export async function chatJSON(system, user, maxTokens = 4000) {
  for (let attempt = 0; attempt < 2; attempt++) {
    const j = await call("/chat/completions", {
      model: MODEL, thinking: { type: "disabled" }, response_format: { type: "json_object" }, max_tokens: maxTokens,
      messages: [{ role: "system", content: system }, { role: "user", content: user }],
    }, 45000);
    const c = j.choices && j.choices[0];
    const text = c && c.message && c.message.content;
    if (c && c.finish_reason === "content_filter") throw Object.assign(new Error("The recipe finder couldn't handle that one"), { status: 422 });
    if (text && text.trim()) { try { return { data: JSON.parse(text), usage: j.usage || {} }; } catch {} }
    // blank or broken JSON: DeepSeek asks you to retry
  }
  throw Object.assign(new Error("The recipe finder gave an unreadable answer. Try again"), { status: 502 });
}

// ---------- per-household daily allowance (Malaysia time) ----------
export const today = () => new Date(Date.now() + 8 * 3600e3).toISOString().slice(0, 10);
export async function usedToday(hh) {
  const [log] = await redis([["HGETALL", `findlog:${hh}:${today()}`]]);
  const names = []; for (let i = 1; i < (log || []).length; i += 2) names.push(JSON.parse(log[i]).name);
  return names;
}
export async function takeOne(hh, name) {   // returns false when today's allowance is used up
  const key = `findn:${hh}:${today()}`;
  const [n] = await redis([["INCR", key]]);
  if (n === 1) await redis([["EXPIRE", key, 2 * 86400]]);
  if (n > DAILY) return false;
  await redis([["HSET", `findlog:${hh}:${today()}`, String(Date.now()), JSON.stringify({ name })], ["EXPIRE", `findlog:${hh}:${today()}`, 2 * 86400]]);
  return true;
}
export async function giveBack(hh) {   // a search that failed on our side doesn't count
  await redis([["DECR", `findn:${hh}:${today()}`]]).catch(() => {});
}

// Cost log: one entry per call, so the real cost per recipe can be checked later.
export async function logUsage(kind, usage, extra = {}) {
  try { await redis([["HSET", `ailog:${today()}`, `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`, JSON.stringify({ kind, model: MODEL, ...usage, ...extra })], ["EXPIRE", `ailog:${today()}`, 30 * 86400]]); } catch {}
}
