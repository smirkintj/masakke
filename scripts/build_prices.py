#!/usr/bin/env python3
"""Build MasakJe price files from KPDN PriceCatcher open data (CC BY 4.0).

Source: https://open.dosm.gov.my/data-catalogue/pricecatcher
Shop locations: geocoded from the address postcode or town name using
GeoNames postcode centroids (CC BY 4.0), falling back to the district centre.

Outputs (in public/data/prices/):
  index.json            national/state/district median prices + tapau prices
  d/<district-id>.json  per-shop prices for one district

Rules:
  * Only prices observed in the last WINDOW_DAYS days are used; for each
    shop + item code we keep the most recent observation.
  * One ingredient can map to several PriceCatcher codes (brands/origins);
    a shop's price for the ingredient is the cheapest of those codes.
  * Area prices are medians across grocery shops in that area.
  * "Tapau" price = median restaurant price for nasi + sayur + ayam/ikan/daging.

Standard library only. Usage: python3 scripts/build_prices.py [--cache DIR]
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import statistics
import sys
import urllib.request
import zipfile

BASE = "https://storage.data.gov.my/pricecatcher/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "data", "prices")
INGREDIENTS = os.path.join(ROOT, "src", "data", "ingredients.json")

WINDOW_DAYS = 45
GROCERY_TYPES = {"Pasar Mini", "Pasar Raya / Supermarket", "Kedai Runcit",
                 "Pasar Basah", "Hypermarket", "Borong"}
RESTAURANT_TYPES = {"Restoran Melayu", "Restoran India Muslim", "Restoran Cina",
                    "Medan Selera", "Foodcourt"}
TAPAU_CODES = {1161, 1162, 1163}  # NASI + SAYUR + IKAN / AYAM / DAGING
MIN_ITEMS_PER_SHOP = 5
GEONAMES = "https://download.geonames.org/export/zip/MY.zip"  # CC BY 4.0


def fetch(name, cache):
    path = os.path.join(cache, name)
    if not os.path.exists(path):
        print(f"downloading {name}", file=sys.stderr)
        tmp = path + ".part"
        with urllib.request.urlopen(BASE + name, timeout=300) as r, open(tmp, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
        os.replace(tmp, path)
    return path


def load_postcodes(cache):
    """GeoNames postcode centroids -> ({postcode: (lat, lng)}, [(place, state, lat, lng)])."""
    path = os.path.join(cache, "geonames_MY.zip")
    if not os.path.exists(path):
        print("downloading geonames MY", file=sys.stderr)
        urllib.request.urlretrieve(GEONAMES, path)
    pcs, places, names = {}, {}, {}
    with zipfile.ZipFile(path) as z:
        for line in z.read("MY.txt").decode("utf-8").splitlines():
            f = line.split("\t")
            lat, lng = float(f[9]), float(f[10])
            pcs[f[1]] = (lat, lng)
            names[f[1]] = f[2].strip()
            places.setdefault((f[2].upper(), f[3].upper()), []).append((lat, lng))
    place_list = [(name, state, sum(p[0] for p in v) / len(v), sum(p[1] for p in v) / len(v))
                  for (name, state), v in places.items() if len(name) >= 4]
    place_list.sort(key=lambda x: -len(x[0]))  # longest name first: "KOTA BHARU" before "KOTA"
    return pcs, place_list, names


STATE_ALIASES = {"W.P. KUALA LUMPUR": "WILAYAH PERSEKUTUAN KUALA LUMPUR", "W.P. PUTRAJAYA": "WILAYAH PERSEKUTUAN PUTRAJAYA",
                 "W.P. LABUAN": "WILAYAH PERSEKUTUAN LABUAN", "PULAU PINANG": "PENANG"}


def geocode(address, state, pcs, places):
    """Return (lat, lng, precision) or None. precision: postcode | near-postcode | place."""
    found = re.findall(r"\b(\d{5})\b", address)
    if found:
        pc = found[-1]
        if pc in pcs:
            return (*pcs[pc], "postcode")
        near = [k for k in pcs if k[:3] == pc[:3]]
        if near:
            k = min(near, key=lambda k: abs(int(k) - int(pc)))
            return (*pcs[k], "near-postcode")
    up = " " + re.sub(r"[^A-Z0-9 ]", " ", address.upper()) + " "
    st = STATE_ALIASES.get(state.upper(), state.upper())
    for name, pstate, lat, lng in places:
        if (pstate == st or st in pstate or pstate in st) and f" {name} " in up:
            return (lat, lng, "place")
    return None


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def median(xs):
    return round(statistics.median(xs), 2) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(ROOT, ".cache", "pricecatcher"))
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)

    postcodes, places, pc_names = load_postcodes(args.cache)

    with open(INGREDIENTS) as f:
        items = json.load(f)["items"]
    code_to_ing = {}
    for key, it in items.items():
        for c in it.get("codes", []):
            code_to_ing.setdefault(c, []).append(key)

    # premises
    premises = {}
    with open(fetch("lookup_premise.csv", args.cache), newline="") as f:
        for r in csv.DictReader(f):
            ptype = (r["premise_type"] or "").strip()
            state = (r["state"] or "").strip()
            district = (r["district"] or "").strip()
            if not state or not district:
                continue
            premises[r["premise_code"]] = {
                "name": r["premise"].strip(), "type": ptype,
                "address": " ".join((r["address"] or "").split()),
                "state": state, "district": district,
            }
            g = geocode(premises[r["premise_code"]]["address"], state, postcodes, places)
            if g:
                premises[r["premise_code"]]["geo"] = [round(g[0], 4), round(g[1], 4), g[2]]

    # monthly price files: current + previous month (always re-download current)
    today = dt.date.today()
    first = today.replace(day=1)
    prev = (first - dt.timedelta(days=1)).replace(day=1)
    months = [prev, first]
    cur_name = f"pricecatcher_{first:%Y-%m}.csv"
    cur_path = os.path.join(args.cache, cur_name)
    if os.path.exists(cur_path):
        os.remove(cur_path)

    cutoff = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    latest = {}  # (premise, code) -> (date, price)
    max_date = ""
    for m in months:
        try:
            path = fetch(f"pricecatcher_{m:%Y-%m}.csv", args.cache)
        except Exception as e:  # current month may not exist on day 1
            print(f"skip {m:%Y-%m}: {e}", file=sys.stderr)
            continue
        with open(path, newline="") as f:
            for r in csv.DictReader(f):
                d = r["date"]
                if d < cutoff:
                    continue
                try:
                    code = int(float(r["item_code"]))
                    price = float(r["price"])
                except (ValueError, TypeError):
                    continue
                if price <= 0 or (code not in code_to_ing and code not in TAPAU_CODES):
                    continue
                k = (r["premise_code"], code)
                if k not in latest or d > latest[k][0]:
                    latest[k] = (d, price)
                max_date = max(max_date, d)

    # per-shop ingredient prices
    shop_prices = {}   # premise -> {ing: price}
    shop_tapau = {}    # premise -> [prices]
    for (pc, code), (_, price) in latest.items():
        p = premises.get(pc)
        if not p:
            continue
        if code in TAPAU_CODES and p["type"] in RESTAURANT_TYPES:
            shop_tapau.setdefault(pc, []).append(price)
        if p["type"] in GROCERY_TYPES:
            for ing in code_to_ing.get(code, []):
                cur = shop_prices.setdefault(pc, {})
                if ing not in cur or price < cur[ing]:
                    cur[ing] = price

    def area_stats(pcs, tapau_pcs):
        by_ing = {}
        for pc in pcs:
            for ing, v in shop_prices[pc].items():
                by_ing.setdefault(ing, []).append(v)
        tap = [statistics.median(shop_tapau[pc]) for pc in tapau_pcs]
        return ({k: median(v) for k, v in sorted(by_ing.items())}, median(tap))

    shops_by_area, tapau_by_area = {}, {}
    for pc in shop_prices:
        p = premises[pc]
        shops_by_area.setdefault((p["state"], p["district"]), []).append(pc)
    for pc in shop_tapau:
        p = premises[pc]
        tapau_by_area.setdefault((p["state"], p["district"]), []).append(pc)

    os.makedirs(os.path.join(OUT, "d"), exist_ok=True)
    for old in os.listdir(os.path.join(OUT, "d")):
        os.remove(os.path.join(OUT, "d", old))

    geo_stats = {}
    all_pcs = list(shop_prices)
    national, national_tapau = area_stats(all_pcs, list(shop_tapau))
    index = {
        "source": "KPDN PriceCatcher via OpenDOSM (CC BY 4.0)",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "latestPriceDate": max_date,
        "windowDays": WINDOW_DAYS,
        "national": {"median": national, "tapau": national_tapau, "shops": len(all_pcs)},
        "states": {},
    }
    states = sorted({s for s, _ in shops_by_area} | {s for s, _ in tapau_by_area})
    for state in states:
        s_pcs = [pc for (s, _), v in shops_by_area.items() if s == state for pc in v]
        s_tap = [pc for (s, _), v in tapau_by_area.items() if s == state for pc in v]
        med, tap = area_stats(s_pcs, s_tap)
        districts = {}
        for (s, d) in sorted(set(shops_by_area) | set(tapau_by_area)):
            if s != state:
                continue
            pcs = shops_by_area.get((s, d), [])
            dmed, dtap = area_stats(pcs, tapau_by_area.get((s, d), []))
            did = slug(f"{s}-{d}")
            located = [premises[pc]["geo"] for pc in pcs if "geo" in premises[pc]]
            centre = ([round(sum(g[0] for g in located) / len(located), 4),
                       round(sum(g[1] for g in located) / len(located), 4)] if located else None)
            shops = []
            for pc in pcs:
                if len(shop_prices[pc]) < MIN_ITEMS_PER_SHOP:
                    continue
                p = premises[pc]
                shops.append({"id": pc, "name": p["name"], "type": p["type"],
                              "address": p["address"],
                              "geo": p.get("geo") or (centre + ["district"] if centre else None),
                              "prices": dict(sorted(shop_prices[pc].items()))})
            shops.sort(key=lambda x: (-len(x["prices"]), x["name"]))
            if shops:
                with open(os.path.join(OUT, "d", f"{did}.json"), "w") as f:
                    json.dump({"state": s, "district": d, "shops": shops}, f,
                              separators=(",", ":"), ensure_ascii=False)
            districts[d] = {"id": did, "median": dmed, "tapau": dtap, "shops": len(shops), "centre": centre}
            for sh in shops:
                g = sh["geo"]
                geo_stats[g[2] if g else "none"] = geo_stats.get(g[2] if g else "none", 0) + 1
        index["states"][state] = {"median": med, "tapau": tap, "shops": len(s_pcs),
                                  "districts": districts}

    with open(os.path.join(OUT, "postcodes.json"), "w") as f:
        json.dump({k: [round(v[0], 4), round(v[1], 4), pc_names[k]] for k, v in sorted(postcodes.items())}, f, separators=(",", ":"))

    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump(index, f, separators=(",", ":"), ensure_ascii=False)

    missing = [k for k, it in items.items() if it.get("codes") and k not in national]
    print(f"shops={len(all_pcs)} states={len(states)} latest={max_date} "
          f"missing={missing} geo={geo_stats}", file=sys.stderr)


if __name__ == "__main__":
    main()
