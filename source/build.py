import csv, json, re, sys, unicodedata
sys.path.insert(0, "/home/claude/nevo-app")
from synonyms import RULES
import icons as ICONS

SRC = "/mnt/user-data/attachments/89ab58b2-0e20-598a-8f96-e199b6c3262f/d4050bd4-NEVO2025_v9.0.csv"

def num(s):
    s = (s or "").strip().strip('"')
    if s == "":
        return None
    return float(s.replace(",", "."))

def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s)

# NEVO abbreviations -> full words (for search only)
ABBR = {"m": "met", "z": "zonder", "v": "van", "gem": "gemiddeld", "ca": "circa",
        "bev": "bevroren", "onber": "onbereid", "ber": "bereid", "gek": "gekookt",
        "geb": "gebakken", "gefr": "gefrituurd", "gedr": "gedroogd", "vb": "volkoren brood"}

# Flemish / Belgian terms. key = word that appears in the NEVO name (normalised), value = extra search words
FLEMISH = {
    "aardappel": "patat patatten aardappelen", "aardappelen": "patatten patat",
    "frites": "frieten friet frietjes patatjes frituur", "patat": "frieten friet",
    "fritessaus": "frietsaus mayonaise", "saus frites": "frietsaus",
    "ui": "ajuin", "uien": "ajuinen ajuin", "uitjes": "ajuintjes",
    "sinaasappel": "appelsien", "sinaasappelsap": "appelsiensap fruitsap", "jus d orange": "appelsiensap fruitsap sinaasappelsap",
    "witlof": "witloof chicon", "spruitjes": "spruiten", "sperziebonen": "prinsessenbonen boontjes princessenboontjes",
    "bonen sperzie": "prinsessenbonen boontjes", "doperwten": "erwtjes erwten", "erwten": "erwtjes",
    "bieten": "rode biet bietjes", "biet": "bietjes", "kroten": "rode bieten",
    "paprika": "paprika", "komkommer": "komkommer", "champignons": "champignons kampernoelies",
    "prei": "prei", "andijvie": "andijvie", "veldsla": "veldsla", "rucola": "rucola",
    "boerenkool": "boerenkool", "koolraap": "koolraap", "koolrabi": "koolrabi",
    "kool bloem": "bloemkool", "kool rode": "rode kool", "kool witte": "witte kool",
    "aubergine": "aubergine", "courgette": "courgette",
    "mandarijn": "mandarijntje clementine", "mandarijnen": "clementines",
    "aardbeien": "aardbei", "pruimen": "pruim", "perzik": "perzik", "abrikoos": "abrikoos",
    "rozijnen": "rozijnen", "krenten": "krenten",
    "biefstuk": "steak biefstuk rundsvlees", "runderbiefstuk": "steak rundsteak biefstuk",
    "rund": "rundsvlees rund", "runder": "rundsvlees runds", "rundvlees": "rundsvlees",
    "rundergehakt": "rundsgehakt gehakt", "gehakt": "gehakt gemalen vlees", "half om half": "gemengd gehakt",
    "varkens": "varkensvlees", "varkenshaas": "varkenshaasje", "karbonade": "kotelet kotelette",
    "speklap": "spek", "spek": "spek", "ham": "hesp", "achterham": "hesp gekookte hesp", "rauwe ham": "rauwe hesp",
    "hamburger": "hamburger", "frikandel": "frikadel curryworst", "kroket": "kroket", "bitterballen": "bitterballen",
    "kipfilet": "kippenfilet kippenwit kipfilet kippenborst", "kip": "kieken kip", "kippen": "kieken", "drumstick": "kippenbout",
    "kipnuggets": "nuggets", "shoarma": "pita pitta", "doner": "pita pitta kebab", "kebab": "pitta",
    "hachee": "stoverij stoofvlees", "stoofvlees": "stoverij stoofvlees vlaamse stoverij", "riblappen": "stoofvlees stoverij", "sukadelappen": "stoofvlees stoverij", "runderlappen": "stoofvlees", "rookworst": "worst",
    "worst": "worst saucisse", "braadworst": "saucisse worst", "knakworst": "worstje knakworst",
    "filet americain": "americain preparé filet americain", "ossenworst": "americain",
    "leverworst": "leverworst leverpastei", "pate": "paté pastei", "pastei": "paté",
    "salami": "salami", "cervelaat": "cervela", "boterhamworst": "lunchworst", "kipfilet beleg": "kippenwit",
    "vis": "vis", "kabeljauw": "kabeljauw", "koolvis": "koolvis", "zalm": "zalm", "tonijn": "tonijn",
    "garnalen": "garnalen grijze garnalen scampi", "mosselen": "mosselen", "kibbeling": "visnuggets gefrituurde vis",
    "lekkerbekje": "gebakken vis", "haring": "haring maatjes", "makreel": "makreel", "paling": "paling",
    "ei": "ei eieren", "eieren": "ei",
    "melk": "melk", "karnemelk": "botermelk", "chocolademelk": "chocomelk chocolademelk cecemel",
    "vla": "pudding vla", "kwark": "plattekaas platte kaas", "hüttenkäse": "cottage cheese",
    "slagroom": "room slagroom", "room": "room",
    "yoghurt": "yoghurt yogurt", "pap": "pap", "havermoutpap": "havermoutpap porridge",
    "kaas": "kaas", "smeerkaas": "smeerkaas", "jonge": "jonge kaas", "belegen": "belegen kaas",
    "brood": "brood boterham boterhammen", "boterham": "boterham", "bruinbrood": "bruin brood",
    "volkoren": "volkoren", "witbrood": "wit brood", "broodje": "pistolet sandwich broodje", "bolletje": "pistolet",
    "pistolet": "pistolet", "stokbrood": "baguette stokbrood", "krentenbol": "rozijnenbrood krentenbrood",
    "suikerbrood": "suikerbrood", "ontbijtkoek": "peperkoek ontbijtkoek", "beschuit": "beschuit",
    "cracker": "cracker", "rijstwafel": "rijstwafel", "wentelteefje": "verloren brood gewonnen brood",
    "pannenkoek": "pannenkoek", "poffertjes": "poffertjes", "wafel": "wafel", "stroopwafel": "stroopwafel",
    "croissant": "croissant", "koffiebroodje": "koffiekoek", "appelflap": "appelflap", "saucijzenbroodje": "worstenbroodje",
    "speculaas": "speculoos speculaas", "pepernoten": "pepernoten", "koek": "koek koekje",
    "koekje": "koekje", "biscuit": "biscuit koekje", "cake": "cake", "taart": "taart", "appeltaart": "appeltaart",
    "gebak": "gebak taartje", "vlaai": "vlaai taart", "eclair": "eclair", "tompouce": "tompoes",
    "hagelslag": "hagelslag muizenstrontjes", "chocoladepasta": "choco chocopasta", "pindakaas": "pindakaas",
    "jam": "confituur jam", "stroop": "siroop stroop", "appelstroop": "sirop de liege appelstroop",
    "honing": "honing", "suiker": "suiker",
    "snoep": "snoep snoepjes", "drop": "drop", "chocolade": "chocolade chocola", "reep": "reep",
    "chips": "chips", "zoutjes": "zoutjes aperitiefkoekjes", "borrelnootjes": "nootjes",
    "pasta": "pasta deegwaren", "macaroni": "macaroni", "spaghetti": "spaghetti", "noedels": "noedels noodles",
    "rijst": "rijst", "couscous": "couscous", "bulgur": "bulgur", "quinoa": "quinoa",
    "havermout": "havervlokken havermout", "muesli": "muesli", "cruesli": "granola krokante muesli", "cornflakes": "cornflakes",
    "brinta": "brinta", "bami": "bami", "nasi": "nasi", "loempia": "loempia",
    "soep": "soep", "erwtensoep": "erwtensoep snert", "tomatensoep": "tomatensoep",
    "mayonaise": "mayonaise mayo", "ketchup": "ketchup", "curry": "curry currysaus", "satesaus": "satésaus",
    "pindasaus": "satésaus", "mosterd": "mosterd", "appelmoes": "appelmoes", "jus": "saus jus",
    "boter": "boter", "halvarine": "minarine halvarine", "margarine": "margarine", "olie": "olie", "olijfolie": "olijfolie",
    "bier": "bier pint pintje", "pils": "pils pintje", "wijn": "wijn", "jenever": "jenever",
    "cola": "cola", "limonade": "limonade frisdrank", "frisdrank": "frisdrank", "ranja": "siroop grenadine",
    "sinas": "orangeade fanta", "ijsthee": "ice tea ijsthee", "sportdrank": "sportdrank isotone drank",
    "energiedrank": "energy drink energiedrank", "koffie": "koffie", "thee": "thee", "water": "water",
    "mineraalwater": "plat water spuitwater bruiswater",
    "sap": "fruitsap sap", "appelsap": "appelsap", "smoothie": "smoothie",
    "ijs": "ijs roomijs crème glace", "roomijs": "roomijs crème glace", "waterijs": "ijsje",
    "pinda": "pinda arachide", "pindas": "pindanoten", "noten": "noten", "amandelen": "amandelen", "walnoten": "walnoten",
    "tofu": "tofu", "tempe": "tempeh", "vegetarische": "veggie vegetarisch",
    "linzen": "linzen", "kikkererwten": "kikkererwten", "bruine bonen": "bruine bonen", "witte bonen": "witte bonen",
    "magnetron": "microgolf", "oven": "oven", "gefrituurd": "frituur gefrituurd", "gebakken": "gebakken",
    "kipsate": "kippensaté saté", "sate": "saté", "kapsalon": "kapsalon",
    "eierkoek": "eierkoek", "tosti": "croque croque monsieur tosti", "croque": "croque monsieur",
    "patatje": "frietjes", "frikadel": "frikandel",
    "slasaus": "vinaigrette slasaus dressing", "dressing": "vinaigrette",
    "zuurkool": "zuurkool choucroute", "stamppot": "stoemp stamppot", "hutspot": "stoemp wortelstoemp",
    "puree": "puree aardappelpuree", "aardappelpuree": "puree stoemp",
    "cervelaatworst": "cervela", "pekelvlees": "pekelvlees", "rosbief": "rosbief",
    "kalkoen": "kalkoen", "eend": "eend", "konijn": "konijn", "lam": "lam lamsvlees",
    "gyros": "pitta", "pizza": "pizza", "lasagne": "lasagne", "wrap": "wrap durum", "durum": "durum",
    "hamburgerbroodje": "hamburgerbroodje", "friet": "frieten",

    "boterham@Brood": "boke boterhammen", "sandwich": "sandwich smos", "koffiebroodje": "koffiekoek ronde suisse rozijnenkoek", "chocoladebroodje": "koffiekoek chocoladekoek",
    "bloedworst": "pens bloedworst beuling", "hoofdkaas": "kipkap tete pressee", "zult": "kipkap kop",
    "jenever": "dreupel jenever", "curryworst": "curryworst", "frikandel": "frikadel curryworst", 
    "vleeskroket": "kroket", "kaas": "kaas", "kaasplank": "kaas",
    "pannenkoek": "pannenkoek", "flensjes": "pannenkoekjes crepes", "wafel": "wafel gaufre", "suikerwafel": "brusselse wafel",
    "appelsap": "appelsap", "jus d orange": "appelsiensap fruitsap", "sinaasappelsap": "appelsiensap fruitsap",
    "koffiemelk": "koffiemelk", "roomboter": "boter", "cottage": "plattekaas", "kwark": "plattekaas platte kaas",
    "limonade": "limonade", "cola": "cola", "ranja": "grenadine siroop", "water": "water plat water", "bruisend": "spuitwater bruiswater",
    "koolzuurhoudend": "spuitwater bruiswater", 
    "tompouce": "tompoes", "soes": "soesje", "eclair": "eclair", 
    "rijstevlaai": "rijsttaart", "worstenbroodje": "worstenbrood",
    "peen": "wortel wortelen", "wortelen": "wortels", "bospeen": "wortelen", "spruitjes": "spruiten",
    "kipfilet": "kippenwit kippenfilet", "kippenbout": "kippenbil billetje", "kippenpoot": "kippenbil",
    "gebakken aardappelen": "gebakken patatten", "puree": "puree stoemp", "krieltjes": "krielpatatjes",
    "schnitzel": "schnitzel", "kalkoenfilet": "kalkoen", "varkenslapje": "varkenslapje",
    "tartaar": "tartaar", "ribeye": "ribeye", "entrecote": "entrecote cote a l os",
    "kipkorn": "kipcorn", "berenklauw": "berenpoot",
    "sinaasappels": "appelsienen", "jus d'orange": "appelsiensap fruitsap",
}

# emoji icon: ordered keyword rules, then food group fallback
ICON_RULES = [
    (r"\bfrites|friet|patat\b|fritessticks", "🍟"), (r"pizza", "🍕"), (r"hamburger|cheeseburger", "🍔"),
    (r"biefstuk|steak|rosbief|entrecote|ribeye|t-bone|runderlap|rundvlees|rund(er)?\b|stoofvlees|hachee|kalfs", "🥩"),
    (r"kip|kalkoen|drumstick|gevogelte|eend|haan|nuggets", "🍗"),
    (r"spek|bacon|speklap|varkens|karbonade|schnitzel|ham\b|achterham|hesp", "🥓"),
    (r"worst|salami|cervelaat|frikandel|knak|saucij|chorizo", "🌭"),
    (r"zalm|forel|tonijn|kabeljauw|koolvis|vis\b|vissticks|haring|makreel|paling|schol|tilapia|pangasius|sardine|ansjovis|kibbeling|lekkerbek|visstick", "🐟"),
    (r"garnaal|garnalen|scampi|gamba|kreeft|krab", "🦐"), (r"mossel|oester|schelp|inktvis|calamar", "🦪"),
    (r"\bei\b|eieren|omelet|eier", "🥚"),
    (r"kaas|cheese|camembert|brie|mozzarella|feta|parmezaan|gouda|smeerkaas|hüttenkäse|kwark|cottage", "🧀"),
    (r"melk|karnemelk|chocolademelk|lactose", "🥛"), (r"yoghurt|vla\b|pudding|skyr|pap\b", "🍶"),
    (r"roomijs|ijs\b|ijsje|sorbet|softijs|magnum|cornetto", "🍦"),
    (r"chocola|bonbon|praline|reep\b|mars|snickers|twix|kitkat|m&m", "🍫"),
    (r"snoep|drop|zuurtje|winegum|lolly|kauwgom|spekjes|toffee|pepermunt", "🍬"),
    (r"taart|vlaai|gebak|tompouce|eclair|cheesecake|brownie|muffin|cupcake|soes", "🍰"),
    (r"cake\b|tulband", "🧁"), (r"koek|biscuit|speculaas|pepernoten|stroopwafel|cracker|beschuit|wafel|bastogne|oreo|kano", "🍪"),
    (r"donut|oliebol|appelflap|appelbeignet", "🍩"), (r"pannenkoek|poffertjes|wentelteefje|crepe", "🥞"),
    (r"croissant|koffiebroodje|chocoladebroodje", "🥐"), (r"stokbrood|baguette|ciabatta", "🥖"), (r"pistolet|broodje|bolletje|pita|wrap|tortilla|bagel|hamburgerbroodje", "🥙"),
    (r"brood|boterham|toast|knackebrod|krentenbol|rozijnenbrood|ontbijtkoek|roggebrood|beschuit", "🍞"),
    (r"pasta|spaghetti|macaroni|tagliatelle|penne|lasagne|noedels|mie\b|ravioli|tortellini|gnocchi", "🍝"),
    (r"rijst|nasi|risotto|sushi", "🍚"), (r"bami|ramen|noodle|soep|bouillon|erwtensoep", "🍜"),
    (r"couscous|bulgur|quinoa|boekweit|gierst|havermout|muesli|cruesli|granola|cornflakes|ontbijtgranen|brinta|havervlokken|graan|tarwe|meel|bloem\b|zemelen", "🌾"),
    (r"aardappel|puree|stamppot|hutspot|rosti|krieltjes|pommes", "🥔"), (r"zoete aardappel|bataat", "🍠"),
    (r"wortel|peen|bospeen|winterpeen", "🥕"), (r"tomaat|tomaten|ketchup|passata", "🍅"),
    (r"paprika|peper rode|chili|pepers|jalapeno|sambal", "🌶️"), (r"komkommer|augurk|courgette", "🥒"),
    (r"sla\b|andijvie|spinazie|rucola|veldsla|boerenkool|postelein|snijbiet|waterkers|kool\b|spruit|bloemkool|broccoli|witlof|prei|selderij|asperge|venkel|spitskool|zuurkool|paksoi|bimi|koolrabi|raap", "🥬"),
    (r"broccoli", "🥦"), (r"mais|maïs|popcorn", "🌽"), (r"champignon|paddenstoel|oesterzwam|shiitake|cantharel", "🍄"),
    (r"aubergine", "🍆"), (r"avocado|guacamole", "🥑"), (r"ui\b|uien|sjalot|knoflook|look", "🧅"),
    (r"erwt|linzen|kikkererwt|bonen|boon\b|sojabonen|kapucijner|hummus|edamame|peulvrucht|tuinbonen|sperzie|snijbonen", "🫘"),
    (r"olijf|olijven", "🫒"), (r"appel\b|appels|appelmoes|appelsap", "🍎"), (r"peer\b|peren", "🍐"),
    (r"sinaasappel|mandarijn|clementine|jus d|citrus", "🍊"), (r"citroen|limoen", "🍋"), (r"banaan|bananen", "🍌"),
    (r"druiven|druif|rozijn|krent", "🍇"), (r"aardbei", "🍓"), (r"kers|kersen", "🍒"), (r"perzik|nectarine|abrikoos", "🍑"),
    (r"meloen|watermeloen", "🍉"), (r"ananas", "🍍"), (r"mango|papaja|passievrucht|lychee|kiwi|granaatappel", "🥭"),
    (r"bessen|bes\b|framboos|frambozen|bosbes|blauwe bes|cranberry|braam|bramen|rode bes", "🫐"),
    (r"kokos", "🥥"), (r"pruim|dadel|vijg", "🫐"), (r"fruit\b|vruchten", "🍎"),
    (r"pinda|noten|noot\b|amandel|walnoot|hazelnoot|cashew|pistache|zaden|zaad|pitten|sesam|lijnzaad|chia|pindakaas|notenpasta", "🥜"),
    (r"honing", "🍯"), (r"jam\b|confituur|marmelade|stroop|hagelslag|chocoladepasta|vlokken|gestampte muisjes", "🫙"),
    (r"boter|halvarine|margarine|bak- en braad|reuzel|ghee", "🧈"), (r"olie|oliën|vet\b|mayonaise|fritessaus|dressing|slasaus|saus", "🫗"),
    (r"suiker|zoetstof|siroop|glucose", "🧂"), (r"zout|kruiden|specerij|peper\b|kaneel|kerrie|bouillonblok|maggi|azijn|mosterd", "🧂"),
    (r"koffie|espresso|cappuccino|latte", "☕"), (r"thee|ijsthee|ice tea|kamille|rooibos", "🍵"),
    (r"bier|pils|witbier|trappist|abdij|stout|radler", "🍺"), (r"wijn|champagne|cava|prosecco|port\b|sherry|vermout", "🍷"),
    (r"jenever|whisky|wodka|rum|gin|likeur|cognac|brandewijn|advocaat|baileys|sterke drank|cocktail|shot", "🍸"),
    (r"cola|limonade|frisdrank|sinas|fanta|sprite|energiedrank|energy|sportdrank|red bull|tonic|cassis|ranja|siroop", "🥤"),
    (r"sap\b|smoothie|nectar|fruitdrank|vruchtendrank|appelsap|sinaasappelsap|druivensap|tomatensap", "🧃"),
    (r"water|spa\b|bruiswater|spuitwater|mineraal", "💧"),
    (r"tofu|tempe|seitan|vegetarisch|vegan|plantaardig|soja|haver drink|amandeldrink|kokosdrink", "🌱"),
    (r"chips|zoutjes|borrelnoot|popcorn|nacho|tortillachips|pretzel|snack", "🍿"),
    (r"kroket|bitterbal|loempia|nasischijf|bamischijf|kaassouffle|kipcorn|sate|saté|shoarma|döner|kebab|gyros|kapsalon|falafel", "🥘"),
    (r"salade|huzaren|eiersalade|kipsalade|vleessalade|krabsalade|zalmsalade|tonijnsalade|filet americain|pate|paté|pastei|leverworst", "🥗"),
    (r"flesvoeding|zuigeling|opvolgmelk|babyvoeding|baby", "🍼"),
    (r"supplement|sportvoeding|eiwitpoeder|proteine|whey|gel\b|energiereep|eiwitreep|mueslireep|granenreep", "💪"),
]
GROUP_ICON = {
    "Groente": "🥬", "Vlees en gevogelte": "🥩", "Gebak en koek": "🍪", "Graanproducten en meelsoorten": "🌾",
    "Melk en melkproducten": "🥛", "Suiker, snoep, zoet beleg en zoete sauzen": "🍬", "Brood": "🍞",
    "Niet-alcoholische dranken": "🥤", "Fruit": "🍎", "Vis, schaal- en schelpdieren": "🐟",
    "Samengestelde gerechten": "🍽️", "Hartige sauzen": "🫗", "Kaas": "🧀", "Hartige snacks en zoutjes": "🍿",
    "Vetten en oliën": "🧈", "Vleeswaren": "🥓", "Vleesvervangers en zuivelvervangers": "🌱",
    "Flesvoeding en preparaten": "🍼", "Kruiden en specerijen": "🧂", "Aardappelen en knolgewassen": "🥔",
    "Alcoholische dranken": "🍺", "Peulvruchten": "🫘", "Noten en zaden": "🥜", "Soepen": "🍲",
    "Hartig broodbeleg": "🥪", "Diversen": "🍽️", "Eieren": "🥚",
}

def icon_for(name_n, group):
    hay = name_n
    for pat, ic in ICON_RULES:
        if re.search(pat, hay):
            return ic
    return GROUP_ICON.get(group, "🍽️")

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig"), delimiter="|"))
out = []
for r in rows:
    name = r["Voedingsmiddelnaam/Dutch food name"].strip()
    syn = r["Synoniem"].strip()
    en = r["Engelse naam/Food name"].strip()
    group = r["Voedingsmiddelgroep"].strip()
    n = norm(name)
    s = norm(syn)
    # expand abbreviations
    expanded = " ".join(ABBR.get(w, w) for w in n.split())
    fl = set()
    for pat, syns in RULES:
        if re.search(pat, n):
            fl.update(syns.split())
    fl -= set((n + " " + s).split())
    item = {
        "c": int(r["NEVO-code"]), "g": group, "n": name, "e": en, "s": syn,
        "f": " ".join(sorted(fl)), "x": expanded if expanded != n else "",
        "u": "ml" if "ml" in r["Hoeveelheid/Quantity"] else "g",
        "i": ICONS.icon_for(n, group),
        "kcal": num(r["ENERCC (kcal)"]), "kj": num(r["ENERCJ (kJ)"]),
        "p": num(r["PROT (g)"]), "fat": num(r["FAT (g)"]), "sat": num(r["FASAT (g)"]),
        "cho": num(r["CHO (g)"]), "sug": num(r["SUGAR (g)"]), "fib": num(r["FIBT (g)"]),
        "alc": num(r["ALC (g)"]), "na": num(r["NA (mg)"]), "w": num(r["WATER (g)"]),
    }
    out.append(item)

# Hide exact duplicates (identical NEVO values) and the baby/toddler section. Values of kept rows stay unchanged;
# the hidden row's name moves onto the kept row as a search term.
HIDE = {61: 2735, 1147: 55, 2: 1, 3: 1, 598: 1885, 599: 1885, 600: 1885, 2819: 841, 5286: 841, 5305: 3352}
BABY = re.compile(r"^(zuigelingenvoeding|opvolgmelk|dreumesmelk|peutermelk|peuterplusmelk|babyvoeding|kindervoeding|orisel|ontbijtproduct olvarit|biscuit baby|biscuit dreumes|pap nestle pyjamapapje|drink soja groeidrink)")
byc = {o["c"]: o for o in out}
for h, k in HIDE.items():
    extra = norm(byc[h]["n"]).split()
    have = set((norm(byc[k]["n"]) + " " + byc[k]["f"]).split())
    byc[k]["f"] = " ".join(sorted(set(byc[k]["f"].split()) | {w for w in extra if w not in have and len(w) > 2 and not any(ch.isdigit() for ch in w) and w not in {"calcium", "liter", "kops", "toegevoegd", "jodium", "gekookt", "rauw"}}))
hidden_baby = [o["n"] for o in out if BABY.search(norm(o["n"]))]
out = [o for o in out if o["c"] not in HIDE and not BABY.search(norm(o["n"]))]
print("hidden duplicates:", len(HIDE), "| hidden baby/toddler:", len(hidden_baby))
groups = sorted({o["g"] for o in out})
js = "let NEVO_VERSION='NEVO-online versie 2025/9.0, RIVM, Bilthoven';\nlet FOODS=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
open("/home/claude/nevo-app/data.js", "w", encoding="utf-8").write(js)
print(len(out), "items;", len(js)//1024, "KB")
import collections
print(collections.Counter(o["i"] for o in out).most_common(12))
print(sum(1 for o in out if o["f"]), "items got Flemish synonyms")
for o in out:
    if o["c"] in (1536, 2108, 1456, 465): print(o)
