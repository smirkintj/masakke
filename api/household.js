// POST /api/household  { household, name }  -> create a household and its first member
import { redis, send, readBody, cleanName, newId, newPin, addMember, guard } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST" });
  if (!guard(res)) return;
  try {
    const body = await readBody(req);
    const household = cleanName(body.household), name = cleanName(body.name);
    if (!household || !name) return send(res, 400, { error: "Enter a household name and your name" });
    const id = newId();
    let pin = null;
    for (let i = 0; i < 8 && !pin; i++) {
      const p = newPin();
      const [ok] = await redis([["SET", `pin:${p}`, id, "NX"]]);
      if (ok === "OK") pin = p;
    }
    if (!pin) return send(res, 503, { error: "Couldn't make a PIN, try again" });
    await redis([["SET", `hh:${id}`, JSON.stringify({ id, name: household, pin, createdAt: Date.now() })]]);
    const m = await addMember(id, name);
    return send(res, 200, { token: m.token, member: { id: m.id, name }, household: { id, name: household, pin } });
  } catch (e) {
    return send(res, e.status || 500, { error: e.status ? e.message : "Something went wrong" });
  }
}
