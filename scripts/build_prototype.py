#!/usr/bin/env python3
"""Bundle recipes, ingredients, shops and postcodes into one self-contained
prototype page: prototype/src.html -> prototype/index.html.

Run scripts/build_prices.py first.

Also turns each recipe's plain steps into guided-cooking steps:
  {"t": text, "ing": [ingredient keys used in this step], "sec": timer seconds or 0}
Step ingredients are matched from the step text with ALIASES below, so wording
in recipes.json matters ("Fry the shallots" links shallots to that step).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "public", "data", "prices")

CHILI = r"\bchil(i|ies)\b(?! (padi|powder|sauce))"
ALIASES = {
    "chicken": r"chicken", "chicken_thigh": r"chicken", "chicken_breast": r"chicken", "chicken_wing": r"chicken",
    "beef": r"beef", "mutton": r"mutton",
    "fish_kembung": r"\bfish\b(?! (sauce|curry))", "fish_selar": r"\bfish\b(?! (sauce|curry))",
    "fish_tenggiri": r"\bfish\b(?! (sauce|curry))", "fish_siakap": r"\bfish\b(?! (sauce|curry))",
    "fish_tilapia": r"\bfish\b(?! (sauce|curry))", "prawn": r"prawn", "squid": r"squid", "cockle": r"cockle",
    "ikan_bilis": r"ikan bilis", "dried_shrimp": r"dried shrimp", "salted_fish": r"salted fish",
    "egg": r"\begg", "tofu": r"tofu", "tempe": r"tempe",
    "kangkung": r"kangkung", "bayam": r"bayam", "sawi": r"sawi", "kailan": r"kailan", "pak_choy": r"pak choy",
    "cabbage": r"cabbage", "chinese_cabbage": r"cabbage", "taugeh": r"taugeh", "long_bean": r"long bean",
    "french_bean": r"\bbeans?\b", "okra": r"okra", "brinjal": r"brinjal", "carrot": r"carrot", "potato": r"potato",
    "tomato": r"tomato(?!(es)? sauce)", "cucumber": r"cucumber", "broccoli": r"broccoli", "cauliflower": r"cauliflower",
    "capsicum": r"capsicum", "spring_onion": r"spring onion", "lemongrass": r"lemongrass", "curry_leaves": r"curry leaves",
    "lime": r"\blime|limau", "shallot": r"shallot", "onion": r"(?<!spring )\bonion", "garlic": r"garlic",
    "ginger": r"ginger", "galangal": r"galangal",
    "chili_red": CHILI, "chili_green": CHILI, "dried_chili": r"dried chili|soaked( dried)? chili|blended chili|cut dried chili|" + CHILI,
    "chili_padi": r"chili padi",
    "santan": r"santan|coconut", "tamarind": r"tamarind", "peanuts": r"peanut", "dhal": r"dhal", "rice": r"\brice\b",
    "yellow_mee": r"noodle", "kuetiau": r"kuetiau", "bihun": r"bihun",
    "oil": r"\bfry|\bfried|\boil\b(?!y)", "salt": r"\bsalt|season", "sugar": r"sugar|season with",
    "kicap_manis": r"kicap|soy|sauces", "soy_light": r"soy|sauces", "soy_dark": r"soy|sauces",
    "oyster_sauce": r"oyster|sauces", "chili_sauce": r"chili sauce|sauces", "tomato_sauce": r"tomato sauce|sauces",
    "fish_sauce": r"fish sauce", "sesame_oil": r"sesame", "belacan": r"belacan", "cornflour": r"cornflour",
    "flour": r"(?<!corn)flour", "tomyam_paste": r"tom yam", "chili_powder": r"chili powder",
    "turmeric_powder": r"turmeric", "curry_meat": r"curry (powder|paste)", "curry_fish": r"curry (powder|paste)",
    "kurma_powder": r"kurma", "soup_spice": r"soup spice", "black_pepper": r"pepper", "white_pepper": r"pepper",
    "cinnamon": r"cinnamon|whole spices", "star_anise": r"star anise|whole spices", "fennel": r"fennel",
}
# Chains: name, regex on PriceCatcher shop name. Price level = median of
# (shop price / state median) over every item at every surveyed branch.
CHAINS = [
    ("Jaya Grocer", r"JAYA GROCER"), ("Village Grocer", r"VILLAGE GROCER"),
    ("TMG", r"\bTMG\b|TUNAS MANJA"), ("Lotus's", r"LOTUS|TESCO"), ("AEON", r"AEON|MAXVALU"),
    ("Mydin", r"MYDIN"), ("Giant", r"\bGIANT\b"), ("99 Speedmart", r"99 ?SPEEDMART"),
    ("Econsave", r"ECONSAVE"), ("NSK", r"\bNSK\b"), ("Hero", r"\bHERO\b"), ("The Store", r"THE STORE"),
    ("Segi Fresh", r"SEGI FRESH"),
]
MIN_CHAIN_SHOPS = 5
TIMER = re.compile(r"(?:(\d+)\s*to\s*)?(\d+(?:\.\d+)?)\s*(minutes?|hours?)", re.I)


def guided_steps(recipe):
    keys = [k for k, _ in recipe["ing"]]
    out = []
    for text in recipe["steps"]:
        low = text.lower()
        used = [k for k in keys if re.search(ALIASES.get(k, re.escape(k)), low)]
        m = TIMER.search(text)
        sec = 0
        if m:
            n = float(m.group(2))
            sec = int(n * (3600 if m.group(3).lower().startswith("hour") else 60))
        out.append({"t": text, "ing": used, "sec": sec})
    return out


def main():
    ingredients = json.load(open(os.path.join(ROOT, "src", "data", "ingredients.json")))["items"]
    recipes = json.load(open(os.path.join(ROOT, "src", "data", "recipes.json")))["recipes"]
    index = json.load(open(os.path.join(P, "index.json")))
    postcodes = json.load(open(os.path.join(P, "postcodes.json")))
    keys = sorted(k for k, v in ingredients.items() if v.get("codes"))

    def pack(m):
        return [m.get(k) or 0 for k in keys]

    for r in recipes:
        r["guide"] = guided_steps(r)

    state_names = sorted(index["states"])
    data_state_medians = [pack(index["states"][st]["median"]) for st in state_names]
    shops = []
    for s in state_names:
        for d, dv in index["states"][s]["districts"].items():
            fp = os.path.join(P, "d", f"{dv['id']}.json")
            if not os.path.exists(fp):
                continue
            for sh in json.load(open(fp))["shops"]:
                g = sh.get("geo")
                if not g:
                    continue
                shops.append([sh["name"], sh["type"], g[0], g[1], g[2], state_names.index(s), d, pack(sh["prices"])])

    import statistics
    chains = []
    for name, pat in CHAINS:
        ratios, n = [], 0
        for sh in shops:
            if re.search(pat, sh[0].upper()):
                n += 1
                med = data_state_medians[sh[5]]
                ratios += [v / med[i] for i, v in enumerate(sh[7]) if v and med[i]]
        if n >= MIN_CHAIN_SHOPS:
            chains.append([name, pat.replace("\\b", "\\b"), round(statistics.median(ratios), 3), n])

    data = {
        "ingredients": ingredients,
        "recipes": recipes,
        "postcodes": postcodes,
        "prices": {"source": index["source"], "date": index["latestPriceDate"], "keys": keys,
                   "national": pack(index["national"]["median"]),
                   "states": state_names,
                   "stateMedian": [pack(index["states"][s]["median"]) for s in state_names],
                   "shops": shops, "chains": chains,
                   "jg": json.load(open(os.path.join(P, "jayagrocer.json"))) if os.path.exists(os.path.join(P, "jayagrocer.json")) else None},
    }
    src = open(os.path.join(ROOT, "prototype", "src.html")).read()
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    out = src.replace("/*__DATA__*/null", blob)
    with open(os.path.join(ROOT, "prototype", "index.html"), "w") as f:
        f.write(out)
    unmatched = sum(1 for r in recipes for k, _ in r["ing"] if not any(k in st["ing"] for st in r["guide"]))
    print(f"prototype/index.html {len(out)//1024} KB, shops={len(shops)}, "
          f"ingredients not linked to any step={unmatched}")


if __name__ == "__main__":
    main()
