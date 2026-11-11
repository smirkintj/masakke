#!/usr/bin/env python3
"""Fetch Jaya Grocer online-store prices for MasakJe ingredients. PERSONAL USE ONLY.

Jaya Grocer runs a public Shopify storefront (robots.txt allows public product pages).
This script:
  * fetches only the food collections listed in COLLECTIONS, 250 products a request,
    with a pause between requests and an identifying User-Agent;
  * keeps title, price, availability and URL of each variant;
  * matches products to ingredients with rules in src/data/jayagrocer_map.json;
  * writes public/data/prices/jayagrocer.json.

Prices are the "Online Store KL" list, not a specific branch. Commercial use of this
data needs Jaya Grocer's permission. Run at most weekly.

Usage: python3 scripts/fetch_jayagrocer.py [--cache DIR] [--offline]
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.jayagrocer.com"
UA = {"User-Agent": "MasakJe-personal/0.1 (weekly price check; personal meal planner)"}
COLLECTIONS = ["fresh-market", "poultry", "chicken", "meat", "beef", "lamb", "fish", "hs-seafood", "seafood",
               "prawns-and-crabs", "eggs", "cooking-ingredients", "dressings-sauces", "sauces-and-specialty",
               "herbs-and-spices", "blended-and-cooking-oil", "cooking-noodles", "tofu-noodles-and-others",
               "rice-and-grains", "white-rice", "dried-meat-and-seafood-1", "chilled-produce", "coconut-milk"]
PAUSE = 2.0
OUT = os.path.join(ROOT, "public", "data", "prices", "jayagrocer.json")
MAP = os.path.join(ROOT, "src", "data", "jayagrocer_map.json")
INGREDIENTS = os.path.join(ROOT, "src", "data", "ingredients.json")


def fetch_products(cache):
    import hashlib
    tag = hashlib.sha1(",".join(COLLECTIONS).encode()).hexdigest()[:8]
    path = os.path.join(cache, f"jg_products_{tag}.json")
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < 6 * 86400:
        return json.load(open(path))
    seen, out = set(), []
    for col in COLLECTIONS:
        for page in range(1, 20):
            url = f"{BASE}/collections/{col}/products.json?limit=250&page={page}"
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                prods = json.load(r)["products"]
            print(f"{col} p{page}: {len(prods)}", file=sys.stderr)
            for p in prods:
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                out.append({"title": p["title"], "handle": p["handle"], "type": p.get("product_type", ""),
                            "variants": [{"title": v.get("title", ""), "price": float(v["price"]),
                                          "available": v.get("available", True)} for v in p["variants"]]})
            time.sleep(PAUSE)
            if len(prods) < 250:
                break
    json.dump(out, open(path, "w"))
    return out


UNIT = re.compile(r"(\d+(?:\.\d+)?)\s*(kg|g|gm|gram|grams|ml|l|ltr|litre|liter|pcs|pc|biji|s|'s|eggs?|sticks?|stalks?|ekor)\b", re.I)
MULTI = re.compile(r"(\d+)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(kg|g|ml|l)\b", re.I)


def pack_size(text, unit):
    """Amount in the ingredient's unit (g, ml or pc) described by a product/variant title."""
    t = text.lower()
    m = MULTI.search(t)
    if m:
        n, q, u = int(m.group(1)), float(m.group(2)), m.group(3)
        return n * to_unit(q, u, unit)
    best = None
    for q, u in UNIT.findall(t):
        v = to_unit(float(q), u.lower(), unit)
        if v:
            best = v  # last size mentioned usually is the pack
    return best


def to_unit(q, u, unit):
    u = u.lower().strip("'")
    if unit == "g":
        return q * 1000 if u == "kg" else q if u in ("g", "gm", "gram", "grams") else None
    if unit == "ml":
        return q * 1000 if u in ("l", "ltr", "litre", "liter", "kg") else q if u in ("ml", "g") else None
    if unit == "pc":
        return q if u in ("pcs", "pc", "biji", "s", "egg", "eggs", "stick", "sticks", "stalk", "stalks", "ekor") else None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(ROOT, ".cache"))
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)
    products = fetch_products(args.cache)
    items = json.load(open(INGREDIENTS))["items"]
    rules = json.load(open(MAP))["rules"]

    result, report = {}, []
    for key, rule in rules.items():
        it = items[key]
        inc, exc = re.compile(rule["match"], re.I), re.compile(rule.get("exclude", r"^\b$"), re.I)
        cands = []
        for p in products:
            if not inc.search(p["title"]) or exc.search(p["title"]):
                continue
            for v in p["variants"]:
                if not v["available"] or v["price"] <= 0:
                    continue
                label = f'{p["title"]} {v["title"]}'
                if it["unit"] == "pc" and rule.get("per_piece_g"):
                    g = pack_size(label, "g")
                    size = g / rule["per_piece_g"] if g else None
                else:
                    size = pack_size(label, it["unit"]) or rule.get("assume")
                if not size:
                    continue
                per_unit = v["price"] / size
                cands.append({"title": p["title"] + ("" if v["title"] in ("Default Title", "1 UNIT") else f' ({v["title"]})'),
                              "url": f'{BASE}/products/{p["handle"]}', "price": v["price"], "size": size,
                              "per": round(per_unit * it["size"], 2)})
        if not cands:
            report.append(f"  no match: {key}")
            continue
        # Typical everyday option: the cheapest per unit, ignoring outliers below a fifth of the median (mis-parsed sizes).
        cands.sort(key=lambda c: c["per"])
        med = cands[len(cands) // 2]["per"]
        sane = [c for c in cands if c["per"] >= med / 5] or cands
        pick = sane[0]
        result[key] = {"per": pick["per"], "title": pick["title"], "url": pick["url"],
                       "price": pick["price"], "size": pick["size"], "options": len(cands)}
        report.append(f"  {key:16s} RM{pick['per']:7.2f}/{it['size']}{it['unit']}  <- {pick['title']} RM{pick['price']} ({len(cands)} options)")

    json.dump({"source": "Jaya Grocer online store (Online Store KL), personal use",
               "fetchedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
               "items": result}, open(OUT, "w"), separators=(",", ":"), ensure_ascii=False)
    print("\n".join(report), file=sys.stderr)
    print(f"matched {len(result)}/{len(rules)} ingredients from {len(products)} products", file=sys.stderr)


if __name__ == "__main__":
    main()
