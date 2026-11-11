// POST /api/join
//   { pin }               -> check the PIN; returns the household name and who is in it (no sign-in yet)
//   { pin, member: id }   -> sign this device in as someone already in the household (their second phone, a laptop)
//   { pin, name }         -> join as someone new; refused if that name is already a member, so nobody ends up twice
// Wrong PINs are rate limited per IP: 10 failures, then locked for 15 minutes.
import { redis, send, readBody, cleanName, clientIp, addMember, addDevice, sameName, guard, hashToObj } from "./_lib.js";

const MAX_FAILS = 10, WINDOW = 15 * 60;

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST" });
  if (!guard(res)) return;
  try {
    const body = await readBody(req);
    const pin = String(body.pin || "").replace(/\D/g, "");
    if (!/^\d{6}$/.test(pin)) return send(res, 400, { error: "Enter the 6-digit PIN" });
    const rl = `rl:join:${clientIp(req)}`;
    const [fails, hh] = await redis([["GET", rl], ["GET", `pin:${pin}`]]);
    if (Number(fails || 0) >= MAX_FAILS) return send(res, 429, { error: "Too many wrong PINs. Try again in 15 minutes" });
    if (!hh) {
      const [n] = await redis([["INCR", rl]]);
      if (n === 1) await redis([["EXPIRE", rl, WINDOW]]);
      return send(res, 404, { error: "No household with that PIN. Check the number and try again" });
    }
    const [raw, mraw] = await redis([["GET", `hh:${hh}`], ["HGETALL", `members:${hh}`]]);
    const h = JSON.parse(raw);
    const members = Object.entries(hashToObj(mraw)).map(([id, v]) => ({ id, name: JSON.parse(v).name }));
    const household = { id: h.id, name: h.name, pin: h.pin };
    if (body.member) {
      const m = members.find(x => x.id === String(body.member));
      if (!m) return send(res, 404, { error: "That person has left the household", members, household: { name: h.name } });
      const token = await addDevice(hh, m.id, m.name);
      return send(res, 200, { token, member: { id: m.id, name: m.name }, household });
    }
    const name = cleanName(body.name);
    if (!name) return send(res, 200, { check: true, household: { name: h.name }, members });
    const dup = members.find(x => sameName(x.name, name));
    if (dup) return send(res, 409, { error: `${dup.name} is already in ${h.name}. If that's you, tap your name above`, members, household: { name: h.name } });
    const m = await addMember(hh, name);
    return send(res, 200, { token: m.token, member: { id: m.id, name }, household });
  } catch (e) {
    return send(res, e.status || 500, { error: e.status ? e.message : "Something went wrong" });
  }
}
