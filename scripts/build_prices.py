#!/usr/bin/env python3
"""Build MasakJe price files from KPDN PriceCatcher open data (CC BY 4.0).

Source: https://open.dosm.gov.my/data-catalogue/pricecatcher

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


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def median(xs):
    return round(statistics.median(xs), 2) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(ROOT, ".cache", "pricecatcher"))
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)

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
            shops = []
            for pc in pcs:
                if len(shop_prices[pc]) < MIN_ITEMS_PER_SHOP:
                    continue
                p = premises[pc]
                shops.append({"id": pc, "name": p["name"], "type": p["type"],
                              "address": p["address"],
                              "prices": dict(sorted(shop_prices[pc].items()))})
            shops.sort(key=lambda x: (-len(x["prices"]), x["name"]))
            if shops:
                with open(os.path.join(OUT, "d", f"{did}.json"), "w") as f:
                    json.dump({"state": s, "district": d, "shops": shops}, f,
                              separators=(",", ":"), ensure_ascii=False)
            districts[d] = {"id": did, "median": dmed, "tapau": dtap, "shops": len(shops)}
        index["states"][state] = {"median": med, "tapau": tap, "shops": len(s_pcs),
                                  "districts": districts}

    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump(index, f, separators=(",", ":"), ensure_ascii=False)

    missing = [k for k, it in items.items() if it.get("codes") and k not in national]
    print(f"shops={len(all_pcs)} states={len(states)} latest={max_date} "
          f"national_tapau={national_tapau} missing={missing}", file=sys.stderr)


if __name__ == "__main__":
    main()
