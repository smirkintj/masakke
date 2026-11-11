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
| Bundles everything into one offline page | `scripts/build_prototype.py` |
| Prototype UI | `prototype/src.html` → `prototype/index.html` |

## Rebuild

```bash
python3 scripts/build_prices.py
python3 scripts/build_prototype.py
```

## Known limits

- Cooked-food (tapau) prices are no longer collected by PriceCatcher; tapau price is a user setting.
- ~15 ingredients (tauhu, taugeh, light/dark soy, whole spices…) have no recent PriceCatcher data and use estimates, labelled "Estimate".
- Recipes are AI-drafted and need review by a home cook.

Price data: KPDN PriceCatcher via OpenDOSM, CC BY 4.0.
