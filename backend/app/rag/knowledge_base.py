"""
knowledge_base.py — Authoritative Agriculture & Crop Health Knowledge Base
=============================================================================
Curated agronomic knowledge for Rice, Maize, Banana, Mango, Citrus/Orange,
Watermelon, Grapes, Beans, Pomegranate, Cotton, Groundnut, Tomato, Potato,
Wheat, Chili, Sugarcane, Soybean, and Onion based on ICAR, FAO-56, and
state agricultural university recommendations (ANGRAU/PJTSAU).

30 knowledge entries covering Diseases, Pests, Fertilizer, Irrigation,
and Integrated Pest Management.
"""

AGRICULTURE_KNOWLEDGE = [
    # ── Original 13 entries (preserved) ──────────────────────
    {
        "id": "banana_black_sigatoka",
        "crop": "Banana",
        "condition": "Black Sigatoka",
        "category": "Disease",
        "title": "Banana Black Sigatoka (Mycosphaerella fijiensis)",
        "content": (
            "Black Sigatoka is a devastating fungal leaf spot disease caused by Pseudocercospora fijiensis "
            "(teleomorph Mycosphaerella fijiensis). Symptoms begin as tiny, reddish-brown to dark streaks on the "
            "lower surface of leaves, typically on the third or fourth leaf from the unfurling spindle. "
            "Streaks enlarge and coalesce into dark oval spots with black borders and sunken gray centers, causing rapid "
            "leaf necrosis and premature ripening of bunches. "
            "Management & Control: (1) Cultural: Regular deleafing of infected leaves to reduce spore inoculum; "
            "maintain optimal spacing (2.0m x 2.0m) to improve air circulation; facilitate field drainage to reduce relative humidity. "
            "(2) Chemical Control: Apply systemic fungicides such as Propiconazole (Tilt 25 EC at 1 ml/L) or Carbendazim (1 g/L) "
            "alternated with contact protectants like Mancozeb 75 WP (2.5 g/L) or mineral oil sprays (10 ml/L) to prevent resistance. "
            "(3) Nutritional support: Ensure balanced potassium (K) nutrition (300 g K2O/plant) to enhance cell wall thickness."
        ),
        "source": "ICAR-NRCB Banana Crop Health Guide & ANGRAU Agronomy"
    },
    {
        "id": "rice_blast",
        "crop": "Rice",
        "condition": "Blast",
        "category": "Disease",
        "title": "Rice Blast Disease (Magnaporthe oryzae)",
        "content": (
            "Rice Blast caused by Magnaporthe oryzae (Pyricularia oryzae) affects leaves, nodes, and panicles. "
            "Symptoms on leaves appear as elliptical, spindle-shaped lesions with brownish-red margins and ash-gray centers. "
            "Neck blast causes blackening and rotting of the panicle neck leading to empty, chaffy grains ('whiteness of ears'). "
            "Favorable conditions: High relative humidity (>90%), dew, temperatures between 20-25°C, and excessive nitrogenous fertilizer application. "
            "Management: (1) Avoid excessive nitrogen; apply nitrogen in 3 split doses (basal, tillering, panicle initiation). "
            "(2) Seed treatment with Tricyclazole 75 WP at 2 g/kg of seed. "
            "(3) Foliar spray: Tricyclazole 75 WP @ 0.6 g/L or Isoprothiolane 40 EC @ 1.5 ml/L or Kasugamycin 3% SL @ 2.5 ml/L at first appearance of leaf lesions."
        ),
        "source": "IRRI & PJTSAU Rice Protection Manual"
    },
    {
        "id": "rice_bph",
        "crop": "Rice",
        "condition": "Brown Plant Hopper",
        "category": "Pest",
        "title": "Rice Brown Plant Hopper - BPH (Nilaparvata lugens)",
        "content": (
            "Brown Plant Hopper (BPH) feeds at the base of the plant stem, sucking sap from phloem vessels. "
            "Severe infestation causes 'hopper burn' — circular patches of drying, lodging, and golden-brown dead plants in fields. "
            "BPH also transmits grassy stunt and ragged stunt viruses. "
            "Management: (1) Adopt alternate wetting and drying (AWD) irrigation; avoid continuous stagnant water. "
            "(2) Provide 'alleyways' of 30 cm every 2-3 meters in transplanted fields for sunlight and aeration. "
            "(3) Avoid synthetic pyrethroids which cause resurgence. "
            "(4) Spray Pymetrozine 50% WG @ 0.6 g/L or Triflumezopyrim 10% SC @ 0.5 ml/L directing spray towards the base of tillers."
        ),
        "source": "ICAR-IIRR Rice Entomology Recommendations"
    },
    {
        "id": "maize_fall_armyworm",
        "crop": "Maize",
        "condition": "Fall Armyworm",
        "category": "Pest",
        "title": "Maize Fall Armyworm - FAW (Spodoptera frugiperda)",
        "content": (
            "Fall Armyworm larvae cause severe defoliation and bore into maize whorls. "
            "Young larvae feed on epidermal tissue causing 'window pane' damage; older larvae chew ragged holes and produce abundant sawdust-like fecal frass inside the central whorl. "
            "Late instars also damage tassels and ears. "
            "Management: (1) Deep summer ploughing to expose pupae to predators and heat. "
            "(2) Intercropping with pulses (cowpea/pigeonpea) and planting napier grass border as trap crop. "
            "(3) Erect pheromone traps @ 5/acre for monitoring. "
            "(4) Bio-control: Release Trichogramma pretiosum or application of Bacillus thuringiensis (Bt) @ 2 g/L. "
            "(5) Chemical: Apply Emamectin benzoate 5% SG @ 0.4 g/L or Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L into the whorl."
        ),
        "source": "ICAR-IIMR Maize Protection Protocols"
    },
    {
        "id": "maize_turcicum_blight",
        "crop": "Maize",
        "condition": "Turcicum Leaf Blight",
        "category": "Disease",
        "title": "Maize Turcicum Leaf Blight (Exserohilum turcicum)",
        "content": (
            "Turcicum leaf blight causes long, elliptical, grayish-green to tan lesions measuring 2.5 to 15 cm on maize leaves. "
            "Lesions start on lower leaves and progress upwards under cool (18-27°C) and humid weather conditions. In severe attacks, leaves dry up completely. "
            "Management: (1) Grow tolerant hybrids such as DHM-117, DHM-121. "
            "(2) Crop rotation with non-host leguminous crops. "
            "(3) Foliar spray of Mancozeb 75 WP @ 2.5 g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L at first sign of disease."
        ),
        "source": "PJTSAU Agronomy Advisory for Maize"
    },
    {
        "id": "citrus_canker",
        "crop": "Orange",
        "condition": "Citrus Canker",
        "category": "Disease",
        "title": "Citrus / Orange Canker (Xanthomonas citri subsp. citri)",
        "content": (
            "Citrus canker is a bacterial disease causing raised, corky, crater-like lesions on leaves, twigs, and fruit. "
            "Lesions on leaves are surrounded by a characteristic oily, water-soaked yellowish halo. Fruit lesions cause premature fruit drop and reduce marketability. "
            "Bacteria enter through stomata and wounds caused by leaf miners or wind. "
            "Management: (1) Prune and burn infected twigs before monsoon flushing. "
            "(2) Control citrus leaf miner (Phyllocnistis citrella) using Imidacloprid 17.8 SL @ 0.3 ml/L. "
            "(3) Spray Copper Oxychloride 50 WP @ 3.0 g/L or Bordeaux mixture (1%) combined with Streptocycline @ 0.1 g/L at flush emergence and fruit setting."
        ),
        "source": "ICAR-CCRI Citrus Disease Compendium"
    },
    {
        "id": "mango_anthracnose",
        "crop": "Mango",
        "condition": "Anthracnose",
        "category": "Disease",
        "title": "Mango Anthracnose (Colletotrichum gloeosporioides)",
        "content": (
            "Anthracnose affects leaves, flowers, panicles, and fruits. On leaves, irregular brownish-black spots form and drop out, creating 'shot-holes'. "
            "Blossom blight destroys flowers and prevents fruit set. On ripening fruits, circular, sunken, dark brown to black rot spots appear (post-harvest decay). "
            "Management: (1) Tree sanitation: Prune dead twigs and open tree canopy for maximum sunlight penetration. "
            "(2) Pre-bloom spray with Carbendazim 50 WP @ 1 g/L or Azoxystrobin 23 SC @ 1 ml/L. "
            "(3) Post-harvest hot water treatment of fruits at 52°C for 5-10 minutes to suppress latent infections."
        ),
        "source": "ICAR-CISH Mango Protection Guide"
    },
    {
        "id": "mango_hopper",
        "crop": "Mango",
        "condition": "Mango Hopper",
        "category": "Pest",
        "title": "Mango Hopper (Idioscopus clypealis, Amritodus atkinsoni)",
        "content": (
            "Mango hoppers are the most destructive insect pest of mango during flowering. Adults and nymphs suck sap from tender inflorescences and shoot buds, "
            "causing flower drying and dropping ('withering of blossom'). They excrete copious honeydew which attracts sooty mold fungus, covering leaves in black soot. "
            "Management: (1) Avoid dense tree spacing; prune dense interior branches. "
            "(2) First spray at panicle emergence: Imidacloprid 17.8 SL @ 0.3 ml/L or Thiamethoxam 25 WG @ 0.25 g/L. "
            "(3) Second spray at fruit set if hopper population exceeds 5 per panicle."
        ),
        "source": "ANGRAU Mango Horticultural Extension"
    },
    {
        "id": "cotton_bollworm",
        "crop": "Cotton",
        "condition": "Pink Bollworm",
        "category": "Pest",
        "title": "Cotton Pink Bollworm (Pectinophora gossypiella)",
        "content": (
            "Pink bollworm larvae enter developing flower buds ('rosette flowers') and young green bolls. "
            "The entry hole heals, and larvae feed inside seeds and lint, resulting in 'locule damage', stained discolored lint, and reduced oil content. "
            "Management: (1) Strictly adhere to closed season (terminate crop by December; avoid ratoon cotton). "
            "(2) Install pheromone traps @ 5-8/acre for monitoring (threshold: 8 moths/trap/day). "
            "(3) Release egg parasitoid Trichogramma bactrae @ 60,000/acre. "
            "(4) Chemical spray: Chlorpyrifos 20 EC @ 2.5 ml/L or Profenofos 50 EC @ 2 ml/L or Spinetoram 11.7 SC @ 0.8 ml/L at threshold."
        ),
        "source": "ICAR-CICR Cotton Pest Management Bulletin"
    },
    {
        "id": "pomegranate_bacterial_blight",
        "crop": "Pomegranate",
        "condition": "Bacterial Blight / Telya",
        "category": "Disease",
        "title": "Pomegranate Bacterial Blight - Telya (Xanthomonas axonopodis pv. punicae)",
        "content": (
            "Telya causes dark water-soaked oily spots on leaves, stems, and fruits. "
            "On fruit, characteristic dark brown to black 'L' or 'Y' shaped cracks develop, rendering the fruit unmarketable. "
            "Splashing rains, warm humid weather (25-35°C), and unsterilized pruning shears accelerate transmission. "
            "Management: (1) Disinfect secateurs with 2.5% sodium hypochlorite or Dettol between cuts. "
            "(2) Prune diseased twigs 2 inches below infected portion and paste cuts with Bordeaux paste. "
            "(3) Spray Streptocycline (0.25 g/L) + Copper Oxychloride (2.5 g/L) or Bronopol (0.5 g/L) at regular 10-14 day intervals during monsoon."
        ),
        "source": "ICAR-NRCP Pomegranate Disease Bulletin"
    },
    {
        "id": "watermelon_downy_mildew",
        "crop": "Watermelon",
        "condition": "Downy Mildew",
        "category": "Disease",
        "title": "Watermelon Downy Mildew (Pseudoperonospora cubensis)",
        "content": (
            "Downy mildew causes angular, chlorotic yellow lesions on the upper leaf surface bounded by leaf veins. "
            "Under humid conditions, a purplish-gray downy mold appears on the underside of leaves corresponding to yellow spots. "
            "Leaves turn brown, curl upwards, and die rapidly. "
            "Management: (1) Drip irrigation instead of overhead sprinklers to keep foliage dry. "
            "(2) Preventative spray: Mancozeb 75 WP @ 2.5 g/L or Chlorothalonil 75 WP @ 2 g/L. "
            "(3) Curative systemic: Cymoxanil 8% + Mancozeb 64% WP @ 2 g/L or Dimethomorph 50 WP @ 1 g/L."
        ),
        "source": "ICAR-IIHR Vegetable Crop Advisory"
    },
    {
        "id": "grapes_powdery_mildew",
        "crop": "Grapes",
        "condition": "Powdery Mildew",
        "category": "Disease",
        "title": "Grapevine Powdery Mildew (Erysiphe necator / Uncinula necator)",
        "content": (
            "Powdery mildew affects all green tissues of grapevine. White-to-gray powdery patches appear on leaves and berries. "
            "Infected young berries become hard, crack open ('berry cracking'), exposing seeds to secondary rots. "
            "Unlike downy mildew, powdery mildew flourishes under warm, dry, shaded conditions with moderate humidity. "
            "Management: (1) Canopy management: Leaf removal around bunch zone to increase airflow and sunlight penetration. "
            "(2) Wettable Sulfur 80 WP @ 2-3 g/L as early preventative. "
            "(3) Systemic: Myclobutanil 10 WP @ 0.4 g/L, Penconazole 10 EC @ 0.5 ml/L, or Fluopyram + Tebuconazole @ 0.6 ml/L."
        ),
        "source": "ICAR-NRCG Grape Health Management"
    },
    {
        "id": "general_fertilizer_npk",
        "crop": "General",
        "condition": "Nutrient Deficiency",
        "category": "Fertilizer",
        "title": "Diagnosing N-P-K Nutrient Deficiencies & Soil Correction",
        "content": (
            "Nitrogen (N) Deficiency: General yellowing (chlorosis) starting on older lower leaves, stunted growth. Correct with Urea (46% N) or Ammonium Sulfate. "
            "Phosphorus (P) Deficiency: Dark green to purplish coloration on older leaves, poor root architecture, delayed maturity. Correct with Single Super Phosphate (SSP) or DAP. "
            "Potassium (K) Deficiency: Marginal leaf scorch, chlorosis along leaf edges of older leaves, weak stems, poor fruit filling. Correct with Muriate of Potash (MOP - 60% K2O) or Potassium Sulfate. "
            "Zinc (Zn) Deficiency: Interveinal chlorosis and 'little leaf' in citrus, rice ('khaira disease'). Correct with Zinc Sulfate 21% @ 25 kg/ha soil or 0.2% foliar spray."
        ),
        "source": "FAO Soil Fertility & Plant Nutrition Guide"
    },

    # ── New entries: Tomato ──────────────────────────────────
    {
        "id": "tomato_late_blight",
        "crop": "Tomato",
        "condition": "Late Blight",
        "category": "Disease",
        "title": "Tomato Late Blight (Phytophthora infestans)",
        "content": (
            "Late blight is a devastating oomycete disease affecting leaves, stems, and fruits of tomato and potato. "
            "Symptoms: Large, irregular, water-soaked, pale-green to dark-brown lesions on leaves, often with a white mold growth on the underside in humid weather. "
            "Stems show dark-brown lesions. Fruits develop firm, dark-brown, greasy patches. Entire fields can collapse within days under favorable conditions (cool 15-22°C, >90% RH). "
            "Management: (1) Use certified disease-free transplants and resistant varieties (e.g., Arka Rakshak). "
            "(2) Prophylactic spray: Mancozeb 75 WP @ 2.5 g/L starting 30 days after transplanting. "
            "(3) Curative: Metalaxyl 8% + Mancozeb 64% WP @ 2.5 g/L or Cymoxanil 8% + Mancozeb 64% WP @ 2 g/L. "
            "(4) Avoid overhead irrigation; provide adequate plant spacing for air circulation."
        ),
        "source": "ICAR-IIHR Vegetable Crop Protection Advisory"
    },
    {
        "id": "tomato_early_blight",
        "crop": "Tomato",
        "condition": "Early Blight",
        "category": "Disease",
        "title": "Tomato Early Blight (Alternaria solani)",
        "content": (
            "Early blight causes characteristic concentric ring 'target board' or 'bull's eye' lesions on lower/older leaves. "
            "Lesions are dark brown to black, round with distinct concentric rings. Severe infection causes defoliation starting from the base, "
            "reducing fruit size and yield. Also causes collar rot in seedlings and fruit rot (leathery, dark, sunken spots at stem end). "
            "Management: (1) Remove and destroy lower infected leaves. "
            "(2) Avoid dense planting; maintain proper spacing (60 cm x 45 cm). "
            "(3) Spray Chlorothalonil 75 WP @ 2 g/L or Azoxystrobin 23 SC @ 1 ml/L alternating with Mancozeb. "
            "(4) Mulching with black polyethylene to prevent rain splash of soil-borne inoculum."
        ),
        "source": "ANGRAU Tomato Production Technology Guide"
    },
    {
        "id": "tomato_whitefly",
        "crop": "Tomato",
        "condition": "Whitefly",
        "category": "Pest",
        "title": "Tomato Whitefly (Bemisia tabaci) & Tomato Leaf Curl Virus",
        "content": (
            "Whitefly (Bemisia tabaci) is both a sap-sucking pest and the vector of Tomato leaf curl virus (ToLCV/Geminiviridae). "
            "Feeding causes yellowing, honeydew excretion, and sooty mold. ToLCV symptoms: severe upward curling, puckering, and stunting "
            "of leaves with interveinal chlorosis; infected plants become bushy, fail to set fruit, and yield loss can reach 100%. "
            "Management: (1) Use ToLCV-resistant hybrids (Arka Ananya, Arka Samrat). "
            "(2) Install yellow sticky traps (12/acre) for monitoring. "
            "(3) Seedling stage: Imidacloprid 70 WG @ 0.3 g/L or Thiamethoxam 25 WG @ 0.3 g/L as drenching. "
            "(4) Neem oil 1% (Azadirachtin 10000 ppm) @ 2 ml/L every 10 days as deterrent."
        ),
        "source": "ICAR-IIHR & ANGRAU Integrated Tomato Advisory"
    },

    # ── Potato ───────────────────────────────────────────────
    {
        "id": "potato_late_blight",
        "crop": "Potato",
        "condition": "Late Blight",
        "category": "Disease",
        "title": "Potato Late Blight (Phytophthora infestans)",
        "content": (
            "Potato late blight is the most destructive disease of potato worldwide. "
            "Water-soaked lesions appear at leaf tips and margins, rapidly enlarging to brown-black necrotic areas. "
            "White cottony sporulation visible on underside of leaves in humid mornings. Tubers develop copper-brown dry rot under the skin. "
            "Management: (1) Plant certified disease-free seed tubers of resistant varieties (Kufri Jyoti, Kufri Girdhari). "
            "(2) Prophylactic: Mancozeb 75 WP @ 2.5 g/L starting 40-45 days after planting. "
            "(3) Curative: Cymoxanil 8% + Mancozeb 64% WP @ 3 g/L or Dimethomorph 50 WP @ 1 g/L at first symptom. "
            "(4) Earthing up (hilling) to prevent zoospore infection of tubers through soil."
        ),
        "source": "ICAR-CPRI Potato Disease Management Guide"
    },

    # ── Groundnut ────────────────────────────────────────────
    {
        "id": "groundnut_tikka_leaf_spot",
        "crop": "Groundnut",
        "condition": "Tikka Leaf Spot",
        "category": "Disease",
        "title": "Groundnut Tikka Disease / Leaf Spot (Cercospora arachidicola & C. personatum)",
        "content": (
            "Tikka disease comprises Early leaf spot (Cercospora arachidicola) and Late leaf spot (Cercosporidium personatum). "
            "Early leaf spot: brown circular spots with yellow halo, dark brown on upper surface with light sporulation. "
            "Late leaf spot: nearly black circular spots without halo, darker with rough surface, more sporulation on underside. "
            "Both cause severe defoliation (up to 50% yield loss) if uncontrolled. "
            "Management: (1) Grow resistant varieties (ICGV 86699, Kadiri 6). "
            "(2) Seed treatment with Thiram + Carbendazim (2+1 g/kg seed). "
            "(3) Spray Chlorothalonil 75 WP @ 2 g/L or Tebuconazole 25.9 EC @ 1 ml/L at 35, 50, and 65 DAS. "
            "(4) Crop rotation with cereals (sorghum/pearl millet) to break disease cycle."
        ),
        "source": "ICAR-DGR Groundnut Pathology Recommendations"
    },

    # ── Wheat ────────────────────────────────────────────────
    {
        "id": "wheat_rust",
        "crop": "Wheat",
        "condition": "Rust",
        "category": "Disease",
        "title": "Wheat Rust Complex (Puccinia spp.)",
        "content": (
            "Three types of rust affect wheat: (a) Brown/Leaf rust (Puccinia triticina) — most common, orange-brown pustules "
            "scattered on upper leaf surface; (b) Yellow/Stripe rust (P. striiformis) — yellow pustules arranged in distinct stripes "
            "along leaf veins, favored by cool temperatures (2-15°C); (c) Black/Stem rust (P. graminis) — large dark reddish-brown "
            "to black pustules on stems and leaf sheaths, most damaging but less frequent. "
            "Management: (1) Grow resistant varieties recommended by the wheat coordination center for your zone. "
            "(2) Timely sowing (Nov 15-30 for NWPZ) to escape disease window. "
            "(3) Foliar spray: Propiconazole 25 EC @ 1 ml/L or Tebuconazole 25.9 EC @ 1 ml/L at first appearance of pustules. "
            "(4) Repeat spray after 15 days if disease pressure continues."
        ),
        "source": "ICAR-IIWBR Wheat Disease Surveillance Bulletin"
    },

    # ── Chili / Pepper ───────────────────────────────────────
    {
        "id": "chili_thrips",
        "crop": "Chili",
        "condition": "Thrips",
        "category": "Pest",
        "title": "Chili Thrips (Scirtothrips dorsalis)",
        "content": (
            "Chili thrips cause upward curling of leaves (leaf curl), distortion of growing points, and silvery sheen on leaves. "
            "Heavy infestation results in stunted bushy plants. Thrips also vector chili leaf curl virus. "
            "The pest is most damaging during dry, hot weather (30-35°C). "
            "Management: (1) Install blue sticky traps @ 12-15/acre for monitoring. "
            "(2) Mulch with silver reflective plastic to repel thrips. "
            "(3) Spray Fipronil 5 SC @ 1.5 ml/L or Spinetoram 11.7 SC @ 0.5 ml/L. "
            "(4) Bio-control: Conserve predatory mites (Amblyseius swirskii) and release Chrysoperla carnea (green lacewing) @ 50,000/ha."
        ),
        "source": "ANGRAU & PJTSAU Chili Integrated Pest Management"
    },
    {
        "id": "chili_fruit_rot",
        "crop": "Chili",
        "condition": "Anthracnose / Fruit Rot",
        "category": "Disease",
        "title": "Chili Fruit Rot / Die-Back (Colletotrichum capsici)",
        "content": (
            "Anthracnose and die-back are major diseases of chili. Fruit rot: sunken circular lesions on fruits with concentric rings "
            "of dark acervuli. Severely affected fruits shrivel and mummify. Die-back: progressive necrosis of shoot tips, branches "
            "drying from tips downward. Yield losses of 10-80% are common in humid conditions. "
            "Management: (1) Hot water treatment of seeds at 52°C for 30 minutes. "
            "(2) Seed treatment with Thiram + Carbendazim (2+1 g/kg). "
            "(3) Field spray: Mancozeb 75 WP @ 2.5 g/L alternated with Azoxystrobin 23 SC @ 1 ml/L at flowering and fruiting. "
            "(4) Avoid overhead irrigation; remove mummified fruits from field to reduce inoculum."
        ),
        "source": "ICAR-IIHR Chili Crop Health Manual"
    },

    # ── Sugarcane ────────────────────────────────────────────
    {
        "id": "sugarcane_red_rot",
        "crop": "Sugarcane",
        "condition": "Red Rot",
        "category": "Disease",
        "title": "Sugarcane Red Rot (Colletotrichum falcatum)",
        "content": (
            "Red rot is the most serious disease of sugarcane (the 'cancer of sugarcane'). "
            "The pathogen enters through borer holes. Internally, the pith turns red with white patches arranged transversely. "
            "External symptoms include drying of the third or fourth leaf from top (mid-rib turns white), then gradual wilting. "
            "In severe epidemics, entire cane fields collapse. "
            "Management: (1) Most important: plant only resistant varieties (consult state variety release). "
            "(2) Sett treatment: Soak setts in Carbendazim 50 WP solution (1 g/L) for 15-20 minutes before planting. "
            "(3) Avoid ratoon of susceptible varieties. "
            "(4) Remove and destroy infected clumps; do not use infected cane as seed material."
        ),
        "source": "ICAR-SBI (Sugarcane Breeding Institute) Red Rot Advisory"
    },
    {
        "id": "sugarcane_borer",
        "crop": "Sugarcane",
        "condition": "Stem Borer",
        "category": "Pest",
        "title": "Sugarcane Shoot / Stem Borer Complex (Chilo spp.)",
        "content": (
            "Sugarcane borers include shoot borer (Chilo infuscatellus) causing 'dead hearts' in early stage, internode borer "
            "(Chilo sacchariphagus) boring into stalks at joints, and top borer (Scirpophaga excerptalis). "
            "Dead hearts: central whorl leaf dries and pulls out easily. Internode damage: bore holes with frass. "
            "Management: (1) Release egg parasitoid Trichogramma chilonis @ 50,000/acre at 30, 45, and 60 DAP. "
            "(2) Apply Carbofuran 3G @ 33 kg/ha in the soil around plants at 30 and 60 DAP. "
            "(3) Light traps @ 1/5 acres to monitor adult moths. "
            "(4) Earthing up at 90 DAP and detrashing (removing lower dry leaves) to remove egg masses."
        ),
        "source": "ICAR-SBI Sugarcane Entomology Manual"
    },

    # ── Soybean ──────────────────────────────────────────────
    {
        "id": "soybean_yellow_mosaic",
        "crop": "Soybean",
        "condition": "Yellow Mosaic Virus",
        "category": "Disease",
        "title": "Soybean Yellow Mosaic (Mungbean Yellow Mosaic India Virus — MYMIV)",
        "content": (
            "Yellow mosaic is a devastating viral disease transmitted by whitefly (Bemisia tabaci). "
            "Symptoms: bright yellow or golden-yellow patches on leaves in irregular mosaic pattern. "
            "Severe infection causes complete yellowing, leaf puckering, reduced pod formation, and seed discoloration. "
            "Management: (1) Grow resistant varieties (JS-335, NRC-37, JS 95-60). "
            "(2) Timely sowing (June 20 - July 10 in kharif) to escape peak whitefly activity. "
            "(3) Seed treatment with Thiamethoxam 30 FS @ 10 ml/kg seed. "
            "(4) Spray Thiamethoxam 25 WG @ 0.3 g/L at 20 DAS if whitefly population exceeds ETL (1 adult/plant). "
            "(5) Border rows of non-host cereal (sorghum/maize) to act as barrier."
        ),
        "source": "ICAR-IISR Soybean Extension Bulletin"
    },

    # ── Onion ────────────────────────────────────────────────
    {
        "id": "onion_purple_blotch",
        "crop": "Onion",
        "condition": "Purple Blotch",
        "category": "Disease",
        "title": "Onion Purple Blotch (Alternaria porri)",
        "content": (
            "Purple blotch is the most common and destructive foliar disease of onion. "
            "Symptoms begin as small, water-soaked white flecks that enlarge into oval to elliptical purplish-brown lesions "
            "with concentric zones and dark margins. Under severe infection, leaves collapse from the tip downward, leading to "
            "poor bulb development and 30-80% yield loss. "
            "Management: (1) Use healthy, disease-free seed. "
            "(2) Proper spacing (15 cm x 10 cm) to reduce canopy humidity. "
            "(3) Spray Mancozeb 75 WP @ 2.5 g/L or Tricyclazole 75 WP @ 1 g/L at 30 DAT and repeat every 10-15 days. "
            "(4) Alternate with Tebuconazole 25.9 EC @ 1 ml/L to prevent fungicide resistance."
        ),
        "source": "ICAR-DOGR (Directorate of Onion & Garlic Research) Advisory"
    },
    {
        "id": "onion_thrips",
        "crop": "Onion",
        "condition": "Thrips",
        "category": "Pest",
        "title": "Onion Thrips (Thrips tabaci)",
        "content": (
            "Onion thrips are tiny (1-1.5 mm), pale yellow insects that feed by rasping leaf surface and sucking the exuded sap. "
            "Damage appears as silvery-white streaks and blotches on leaves, leading to leaf curling, drying from tips, "
            "and significant bulb size reduction (up to 50% yield loss). Most destructive during dry, hot weather (25-30°C). "
            "Management: (1) Overhead irrigation or sprinkler to mechanically dislodge thrips and increase humidity. "
            "(2) Blue sticky traps @ 15/acre for monitoring. "
            "(3) Spray Fipronil 5 SC @ 1.5 ml/L or Spinetoram 11.7 SC @ 0.5 ml/L alternated with Lambda-cyhalothrin 5 EC @ 0.6 ml/L. "
            "(4) Neem oil (Azadirachtin 1500 ppm) @ 5 ml/L as eco-friendly option."
        ),
        "source": "ICAR-DOGR Onion Entomology Guide"
    },

    # ── Cross-cutting: Irrigation & Soil Management ─────────
    {
        "id": "general_irrigation_scheduling",
        "crop": "General",
        "condition": "Irrigation Management",
        "category": "Irrigation",
        "title": "Irrigation Scheduling & Water Use Efficiency for Major Crops",
        "content": (
            "Efficient irrigation scheduling maximizes water use efficiency (WUE) and prevents water stress. "
            "Rice: Maintain 5 cm standing water during vegetative stage; adopt AWD (Alternate Wetting and Drying) to save 20-25% water. "
            "Wheat: Critical stages — Crown Root Initiation (21 DAS), Tillering (40-45 DAS), Jointing (60-65 DAS), Flowering (80-85 DAS), Milk (100-105 DAS). "
            "Maize: IW/CPE ratio of 1.0; irrigate at 50% depletion of available soil moisture. "
            "Cotton: Skip furrow irrigation during vegetative phase; drip at 0.6 Epan during boll development. "
            "Vegetables (Tomato/Chili): Drip irrigation at 100% Epan with fertigation reduces water use by 40% and increases yield 20-30%. "
            "General principle: Morning irrigation is preferred to reduce disease incidence from overnight leaf wetness."
        ),
        "source": "FAO-56 & ANGRAU Agronomy Advisory on Water Management"
    },
    {
        "id": "general_organic_ipm",
        "crop": "General",
        "condition": "Organic Pest Management",
        "category": "Pest",
        "title": "Organic & Biological Integrated Pest Management (IPM) Practices",
        "content": (
            "Integrated Pest Management (IPM) combines cultural, biological, and selective chemical methods to keep pest populations "
            "below economic threshold levels (ETL) while minimizing environmental harm. "
            "Bio-control agents: (1) Trichogramma spp. (egg parasitoids for lepidopteran pests) @ 50,000-1,00,000/ha. "
            "(2) Chrysoperla carnea (green lacewing, predator of aphids, whiteflies, and small caterpillars) @ 50,000 eggs/ha. "
            "(3) Trichoderma viride/harzianum (soil-borne disease bio-control) @ 4 g/kg seed or 2.5 kg/ha with FYM. "
            "(4) Pseudomonas fluorescens @ 10 g/kg seed or 2.5 kg/ha mixed with FYM for wilt/root rot suppression. "
            "Botanical pesticides: Neem oil (Azadirachtin) 1500-10000 ppm as antifeedant and IGR @ 5 ml/L. "
            "Trap crops: Marigold for nematodes, Napier grass for stem borer, Mustard for aphids in Brassica."
        ),
        "source": "ICAR-NBAIR Biological Control Manual & NPOF Organic Standards"
    },
    {
        "id": "general_soil_testing",
        "crop": "General",
        "condition": "Soil Health",
        "category": "Fertilizer",
        "title": "Soil Testing & Integrated Nutrient Management (INM)",
        "content": (
            "Soil testing is the foundation of scientific fertilizer management. Collect composite soil samples (0-15 cm depth) "
            "from 10-15 spots per field in a zigzag pattern. Avoid sampling near bunds, manure heaps, or trees. "
            "Optimal soil pH for most crops: 6.0-7.5. Acidic soils (<5.5): apply lime @ 2-4 t/ha based on lime requirement. "
            "Alkaline/sodic soils (>8.5): apply Gypsum @ 5-10 t/ha based on gypsum requirement. "
            "INM strategy: 50% N through organic (FYM 10 t/ha or Vermicompost 5 t/ha) + 50% N through inorganic sources. "
            "Apply full P & K and half N as basal; remaining N in 2 split top-dressings. "
            "Micronutrient application: ZnSO4 @ 25 kg/ha (for zinc), Borax @ 10 kg/ha (for boron), FeSO4 @ 50 kg/ha (for iron)."
        ),
        "source": "ICAR-IISS Soil Health Card Scheme & ANGRAU INM Manual"
    },
    {
        "id": "general_seed_treatment",
        "crop": "General",
        "condition": "Seed Treatment",
        "category": "Disease",
        "title": "Seed Treatment Protocols for Major Field Crops",
        "content": (
            "Seed treatment is the most cost-effective plant protection measure, providing protection during the critical "
            "germination and seedling establishment phase. "
            "Standard fungicide treatment: Thiram 75% WS @ 3 g/kg + Carbendazim 50 WP @ 2 g/kg (broad-spectrum). "
            "Insecticidal treatment: Imidacloprid 48 FS @ 1.25 ml/kg or Thiamethoxam 30 FS @ 3.3 ml/kg (systemic, sucking pests). "
            "Bio-agent treatment: Trichoderma viride @ 4 g/kg seed (for soil-borne diseases). Apply bio-agents separately from "
            "chemical fungicides (wait 48 hours between treatments). "
            "Rhizobium inoculation: For legumes (soybean, groundnut, chickpea) @ 25 g culture/kg seed with jaggery solution. "
            "Protocol: Apply fungicide first → dry in shade → insecticide → dry → bio-agent (last). "
            "Never expose treated seeds to direct sunlight."
        ),
        "source": "ICAR Seed Technology Manual & ANGRAU Seed Treatment Advisory"
    },

    # ── Rice additional ──────────────────────────────────────
    {
        "id": "rice_sheath_blight",
        "crop": "Rice",
        "condition": "Sheath Blight",
        "category": "Disease",
        "title": "Rice Sheath Blight (Rhizoctonia solani)",
        "content": (
            "Sheath blight is caused by the soil-borne fungus Rhizoctonia solani. Symptoms: oval to irregular greenish-gray "
            "water-soaked lesions with dark-brown borders on leaf sheaths near the water line. Lesions coalesce and spread upward, "
            "causing sheaths to rot, leaves to dry, and lodging. "
            "Favorable conditions: close spacing, high nitrogen, warm (25-32°C), and humid weather with standing water. "
            "Management: (1) Avoid excessive nitrogen application (reduce by 25% from standard recommendation). "
            "(2) Maintain wider spacing (20 cm x 15 cm) and drain standing water periodically. "
            "(3) Spray Hexaconazole 5 EC @ 2 ml/L or Validamycin 3 SL @ 2 ml/L at boot leaf stage. "
            "(4) Seed treatment with Trichoderma viride @ 4 g/kg seed as biological control."
        ),
        "source": "ICAR-IIRR Rice Disease Management Protocol"
    },
]
