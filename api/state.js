// GET  /api/state[?since=<ver>]  -> household, members and shared state (or {same:true} if unchanged)
// POST /api/state { set: {field: value}, del: [field] } -> update shared fields
//
// Shared state is a Redis hash. Whole objects use plain names (settings, plan, flow, onboarded);
// per-item maps use one field per item (bought.kangkung, kitchen.chicken), so two people ticking
// different items at the same time never overwrite each other.
import { redis, send, readBody, auth, hashToObj, guard } from "./_lib.js";

const FIELD = /^(settings|plan|flow|onboarded|(bought|pantryNeed|kitchen)\.[A-Za-z0-9_-]{1,60})$/;

export default async function handler(req, res) {
  if (!guard(res)) return;
  try {
    const me = await auth(req);
    if (!me) return send(res, 401, { error: "Please log in again" });
    const hh = me.hh;

    if (req.method === "GET") {
      const since = new URL(req.url, "http://x").searchParams.get("since");
      const [ver] = await redis([["GET", `ver:${hh}`]]);
      if (since !== null && since === String(ver || 0)) return send(res, 200, { ver: Number(ver || 0), same: true });
      const [fields, members, raw] = await redis([["HGETALL", `state:${hh}`], ["HGETALL", `members:${hh}`], ["GET", `hh:${hh}`]]);
      const h = JSON.parse(raw || "{}");
      return send(res, 200, {
        ver: Number(ver || 0),
        household: { id: h.id, name: h.name, pin: h.pin },
        me: { id: me.id, name: me.name },
        members: Object.entries(hashToObj(members)).map(([id, v]) => ({ id, ...JSON.parse(v) })),
        fields: hashToObj(fields),
      });
    }

    if (req.method === "POST") {
      const body = await readBody(req);
      const set = body.set && typeof body.set === "object" ? body.set : {};
      const del = Array.isArray(body.del) ? body.del : [];
      const keys = [...Object.keys(set), ...del];
      if (keys.length > 400) return send(res, 400, { error: "Too many changes at once" });
      for (const k of keys) if (!FIELD.test(k)) return send(res, 400, { error: `Unknown field ${String(k).slice(0, 40)}` });
      const cmds = [];
      const pairs = Object.entries(set).flatMap(([k, v]) => [k, JSON.stringify(v)]);
      if (pairs.length) cmds.push(["HSET", `state:${hh}`, ...pairs]);
      if (del.length) cmds.push(["HDEL", `state:${hh}`, ...del]);
      cmds.push(["INCR", `ver:${hh}`]);
      const out = await redis(cmds);
      return send(res, 200, { ver: out[out.length - 1] });
    }

    return send(res, 405, { error: "Use GET or POST" });
  } catch (e) {
    return send(res, e.status || 500, { error: e.status ? e.message : "Something went wrong" });
  }
}
