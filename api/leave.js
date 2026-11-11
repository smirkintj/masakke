// POST /api/leave -> sign this device out of the household and remove the member
import { redis, send, auth, sha256, guard, hashToObj } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST" });
  if (!guard(res)) return;
  try {
    const me = await auth(req);
    if (!me) return send(res, 200, { ok: true });
    // sign out this device; the person stays in the household while they're signed in somewhere else
    const th = sha256(me.token);
    const [, , devs] = await redis([["DEL", `tok:${th}`], ["HDEL", `dev:${me.hh}`, th], ["HGETALL", `dev:${me.hh}`]]);
    const left = Object.values(hashToObj(devs)).filter(id => id === me.id).length;
    await redis([...(left ? [] : [["HDEL", `members:${me.hh}`, me.id]]), ["INCR", `ver:${me.hh}`]]);
    return send(res, 200, { ok: true, removed: !left });
    return send(res, 200, { ok: true });
  } catch (e) {
    return send(res, 500, { error: "Something went wrong" });
  }
}
