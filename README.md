# MasakJe

Weekly dinner planner for Malaysian households of 2–4. It plans rice + lauk + sayur dinners,
builds the shopping list, and prices it with real shop prices from KPDN PriceCatcher.

**Status:** hosted app on Vercel (`public/index.html` + `api/`) with shared households; the claude.ai prototype (`prototype/index.html`) is the same page in local-only mode.

## Households

- Create a household → get a 6-digit PIN → family joins with PIN + their name.
- Plan, shopping ticks (with who ticked), pantry and fridge sync between phones (~12 s, and on open).
- Storage: Upstash Redis via Vercel Marketplace (`KV_REST_API_URL`, `KV_REST_API_TOKEN`). Device tokens are stored hashed. Wrong PINs: 10 per IP per 15 min.
- Local: `npm run dev` (in-memory storage) → http://localhost:3000

## How it works

| Part | File |
|---|---|
| 59 draft recipes (34 lauk, 16 sayur, 9 one-pot), quantities for 4, all halal | `src/data/recipes.json` |
| Ingredient catalog: PriceCatcher item codes, pack sizes, fallback prices | `src/data/ingredients.json` |
| Price pipeline: downloads PriceCatcher, keeps latest price per shop (last 45 days), district/state medians | `scripts/build_prices.py` |
| Geocodes shops (postcode → town name → district centre) with GeoNames postcodes | `scripts/build_prices.py` |
| Jaya Grocer online prices (personal use, weekly, polite) matched to ingredients | `scripts/fetch_jayagrocer.py` + `src/data/jayagrocer_map.json` |
| Shops + opening hours + neighbourhood names from OpenStreetMap (10.6k shops), linked to PriceCatcher shops | `scripts/build_osm_shops.py` |
| Approximate macros per serving | `src/data/nutrition.json` |
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
- Recipe browser: sort by quickest, cheapest per plate, most protein, fewest calories, family favourites; filter by protein, time, type, heat, fridge
- Household recipes ("Write your own" or "Make my version" of ours): shared with everyone, anyone can edit; the planner starts picking one after it has been cooked once and nobody said "Not again"
- Sounds and springy feedback on taps, selections and completions (mute from cooking mode)

## Weekly refresh

`.github/workflows/weekly-prices.yml` runs every Monday 03:17 MYT: PriceCatcher → Jaya Grocer → rebuild → commit.

## Known limits

- Only 37% of shops geocode by postcode; 31% by town name, 28% fall back to district centre (shown as approx.).
- KPDN surveys ~2,100 shops; many branches (e.g. Jaya Grocer Bukit Jelutong) are missing. Chain price levels (Jaya Grocer +6%, Lotus's −13%…) adjust nearby prices for user-added shops.
- Jaya Grocer prices are the Online Store KL list, may differ in-store; personal use only, commercial use needs their permission. 7 ingredients unmatched (chicken breast, kembung, tilapia, salted fish, cornflour, flour, star anise) fall back to PriceCatcher.
- Step ingredients and timers are matched from step text; wording in recipes.json matters.
- ~15 ingredients (tauhu, taugeh, light/dark soy, whole spices…) have no recent PriceCatcher data and use estimates, labelled "Estimate".
- Recipes are AI-drafted and need review by a home cook.

Price data: KPDN PriceCatcher via OpenDOSM, CC BY 4.0. Postcode coordinates: GeoNames, CC BY 4.0. Shops and opening hours: © OpenStreetMap contributors, ODbL 1.0.
