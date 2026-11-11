#!/usr/bin/env python3
"""Extract grocery shops in Malaysia from OpenStreetMap (ODbL) with opening hours.

Source: the Malaysia extract at download.openstreetmap.fr (OSM data, ODbL 1.0,
"© OpenStreetMap contributors"). The public Overpass servers refuse requests from
cloud machines, so we read the extract file locally with pyosmium.

Each shop is matched to the nearest PriceCatcher premise with a similar name
(within 1.5 km) so it can carry that shop's real prices.

Output: public/data/prices/osm_shops.json
Usage:  pip install osmium && python3 scripts/build_osm_shops.py [--pbf FILE]
"""
import argparse
import json
import math
import os
import re
import sys
import urllib.request

import osmium

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://download.openstreetmap.fr/extracts/asia/malaysia-latest.osm.pbf"
OUT = os.path.join(ROOT, "public", "data", "prices", "osm_shops.json")
P = os.path.join(ROOT, "public", "data", "prices")
SHOP_TAGS = {"supermarket", "grocery", "convenience", "greengrocer", "butcher", "seafood", "wholesale"}


class Shops(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.out = []
        self.places = []  # (lat, lng, name) of suburbs / neighbourhoods, for "Jaya Grocer · Bukit Jelutong"

    def take(self, tags, lat, lng):
        shop, amenity = tags.get("shop"), tags.get("amenity")
        if shop not in SHOP_TAGS and amenity != "marketplace":
            return
        name = tags.get("name") or tags.get("name:en") or tags.get("brand")
        if not name:
            return
        self.out.append({
            "name": name, "brand": tags.get("brand", ""),
            "type": "Wet market" if amenity == "marketplace" else shop.capitalize(),
            "lat": round(lat, 5), "lng": round(lng, 5),
            "hours": tags.get("opening_hours", ""),
            "area": tags.get("addr:suburb") or tags.get("addr:city") or tags.get("addr:place") or "",
            "postcode": tags.get("addr:postcode", ""),
        })

    def node(self, n):
        if n.tags.get("place") in ("suburb", "neighbourhood", "quarter", "village", "hamlet") and n.tags.get("name"):
            self.places.append((n.location.lat, n.location.lon, n.tags.get("name:en") or n.tags["name"]))
        if "shop" in n.tags or n.tags.get("amenity") == "marketplace":
            self.take(n.tags, n.location.lat, n.location.lon)

    def way(self, w):
        if "shop" not in w.tags and w.tags.get("amenity") != "marketplace":
            return
        pts = [(nd.lat, nd.lon) for nd in w.nodes if nd.location.valid()]
        if pts:
            self.take(w.tags, sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def km(a, b, c, d):
    t = math.pi / 180
    h = math.sin((c - a) * t / 2) ** 2 + math.cos(a * t) * math.cos(c * t) * math.sin((d - b) * t / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def words(s):
    stop = {"sdn", "bhd", "the", "pasaraya", "pasar", "raya", "supermarket", "mart", "store", "kedai", "runcit", "mini", "market", "and", "dan"}
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2 and w not in stop}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pbf", default=os.path.join(ROOT, ".cache", "malaysia.osm.pbf"))
    args = ap.parse_args()
    if not os.path.exists(args.pbf):
        os.makedirs(os.path.dirname(args.pbf), exist_ok=True)
        print("downloading OSM extract", file=sys.stderr)
        urllib.request.urlretrieve(URL, args.pbf)
    h = Shops()
    h.apply_file(args.pbf, locations=True, idx="flex_mem")

    # PriceCatcher shops with coordinates, for linking prices
    index = json.load(open(os.path.join(P, "index.json")))
    pc = []
    for s, sv in index["states"].items():
        for d, dv in sv["districts"].items():
            fp = os.path.join(P, "d", f"{dv['id']}.json")
            if os.path.exists(fp):
                for sh in json.load(open(fp))["shops"]:
                    if sh.get("geo") and sh["geo"][2] in ("postcode", "near-postcode", "place"):
                        pc.append((sh["id"], sh["name"], sh["geo"][0], sh["geo"][1]))
    grid = {}
    for la, ln, nm in h.places:
        grid.setdefault((round(la, 1), round(ln, 1)), []).append((la, ln, nm))
    for s in h.out:
        best, bd = "", 3.0  # within 3 km
        for dla in (-0.1, 0, 0.1):
            for dln in (-0.1, 0, 0.1):
                for la, ln, nm in grid.get((round(s["lat"] + dla, 1), round(s["lng"] + dln, 1)), []):
                    d = km(s["lat"], s["lng"], la, ln)
                    if d < bd:
                        bd, best = d, nm
        if best:
            s["area"] = best
    # Typical hours per chain, from its branches that do list hours (>= 3 branches, >= 40% agree).
    from collections import Counter
    def chain_key(s):
        return (s["brand"] or re.sub(r"\s*[\(@\-–].*$", "", s["name"])).strip().lower()
    by = {}
    for s in h.out:
        if s["hours"]:
            by.setdefault(chain_key(s), []).append(s["hours"].strip())
    typical = {}
    for k, hs in by.items():
        if len(hs) >= 3:
            val, n = Counter(hs).most_common(1)[0]
            if n / len(hs) >= 0.4:
                typical[k] = val
    for s in h.out:
        if not s["hours"] and chain_key(s) in typical:
            s["typ"] = typical[chain_key(s)]
    linked = 0
    for s in h.out:
        sw = words(s["name"] + " " + s["brand"])
        best = None
        for pid, name, la, ln in pc:
            if abs(la - s["lat"]) > 0.03 or abs(ln - s["lng"]) > 0.03:
                continue
            overlap = len(sw & words(name))
            if overlap and km(s["lat"], s["lng"], la, ln) <= 1.5:
                if not best or overlap > best[0]:
                    best = (overlap, pid)
        if best:
            s["pc"] = best[1]
            linked += 1
    json.dump(h.out, open(OUT, "w"), separators=(",", ":"), ensure_ascii=False)
    json.dump([[round(a, 4), round(b, 4), n] for a, b, n in h.places], open(os.path.join(P, "osm_places.json"), "w"), separators=(",", ":"), ensure_ascii=False)
    with_hours = sum(1 for s in h.out if s["hours"])
    with_typ = sum(1 for s in h.out if s.get("typ"))
    print(f"osm shops={len(h.out)} with_hours={with_hours} typical_hours={with_typ} chains_with_typical={len(typical)} linked_to_pricecatcher={linked}", file=sys.stderr)
    for k, v in sorted(typical.items(), key=lambda kv: -len(by[kv[0]]))[:15]:
        print(f"  {k:28s} {v}  ({len(by[k])} branches with hours)", file=sys.stderr)


if __name__ == "__main__":
    main()
