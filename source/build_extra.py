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

# ---------- Gerechten ----------
v, r = recipe([(1547, 590, "runderriblappen bereid (uit 1 kg rauw)"), (64, 280, "ui gekookt"), (389, 500, "bier oud bruin"),
               (236, 80, "bruin brood"), (824, 20, "mosterd"), (310, 40, "boter"), (374, 10, "bruine suiker")], 1300, alc_keep=0.25)
add(900001, "Stoofvlees op Vlaamse wijze bereid", "Samengestelde gerechten", "🍲", v, "Berekend uit recept met NEVO-ingrediënten",
    "Rundstoofvlees met ui, bruin bier, brood en mosterd; saus inbegrepen. Schatting op basis van een standaardrecept.",
    syn="Stoverij/Vlaamse stoofkarbonaden/Carbonnade flamande", flem="stoverij stoofvlees karbonaden carbonnade stoofpotje", en="Flemish beef stew (carbonnade)", recipe_txt=r, portion=250)

add(900002, "Vol-au-vent met kip (bouchée à la reine)", "Samengestelde gerechten", "🥧",
    vals(258, 7.1, 16.8, 19.0, sat=3.6, sug=2.0, fib=1.0, salt=1.43, w=55),
    "Ciqual 2013 (ANSES, Frankrijk)", "Bladerdeegkorst met kippenragout. Franse referentiewaarde; Belgische versies met balletjes en champignons liggen in dezelfde buurt.",
    syn="Videe/Koninginnenhapje", flem="videe koninginnenhapje vol au vent kippenragout", en="Vol-au-vent, chicken", portion=200)

v, r = recipe([(68, 500, "witlof gekookt"), (784, 150, "achterham (hesp)"), (2419, 400, "kaassaus op basis van roux"), (2756, 30, "Goudse kaas jong")], 1000)
add(900005, "Witloof met hesp in kaassaus gegratineerd", "Samengestelde gerechten", "🧀", v, "Berekend uit recept met NEVO-ingrediënten",
    "Gegratineerde witloofrolletjes met hesp en kaassaus, zonder puree.", syn="Witlof met ham in kaassaus/Chicon au gratin", flem="witloof hesp kaassaus chicon gratin witloofrolletjes", en="Chicory and ham gratin", recipe_txt=r, portion=300)

v, r = recipe([(1568, 100, "gehaktbal half-om-half gebakken"), (1524, 80, "tomatensaus")], 180)
add(900006, "Balletjes in tomatensaus", "Samengestelde gerechten", "🍝", v, "Berekend uit recept met NEVO-ingrediënten",
    "Gehaktballetjes met tomatensaus, 100 g vlees op 80 g saus.", syn="Gehaktballetjes in tomatensaus/Boulets sauce tomate", flem="balletjes boulets tomatensaus gehaktballetjes", en="Meatballs in tomato sauce", recipe_txt=r, portion=180)

v, r = recipe([(1568, 100, "gehaktbal half-om-half gebakken"), (167, 80, "zure kersen (krieken)")], 180)
add(900007, "Frikadellen met krieken", "Samengestelde gerechten", "🍒", v, "Berekend uit recept met NEVO-ingrediënten",
    "Gehaktbal met warme krieken, 100 g vlees op 80 g krieken (zonder extra suiker of binding).", syn="Boulet met krieken/Balletjes met krieken", flem="boulet krieken frikadel balletjes kersen", en="Meatballs with sour cherries", recipe_txt=r, portion=180)

v, r = recipe([(2793, 120, "wit stokbrood"), (2107, 150, "frites gefrituurd"), (322, 90, "frikandel gefrituurd"), (451, 25, "mayonaise")], 385)
add(900008, "Mitraillette met frikandel en mayonaise", "Samengestelde gerechten", "🥖", v, "Berekend uit recept met NEVO-ingrediënten",
    "Half stokbrood met frieten, frikandel en mayonaise.", syn="Mitraillette", flem="mitraillette frituur broodje frieten", en="Mitraillette (baguette with fries and sausage)", recipe_txt=r, portion=385)

# ---------- Frituur ----------
# Bicky Original Burger patty, frozen, per 100 g (productfiche): 231 kcal, 13.7 E, 16.3 V (5.3 verz), 7 K, 0.6 suiker, 2.4 g zout
bicky_raw = vals(231, 13.7, 16.3, 7.0, sat=5.3, sug=0.6, salt=2.4, w=60)
bicky_fried = fried(bicky_raw, F_FRIK)
v, r = recipe([(2351, 50, "zacht wit broodje"), (bicky_fried, 90, "Bicky burger gefrituurd (uit 100 g diepvries)"),
               (2651, 15, "Bicky dressing ≈ cocktailsaus >25% olie"), (583, 10, "hot ketchup"), (584, 10, "curryketchup"),
               (1484, 10, "gebakken uitjes"), (131, 10, "augurk")], 195)
add(900010, "Bicky Burger compleet (broodje, burger, 3 sauzen, uitjes, augurk)", "Hartige snacks en zoutjes", "🍔", v,
    "Berekend: productfiche Bicky Original + NEVO-ingrediënten", "Frituur-Bicky zoals geserveerd. Burger gefrituurd (vetopname geschat zoals NEVO voor frikandel), broodje, Bicky-dressing, hot en curryketchup, gebakken uitjes en augurk.",
    syn="Bicky", flem="bicky bickyburger frituur hamburger", en="Bicky Burger (complete)", recipe_txt=r, portion=195)
add(900011, "Bicky burger gefrituurd (alleen de burger)", "Hartige snacks en zoutjes", "🍔", bicky_fried,
    "Berekend: productfiche Bicky Original diepvries + NEVO-frituurfactor (frikandel)", "Alleen het gefrituurde vleesschijfje (kip en spek), zonder broodje of saus. Eén burger ≈ 90 g gefrituurd.",
    syn="Bicky burger los", flem="bicky burger vlees", en="Bicky patty, deep-fried", portion=90)

mex = vals(227, 13.0, 16.0, 7.9, sat=5.3, sug=0.3, fib=0.6, salt=2.27, w=58)
add(900012, "Mexicano gefrituurd", "Hartige snacks en zoutjes", "🌶️", fried(mex, F_FRIK),
    "Berekend: productfiche Mexicano Classic diepvries + NEVO-frituurfactor (frikandel)", "Pittige gekruide vleessnack (varken, rund, kip). Eén stuk ≈ 85 g gefrituurd.",
    syn="Mexicano", flem="mexicano frituur pikante snack", en="Mexicano (spicy meat snack), deep-fried", portion=85)

luc = vals(290, 11.0, 17.0, 21.0, sat=5.5, sug=1.5, salt=2.7, w=46)
add(900013, "Lucifer gefrituurd", "Hartige snacks en zoutjes", "🥓", fried(luc, F_FRIK),
    "Berekend: productfiche Mora Lucifer diepvries + NEVO-frituurfactor (frikandel)", "Gekruide vleesstick omwikkeld met spek. Eén stuk ≈ 90 g gefrituurd.",
    syn="Lucifer (Mora)", flem="lucifer frituur stick spek", en="Lucifer (bacon-wrapped meat stick), deep-fried", portion=90)

kaask = vals(166, 6.1, 3.8, 25.0, sat=2.1, sug=3.2, salt=1.2, w=63)
add(900014, "Kaaskroket gefrituurd", "Hartige snacks en zoutjes", "🧀", fried(kaask, F_KROK),
    "Berekend: productfiche Van Geloven kaaskroket diepvries + NEVO-frituurfactor (vleeskroket)", "Kroket met kaasvulling. Eén kroket ≈ 45 g gefrituurd.",
    syn="Kaaskroketten/Croquette au fromage", flem="kaaskroket kaaskroketten kroket kaas", en="Cheese croquette, deep-fried", portion=45)

garn = vals(184, 7.5, 8.8, 18.0, sat=4.2, sug=1.7, fib=1.5, salt=1.0, w=62)
add(900003, "Garnaalkroket gefrituurd", "Hartige snacks en zoutjes", "🦐", fried(garn, F_KROK),
    "Berekend: productfiche grijze garnaalkroket diepvries + NEVO-frituurfactor (vleeskroket)", "Kroket met grijze Noordzeegarnalen. Eén kroket ≈ 45 g gefrituurd.",
    syn="Garnalenkroket/Croquette aux crevettes", flem="garnaalkroketten garnalenkroket kroket garnalen crevettes", en="Shrimp croquette, deep-fried", portion=45)

# Belgian cervela (fresh pork sausage, not the Dutch dry cervelaat): average of Colruyt 200, Everyday 211, Vanreusel 247, Délifin 256 kcal
cerv = vals(229, 12.8, 17.3, 4.9, sat=6.5, salt=2.0, w=62)
add(900015, "Cervela gefrituurd", "Hartige snacks en zoutjes", "🌭", fried(cerv, F_FRIK),
    "Berekend: gemiddelde van 4 Belgische merken + NEVO-frituurfactor (frikandel)", "Belgische frituurcervela (verse varkensworst), niet te verwarren met Nederlandse cervelaatworst (droge worst, NEVO 638). Eén stuk ≈ 95 g gefrituurd.",
    syn="Cervela frituur/Cervelas", flem="cervela cervelas frituur worst", en="Cervela sausage, deep-fried", portion=95)

add(900016, "Viandel gefrituurd", "Hartige snacks en zoutjes", "🌭", fried(FOODS[2555], F_FRIK),
    "Berekend: NEVO 2555 (Viandel onbereid) + NEVO-frituurfactor (frikandel)", "Gefrituurde versie van NEVO's Viandel onbereid. Eén stuk ≈ 85 g gefrituurd.",
    syn="Viandel", flem="viandel frituur", en="Viandel, deep-fried", portion=85)

# ---------- Bakkerij / koffiekoeken ----------
add(900020, "Lange suisse (koffiekoek met pudding en glazuur)", "Gebak en koek", "🥐",
    vals(321, 5.9, 14.0, 42.0, sat=6.3, sug=17.0, fib=1.9, salt=0.75, w=35),
    "Productfiche AH lange suisse (België)", "Langwerpige koffiekoek van korstdeeg met banketbakkersroom en suikerglazuur. Eén stuk ≈ 120 g.",
    syn="Suisse/Koffiekoek met pudding", flem="suisse lange suisse koffiekoek pudding", en="Long Danish pastry with custard", portion=120)
# Koffiekoek met chocolade en pudding = lange suisse-deeg + chocolade: gemiddelde van lange suisse en pain au chocolat (NEVO 2400)
pc = FOODS[2400]; ls = items[-1]
avg = {k: (round(((ls[k] or 0) + (pc[k] or 0)) / 2, 1) if (ls.get(k) is not None and pc.get(k) is not None) else None) for k in KEYS}
for k in ("kcal", "kj", "na", "w"): avg[k] = round(avg[k]) if avg[k] is not None else None
add(900021, "Koffiekoek met chocolade en pudding (achtje)", "Gebak en koek", "🍫", avg,
    "Berekend: gemiddelde van lange suisse en chocoladekoek (NEVO 2400)", "Koffiekoek met chocoladestukjes en banketbakkersroom. Eén stuk ≈ 110 g.",
    syn="Achtje/Chocoladekoek met pudding", flem="achtje koffiekoek chocolade pudding", en="Danish pastry with chocolate and custard", portion=110)
add(900022, "Mattentaart", "Gebak en koek", "🥧",
    vals(374, 10.5, 20.1, 37.7, sat=10.6, sug=21.5, fib=0.75, salt=0.4, w=29),
    "Productfiche Holeki mattentaart (Geraardsbergen)", "Bladerdeegtaartje gevuld met matten (verse kaas), ei en suiker. Eén stuk ≈ 115 g.",
    syn="Geraardsbergse mattentaart", flem="mattentaart matten taartje geraardsbergen", en="Mattentaart (curd tart)", portion=115)

# ---------- Synonyms on existing NEVO items (no duplicates) ----------
EXTRA_SYN = {
    5354: "croque monsieur croque croque-monsieur", 5534: "croque monsieur croque croque-monsieur",
    1485: "wortelstoemp stoemp", 1483: "boerenkoolstoemp stoemp", 1531: "andijviestoemp stoemp", 1486: "zuurkoolstoemp stoemp",
    489: "rijsttaart rijsttaartje rijstevlaai", 2661: "luikse wafel gaufre de liege", 2662: "brusselse wafel suikerwafel",
    810: "americain prepare préparé martino", 474: "smoutebol smoutebollen", 5329: "stoofvlees stoverij hachee",
    2793: "baguette stokbrood", 322: "frikadel curryworst", 326: "vleeskroket kroket",
    232: "ronde suisse rozijnenkoek koffiekoek rozijnen", 2400: "chocoladekoek chocoladebroodje koffiekoek", 5240: "appelkoek koffiekoek appel",
    2818: "koffiekoek", 1568: "boulet frituurboulet boulet frituur", 5182: "berenpoot berenpoten", 5183: "kipcorn",
    1470: "boule de berlin berlijnse bol", 2355: "craquelin", 244: "cramique kramiek", 5355: "hamburger broodje",
}

out = "const EXTRA=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";\nconst EXTRA_SYN=" + json.dumps(EXTRA_SYN) + ";\n"
open("/home/claude/nevo-app/extra.js", "w", encoding="utf-8").write(out)
for i in items:
    print(i["c"], i["n"], "|", i["kcal"], "kcal  E", i["p"], " K", i["cho"], " V", i["fat"], "| portie", i["portion"], "g →", round(i["kcal"] * i["portion"] / 100), "kcal")
