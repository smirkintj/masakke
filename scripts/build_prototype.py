#!/usr/bin/env python3
"""Bundle recipes, ingredients and PriceCatcher prices into one self-contained
prototype page: prototype/src.html -> prototype/index.html.

Prices are packed as arrays aligned to `keys` to keep the page small, and only
the SHOPS_PER_DISTRICT best-covered shops per district are kept.
Run scripts/build_prices.py first.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "public", "data", "prices")
SHOPS_PER_DISTRICT = 6


def main():
    ingredients = json.load(open(os.path.join(ROOT, "src", "data", "ingredients.json")))["items"]
    recipes = json.load(open(os.path.join(ROOT, "src", "data", "recipes.json")))["recipes"]
    index = json.load(open(os.path.join(P, "index.json")))
    keys = sorted(k for k, v in ingredients.items() if v.get("codes"))

    def pack(m):
        return [m.get(k) for k in keys]

    states = {}
    for s, sv in index["states"].items():
        ds = {}
        for d, dv in sv["districts"].items():
            shops = []
            fp = os.path.join(P, "d", f"{dv['id']}.json")
            if os.path.exists(fp):
                for sh in json.load(open(fp))["shops"][:SHOPS_PER_DISTRICT]:
                    shops.append([sh["name"], sh["type"], pack(sh["prices"])])
            ds[d] = {"m": pack(dv["median"]), "shops": shops}
        states[s] = {"m": pack(sv["median"]), "d": ds}

    data = {
        "ingredients": ingredients,
        "recipes": recipes,
        "prices": {"source": index["source"], "date": index["latestPriceDate"],
                   "shops": index["national"]["shops"], "keys": keys,
                   "national": pack(index["national"]["median"]), "states": states},
    }
    src = open(os.path.join(ROOT, "prototype", "src.html")).read()
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    out = src.replace("/*__DATA__*/null", blob)
    with open(os.path.join(ROOT, "prototype", "index.html"), "w") as f:
        f.write(out)
    print(f"prototype/index.html {len(out)//1024} KB")


if __name__ == "__main__":
    main()
