"""One-off: adds 14 ingredients and 47 recipes (Malaysian, Asian, Western) to src/data.

Recipes are for 4 people. Steps are [text, ingredient keys added at that step, timer seconds, wait-until cue],
in the order things go into the pot, like the existing ones. Run once; it refuses to add anything twice.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "src", "data")

NEW_ING = {
    "spaghetti": {"name": "Spaghetti", "unit": "g", "aisle": "Noodles", "size": 500, "pack": 500, "fallback": 5.5},
    "sohun": {"name": "Sohun (glass noodles)", "unit": "g", "aisle": "Noodles", "size": 250, "pack": 250, "fallback": 3.5},
    "butter": {"name": "Butter", "unit": "g", "aisle": "Dairy", "size": 250, "pack": 250, "fallback": 11.9},
    "cheese": {"name": "Cheddar cheese", "unit": "g", "aisle": "Dairy", "size": 250, "pack": 250, "fallback": 12.9},
    "milk": {"name": "Fresh milk", "unit": "ml", "aisle": "Dairy", "size": 1000, "pack": 1000, "fallback": 7.9},
    "mushroom": {"name": "Cendawan butang (button mushrooms)", "unit": "g", "aisle": "Vegetables", "size": 200, "pack": 200, "fallback": 4.9},
    "lemon": {"name": "Lemon", "unit": "pc", "aisle": "Vegetables", "size": 1, "pack": 1, "fallback": 1.5},
    "breadcrumbs": {"name": "Serbuk roti (breadcrumbs)", "unit": "g", "aisle": "Dry goods", "size": 200, "pack": 200, "fallback": 4.5},
    "gochujang": {"name": "Gochujang (Korean chili paste)", "unit": "g", "aisle": "Pantry", "size": 500, "pack": 500, "fallback": 17.9, "pantry": True},
    "honey": {"name": "Madu (honey)", "unit": "g", "aisle": "Pantry", "size": 500, "pack": 500, "fallback": 16.9, "pantry": True},
    "vinegar": {"name": "Cuka (vinegar)", "unit": "ml", "aisle": "Pantry", "size": 500, "pack": 500, "fallback": 3.2, "pantry": True},
    "stock_cube": {"name": "Kiub stok ayam (stock cubes)", "unit": "pc", "aisle": "Pantry", "size": 12, "pack": 12, "fallback": 4.9, "pantry": True},
    "sesame_seed": {"name": "Bijan (sesame seeds)", "unit": "g", "aisle": "Spices", "size": 100, "pack": 100, "fallback": 3.9, "pantry": True},
    "mixed_herbs": {"name": "Herba campur (dried mixed herbs)", "unit": "g", "aisle": "Spices", "size": 20, "pack": 20, "fallback": 6.5, "pantry": True},
}
# per 100 g/ml, or per piece for "pc": [kcal, protein, carbs, fat]
NEW_NUT = {"spaghetti": [371, 13, 75, 1.5], "sohun": [351, 0.2, 86, 0.1], "butter": [717, 0.9, 0.1, 81], "cheese": [403, 25, 1.3, 33],
           "milk": [61, 3.2, 4.8, 3.3], "mushroom": [22, 3.1, 3.3, 0.3], "lemon": [17, 0.6, 5.4, 0.2], "breadcrumbs": [395, 13, 72, 5],
           "gochujang": [195, 4.5, 40, 1.5], "honey": [304, 0.3, 82, 0], "vinegar": [18, 0, 0, 0], "stock_cube": [15, 0.5, 1.5, 1],
           "sesame_seed": [573, 18, 23, 50], "mixed_herbs": [265, 9, 69, 4]}
NEW_JG = {
    "spaghetti": {"match": "spaghetti", "exclude": "sauce|ready|instant|whole ?wheat|gluten"},
    "sohun": {"match": "glass noodle|sohun|tang hoon|vermicelli.*(mung|bean)", "exclude": "soup|cup|instant"},
    "butter": {"match": "butter", "exclude": "peanut|cookie|biscuit|cake|garlic|spread|margarine|milk|bread|popcorn|croissant|ghee"},
    "cheese": {"match": "cheddar", "exclude": "cracker|biscuit|snack|bread|sauce|cake|stick"},
    "milk": {"match": "fresh milk|full cream milk|pasteuri[sz]ed milk", "exclude": "chocolate|strawberry|banana|coffee|uht|powder|soy|oat|almond|condensed|evaporated"},
    "mushroom": {"match": "button mushroom|cendawan butang|white mushroom", "exclude": "can|soup|dried"},
    "lemon": {"match": "^lemon|lemon \\(", "exclude": "juice|tea|grass|cake|cookie|sauce|drink|flavour"},
    "breadcrumbs": {"match": "bread ?crumb|panko", "exclude": "chicken|fish|nugget"},
    "gochujang": {"match": "gochujang|red pepper paste", "exclude": "sauce mix|ramyun|noodle"},
    "honey": {"match": "honey", "exclude": "lemon|chicken|cereal|biscuit|cake|drink|tea|mustard|bee pollen|comb|stick"},
    "vinegar": {"match": "vinegar|cuka", "exclude": "apple cider|balsamic|wine|chip"},
    "stock_cube": {"match": "chicken (stock|bouillon) cube|kiub", "exclude": "beef|fish|vegetable"},
    "sesame_seed": {"match": "sesame seed|bijan", "exclude": "oil|paste|bun|biscuit|candy"},
    "mixed_herbs": {"match": "mixed herbs|italian (herbs|seasoning)|oregano", "exclude": "sauce|pizza|chicken"},
}

R = []
def rec(id, name, en, kind, protein, cuisine, mins, spicy, ing, steps):
    R.append(dict(id=id, name=name, en=en, kind=kind, protein=protein, cuisine=cuisine, mins=mins, spicy=spicy, ing=[list(x) for x in ing], guide=steps))

# ---------------- Malaysian ----------------
rec("ayam-percik", "Ayam percik", "Grilled chicken in spiced coconut gravy", "lauk", "chicken", "Malay", 60, 1,
    [("chicken_thigh", 800), ("santan", 400), ("dried_chili", 15), ("shallot", 60), ("garlic", 20), ("ginger", 15), ("lemongrass", 2), ("turmeric_powder", 5), ("tamarind", 15), ("sugar", 20), ("salt", 6), ("oil", 30)],
    [["Soak the dried chili in hot water, then blend with the shallots, garlic, ginger and lemongrass", ["dried_chili", "shallot", "garlic", "ginger", "lemongrass"], 0, "A smooth paste"],
     ["Rub the chicken with the turmeric and a little of the salt", ["chicken_thigh", "turmeric_powder"], 0, ""],
     ["Heat the oil and tumis the paste on low-medium heat", ["oil"], 480, "Pecah minyak: the oil separates, 6 to 8 min"],
     ["Add the santan, tamarind water, sugar and the rest of the salt. Simmer, stirring, until thick", ["santan", "tamarind", "sugar", "salt"], 600, "Thick enough to coat a spoon"],
     ["Grill or pan-sear the chicken, basting with the gravy and turning often", [], 1200, "Charred at the edges and cooked through, about 20 min"],
     ["Pour the rest of the gravy over to serve", [], 0, ""]])
rec("ayam-goreng-kunyit", "Ayam goreng kunyit", "Turmeric fried chicken", "lauk", "chicken", "Malay", 40, 0,
    [("chicken", 1000), ("turmeric_powder", 10), ("chili_powder", 5), ("salt", 8), ("garlic", 15), ("oil", 400)],
    [["Pound the garlic to a paste", ["garlic"], 0, ""],
     ["Rub the chicken with the turmeric, chili powder, salt and garlic. Leave 15 min", ["chicken", "turmeric_powder", "chili_powder", "salt"], 900, "Marinated, deep yellow all over"],
     ["Heat the oil in a wok on medium", ["oil"], 120, "A drop of marinade sizzles at once"],
     ["Fry the chicken in batches, turning once", [], 720, "Deep golden and crisp, about 12 min"],
     ["Drain on paper and serve", [], 0, ""]])
rec("ayam-sos-tiram", "Ayam masak sos tiram", "Chicken in oyster sauce", "lauk", "chicken", "Chinese", 35, 0,
    [("chicken_thigh", 700), ("oyster_sauce", 45), ("soy_dark", 10), ("sugar", 10), ("garlic", 20), ("ginger", 15), ("onion", 150), ("spring_onion", 30), ("cornflour", 8), ("oil", 45), ("salt", 3)],
    [["Toss the chicken with the cornflour and a spoon of the oyster sauce. Leave 10 min", ["chicken_thigh", "cornflour"], 600, ""],
     ["Heat the oil and fry the chicken until browned", ["oil"], 360, "Golden on all sides"],
     ["Add the garlic, ginger and onion and stir-fry", ["garlic", "ginger", "onion"], 120, "Fragrant and the onion softens"],
     ["Add the rest of the oyster sauce, the dark soy, sugar, salt and half a cup of water. Simmer", ["oyster_sauce", "soy_dark", "sugar", "salt"], 600, "Glossy, thick sauce and the chicken cooked through"],
     ["Toss in the spring onion and serve", ["spring_onion"], 0, ""]])
rec("ayam-goreng-madu", "Ayam goreng madu", "Honey-glazed fried chicken wings", "lauk", "chicken", "Malay", 40, 0,
    [("chicken_wing", 800), ("honey", 60), ("soy_light", 20), ("oyster_sauce", 15), ("garlic", 15), ("sesame_seed", 5), ("flour", 60), ("salt", 5), ("white_pepper", 2), ("oil", 400)],
    [["Season the wings with the salt and pepper and coat lightly in flour", ["chicken_wing", "salt", "white_pepper", "flour"], 0, ""],
     ["Deep-fry in batches", ["oil"], 600, "Golden and crisp, about 10 min"],
     ["Pour off the oil and fry the chopped garlic", ["garlic"], 45, "Pale gold"],
     ["Add the honey, light soy and oyster sauce and let it bubble", ["honey", "soy_light", "oyster_sauce"], 60, "Sticky and glossy"],
     ["Toss the wings in the glaze and scatter the sesame seeds", ["sesame_seed"], 0, ""]])
rec("daging-lada-hitam", "Daging masak lada hitam", "Black pepper beef", "lauk", "beef", "Malay", 35, 1,
    [("beef", 600), ("black_pepper", 10), ("oyster_sauce", 30), ("soy_dark", 10), ("sugar", 8), ("onion", 150), ("capsicum", 150), ("garlic", 15), ("cornflour", 8), ("oil", 45), ("salt", 3)],
    [["Slice the beef thinly against the grain and toss with the cornflour", ["beef", "cornflour"], 0, ""],
     ["Heat the oil until smoking and sear the beef in 2 batches. Lift out", ["oil"], 180, "Browned outside, still pink inside"],
     ["Fry the garlic and crushed black pepper", ["garlic", "black_pepper"], 60, "Fragrant, about 1 min"],
     ["Add the onion and capsicum and stir-fry", ["onion", "capsicum"], 120, "Just softened, still bright"],
     ["Put the beef back with the oyster sauce, dark soy, sugar, salt and a third of a cup of water. Toss", ["oyster_sauce", "soy_dark", "sugar", "salt"], 120, "The sauce coats the beef"]])
rec("daging-masak-merah", "Daging masak merah", "Beef in spiced tomato chili sauce", "lauk", "beef", "Malay", 75, 1,
    [("beef", 700), ("dried_chili", 25), ("shallot", 80), ("garlic", 20), ("ginger", 15), ("onion", 150), ("tomato", 200), ("tomato_sauce", 80), ("sugar", 20), ("salt", 6), ("oil", 80), ("cinnamon", 3), ("star_anise", 2)],
    [["Boil the beef pieces in 3 cups of water until tender. Keep the stock", ["beef"], 2400, "A fork slides in easily, about 40 min"],
     ["Blend the soaked dried chili with the shallots, garlic and ginger", ["dried_chili", "shallot", "garlic", "ginger"], 0, "A smooth red paste"],
     ["Heat the oil and fry the cinnamon and star anise", ["oil", "cinnamon", "star_anise"], 60, "Fragrant"],
     ["Add the paste and tumis", [], 600, "Pecah minyak: the oil separates, 8 to 10 min"],
     ["Add the beef, a cup of the stock, the tomato sauce, sugar and salt. Simmer", ["tomato_sauce", "sugar", "salt"], 600, "Thick and glossy red"],
     ["Add the sliced onion and tomato wedges and cook 2 min", ["onion", "tomato"], 120, "The onion is just soft"]])
rec("ikan-bakar-air-asam", "Ikan bakar air asam", "Grilled mackerel with tamarind chili dip", "lauk", "fish", "Malay", 40, 2,
    [("fish_kembung", 800), ("turmeric_powder", 5), ("salt", 6), ("oil", 15), ("tamarind", 30), ("chili_padi", 20), ("shallot", 40), ("tomato", 100), ("belacan", 10), ("sugar", 10), ("lime", 2)],
    [["Clean and score the fish, then rub with the turmeric and salt", ["fish_kembung", "turmeric_powder", "salt"], 0, ""],
     ["Toast the belacan in a dry pan", ["belacan"], 90, "Fragrant and crumbly"],
     ["Pound the chili padi with the belacan, then mix with the tamarind water, sliced shallot, chopped tomato, sugar and lime juice", ["chili_padi", "tamarind", "shallot", "tomato", "sugar", "lime"], 0, "Sour, spicy and a little sweet"],
     ["Brush the fish with oil and grill, turning once", ["oil"], 900, "The skin blisters and the flesh flakes at the bone, about 15 min"],
     ["Serve with the air asam", [], 0, ""]])
rec("ikan-goreng-sambal", "Ikan goreng sambal", "Fried fish with sambal", "lauk", "fish", "Malay", 45, 2,
    [("fish_selar", 800), ("turmeric_powder", 5), ("salt", 8), ("oil", 350), ("dried_chili", 25), ("shallot", 80), ("garlic", 15), ("belacan", 8), ("tamarind", 20), ("sugar", 20), ("onion", 150)],
    [["Rub the fish with the turmeric", ["fish_selar", "turmeric_powder"], 0, ""],
     ["Fry the fish in hot oil, turning once. Set aside", ["oil"], 600, "Crisp and golden, about 10 min"],
     ["Blend the soaked chili with the shallots, garlic and belacan", ["dried_chili", "shallot", "garlic", "belacan"], 0, "A thick paste"],
     ["Pour off all but 4 tbsp oil and tumis the paste", [], 720, "Pecah minyak and dark red"],
     ["Add the tamarind water, sugar, salt and the sliced onion", ["tamarind", "sugar", "salt", "onion"], 180, "The sambal is thick and shiny"],
     ["Spoon the sambal over the fish", [], 0, ""]])
rec("ikan-tiga-rasa", "Ikan tiga rasa", "Crispy fish in sweet, sour and spicy sauce", "lauk", "fish", "Malay", 40, 2,
    [("fish_tilapia", 900), ("flour", 40), ("salt", 5), ("oil", 400), ("garlic", 15), ("chili_red", 40), ("chili_padi", 10), ("onion", 150), ("capsicum", 100), ("tomato_sauce", 60), ("chili_sauce", 60), ("tamarind", 15), ("sugar", 20), ("fish_sauce", 10)],
    [["Score the fish, rub with salt and dust with flour", ["fish_tilapia", "salt", "flour"], 0, ""],
     ["Deep-fry until crisp, turning once", ["oil"], 720, "Crisp skin, white at the bone"],
     ["Pour off most of the oil and fry the garlic, chili and chili padi", ["garlic", "chili_red", "chili_padi"], 60, "Fragrant"],
     ["Add the onion and capsicum", ["onion", "capsicum"], 90, "Just soft"],
     ["Add the tomato sauce, chili sauce, tamarind water, sugar, fish sauce and half a cup of water. Simmer", ["tomato_sauce", "chili_sauce", "tamarind", "sugar", "fish_sauce"], 180, "A thick, glossy sauce"],
     ["Pour over the fish", [], 0, ""]])
rec("ikan-selar-sumbat", "Ikan selar sumbat", "Mackerel stuffed with sambal", "lauk", "fish", "Malay", 45, 2,
    [("fish_selar", 800), ("dried_chili", 20), ("shallot", 60), ("garlic", 10), ("belacan", 5), ("sugar", 10), ("salt", 6), ("turmeric_powder", 3), ("oil", 300)],
    [["Clean the fish and slit along both sides of the backbone to make a pocket", ["fish_selar"], 0, ""],
     ["Blend the soaked chili with the shallots, garlic and belacan", ["dried_chili", "shallot", "garlic", "belacan"], 0, "A thick paste"],
     ["Tumis the paste in 3 tbsp of the oil with the sugar", ["sugar"], 480, "Pecah minyak, thick and dark"],
     ["Rub the fish with the turmeric and salt, then fill the pockets with sambal", ["turmeric_powder", "salt"], 0, "Pockets full"],
     ["Shallow-fry the fish in the rest of the oil, turning carefully", ["oil"], 600, "Crisp and golden on both sides"]])
rec("udang-masak-kicap", "Udang masak kicap", "Prawns in sweet soy", "lauk", "seafood", "Malay", 25, 1,
    [("prawn", 500), ("kicap_manis", 45), ("soy_light", 10), ("garlic", 15), ("shallot", 40), ("chili_red", 30), ("onion", 100), ("sugar", 5), ("oil", 30), ("salt", 2)],
    [["Peel and devein the prawns, leaving the tails on", ["prawn"], 0, ""],
     ["Heat the oil and fry the garlic and shallots", ["oil", "garlic", "shallot"], 90, "Golden and fragrant"],
     ["Add the prawns and stir-fry", [], 120, "Just turning pink"],
     ["Add the kicap manis, light soy, sugar, salt and 3 tbsp water", ["kicap_manis", "soy_light", "sugar", "salt"], 120, "Bubbling and sticky"],
     ["Toss in the sliced chili and onion", ["chili_red", "onion"], 60, "The onion still has a little crunch"]])
rec("sotong-goreng-tepung", "Sotong goreng tepung", "Crispy fried squid", "lauk", "seafood", "Malay", 30, 0,
    [("squid", 600), ("flour", 120), ("cornflour", 60), ("egg", 1), ("chili_powder", 3), ("white_pepper", 2), ("salt", 5), ("oil", 500), ("chili_sauce", 60)],
    [["Clean the squid, cut into rings and pat dry", ["squid"], 0, ""],
     ["Mix the flour, cornflour, chili powder, pepper and salt", ["flour", "cornflour", "chili_powder", "white_pepper", "salt"], 0, ""],
     ["Dip the rings in beaten egg, then coat in the flour mix", ["egg"], 0, "Fully coated; shake off the excess"],
     ["Deep-fry in batches in hot oil", ["oil"], 120, "Light golden and crisp, about 2 min a batch. Longer makes it rubbery"],
     ["Serve with chili sauce", ["chili_sauce"], 0, ""]])
rec("sambal-kerang", "Sambal kerang", "Cockles in sambal", "lauk", "seafood", "Malay", 30, 2,
    [("cockle", 800), ("dried_chili", 25), ("shallot", 80), ("garlic", 15), ("belacan", 8), ("tamarind", 15), ("sugar", 15), ("salt", 4), ("oil", 60), ("onion", 100)],
    [["Scrub the cockles, blanch 1 min, then take them out of the shells", ["cockle"], 60, "Shells just open"],
     ["Blend the soaked chili with the shallots, garlic and belacan", ["dried_chili", "shallot", "garlic", "belacan"], 0, "A thick paste"],
     ["Heat the oil and tumis the paste", ["oil"], 600, "Pecah minyak"],
     ["Add the tamarind water, sugar, salt and sliced onion", ["tamarind", "sugar", "salt", "onion"], 120, "A thick sambal"],
     ["Stir in the cockles and turn off the heat", [], 30, "Just heated; longer makes them tough"]])
rec("telur-masak-kicap", "Telur masak kicap", "Eggs in sweet soy", "lauk", "egg", "Malay", 25, 1,
    [("egg", 8), ("oil", 200), ("kicap_manis", 50), ("soy_dark", 10), ("onion", 150), ("garlic", 10), ("chili_red", 20), ("sugar", 5), ("salt", 2)],
    [["Boil the eggs 9 min, cool and peel", ["egg"], 540, "Hard-boiled"],
     ["Shallow-fry the eggs in the oil, rolling them around", ["oil"], 240, "Blistered golden skin"],
     ["Pour off most of the oil and fry the garlic and onion", ["garlic", "onion"], 120, "The onion is soft"],
     ["Add the kicap manis, dark soy, sugar, salt and half a cup of water", ["kicap_manis", "soy_dark", "sugar", "salt"], 180, "Thick and sticky"],
     ["Add the eggs and sliced chili and coat well", ["chili_red"], 60, ""]])
rec("kari-telur", "Kari telur", "Egg and potato curry", "lauk", "egg", "Indian", 35, 1,
    [("egg", 8), ("curry_meat", 30), ("santan", 200), ("potato", 300), ("onion", 150), ("garlic", 15), ("ginger", 10), ("curry_leaves", 2), ("tomato", 100), ("oil", 45), ("salt", 6), ("star_anise", 1), ("cinnamon", 2)],
    [["Boil the eggs 9 min, cool and peel", ["egg"], 540, "Hard-boiled"],
     ["Mix the curry powder with a little water", ["curry_meat"], 0, "A thick paste"],
     ["Heat the oil and fry the cinnamon, star anise and curry leaves", ["oil", "cinnamon", "star_anise", "curry_leaves"], 60, "The leaves crackle"],
     ["Add the onion, garlic and ginger and tumis", ["onion", "garlic", "ginger"], 120, "Soft and golden"],
     ["Add the curry paste and fry", [], 300, "Pecah minyak"],
     ["Add the potato cubes and a cup and a half of water. Simmer", ["potato"], 900, "The potato is tender"],
     ["Add the santan, tomato, salt and eggs. Simmer gently", ["santan", "tomato", "salt"], 300, "The gravy thickens; don't let the santan boil hard"]])
rec("buncis-goreng-udang", "Buncis goreng udang", "French beans with prawns", "sayur", "veg", "Malay", 15, 0,
    [("french_bean", 300), ("prawn", 150), ("garlic", 10), ("oyster_sauce", 15), ("oil", 30), ("salt", 2)],
    [["Slice the beans diagonally", ["french_bean"], 0, ""],
     ["Fry the garlic in the oil", ["oil", "garlic"], 45, "Fragrant"],
     ["Add the prawns", ["prawn"], 90, "Pink"],
     ["Add the beans, oyster sauce, salt and 3 tbsp water. Stir-fry", ["oyster_sauce", "salt"], 180, "Bright green and tender-crisp"]])
rec("kobis-bunga-goreng", "Kobis bunga goreng", "Cauliflower and carrot stir-fry", "sayur", "veg", "Chinese", 15, 0,
    [("cauliflower", 400), ("carrot", 100), ("garlic", 10), ("oyster_sauce", 15), ("cornflour", 5), ("oil", 30), ("salt", 2)],
    [["Cut the cauliflower into florets and slice the carrot", ["cauliflower", "carrot"], 0, ""],
     ["Fry the garlic in the oil", ["oil", "garlic"], 45, "Fragrant"],
     ["Add the vegetables and a quarter cup of water. Cover", [], 180, "The florets are just tender"],
     ["Add the oyster sauce and salt, then the cornflour mixed with a little water", ["oyster_sauce", "salt", "cornflour"], 60, "The sauce clings"]])
rec("acar-timun", "Acar timun", "Cucumber and carrot pickle", "sayur", "veg", "Malay", 20, 1,
    [("cucumber", 300), ("carrot", 100), ("onion", 100), ("chili_red", 30), ("salt", 4), ("oil", 20), ("garlic", 10), ("turmeric_powder", 2), ("vinegar", 60), ("sugar", 40), ("peanuts", 30)],
    [["Cut the cucumber and carrot into sticks; slice the onion and chili", ["cucumber", "carrot", "onion", "chili_red"], 0, ""],
     ["Toss with the salt, leave 10 min, then squeeze dry", ["salt"], 600, "Softened, water drawn out"],
     ["Fry the garlic and turmeric in the oil", ["oil", "garlic", "turmeric_powder"], 30, "Fragrant"],
     ["Add the vinegar and sugar, bring to the boil, then cool", ["vinegar", "sugar"], 120, "The sugar has dissolved"],
     ["Pour over the vegetables, mix, and top with crushed peanuts", ["peanuts"], 0, ""]])
rec("mee-kari", "Mee kari", "Curry noodles with chicken", "onepot", "chicken", "Malay", 45, 1,
    [("yellow_mee", 600), ("chicken_thigh", 400), ("curry_meat", 40), ("santan", 400), ("taugeh", 150), ("tofu", 2), ("egg", 4), ("shallot", 60), ("garlic", 15), ("lemongrass", 2), ("chili_padi", 10), ("oil", 45), ("salt", 6), ("sugar", 10), ("lime", 2)],
    [["Boil the eggs 9 min and peel; blanch the taugeh and noodles", ["egg", "taugeh", "yellow_mee"], 540, ""],
     ["Blend the shallots, garlic and lemongrass", ["shallot", "garlic", "lemongrass"], 0, "A smooth paste"],
     ["Tumis the paste with the curry powder in the oil", ["oil", "curry_meat"], 420, "Pecah minyak"],
     ["Add the chicken and 4 cups of water. Simmer", ["chicken_thigh"], 900, "The chicken is cooked through"],
     ["Add the santan, cubed tofu, sugar and salt. Simmer gently", ["santan", "tofu", "sugar", "salt"], 300, "Hot but not boiling hard"],
     ["Pour over the noodles and top with egg, chili padi and lime", ["chili_padi", "lime"], 0, ""]])
rec("nasi-tomato", "Nasi tomato", "Tomato rice with spiced chicken", "onepot", "chicken", "Malay", 50, 0,
    [("rice", 400), ("chicken_thigh", 600), ("turmeric_powder", 3), ("chili_powder", 3), ("salt", 6), ("oil", 30), ("onion", 100), ("garlic", 10), ("ginger", 10), ("cinnamon", 3), ("star_anise", 2), ("tomato", 150), ("tomato_sauce", 60), ("milk", 100)],
    [["Rub the chicken with the turmeric, chili powder and half the salt", ["chicken_thigh", "turmeric_powder", "chili_powder"], 0, ""],
     ["Wash the rice and drain", ["rice"], 0, ""],
     ["Fry the onion, garlic, ginger, cinnamon and star anise in the oil", ["oil", "onion", "garlic", "ginger", "cinnamon", "star_anise"], 120, "The onion is golden"],
     ["Add the chopped tomato and tomato sauce and cook down", ["tomato", "tomato_sauce"], 180, "Jammy"],
     ["Stir in the rice, milk, the rest of the salt and a cup and a half of water. Cook in the rice cooker or a covered pot", ["milk", "salt"], 1200, "The water is absorbed and the grains are tender"],
     ["Meanwhile bake or pan-grill the chicken", [], 1500, "Golden and the juices run clear"]])
rec("bihun-sup", "Bihun sup ayam", "Rice vermicelli chicken soup", "onepot", "chicken", "Malay", 40, 0,
    [("bihun", 300), ("chicken_breast", 400), ("ginger", 10), ("soup_spice", 10), ("shallot", 40), ("garlic", 15), ("oil", 30), ("salt", 6), ("white_pepper", 2), ("sawi", 200), ("taugeh", 150), ("spring_onion", 20)],
    [["Boil the chicken in 6 cups of water with the ginger and soup spice", ["chicken_breast", "ginger", "soup_spice"], 1200, "Cooked through. Shred it and keep the stock"],
     ["Fry the sliced shallots and garlic in the oil", ["shallot", "garlic", "oil"], 120, "Golden and crisp. Set aside"],
     ["Soak the bihun in hot water and drain", ["bihun"], 300, "Soft"],
     ["Season the stock with the salt and pepper, then blanch the sawi and taugeh in it", ["salt", "white_pepper", "sawi", "taugeh"], 60, "The greens are bright"],
     ["Put noodles, greens and chicken in bowls, ladle the soup over, and top with fried shallots and spring onion", ["spring_onion"], 0, ""]])
rec("mee-hailam", "Mee hailam", "Hainanese braised noodles", "onepot", "chicken", "Chinese", 30, 0,
    [("yellow_mee", 600), ("chicken_breast", 250), ("carrot", 80), ("oil", 30), ("garlic", 15), ("prawn", 150), ("oyster_sauce", 30), ("soy_dark", 15), ("soy_light", 15), ("white_pepper", 2), ("salt", 2), ("sawi", 200), ("cornflour", 15), ("egg", 2)],
    [["Slice the chicken and carrot; blanch the noodles", ["chicken_breast", "carrot", "yellow_mee"], 0, ""],
     ["Fry the garlic in the oil", ["oil", "garlic"], 45, "Fragrant"],
     ["Add the chicken and prawns and stir-fry", ["prawn"], 180, "The prawns are pink and the chicken white"],
     ["Add 2 cups of water, the sauces, pepper, salt, carrot and sawi. Boil", ["oyster_sauce", "soy_dark", "soy_light", "white_pepper", "salt", "sawi"], 180, "The greens are tender"],
     ["Add the noodles, thicken with the cornflour mixed in water, then swirl in the beaten egg", ["cornflour", "egg"], 60, "A thick gravy with egg ribbons"]])

# ---------------- Asian ----------------
rec("tom-kha-gai", "Tom kha gai", "Thai chicken coconut soup", "lauk", "chicken", "Thai", 30, 1,
    [("lemongrass", 3), ("galangal", 30), ("santan", 400), ("chicken_breast", 400), ("mushroom", 150), ("tomato", 100), ("fish_sauce", 30), ("sugar", 8), ("salt", 2), ("chili_padi", 8), ("lime", 4)],
    [["Bruise the lemongrass and slice the galangal", ["lemongrass", "galangal"], 0, ""],
     ["Bring the santan and 2 cups of water to a gentle simmer with the lemongrass and galangal", ["santan"], 300, "Fragrant; keep it gentle"],
     ["Add the sliced chicken and mushrooms", ["chicken_breast", "mushroom"], 420, "The chicken is white through"],
     ["Add the tomato, fish sauce, sugar, salt and bruised chili padi", ["tomato", "fish_sauce", "sugar", "salt", "chili_padi"], 120, ""],
     ["Turn off the heat and squeeze in the lime", ["lime"], 0, "Sour, salty and creamy"]])
rec("pad-thai", "Pad thai", "Thai fried flat noodles with prawns", "onepot", "seafood", "Thai", 30, 1,
    [("tamarind", 30), ("fish_sauce", 30), ("sugar", 30), ("oil", 60), ("garlic", 15), ("shallot", 30), ("tofu", 1), ("prawn", 250), ("egg", 3), ("kuetiau", 400), ("taugeh", 150), ("spring_onion", 30), ("peanuts", 40), ("chili_powder", 3), ("lime", 2)],
    [["Mix the tamarind water, fish sauce and sugar into a sauce", ["tamarind", "fish_sauce", "sugar"], 0, ""],
     ["Fry the garlic, shallots and diced tofu in the oil", ["oil", "garlic", "shallot", "tofu"], 120, "The tofu is golden"],
     ["Add the prawns", ["prawn"], 90, "Pink"],
     ["Push to one side and scramble the eggs", ["egg"], 60, "Just set"],
     ["Add the noodles and the sauce and toss", ["kuetiau"], 180, "The noodles are soft and the sauce absorbed"],
     ["Toss in the taugeh and spring onion. Serve with crushed peanuts, chili powder and lime", ["taugeh", "spring_onion", "peanuts", "chili_powder", "lime"], 0, ""]])
rec("khao-pad-gai", "Khao pad gai", "Thai chicken fried rice", "onepot", "chicken", "Thai", 25, 1,
    [("rice", 400), ("oil", 45), ("garlic", 15), ("onion", 100), ("chicken_breast", 300), ("egg", 3), ("tomato", 100), ("fish_sauce", 20), ("soy_light", 10), ("sugar", 5), ("spring_onion", 20), ("cucumber", 100), ("lime", 2), ("chili_padi", 6)],
    [["Use rice cooked a day ahead, or spread fresh rice out to cool", ["rice"], 0, ""],
     ["Fry the garlic and onion in the oil", ["oil", "garlic", "onion"], 90, "Fragrant"],
     ["Add the diced chicken", ["chicken_breast"], 240, "Cooked through"],
     ["Push aside and scramble the eggs", ["egg"], 60, "Just set"],
     ["Add the rice, tomato, fish sauce, light soy and sugar. Toss over high heat", ["tomato", "fish_sauce", "soy_light", "sugar"], 180, "Piping hot, the grains separate"],
     ["Serve with spring onion, cucumber, lime and chili padi", ["spring_onion", "cucumber", "lime", "chili_padi"], 0, ""]])
rec("pla-rad-prik", "Pla rad prik", "Crispy fish with chili garlic sauce", "lauk", "fish", "Thai", 35, 2,
    [("fish_siakap", 900), ("salt", 4), ("cornflour", 40), ("oil", 500), ("garlic", 25), ("chili_red", 40), ("chili_padi", 10), ("shallot", 30), ("tamarind", 20), ("fish_sauce", 25), ("sugar", 40)],
    [["Score the fish, salt it and dust with cornflour", ["fish_siakap", "salt", "cornflour"], 0, ""],
     ["Deep-fry until crisp", ["oil"], 840, "Crisp all over, about 14 min"],
     ["Pound the garlic, chilies and shallots", ["garlic", "chili_red", "chili_padi", "shallot"], 0, "A rough paste"],
     ["Fry the paste in 2 tbsp of the oil", [], 90, "Fragrant"],
     ["Add the tamarind water, fish sauce, sugar and a quarter cup of water. Simmer", ["tamarind", "fish_sauce", "sugar"], 180, "Syrupy"],
     ["Pour over the fish", [], 0, ""]])
rec("kai-jeow", "Kai jeow", "Thai crispy omelette", "lauk", "egg", "Thai", 10, 0,
    [("egg", 6), ("fish_sauce", 10), ("oil", 200), ("spring_onion", 20), ("chili_sauce", 40)],
    [["Beat the eggs with the fish sauce and 1 tbsp of water", ["egg", "fish_sauce"], 0, "Very frothy"],
     ["Heat the oil in a wok until smoking", ["oil"], 120, "Shimmering"],
     ["Pour in the eggs from a height", [], 60, "Puffs up and crisps at the edges"],
     ["Flip and cook the other side", [], 45, "Golden brown"],
     ["Top with spring onion and serve with chili sauce", ["spring_onion", "chili_sauce"], 0, ""]])
rec("mapo-tofu", "Mapo tofu daging", "Spicy tofu with minced beef", "lauk", "tofu", "Chinese", 25, 2,
    [("beef", 200), ("tofu", 3), ("oil", 30), ("garlic", 15), ("ginger", 10), ("chili_powder", 5), ("chili_sauce", 30), ("soy_light", 15), ("soy_dark", 5), ("sugar", 5), ("black_pepper", 2), ("cornflour", 10), ("sesame_oil", 5), ("spring_onion", 20)],
    [["Mince the beef finely and cube the tofu", ["beef", "tofu"], 0, ""],
     ["Fry the garlic, ginger and chili powder in the oil", ["oil", "garlic", "ginger", "chili_powder"], 45, "A red, fragrant oil"],
     ["Add the beef", [], 180, "Browned and crumbly"],
     ["Add the chili sauce, soy sauces, sugar, pepper and a cup of water, then the tofu. Simmer", ["chili_sauce", "soy_light", "soy_dark", "sugar", "black_pepper"], 240, "The tofu is heated through"],
     ["Thicken with the cornflour mixed in water; add the sesame oil and spring onion", ["cornflour", "sesame_oil", "spring_onion"], 30, "A glossy sauce"]])
rec("telur-tomato", "Telur goreng tomato", "Tomato and egg stir-fry", "lauk", "egg", "Chinese", 15, 0,
    [("egg", 6), ("salt", 3), ("oil", 45), ("tomato", 400), ("tomato_sauce", 20), ("sugar", 10), ("cornflour", 5), ("spring_onion", 20)],
    [["Beat the eggs with a pinch of the salt", ["egg"], 0, ""],
     ["Softly scramble the eggs in half the oil and lift out", ["oil"], 60, "Just set, still soft"],
     ["Fry the tomato wedges in the rest of the oil", ["tomato"], 180, "Soft and juicy"],
     ["Add the ketchup, sugar, salt and a quarter cup of water, then thicken with the cornflour", ["tomato_sauce", "sugar", "salt", "cornflour"], 60, "Saucy"],
     ["Fold the eggs back in gently and top with spring onion", ["spring_onion"], 30, ""]])
rec("daging-brokoli", "Daging brokoli", "Beef and broccoli", "lauk", "beef", "Chinese", 25, 0,
    [("beef", 450), ("cornflour", 12), ("broccoli", 400), ("oil", 45), ("garlic", 15), ("ginger", 10), ("oyster_sauce", 40), ("soy_dark", 10), ("sugar", 8), ("salt", 2), ("sesame_oil", 5)],
    [["Slice the beef thinly and toss with half the cornflour", ["beef"], 0, ""],
     ["Blanch the broccoli for 1 min", ["broccoli"], 60, "Bright green"],
     ["Sear the beef in hot oil and lift out", ["oil"], 120, "Browned"],
     ["Fry the garlic and ginger", ["garlic", "ginger"], 30, "Fragrant"],
     ["Add the oyster sauce, dark soy, sugar, salt and half a cup of water; put the beef and broccoli back and thicken with the rest of the cornflour", ["oyster_sauce", "soy_dark", "sugar", "salt", "cornflour"], 90, "Glossy and coating"],
     ["Drizzle with sesame oil", ["sesame_oil"], 0, ""]])
rec("ayam-stim-cendawan", "Ayam stim cendawan", "Steamed chicken with mushrooms", "lauk", "chicken", "Chinese", 35, 0,
    [("chicken_thigh", 600), ("mushroom", 150), ("ginger", 20), ("oyster_sauce", 20), ("soy_light", 15), ("sesame_oil", 10), ("cornflour", 8), ("sugar", 5), ("white_pepper", 2), ("spring_onion", 20)],
    [["Cut the chicken into pieces and slice the mushrooms and ginger", ["chicken_thigh", "mushroom", "ginger"], 0, ""],
     ["Mix with the oyster sauce, light soy, sesame oil, cornflour, sugar and pepper. Leave 15 min", ["oyster_sauce", "soy_light", "sesame_oil", "cornflour", "sugar", "white_pepper"], 900, "Marinated"],
     ["Spread on a plate and steam over high heat", [], 1200, "The chicken is cooked through and the juices clear, about 20 min"],
     ["Top with spring onion", ["spring_onion"], 0, ""]])
rec("ayam-teriyaki", "Ayam teriyaki", "Chicken teriyaki", "lauk", "chicken", "Japanese", 25, 0,
    [("soy_light", 60), ("sugar", 25), ("honey", 30), ("ginger", 10), ("garlic", 10), ("chicken_thigh", 700), ("oil", 15), ("cornflour", 5), ("sesame_seed", 5), ("spring_onion", 15)],
    [["Mix the soy, sugar, honey, grated ginger, garlic and 4 tbsp of water", ["soy_light", "sugar", "honey", "ginger", "garlic"], 0, ""],
     ["Pan-fry the chicken skin-side down in the oil", ["chicken_thigh", "oil"], 480, "The skin is crisp and golden"],
     ["Flip and cook the other side", [], 300, "Cooked through"],
     ["Pour in the sauce and let it bubble, turning the chicken. Thicken with the cornflour if needed", ["cornflour"], 180, "Glossy and sticky"],
     ["Slice and top with sesame seeds and spring onion", ["sesame_seed", "spring_onion"], 0, ""]])
rec("oyakodon", "Oyakodon", "Japanese chicken and egg rice bowl", "onepot", "chicken", "Japanese", 30, 0,
    [("rice", 400), ("stock_cube", 1), ("soy_light", 50), ("sugar", 20), ("onion", 200), ("chicken_thigh", 400), ("egg", 5), ("spring_onion", 20)],
    [["Cook the rice", ["rice"], 1200, ""],
     ["Dissolve the stock cube in a cup of hot water with the soy and sugar", ["stock_cube", "soy_light", "sugar"], 0, ""],
     ["Simmer the sliced onion in the stock", ["onion"], 180, "Soft"],
     ["Add the chicken pieces and simmer", ["chicken_thigh"], 360, "Cooked through"],
     ["Pour in the lightly beaten eggs and cover", ["egg"], 60, "Just set, still soft on top"],
     ["Slide over bowls of rice and top with spring onion", ["spring_onion"], 0, ""]])
rec("chicken-katsu", "Chicken katsu", "Japanese crispy chicken cutlet", "lauk", "chicken", "Japanese", 30, 0,
    [("chicken_breast", 600), ("salt", 4), ("black_pepper", 2), ("flour", 60), ("egg", 2), ("breadcrumbs", 120), ("oil", 400), ("tomato_sauce", 40), ("oyster_sauce", 15), ("sugar", 5), ("cabbage", 200)],
    [["Butterfly the chicken, pound to an even thickness and season", ["chicken_breast", "salt", "black_pepper"], 0, ""],
     ["Coat in flour, then beaten egg, then breadcrumbs", ["flour", "egg", "breadcrumbs"], 0, "Fully coated"],
     ["Fry in hot oil, turning once", ["oil"], 480, "Deep golden and cooked through, about 8 min"],
     ["Mix the ketchup, oyster sauce and sugar for the sauce", ["tomato_sauce", "oyster_sauce", "sugar"], 0, ""],
     ["Slice and serve with finely shredded cabbage", ["cabbage"], 0, ""]])
rec("ayam-gochujang", "Ayam gochujang", "Spicy Korean gochujang chicken", "lauk", "chicken", "Korean", 35, 2,
    [("gochujang", 60), ("soy_light", 20), ("sugar", 15), ("honey", 20), ("garlic", 20), ("ginger", 10), ("chicken_thigh", 700), ("oil", 30), ("onion", 150), ("cabbage", 200), ("sesame_oil", 10), ("sesame_seed", 5), ("spring_onion", 20)],
    [["Mix the gochujang, soy, sugar, honey, garlic and ginger", ["gochujang", "soy_light", "sugar", "honey", "garlic", "ginger"], 0, ""],
     ["Coat the chicken pieces in half the sauce and leave 15 min", ["chicken_thigh"], 900, "Marinated"],
     ["Fry the chicken in the oil", ["oil"], 420, "Browned"],
     ["Add the onion, cabbage, the rest of the sauce and a quarter cup of water", ["onion", "cabbage"], 360, "The chicken is cooked, the cabbage soft and the sauce sticky"],
     ["Finish with sesame oil, sesame seeds and spring onion", ["sesame_oil", "sesame_seed", "spring_onion"], 0, ""]])
rec("japchae", "Japchae", "Korean glass noodles with beef and vegetables", "onepot", "beef", "Korean", 35, 0,
    [("sohun", 250), ("bayam", 200), ("egg", 2), ("beef", 200), ("garlic", 15), ("oil", 30), ("carrot", 100), ("onion", 100), ("mushroom", 100), ("soy_light", 50), ("sugar", 25), ("sesame_oil", 25), ("black_pepper", 2), ("sesame_seed", 5)],
    [["Soak the sohun, boil 5 min and drain", ["sohun"], 300, "Soft and springy"],
     ["Blanch the bayam and squeeze dry", ["bayam"], 30, ""],
     ["Fry the beaten egg into a thin omelette and slice it", ["egg"], 60, ""],
     ["Stir-fry the beef strips with the garlic in the oil", ["beef", "garlic", "oil"], 120, "Browned"],
     ["Add the carrot, onion and mushroom", ["carrot", "onion", "mushroom"], 180, "Just tender"],
     ["Toss everything with the soy, sugar, sesame oil, pepper and seeds", ["soy_light", "sugar", "sesame_oil", "black_pepper", "sesame_seed"], 60, "The noodles are glossy"]])
rec("bibimbap", "Bibimbap", "Korean mixed rice bowl", "onepot", "beef", "Korean", 40, 1,
    [("rice", 400), ("beef", 250), ("soy_light", 30), ("sugar", 15), ("garlic", 15), ("bayam", 200), ("taugeh", 150), ("sesame_oil", 20), ("carrot", 100), ("oil", 30), ("egg", 4), ("gochujang", 40), ("sesame_seed", 5)],
    [["Cook the rice", ["rice"], 1200, ""],
     ["Toss the beef strips with the soy, sugar and garlic", ["beef", "soy_light", "sugar", "garlic"], 0, ""],
     ["Blanch the bayam and taugeh separately and season with sesame oil", ["bayam", "taugeh", "sesame_oil"], 60, ""],
     ["Stir-fry the carrot sticks, then the beef, in the oil", ["carrot", "oil"], 240, "The beef is browned"],
     ["Fry the eggs sunny-side up", ["egg"], 120, "The whites are set, the yolks runny"],
     ["Top the rice with everything, a spoon of gochujang and sesame seeds. Mix before eating", ["gochujang", "sesame_seed"], 0, ""]])

# ---------------- Western ----------------
rec("spaghetti-aglio-olio", "Spaghetti aglio olio", "Garlic and chili spaghetti with prawns", "onepot", "seafood", "Western", 20, 1,
    [("spaghetti", 400), ("salt", 8), ("oil", 80), ("garlic", 30), ("chili_powder", 3), ("prawn", 250), ("black_pepper", 2), ("lemon", 1), ("spring_onion", 20), ("cheese", 30)],
    [["Boil the spaghetti in salted water 1 min less than the packet says. Keep a cup of the pasta water", ["spaghetti", "salt"], 600, "Al dente: a little bite left"],
     ["Gently fry the sliced garlic and chili flakes in the oil", ["oil", "garlic", "chili_powder"], 120, "Pale gold, not brown"],
     ["Add the prawns", ["prawn"], 120, "Pink"],
     ["Toss in the pasta with a splash of the pasta water", [], 60, "A silky sauce coats the pasta"],
     ["Finish with pepper, lemon, spring onion and grated cheese", ["black_pepper", "lemon", "spring_onion", "cheese"], 0, ""]])
rec("spaghetti-bolognese", "Spaghetti bolognese", "Spaghetti with beef tomato sauce", "onepot", "beef", "Western", 50, 0,
    [("onion", 150), ("carrot", 100), ("garlic", 15), ("oil", 30), ("beef", 400), ("tomato", 400), ("tomato_sauce", 60), ("mixed_herbs", 3), ("sugar", 5), ("salt", 6), ("black_pepper", 2), ("spaghetti", 400), ("cheese", 40)],
    [["Finely chop the onion, carrot and garlic", ["onion", "carrot", "garlic"], 0, ""],
     ["Fry them in the oil", ["oil"], 300, "Soft and sweet"],
     ["Add the minced beef", ["beef"], 300, "Browned and crumbly"],
     ["Add the chopped tomato, ketchup, herbs, sugar, salt, pepper and a cup of water. Simmer", ["tomato", "tomato_sauce", "mixed_herbs", "sugar", "salt", "black_pepper"], 1500, "Thick and rich, about 25 min"],
     ["Boil the spaghetti", ["spaghetti"], 600, "Al dente"],
     ["Serve the sauce on the pasta with grated cheese", ["cheese"], 0, ""]])
rec("pasta-ayam-cendawan", "Creamy chicken mushroom pasta", "Spaghetti in a creamy chicken and mushroom sauce", "onepot", "chicken", "Western", 30, 0,
    [("spaghetti", 400), ("chicken_breast", 350), ("butter", 30), ("onion", 100), ("garlic", 15), ("mushroom", 200), ("flour", 20), ("milk", 400), ("cheese", 50), ("mixed_herbs", 2), ("salt", 6), ("black_pepper", 2)],
    [["Boil the spaghetti", ["spaghetti"], 600, "Al dente"],
     ["Season the chicken strips and fry in the butter. Lift out", ["chicken_breast", "butter"], 300, "Cooked through"],
     ["Fry the onion, garlic and mushrooms", ["onion", "garlic", "mushroom"], 240, "The mushrooms are golden"],
     ["Stir in the flour, then slowly the milk", ["flour", "milk"], 240, "Smooth and thickened"],
     ["Add the cheese, herbs, salt, pepper, the chicken and pasta. Toss", ["cheese", "mixed_herbs", "salt", "black_pepper"], 60, "Creamy and coating the pasta"]])
rec("chicken-chop", "Chicken chop", "Chicken chop with black pepper sauce, wedges and coleslaw", "onepot", "chicken", "Western", 45, 1,
    [("chicken_thigh", 700), ("salt", 6), ("black_pepper", 8), ("flour", 30), ("potato", 500), ("oil", 60), ("butter", 20), ("onion", 100), ("garlic", 10), ("oyster_sauce", 20), ("soy_dark", 5), ("sugar", 5), ("milk", 100), ("cabbage", 200), ("carrot", 80), ("vinegar", 15)],
    [["Season the thighs with salt and half the pepper and dust with flour", ["chicken_thigh", "salt", "black_pepper", "flour"], 0, ""],
     ["Cut the potatoes into wedges and fry until golden", ["potato", "oil"], 900, "Crisp outside, soft inside"],
     ["Pan-fry the chicken skin-side down, then turn", [], 600, "Golden and cooked through"],
     ["Melt the butter and fry the onion, garlic and the rest of the pepper", ["butter", "onion", "garlic"], 120, "Fragrant"],
     ["Add the oyster sauce, dark soy, sugar, milk and a quarter cup of water. Simmer", ["oyster_sauce", "soy_dark", "sugar", "milk"], 180, "A thick pepper sauce"],
     ["Toss the shredded cabbage and carrot with the vinegar for the coleslaw, and serve everything together", ["cabbage", "carrot", "vinegar"], 0, ""]])
rec("fish-and-chips", "Fish and chips", "Battered fish with chips and slaw", "onepot", "fish", "Western", 40, 0,
    [("potato", 800), ("oil", 700), ("flour", 150), ("cornflour", 30), ("egg", 1), ("salt", 6), ("black_pepper", 2), ("fish_siakap", 600), ("lemon", 1), ("cabbage", 150), ("vinegar", 15), ("sugar", 5)],
    [["Cut the potatoes into thick chips, soak 10 min and pat dry", ["potato"], 600, ""],
     ["Fry the chips until soft but pale. Lift out", ["oil"], 360, "Soft, not coloured"],
     ["Whisk the flour, cornflour, egg, salt, pepper and cold water into a batter", ["flour", "cornflour", "egg", "salt", "black_pepper"], 0, "Like thick cream"],
     ["Dip the fish pieces in batter and fry", ["fish_siakap"], 420, "Puffed and golden"],
     ["Fry the chips again", [], 180, "Golden and crisp"],
     ["Serve with lemon and a quick slaw of cabbage, vinegar and sugar", ["lemon", "cabbage", "vinegar", "sugar"], 0, ""]])
rec("shepherds-pie", "Shepherd's pie", "Minced beef under mashed potato", "onepot", "beef", "Western", 70, 0,
    [("potato", 900), ("oil", 15), ("onion", 150), ("carrot", 150), ("garlic", 10), ("beef", 500), ("flour", 10), ("tomato_sauce", 40), ("soy_light", 10), ("stock_cube", 1), ("mixed_herbs", 2), ("butter", 40), ("milk", 100), ("salt", 6), ("black_pepper", 2), ("cheese", 50)],
    [["Boil the potatoes until tender", ["potato"], 1200, "A knife slides in"],
     ["Fry the onion, carrot and garlic in the oil", ["oil", "onion", "carrot", "garlic"], 300, "Soft"],
     ["Add the minced beef", ["beef"], 300, "Browned"],
     ["Stir in the flour, then the ketchup, soy, stock cube, herbs and a cup of water. Simmer", ["flour", "tomato_sauce", "soy_light", "stock_cube", "mixed_herbs"], 900, "A thick gravy"],
     ["Mash the potatoes with the butter, milk, salt and pepper", ["butter", "milk", "salt", "black_pepper"], 0, "Smooth"],
     ["Spread the mash over the beef, top with cheese and bake at 200°C", ["cheese"], 1200, "Golden and bubbling at the edges"]])
rec("ikan-lemon-mentega", "Lemon butter fish", "Pan-fried fish with lemon butter, mash and broccoli", "onepot", "fish", "Western", 35, 0,
    [("potato", 600), ("broccoli", 250), ("fish_siakap", 600), ("flour", 30), ("salt", 5), ("black_pepper", 2), ("oil", 15), ("butter", 50), ("garlic", 10), ("lemon", 2), ("milk", 100)],
    [["Boil the potatoes until tender", ["potato"], 1200, "A knife slides in"],
     ["Steam or blanch the broccoli", ["broccoli"], 180, "Bright green"],
     ["Season the fish, dust with flour and pan-fry in the oil", ["fish_siakap", "flour", "salt", "black_pepper", "oil"], 360, "Golden and flakes easily"],
     ["Melt the butter with the garlic, then squeeze in the lemon", ["butter", "garlic", "lemon"], 60, "Foaming and fragrant"],
     ["Mash the potatoes with the milk and some of the lemon butter; spoon the rest over the fish", ["milk"], 0, ""]])
rec("stew-ayam", "Chicken stew", "Chicken, potato and carrot stew", "onepot", "chicken", "Western", 50, 0,
    [("chicken_thigh", 700), ("butter", 20), ("onion", 150), ("garlic", 10), ("flour", 20), ("potato", 400), ("carrot", 200), ("stock_cube", 1), ("mixed_herbs", 2), ("soy_light", 10), ("milk", 100), ("salt", 4), ("black_pepper", 2)],
    [["Season the chicken and brown it in the butter", ["chicken_thigh", "butter"], 360, "Browned"],
     ["Add the onion and garlic", ["onion", "garlic"], 120, "Soft"],
     ["Stir in the flour", ["flour"], 60, ""],
     ["Add the potato, carrot, stock cube, herbs, soy and 3 cups of water. Simmer covered", ["potato", "carrot", "stock_cube", "mixed_herbs", "soy_light"], 1800, "The vegetables are tender and the chicken falls off the bone"],
     ["Stir in the milk, salt and pepper", ["milk", "salt", "black_pepper"], 120, "Creamy"]])
rec("udang-butter-bawang-putih", "Garlic butter prawns", "Prawns in garlic butter", "lauk", "seafood", "Western", 15, 0,
    [("prawn", 600), ("salt", 3), ("black_pepper", 2), ("butter", 50), ("garlic", 30), ("chili_powder", 2), ("lemon", 1), ("spring_onion", 15)],
    [["Peel the prawns, leaving the tails on, pat dry and season", ["prawn", "salt", "black_pepper"], 0, ""],
     ["Melt the butter and fry the garlic and chili", ["butter", "garlic", "chili_powder"], 60, "Foaming, the garlic pale gold"],
     ["Add the prawns", [], 180, "Pink and curled"],
     ["Squeeze in the lemon and top with spring onion", ["lemon", "spring_onion"], 0, ""]])
rec("coleslaw", "Coleslaw", "Creamy cabbage and carrot slaw", "sayur", "veg", "Western", 15, 0,
    [("cabbage", 300), ("carrot", 100), ("onion", 50), ("milk", 60), ("vinegar", 20), ("sugar", 15), ("lemon", 1), ("salt", 3), ("black_pepper", 1)],
    [["Finely shred the cabbage, carrot and onion", ["cabbage", "carrot", "onion"], 0, ""],
     ["Whisk the milk, vinegar, sugar, lemon juice, salt and pepper", ["milk", "vinegar", "sugar", "lemon", "salt", "black_pepper"], 0, ""],
     ["Toss together and chill 10 min", [], 600, "Slightly softened"]])


def main():
    ing = json.load(open(os.path.join(D, "ingredients.json")))
    nut = json.load(open(os.path.join(D, "nutrition.json")))
    jg = json.load(open(os.path.join(D, "jayagrocer_map.json")))
    recs = json.load(open(os.path.join(D, "recipes.json")))
    steps = json.load(open(os.path.join(D, "steps.json")))
    have = {r["id"] for r in recs["recipes"]}
    clash = [r["id"] for r in R if r["id"] in have]
    if clash:
        raise SystemExit(f"already added: {clash}")
    if set(NEW_ING) & set(ing["items"]):
        raise SystemExit("ingredients already added")
    for k, v in NEW_ING.items():
        nut["per"].setdefault(k, NEW_NUT[k])
        jg["rules"].setdefault(k, NEW_JG[k])
    keys = set(ing["items"]) | set(NEW_ING)
    for r in R:
        used = [k for k, _ in r["ing"]]
        placed = [k for st in r["guide"] for k in st[1]]
        bad = [k for k in used if k not in keys] + [k for k in placed if k not in used]
        missing = [k for k in used if k not in placed]
        dup = {k for k in placed if placed.count(k) > 1}
        if bad or missing or dup:
            raise SystemExit(f"{r['id']}: unknown {bad}, not in any step {missing}, in two steps {dup}")
    # nutrition and the Jaya Grocer map are plain JSON (indent 1); the other three are hand-laid-out, so append in their style
    for name, obj in (("nutrition.json", nut), ("jayagrocer_map.json", jg)):
        json.dump(obj, open(os.path.join(D, name), "w"), ensure_ascii=False, indent=1)
    J = lambda v: json.dumps(v, ensure_ascii=False)
    def append(name, tail, lines):
        path = os.path.join(D, name); t = open(path).read().rstrip()
        assert t.endswith(tail), name
        open(path, "w").write(t[: -len(tail)].rstrip() + ",\n" + ",\n".join(lines) + "\n" + tail + "\n")
    append("ingredients.json", "}\n}", [f'    {J(k) + ":":<19} {{ ' + ", ".join(f"{J(a)}: {J(b)}" for a, b in v.items()) + " }" for k, v in NEW_ING.items()])
    append("recipes.json", "]\n}", [f'    {{ "id": {J(r["id"])}, "name": {J(r["name"])}, "en": {J(r["en"])}, "kind": {J(r["kind"])}, "protein": {J(r["protein"])}, "cuisine": {J(r["cuisine"])}, "mins": {r["mins"]}, "spicy": {r["spicy"]},\n'
                                       f'      "ing": [' + ",".join(f"[{J(k)},{q}]" for k, q in r["ing"]) + '],\n'
                                       f'      "steps": [' + ", ".join(J(st[0]) for st in r["guide"]) + '] }' for r in R])
    append("steps.json", "}\n}", [f'    {J(r["id"])}: [\n' + ",\n".join(f"      [{J(t)}, {J(k)}, {sec}, {J(cue)}]" for t, k, sec, cue in r["guide"]) + "\n    ]" for r in R])
    print(f"added {len(NEW_ING)} ingredients and {len(R)} recipes; now {len(recs['recipes']) + len(R)} recipes")


if __name__ == "__main__":
    main()
