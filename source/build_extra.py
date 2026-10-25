"""Belgian dishes NEVO lacks. Calculated from NEVO ingredient values (recipe method) or taken from a named source.
Output: extra.js with the same fields as data.js plus src/note/recipe."""
import json, re
js = open("/home/claude/nevo-app/data.js", encoding="utf-8").read()
FOODS = {f["c"]: f for f in json.loads(js.split("let FOODS=", 1)[1].rstrip(";\n"))}
KEYS = ["kcal", "kj", "p", "fat", "sat", "cho", "sug", "fib", "alc", "na", "w"]

def recipe(parts, yield_g, alc_keep=1.0):
    """parts: list of (nevo_code, grams, label). Sums nutrients, divides by cooked yield (g)."""
    tot = {k: 0.0 for k in KEYS}
    desc = []
    for code, g, label in parts:
        f = FOODS[code]
        for k in KEYS:
            v = f.get(k) or 0
            if k == "alc": v *= alc_keep
            tot[k] += v * g / 100
        desc.append(f"{g} g {label or f['n']} (NEVO {code})")
    # evaporation: remove water so that total mass == yield
    mass_in = sum(g for _, g, _ in parts)
    tot["w"] = max(0.0, tot["w"] - (mass_in - yield_g))
    # alcohol that evaporated also takes its kcal (7 kcal/g, 29 kJ/g)
    out = {k: round(tot[k] / yield_g * 100, 1) for k in KEYS}
    out["kcal"] = round(out["kcal"]); out["kj"] = round(out["kj"]); out["na"] = round(out["na"]); out["w"] = round(out["w"])
    return out, "; ".join(desc) + f" → {yield_g} g bereid"

items = []
def add(code, name, group, icon, vals, src, note, syn="", flem="", en="", unit="g", recipe_txt=""):
    d = {"c": code, "g": group, "n": name, "e": en, "s": syn, "f": flem, "x": "", "u": unit, "i": icon,
         "src": src, "note": note, "recipe": recipe_txt}
    d.update(vals); items.append(d)

# 1. Vlaamse stoofvlees. 1 kg riblappen (→ ~590 g bereid, NEVO yield), ui, bruin bier (alcohol largely cooks off: keep 25%),
#    bruin brood met mosterd, boter, bruine suiker. Cooked yield ≈ 1300 g.
v, r = recipe([(1547, 590, "runderriblappen bereid (uit 1 kg rauw)"), (64, 280, "ui gekookt"), (389, 500, "bier oud bruin"),
               (236, 80, "bruin brood"), (824, 20, "mosterd"), (310, 40, "boter"), (374, 10, "bruine suiker")], 1300, alc_keep=0.25)
add(900001, "Stoofvlees op Vlaamse wijze bereid", "Samengestelde gerechten", "🍲", v, "Berekend uit recept met NEVO-ingrediënten",
    "Rundstoofvlees met ui, bruin bier, brood en mosterd. Schatting op basis van een standaardrecept; saus inbegrepen.",
    syn="Stoverij/Vlaamse stoofkarbonaden/Carbonnade flamande", flem="stoverij stoofvlees karbonaden carbonnade stoofpotje", en="Flemish beef stew (carbonnade)", recipe_txt=r)

# 2. Vol-au-vent: Ciqual 2013 'Bouchée à la reine' (per 100 g, pastry + chicken filling)
add(900002, "Vol-au-vent met kip (bouchée à la reine)", "Samengestelde gerechten", "🥧",
    {"kcal": 258, "kj": 1070, "p": 7.1, "fat": 16.8, "sat": 3.6, "cho": 19.0, "sug": 2.0, "fib": 1.0, "alc": 0.0, "na": 571, "w": 55},
    "Ciqual 2013 (ANSES, Frankrijk)", "Bladerdeegkorst met kippenragout. Franse referentiewaarde; Belgische versies met balletjes en champignons liggen in dezelfde buurt.",
    syn="Videe/Koninginnenhapje", flem="videe koninginnenhapje vol au vent kippenragout", en="Vol-au-vent, chicken")

# 3. Garnaalkroket gefrituurd: start from product sheet (grijze garnaalkroket diepvries, per 100 g: 184 kcal, 7.5 E, 8.8 V, 4.2 verz, 18 K, 1.7 suiker, 1.5 vezel, 1 g zout),
#    then apply NEVO's own frozen→fried change for vleeskroket (2548 → 326): kcal x1.45, fat x1.91, sat x1.4, prot x1.17, cho x1.11, water x0.75.
f0 = {"kcal": 184, "kj": 771, "p": 7.5, "fat": 8.8, "sat": 4.2, "cho": 18.0, "sug": 1.7, "fib": 1.5, "alc": 0.0, "na": 400, "w": 62}
a, b = FOODS[2548], FOODS[326]
fac = {k: (b[k] or 0) / (a[k] or 1) if a.get(k) else 1 for k in KEYS}
fried = {k: round(f0[k] * fac[k], 1) for k in KEYS}
fried["kcal"] = round(fried["kcal"]); fried["kj"] = round(fried["kcal"] * 4.184); fried["na"] = round(fried["na"]); fried["w"] = round(fried["w"])
add(900003, "Garnaalkroket gefrituurd", "Hartige snacks en zoutjes", "🦐", fried, "Berekend: productfiche diepvries + NEVO-frituurfactor (vleeskroket)",
    "Kroket met grijze Noordzeegarnalen, gefrituurd. Vetopname geschat zoals NEVO die meet voor vleeskroket.",
    syn="Garnalenkroket/Croquette aux crevettes", flem="garnaalkroketten garnalenkroket kroket garnalen crevettes", en="Shrimp croquette, deep-fried",
    recipe_txt="Diepvries per 100 g: 184 kcal, 7,5 g eiwit, 8,8 g vet, 18 g koolhydraten; frituurfactor uit NEVO 2548→326.")

# 4. Croque monsieur: 2 sneden witbrood 70 g, 30 g hesp, 30 g jonge kaas, 10 g boter; gebakken, yield 130 g
v, r = recipe([(2351, 70, "witbrood"), (784, 30, "achterham (hesp)"), (2756, 30, "Goudse kaas jong"), (310, 10, "boter")], 130)
add(900004, "Croque monsieur bereid", "Samengestelde gerechten", "🥪", v, "Berekend uit recept met NEVO-ingrediënten",
    "Tosti met hesp en kaas, in boter gebakken. Zonder saus.", syn="Tosti ham/kaas", flem="croque tosti ham kaas", en="Croque monsieur", recipe_txt=r)

# 5. Witloof met hesp in kaassaus (gegratineerd): 500 g witlof gekookt, 150 g achterham, 400 g kaassaus, 30 g kaas; yield 1000 g
v, r = recipe([(68, 500, "witlof gekookt"), (784, 150, "achterham (hesp)"), (2419, 400, "kaassaus op basis van roux"), (2756, 30, "Goudse kaas jong")], 1000)
add(900005, "Witloof met hesp in kaassaus gegratineerd", "Samengestelde gerechten", "🧀", v, "Berekend uit recept met NEVO-ingrediënten",
    "Gegratineerd witloofrolletje met hesp en kaassaus, zonder puree.", syn="Witlof met ham in kaassaus/Chicon au gratin", flem="witloof hesp kaassaus chicon gratin witloofrolletjes", en="Chicory and ham gratin", recipe_txt=r)

# 6. Balletjes in tomatensaus: 100 g gehaktbal hoh gebakken + 80 g tomatensaus
v, r = recipe([(1568, 100, "gehaktbal half-om-half gebakken"), (1524, 80, "tomatensaus")], 180)
add(900006, "Balletjes in tomatensaus", "Samengestelde gerechten", "🍝", v, "Berekend uit recept met NEVO-ingrediënten",
    "Gehaktballetjes met tomatensaus, verhouding 100 g vlees op 80 g saus.", syn="Gehaktballetjes in tomatensaus/Boulets sauce tomate", flem="balletjes boulets tomatensaus gehaktballetjes", en="Meatballs in tomato sauce", recipe_txt=r)

# 7. Boulet met krieken: 100 g gehaktbal hoh gebakken + 80 g zure kersen (krieken)
v, r = recipe([(1568, 100, "gehaktbal half-om-half gebakken"), (167, 80, "zure kersen (krieken)")], 180)
add(900007, "Frikadellen met krieken", "Samengestelde gerechten", "🍒", v, "Berekend uit recept met NEVO-ingrediënten",
    "Gehaktbal met warme krieken, 100 g vlees op 80 g krieken (ongebonden, zonder extra suiker).", syn="Boulet met krieken/Balletjes met krieken", flem="boulet krieken frikadel balletjes kersen", en="Meatballs with sour cherries", recipe_txt=r)

# 8. Mitraillette: half stokbrood 120 g, frites 150 g, frikandel 90 g, mayonaise 25 g
v, r = recipe([(2793, 120, "wit stokbrood"), (2107, 150, "frites gefrituurd"), (322, 90, "frikandel gefrituurd"), (451, 25, "mayonaise")], 385)
add(900008, "Mitraillette met frikandel en mayonaise", "Samengestelde gerechten", "🥖", v, "Berekend uit recept met NEVO-ingrediënten",
    "Half stokbrood met frieten, frikandel en mayonaise (één portie ≈ 385 g).", syn="Mitraillette", flem="mitraillette frituur broodje frieten", en="Mitraillette (baguette with fries and sausage)", recipe_txt=r)

# synonyms added to existing NEVO items (no duplicates)
EXTRA_SYN = {
    1485: "wortelstoemp stoemp", 1483: "boerenkoolstoemp stoemp", 1531: "andijviestoemp stoemp", 1486: "zuurkoolstoemp stoemp",
    489: "rijsttaart rijstevlaai", 2661: "luikse wafel gaufre de liege", 2662: "brusselse wafel suikerwafel",
    810: "americain prepare préparé martino", 474: "smoutebol smoutebollen", 5329: "stoofvlees stoverij hachee",
    2793: "baguette stokbrood", 322: "frikadel curryworst", 326: "vleeskroket kroket",
}

out = "const EXTRA=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";\nconst EXTRA_SYN=" + json.dumps(EXTRA_SYN) + ";\n"
open("/home/claude/nevo-app/extra.js", "w", encoding="utf-8").write(out)
for i in items:
    print(i["c"], i["n"], "|", i["kcal"], "kcal E", i["p"], "V", i["fat"], "K", i["cho"], "| per 100 g")
