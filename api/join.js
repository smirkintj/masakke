// POST /api/join  { pin, name }  -> join an existing household with its 6-digit PIN
// Wrong PINs are rate limited per IP: 10 failures, then locked for 15 minutes.
import { redis, send, readBody, cleanName, clientIp, addMember, guard } from "./_lib.js";

const MAX_FAILS = 10, WINDOW = 15 * 60;

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST" });
  if (!guard(res)) return;
  try {
    const body = await readBody(req);
    const pin = String(body.pin || "").replace(/\D/g, ""), name = cleanName(body.name);
    if (!/^\d{6}$/.test(pin) || !name) return send(res, 400, { error: "Enter the 6-digit PIN and your name" });
    const rl = `rl:join:${clientIp(req)}`;
    const [fails, hh] = await redis([["GET", rl], ["GET", `pin:${pin}`]]);
    if (Number(fails || 0) >= MAX_FAILS) return send(res, 429, { error: "Too many wrong PINs. Try again in 15 minutes" });
    if (!hh) {
      const [n] = await redis([["INCR", rl]]);
      if (n === 1) await redis([["EXPIRE", rl, WINDOW]]);
      return send(res, 404, { error: "No household with that PIN. Check the number and try again" });
    }
    const [raw] = await redis([["GET", `hh:${hh}`]]);
    const h = JSON.parse(raw);
    const m = await addMember(hh, name);
    return send(res, 200, { token: m.token, member: { id: m.id, name }, household: { id: h.id, name: h.name, pin: h.pin } });
  } catch (e) {
    return send(res, e.status || 500, { error: e.status ? e.message : "Something went wrong" });
  }
}
