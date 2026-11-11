// GET /api/health -> is storage connected?
import { send, storageReady } from "./_lib.js";

export default function handler(req, res) {
  send(res, 200, { ok: true, storage: storageReady() });
}
