# MasakJe

Weekly dinner planner for Malaysian households of 2–4. It plans rice + lauk + sayur dinners,
builds the shopping list, and prices it with real shop prices from KPDN PriceCatcher.

**Status:** clickable prototype (`prototype/index.html`). The full PWA comes after feedback.

## How it works

| Part | File |
|---|---|
| 59 draft recipes (34 lauk, 16 sayur, 9 one-pot), quantities for 4, all halal | `src/data/recipes.json` |
| Ingredient catalog: PriceCatcher item codes, pack sizes, fallback prices | `src/data/ingredients.json` |
| Price pipeline: downloads PriceCatcher, keeps latest price per shop (last 45 days), district/state medians | `scripts/build_prices.py` |
| Geocodes shops (postcode → town name → district centre) with GeoNames postcodes | `scripts/build_prices.py` |
| Bundles everything into one offline page, derives per-step ingredients and timers | `scripts/build_prototype.py` |
| Prototype UI | `prototype/src.html` → `prototype/index.html` |

## Rebuild

```bash
python3 scripts/build_prices.py
python3 scripts/build_prototype.py
```

## Features (prototype)

- Postcode → nearest PriceCatcher shops, search all shops, or add your own shop (chain-adjusted estimate)
- Plan → Shop → Cook flow; "I'm at the shop" / "I'm cooking now" entry points
- Shopping list with shop unit prices, progress, pantry check
- Fridge & freezer: list subtracts it, planner prefers it, pack leftovers added after shopping
- Cooking mode: get-ready checklist with progress, one step per screen, step timers, total elapsed time
- Allergies (incl. hidden in sauces) and vegetable dislikes

## Known limits

- Only 37% of shops geocode by postcode; 31% by town name, 28% fall back to district centre (shown as approx.).
- KPDN surveys ~2,100 shops; many branches (e.g. Jaya Grocer Bukit Jelutong) are missing. Chain price levels (Jaya Grocer +6%, Lotus's −13%…) adjust nearby prices for user-added shops.
- Step ingredients and timers are matched from step text; wording in recipes.json matters.
- ~15 ingredients (tauhu, taugeh, light/dark soy, whole spices…) have no recent PriceCatcher data and use estimates, labelled "Estimate".
- Recipes are AI-drafted and need review by a home cook.

Price data: KPDN PriceCatcher via OpenDOSM, CC BY 4.0. Postcode coordinates: GeoNames, CC BY 4.0.
