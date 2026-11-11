// POST /api/leave -> sign this device out of the household and remove the member
import { redis, send, auth, sha256, guard } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST" });
  if (!guard(res)) return;
  try {
    const me = await auth(req);
    if (!me) return send(res, 200, { ok: true });
    await redis([["DEL", `tok:${sha256(me.token)}`], ["HDEL", `members:${me.hh}`, me.id], ["INCR", `ver:${me.hh}`]]);
    return send(res, 200, { ok: true });
  } catch (e) {
    return send(res, 500, { error: "Something went wrong" });
  }
}
