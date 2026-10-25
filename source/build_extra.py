"""Belgian dishes, pastries and frituur snacks that NEVO lacks.
Rule: before adding anything, check NEVO. If NEVO has it under another name, add a synonym (EXTRA_SYN) instead.
Output: extra.js with the same fields as data.js plus src/note/recipe/portion."""
import json
js = open("/home/claude/nevo-app/data.js", encoding="utf-8").read()
FOODS = {f["c"]: f for f in json.loads(js.split("let FOODS=", 1)[1].rstrip(";\n"))}
KEYS = ["kcal", "kj", "p", "fat", "sat", "cho", "sug", "fib", "alc", "na", "w"]

def vals(kcal, p, fat, cho, sat=None, sug=None, fib=None, salt=None, w=None):
    return {"kcal": kcal, "kj": round(kcal * 4.184), "p": p, "fat": fat, "sat": sat, "cho": cho, "sug": sug, "fib": fib,
            "alc": 0.0, "na": None if salt is None else round(salt * 400), "w": w}

def recipe(parts, yield_g, alc_keep=1.0):
    """parts: (nevo_code | dict of values, grams, label). Sums nutrients and divides by the cooked yield."""
    tot = {k: 0.0 for k in KEYS}; desc = []
    for src, g, label in parts:
        f = FOODS[src] if isinstance(src, int) else src
        for k in KEYS:
            v = f.get(k) or 0
            if k == "alc": v *= alc_keep
            tot[k] += v * g / 100
        desc.append(f"{g} g {label}" + (f" (NEVO {src})" if isinstance(src, int) else ""))
    mass_in = sum(g for _, g, _ in parts)
    tot["w"] = max(0.0, tot["w"] - (mass_in - yield_g))
    out = {k: round(tot[k] / yield_g * 100, 1) for k in KEYS}
    for k in ("kcal", "kj", "na", "w"): out[k] = round(out[k])
    return out, "; ".join(desc) + f" → {yield_g} g"

# NEVO's own frozen→deep-fried change, used for frozen products whose fried values are unknown
def fry_factor(raw_code, fried_code):
    a, b = FOODS[raw_code], FOODS[fried_code]
    return {k: ((b.get(k) or 0) / a[k]) if a.get(k) else 1 for k in KEYS}
F_FRIK = fry_factor(2362, 322)   # frikandel: unbreaded meat snack
F_KROK = fry_factor(2548, 326)   # vleeskroket: breaded, absorbs fat
def fried(v, fac):
    o = {k: round((v[k] or 0) * fac[k], 1) if v.get(k) is not None else None for k in KEYS}
    for k in ("kcal", "kj", "na", "w"):
        if o.get(k) is not None: o[k] = round(o[k])
    o["kcal"] = round(4 * (o["p"] or 0) + 9 * (o["fat"] or 0) + 4 * (o["cho"] or 0) + 2 * (o["fib"] or 0))
    o["kj"] = round(o["kcal"] * 4.184)
    return o

items = []
def add(code, name, group, icon, v, src, note, syn="", flem="", en="", unit="g", recipe_txt="", portion=None):
    d = {"c": code, "g": group, "n": name, "e": en, "s": syn, "f": flem, "x": "", "u": unit, "i": icon,
         "src": src, "note": note, "recipe": recipe_txt, "portion": portion}
    d.update(v); items.append(d)


def avg(*vs):
    """Average several value dicts; None-values are ignored per field."""
    o = {}
    for k in KEYS:
        xs = [v[k] for v in vs if v.get(k) is not None]
        o[k] = round(sum(xs) / len(xs), 1) if xs else None
    for k in ("kcal", "kj", "na", "w"):
        if o.get(k) is not None: o[k] = round(o[k])
    return o
def nb(kcal, p, cho, fat, sat=None, sug=None, fib=None, salt=None, w=None):
    """Nubel record in the order Nubel shows it (kcal, eiwit, koolhydraten, vet, ...)."""
    return vals(kcal, p, fat, cho, sat=sat, sug=sug, fib=fib, salt=salt, w=w)
NUBEL = "Nubel (internubel.be)"

# ---------- Gerechten ----------
add(900002, "Vol-au-vent bereid (vulling)", "Samengestelde gerechten", "🥧",
    nb(122, 11.7, 4.4, 6.4, sat=2.57, sug=1.1, fib=0.3, salt=1.04, w=76),
    NUBEL + " · generiek product 5208", "Belgische vol-au-vent zoals geserveerd: ragout met kip, balletjes en champignons, zonder bladerdeegkorst en zonder frieten of puree.",
    syn="Videe/Koninginnenhapje/Koninginnevulling", flem="videe koninginnenhapje vol au vent kippenragout", en="Vol-au-vent (Belgian chicken ragout)", portion=250)

add(900006, "Balletjes in tomatensaus", "Samengestelde gerechten", "🍝",
    avg(nb(118, 6.6, 7.6, 6.5, 2.3, 3.4, 1.3, 0.81, 77), nb(116, 7.6, 7.2, 6.0, 2.5, 2.1, 1.2, 1.8, 77),
        nb(100, 4.3, 9.6, 4.7, 1.0, 1.9, 0.9, 0.77, 79), nb(125, 8.9, 8.1, 6.1, 2.0, 3.8, 1.1, 0.99, 74)),
    NUBEL + " · gemiddelde van 4 merken (Chef Select ×2, Iglo, Carrefour)", "Gehaktballetjes in tomatensaus, zonder puree of pasta.",
    syn="Gehaktballetjes in tomatensaus/Boulets sauce tomate", flem="balletjes boulets tomatensaus gehaktballetjes", en="Meatballs in tomato sauce", portion=250)

add(900007, "Gehaktballetjes met krieken", "Samengestelde gerechten", "🍒",
    nb(180, 6.2, 11.7, 11.2, sat=4.29, sug=9.4, fib=0.6, salt=0.56, w=68),
    NUBEL + " · generiek product 24707", "Gebakken gehaktballetjes met krieken, saus inbegrepen.",
    syn="Boulet met krieken/Frikadellen met krieken", flem="boulet krieken frikadel frikadellen balletjes kersen", en="Meatballs with sour cherries", portion=250)

add(900030, "Croque monsieur", "Samengestelde gerechten", "🥪",
    nb(289, 14.5, 23.9, 14.8, sat=7.48, sug=3.0, fib=1.2, salt=1.52, w=44),
    NUBEL + " · generiek product 26169", "Belgische croque met hesp en kaas, in het croque-ijzer of de pan gebakken. NEVO's 'Tosti ham-kaas' ligt 14% lager.",
    syn="Croque/Croque-monsieur", flem="croque croque monsieur tosti hesp kaas", en="Croque monsieur", portion=150)

v, r = recipe([(2793, 120, "wit stokbrood"), (2107, 150, "frites gefrituurd"), (322, 90, "frikandel gefrituurd"), (451, 25, "mayonaise")], 385)
add(900008, "Mitraillette met frikandel en mayonaise", "Samengestelde gerechten", "🥖", v, "Berekend uit recept met NEVO-ingrediënten",
    "Half stokbrood met frieten, frikandel en mayonaise. Niet in Nubel.", syn="Mitraillette", flem="mitraillette frituur broodje frieten", en="Mitraillette (baguette with fries and sausage)", recipe_txt=r, portion=385)

# ---------- Frituur ----------
bicky_raw = vals(231, 13.7, 16.3, 7.0, sat=5.3, sug=0.6, salt=2.4, w=60)
bicky_fried = fried(bicky_raw, F_FRIK)
v, r = recipe([(2351, 50, "zacht wit broodje"), (bicky_fried, 90, "Bicky burger gefrituurd (uit 100 g diepvries)"),
               (2651, 15, "Bicky dressing ≈ cocktailsaus >25% olie"), (583, 10, "hot ketchup"), (584, 10, "curryketchup"),
               (1484, 10, "gebakken uitjes"), (131, 10, "augurk")], 195)
add(900010, "Bicky Burger compleet (broodje, burger, 3 sauzen, uitjes, augurk)", "Hartige snacks en zoutjes", "🍔", v,
    "Berekend: productfiche Bicky Original + NEVO-ingrediënten", "Frituur-Bicky zoals geserveerd. Niet in Nubel.",
    syn="Bicky", flem="bicky bickyburger frituur", en="Bicky Burger (complete)", recipe_txt=r, portion=195)
add(900011, "Bicky burger gefrituurd (alleen de burger)", "Hartige snacks en zoutjes", "🍔", bicky_fried,
    "Berekend: productfiche Bicky Original diepvries + NEVO-frituurfactor (frikandel)", "Alleen het gefrituurde vleesschijfje (kip en spek). Eén burger ≈ 90 g gefrituurd.",
    syn="Bicky burger los", flem="bicky burger", en="Bicky patty, deep-fried", portion=90)

add(900012, "Mexicano gefrituurd", "Hartige snacks en zoutjes", "🌶️", fried(vals(227, 13.0, 16.0, 7.9, sat=5.3, sug=0.3, fib=0.6, salt=2.27, w=58), F_FRIK),
    "Berekend: productfiche Mexicano Classic diepvries + NEVO-frituurfactor (frikandel)", "Pittige gekruide vleessnack. Eén stuk ≈ 85 g gefrituurd. Niet in Nubel.",
    syn="Mexicano", flem="mexicano frituur", en="Mexicano (spicy meat snack), deep-fried", portion=85)
add(900013, "Lucifer gefrituurd", "Hartige snacks en zoutjes", "🥓", fried(vals(290, 11.0, 17.0, 21.0, sat=5.5, sug=1.5, salt=2.7, w=46), F_FRIK),
    "Berekend: productfiche Mora Lucifer diepvries + NEVO-frituurfactor (frikandel)", "Gekruide vleesstick omwikkeld met spek. Eén stuk ≈ 90 g gefrituurd. Niet in Nubel.",
    syn="Lucifer (Mora)", flem="lucifer frituur", en="Lucifer, deep-fried", portion=90)

kaas_base = nb(205, 6.7, 18.0, 11.2, sat=6.9, sug=1.7, fib=1.2, salt=1.36, w=62)
add(900014, "Kaaskroket gefrituurd", "Hartige snacks en zoutjes", "🧀", fried(kaas_base, F_KROK),
    "Berekend: Nubel generiek 15119 (voorgebakken diepvries) + NEVO-frituurfactor (vleeskroket)", "Kroket met kaasvulling. Eén kroket ≈ 45 g gefrituurd. Nubel-merken (198–229 kcal diepvries) bevestigen de basiswaarde.",
    syn="Kaaskroketten/Croquette au fromage", flem="kaaskroket kaaskroketten kroket", en="Cheese croquette, deep-fried", portion=45)

garn_base = avg(nb(156, 9.4, 14.4, 6.4, 3.67, 5.8, 1.5, 1.28, 67), nb(151, 10, 14, 6, 3.8, 1.0, 1.0, 1.1, 68),
                nb(134, 11, 15, 3.3, 1.6, 2.7, 1.0, 1.5, 68), nb(188, 10, 16, 9.1, 6.24, 1.7, 0.8, 0.96, 63))
add(900003, "Garnaalkroket gefrituurd", "Hartige snacks en zoutjes", "🦐", fried(garn_base, F_KROK),
    "Berekend: Nubel gemiddelde van 4 merken (Lidl, Delhaize ×2, Carrefour) + NEVO-frituurfactor (vleeskroket)", "Kroket met grijze garnalen. Eén kroket ≈ 50 g gefrituurd.",
    syn="Garnalenkroket/Croquette aux crevettes", flem="garnaalkroketten garnalenkroket kroket garnalen", en="Shrimp croquette, deep-fried", portion=50)

cerv_base = avg(vals(200, 13, 14, 3.9, salt=2.0, w=65), vals(211, 13, 16, 3.8, salt=2.0, w=64), vals(247, 12, 18, 7, salt=2.0, w=60),
                vals(256, 13, 21, 5, salt=2.0, w=58), nb(300, 10, 4, 27, 8, 0.3, 0, 1.5, 58), nb(233, 14.4, 2.2, 18.5, 6.9, 1.7, None, 1.75, 62))
add(900015, "Cervela gefrituurd", "Hartige snacks en zoutjes", "🌭", fried(cerv_base, F_FRIK),
    "Berekend: gemiddelde van 6 Belgische merken (o.a. Nubel: Carrefour, Saint Alby) + NEVO-frituurfactor (frikandel)",
    "Belgische frituurcervela (verse varkensworst), niet de Nederlandse cervelaatworst (droge worst, NEVO 638). Eén stuk ≈ 140 g gefrituurd.",
    syn="Cervela frituur/Cervelas", flem="cervela cervelas frituur worst", en="Cervela sausage, deep-fried", portion=140)

add(900016, "Viandel gefrituurd", "Hartige snacks en zoutjes", "🌭", fried(FOODS[2555], F_FRIK),
    "Berekend: NEVO 2555 (Viandel onbereid) + NEVO-frituurfactor (frikandel)", "Eén stuk ≈ 85 g gefrituurd.",
    syn="Viandel", flem="viandel frituur", en="Viandel, deep-fried", portion=85)

# ---------- Charcuterie ----------
add(900040, "Witte pens gekookt", "Vleeswaren", "🌭", nb(239, 10, 8.8, 18, sat=6.55, sug=1.1, fib=0.5, salt=1.5, w=62),
    NUBEL + " · generiek product 4442 (beuling, wit, gekookt)", "Belgische witte pens. Eén stuk ≈ 150 g. NEVO's 'Worst bloed-' is een ander, veel vetter product.",
    syn="Witte beuling/Boudin blanc", flem="witte pens beuling boudin blanc", en="White pudding (boudin blanc)", portion=150)
add(900041, "Zwarte pens gekookt", "Vleeswaren", "🌭", nb(186, 11.8, 9.2, 10.9, sat=3.7, sug=0.9, fib=0.3, salt=1.68, w=65),
    NUBEL + " · generiek product 11785 (beuling, zwart, gekookt)", "Belgische zwarte pens (bloedworst). Eén stuk ≈ 150 g. NEVO's 'Worst bloed-' (386 kcal) is de Nederlandse versie.",
    syn="Zwarte beuling/Boudin noir", flem="zwarte pens beuling bloedpens boudin noir", en="Black pudding (boudin noir)", portion=150)
add(900042, "Kipkap (hoofdkaas, varken)", "Vleeswaren", "🥓", nb(190, 14.5, 1.0, 14, sat=5.3, sug=0.5, fib=0.5, salt=1.55, w=68),
    NUBEL + " · generiek product 4620 (hoofdkaas, varken)", "Kipkap, preskop of hoofdkaas. Merken in Nubel (189–218 kcal) bevestigen de waarde. Eén snede ≈ 50 g.",
    syn="Preskop/Hoofdkaas/Tête pressée", flem="kipkap preskop hoofdkaas kop tete pressee", en="Head cheese (brawn)", portion=50)

# ---------- Brood & zuivel ----------
add(900043, "Sandwich (zacht, gesuikerd)", "Brood", "🥖", nb(305, 8.4, 51, 6.7, sat=2.48, sug=7.2, fib=2.2, salt=1.18, w=29),
    NUBEL + " · generiek product 12086", "Belgische zachte, licht gezoete sandwich (botersandwich). Eén stuk ≈ 40 g. Een gewoon zacht broodje is NEVO 'Tarwebroodje wit zacht'.",
    syn="Botersandwich/Sandwich", flem="sandwich sandwiches botersandwich", en="Belgian soft sweet bun", portion=40)
add(900044, "Rijstpap", "Melk en melkproducten", "🍚",
    avg(nb(138, 3.4, 18.8, 5.4, 3.5, 10.6, 0.2, 0.23, 71), nb(108, 3.2, 18, 2.6, 1.8, 9.0, 0.1, 0.18, 75)),
    NUBEL + " · gemiddelde van 2 merken (La Laitière, Carrefour)", "Gezoete Belgische rijstpap. NEVO's 'Pap rijste-' (86 kcal) is ongezoet.",
    syn="Rijstpap/Riz au lait", flem="rijstpap riz au lait", en="Rice pudding", portion=125)

# ---------- Bakkerij ----------
add(900036, "Koffiekoek met vanillecrème (achtje)", "Gebak en koek", "🥐", nb(378, 6.1, 47.6, 17.5, sat=8.51, sug=33.7, fib=2.9, salt=0.51, w=24),
    NUBEL + " · generiek product 13051 (koffiekoek met vanillecrème)", "Achtje: koffiekoek met banketbakkersroom (pudding), zonder chocolade en zonder rozijnen. Met rozijnen = suisse (NEVO 'Broodje koffie-'). Eén stuk ≈ 80 g.",
    syn="Achtje/Achtkoek/Puddingkoek/Koffiekoek met pudding", flem="achtje achtkoek koffiekoek pudding puddingkoek vanillecreme vanille", en="Danish with custard", portion=80)
add(900021, "Koffiekoek met chocolade en crème", "Gebak en koek", "🍫", nb(381, 7.2, 40.4, 21.2, w=30),
    NUBEL + " · product 18606 (Bake Off, Lidl)", "Koffiekoek met chocolade en vanillecrème. Eén merk in Nubel; geen generieke waarde beschikbaar. Eén stuk ≈ 84 g.",
    syn="Koffiekoek met chocolade en vanille/Koffiekoek met chocolade en pudding", flem="koffiekoek chocolade creme pudding vanille", en="Danish with chocolate and custard", portion=84)
add(900037, "Koffiekoek met boter en rozijnen, zonder pudding (rozijnenkoek)", "Gebak en koek", "🥐", nb(426, 9.2, 39.4, 23.8, sat=16.68, sug=10.8, fib=8.7, salt=0.66, w=17),
    NUBEL + " · generiek product 13050", "Boterdeeg (croissantdeeg) met rozijnen, zonder pudding. Brands in Nubel (405–440) bevestigen. Let op: met pudding = suisse (NEVO 'Broodje koffie-', ±320–350). Eén stuk ≈ 85 g.",
    syn="Rozijnenkoek/Boterkoek met rozijnen", flem="rozijnenkoek koffiekoek rozijnen boterkoek", en="Raisin butter pastry", portion=85)
add(900038, "Koffiekoek met pudding en fruit (abrikozenkoek, strik)", "Gebak en koek", "🥐", nb(325, 5.9, 34.7, 16.9, sat=7.39, sug=20.4, fib=5.4, salt=0.65, w=36),
    NUBEL + " · generiek product 13052 (koffiekoek met vanillecrème en abrikozen)", "Koffiekoek met banketbakkersroom en abrikoos of framboos. Merken 280–341 kcal. Bladerdeegflappen en gozetten zijn een ander product (NEVO 'Appelflap gem'). Eén stuk ≈ 90 g.",
    syn="Abrikozenkoek/Frambozenstrik/Abrikozenstrik", flem="abrikozenkoek koffiekoek abrikoos strik frambozenstrik abrikozenstrik", en="Apricot Danish", portion=90)
add(900039, "Koffiekoek boterkoek (Belgisch)", "Gebak en koek", "🥐", nb(410, 7.9, 38.8, 24, sat=17.1, sug=6.6, fib=3.9, salt=0.79, w=24),
    NUBEL + " · generiek product 13048 (koffiekoek met boter)", "Belgische boterkoek uit croissantdeeg. Niet de Nederlandse boterkoek (NEVO 'Koek boter-', een dichte cake). Eén stuk ≈ 60 g.",
    syn="Koffiekoek met boter", flem="boterkoek koffiekoek", en="Belgian butter pastry", portion=60)
add(900022, "Mattentaart", "Gebak en koek", "🥧", nb(364, 9.2, 35, 19.9, sat=12.58, sug=16.4, fib=3.9, salt=0.46, w=31),
    NUBEL + " · generiek product 12106", "Bladerdeegtaartje met matten (verse kaas). Eén stuk ≈ 120 g.",
    syn="Geraardsbergse mattentaart", flem="mattentaart matten geraardsbergen", en="Mattentaart (curd tart)", portion=120)
add(900031, "Eclair met chocolade", "Gebak en koek", "🍫",
    avg(nb(232, 3.8, 31, 10, None, 22, 0.7, 0.19, 53), nb(236, 4.6, 32, 9.7, 5.1, 24, 0.6, 0.23, 52), nb(235, 4.0, 30.1, 10.9, None, None, None, 0.5, 54)),
    NUBEL + " · gemiddelde van 3 merken (Delhaize, Delhaize Bio, Lidl)", "Soes met banketbakkersroom en chocoladeglazuur. Eén stuk ≈ 90 g. Mini-eclairs (meer room, ±320 kcal) en suikerarme diepvriesversies zijn niet meegeteld.",
    syn="Eclair", flem="eclair eclairs", en="Chocolate eclair", portion=90)
add(900033, "Frangipane", "Gebak en koek", "🥧", nb(432, 4.7, 56.8, 20.1, sat=6.43, sug=29.8, fib=1.5, salt=0.59, w=16),
    NUBEL + " · generiek product 2770 (cake, frangipane)", "Individueel frangipanegebakje. Merken (Lotus, Delhaize, Lidl: 418–444 kcal) bevestigen. Eén stuk ≈ 60 g (bakker ±80 g).",
    syn="Frangipane", flem="frangipane frangipanes", en="Frangipane cake", portion=60)
add(900034, "Frangipanetaart", "Gebak en koek", "🥧", nb(495, 2.5, 45.4, 32.6, sat=12.17, sug=31.2, fib=4.6, salt=0.7, w=12),
    NUBEL + " · generiek product 4267 (taart, frangipane)", "Grote frangipanetaart, per spie (≈ 100 g).",
    syn="Frangipanetaart", flem="frangipanetaart frangipane taart", en="Frangipane tart", portion=100)
add(900035, "Carré confituur", "Gebak en koek", "🟧",
    avg(nb(364, 3.4, 51.9, 15.3, 7.8, 30.3, 2.7, 0.68, 25), nb(338, 4.9, 40, 17, 10, 31, 1.7, 0.42, 35),
        nb(415, 4.0, 55, 18, 10, 23, 1.3, 1.08, 14), nb(413, 4.0, 61.4, 16.1, 8.2, 32, 3.0, 0.58, 14)),
    NUBEL + " · gemiddelde van 4 merken (Lidl, Delhaize, Lotus, Belgix)", "Zandgebak met confituur. Bakkerijversie (≈ 75 g) zit rond 350 kcal/100 g, verpakte koekjes (≈ 35 g) rond 415.",
    syn="Carré confituur/Confituurcarré", flem="carre confituur confituurcarre", en="Jam square", portion=60)

add(900045, "Koffiekoek chocotwist / chocoladevlecht", "Gebak en koek", "🍫",
    avg(nb(349, 7.6, 47.9, 13.3, 6.09, 14.5, None, None, 26), nb(298, 5.5, 39, 13, 8.4, 14, None, None, 39),
        nb(389, 6, 43, 21, 10, 17, None, None, 26), nb(307, 7.1, 52.7, 7, 3.5, 12.6, None, None, 29)),
    NUBEL + " · gemiddelde van 4 merken (Carrefour vlecht, Delhaize chocotwist, Delhaize hazelnoot-chococroissant, Carrefour gevulde chococroissant)",
    "Gedraaide of gevlochten koffiekoek met chocolade- of hazelnootvulling. Lichter dan een chocoladebroodje (pain au chocolat, ±430). Eén stuk ≈ 90 g.",
    syn="Chocotwist/Chocoladevlecht", flem="chocotwist twist chocoladevlecht vlecht koffiekoek chocolade hazelnoot", en="Chocolate twist pastry", portion=90)

EXTRA_SYN = {}
# Labels shown above the name for NEVO products, so koffiekoeken are recognisable as such without changing NEVO's names.
EXTRA_LABEL = {
    2400: "Koffiekoek · chocoladebroodje / pain au chocolat",
    232: "Koffiekoek · suisse met pudding en rozijnen (rozijnenkoek)",
    2818: "Koffiekoek · croissant", 2801: "Koffiekoek · croissant", 2802: "Koffiekoek · croissant",
    250: "Koffiekoek · amandelcroissant",
    5240: "Koffiekoek · flap / gozet (bladerdeeg met fruit)", 2560: "Koffiekoek · flap / gozet (bladerdeeg met fruit)", 3060: "Koffiekoek · flap / gozet (bladerdeeg met fruit)",
}
out = "const EXTRA=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";\nconst EXTRA_SYN=" + json.dumps(EXTRA_SYN) + ";\nconst EXTRA_LABEL=" + json.dumps(EXTRA_LABEL, ensure_ascii=False) + ";\n"
open("/home/claude/nevo-app/extra.js", "w", encoding="utf-8").write(out)
for i in items:
    print(i["c"], i["n"], "|", i["kcal"], "kcal  E", i["p"], " K", i["cho"], " V", i["fat"], "| portie", i["portion"], "g →", round(i["kcal"] * i["portion"] / 100), "kcal")
