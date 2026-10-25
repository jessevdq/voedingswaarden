"""Icon per product: rules on the START of the normalised NEVO name, checked per food group,
then a group default. Never matches words in the middle of a name (no 'ijs' in 'radijs')."""
import re
COMMON = [  # checked for every group, before the group rules
    (r"^(zuigelingenvoeding|opvolgmelk|dreumesmelk|peutermelk|peuterplusmelk|babyvoeding|kindervoeding|orisel)", "🍼"),
    (r"^(salade|rauwkost)", "🥗"),
    (r"^pizza", "🍕"), (r"^(hamburger|broodje hamburger|broodje cheeseburger)", "🍔"),
    (r"^(tosti|croque|broodje gezond|sandwich)", "🥪"),
    (r"^(wrap m|burrito|taco)", "🌯"), (r"^(wrap tortilla|roti)", "🫓"), (r"^sushi", "🍣"),
    (r"^(soep|bouillon)\b", "🍲"), (r"^soepstengel", "🥖"),
    (r"^(pannenkoek|poffertjes|wentelteefje|bakmix voor (pannenkoeken|poffertjes))", "🥞"),
    (r"^(puddingpoeder|custardpoeder)", "🍮"), (r"^(zout)\b", "🧂"), (r"^(cacaopoeder|cacaoproduct)", "🍫"),
    (r"^(olijven)", "🫒"), (r"^(gnocchi)", "🍝"), (r"^(uitjes gebakken)", "🧅"),
    (r"^frites (bereid|oven|voorgebakken|speciaal|m sauzen|kapsalon)|^frites$", "🍟"),
]
GROUPS = {
    "Groente": [
        (r"^(tomaat|tomaten|puree tomaten)", "🍅"), (r"^(paprika|peper spaanse|pepers)", "🫑"),
        (r"^(komkommer|augurk|courgette|sopropo)", "🥒"), (r"^wortel", "🥕"),
        (r"^(champignon|cantharel|groente roerbakmix champignon)", "🍄"),
        (r"^(ui |ui$|knoflook|bieslook)", "🧅"), (r"^(aubergine|antroewa)", "🍆"), (r"^mais", "🌽"),
        (r"^broccoli", "🥦"), (r"^kool bloem", "🥦"), (r"^(bonen|doperwten|kousenband|peultjes)", "🫘"),
        (r"^pompoen", "🎃"), (r"^(avocado|guacamole)", "🥑"), (r"^(olijven)", "🫒"),
        (r"^(frites groente)", "🍟"), (r"^(cassave|aardpeer|taro|yam|pomtajer)", "🥔"),
    ],
    "Fruit": [
        (r"^(appel|appeltjes|appelmoes)", "🍎"), (r"^(peer|peren|stoofperen)", "🍐"),
        (r"^(sinaasappel|mandarijn|grapefruit|kumquat)", "🍊"), (r"^(citroen|limoen)", "🍋"),
        (r"^banaan", "🍌"), (r"^(druiven|rozijnen|krenten)", "🍇"), (r"^aardbei", "🍓"), (r"^kersen", "🍒"),
        (r"^(perzik|nectarine|abrikoz)", "🍑"), (r"^meloen", "🍈"), (r"^ananas", "🍍"), (r"^kiwi", "🥝"),
        (r"^(mango|papaja|passievrucht|lychee|guave|carambola|kaki|granaatappel|mispel|jackfruit|tamarinde)", "🥭"),
        (r"^(bessen|frambozen|bramen|cranberry)", "🫐"), (r"^kokos", "🥥"), (r"^(pruimen|dadels|vijgen)", "🫐"),
        (r"^rabarber", "🥬"),
    ],
    "Aardappelen en knolgewassen": [(r"^aardappel zoete", "🍠")],
    "Niet-alcoholische dranken": [
        (r"^(water|mineraalwater)", "💧"), (r"^kokoswater", "🥥"), (r"^wijn", "🍷"), (r"^sap tomat", "🍅"), (r"^(koffie|ijskoffie|cafe)", "☕"), (r"^(thee|ijsthee)", "🍵"),
        (r"^(frisdrank|energydrink|sportdrank)", "🥤"), (r"^bier", "🍺"),
        (r"^(drink|melk|milkshake|zuiveldrank|chocolademelk|drinkontbijt)", "🥛"),
        (r"^(sap|vruchtendrank|smoothie|limonade|diksap|siroop|fruitsnack)", "🧃"),
    ],
    "Alcoholische dranken": [
        (r"^(bier|cider|shandy|breezer)", "🍺"), (r"^(wijn|port|sherry|madeira|vermouth|muskaatwijn|champagne)", "🍷"),
        (r"^irish coffee", "☕"),
    ],
    "Melk en melkproducten": [
        (r"^(ijs|plantaardig alternatief voor roomijs)", "🍨"),
        (r"^(yoghurt|skyr|kwark|kefir|pap|krentjebrij|plantaardig alternatief voor (vruchten |)yoghurt|plantaardig alternatief voor vruchten)", "🥣"),
        (r"^(vla|pudding|dessert|toetje|mousse|tiramisu|puddingpoeder|custard)", "🍮"),
        (r"^(chocolade|vlokken chocolade|hagelslag)", "🍫"),
    ],
    "Vleesvervangers en zuivelvervangers": [
        (r"^(drink|kokosmelk|creamer|plantaardig alternatief voor room|santen)", "🥛"),
        (r"^plantaardig alternatief voor (vruchten |)(vanille|yoghurt|vruchten)|^dessert soja", "🥣"),
        (r"^plantaardig alternatief voor roomijs", "🍨"), (r"^plantaardig alternatief voor goudse kaas", "🧀"),
    ],
    "Kaas": [(r"^pindakaas", "🥜"), (r"^zult", "🥓"), (r"^(tarwestokbrood)", "🥖")],
    "Vlees en gevogelte": [
        (r"^(kip|kalkoen|eend|patrijs|fazant|struisvogel|gehakt kippen|worst grill kip|lever kippen|vet kippen)", "🍗"),
        (r"^(spek|speklap|bacon)", "🥓"),
        (r"^(worst|varkensbraadworst|runderbraadworst|kalfsbraadworst|frikandel)", "🌭"),
        (r"^(gehaktbal)", "🧆"), (r"^(sate)", "🍢"), (r"^shoarma", "🥙"),
        (r"^(varkens|spareribs|casseler|lams|schapen)", "🍖"),
    ],
    "Vleeswaren": [(r"^(worst|leverkaas)", "🌭"), (r"^(pate|pastei)", "🥫"), (r"^filet americain", "🥩"), (r"^(kipfilet|kalkoenfilet)", "🍗")],
    "Vis, schaal- en schelpdieren": [
        (r"^(garnalen|krab|kreeft|surimi)", "🦐"), (r"^(mosselen|oesters|jacobsschelpen|slakken)", "🦪"),
        (r"^inktvis", "🦑"), (r"^kaviaar|^kuit", "🐟"),
    ],
    "Hartig broodbeleg": [(r"^pindakaas", "🥜"), (r"^hummus", "🫘"), (r"^pasta (sesam|noten)", "🥜")],
    "Diversen": [(r"^azijn", "🫗"), (r"^(spijs|amandelspijs)", "🌰")],
    "Eieren": [(r"^omelet", "🍳")],
    "Brood": [
        (r"^(tarwestokbrood|tarwe ciabatta|focaccia)", "🥖"), (r"^(croissant|brioche)", "🥐"),
        (r"^(wrap|tortilla|tarwebrood wit pita|roti)", "🫓"),
        (r"^(knackebrod|beschuit|cracker|toast|wafel rijst|wafel mais|croutons)", "🫓"),
    ],
    "Gebak en koek": [
        (r"^(wafel)", "🧇"), (r"^(pannenkoek|poffertjes|wentelteefje|bakmix voor (pannenkoeken|poffertjes))", "🥞"),
        (r"^(donut|oliebol|berliner|beignet|bakmix voor oliebollen)", "🍩"),
        (r"^(croissant|broodje koffie|broodje amandel|broodje pudding|appelflap)", "🥐"),
        (r"^(taart|vlaai|tompouce|cheesecake|soes|baklava|carrotcake|brownie|bojo|mergpijpje|tulumba|bakmix voor (appeltaart|kwarktaart))", "🍰"),
        (r"^(cake|bakmix voor cake)", "🍰"),
        (r"^(stol|spijs|amandelspijs|bananenbrood)", "🍞"),
    ],
    "Graanproducten en meelsoorten": [
        (r"^(pasta|tortellini|gnocchi|manti|mihoen|noodles|lasagne|macaroni|spaghetti)", "🍝"),
        (r"^(rijst|bloem rijste|meel rijst)", "🍚"),
        (r"^(ontbijtproduct|muesli|vlokken|volkoren graanontbijt|maaltijdvervanger)", "🥣"),
        (r"^(bladerdeeg|filodeeg|brooddeeg|pasteibakje)", "🥐"),
    ],
    "Suiker, snoep, zoet beleg en zoete sauzen": [
        (r"^(chocolade|candybar|bonbon|hagelslag chocolade|vlokken chocolade|pasta chocolade|pasta duo|after eight|chocoladereep|kikkers|rozijnen omhuld|pinda s omhuld|maltesers|kruidnoten m chocolade)", "🍫"),
        (r"^(honing)", "🍯"), (r"^boter chocolade", "🍫"), (r"^kokosbrood", "🥥"), (r"^broodbeleg zoet", "🫙"), (r"^(jam|marmelade|spread fruit|stroop|siroop|pasta speculoos|hagelslag vruchten|vlokken|muisjes|appelstroop|dessertsaus)", "🫙"),
        (r"^(suiker|zoetstof|glucose|dextrose|fructose|glazuur|topping)", "🍬"),
        (r"^(ijs|plantaardig)", "🍧"), (r"^(graanreep|mueslireep|fruitreep|eiwitreep|sportvoeding)", "🌾"),
        (r"^(pinda|noga)", "🥜"),
    ],
    "Hartige snacks en zoutjes": [
        (r"^(popcorn)", "🍿"), (r"^(chips|kroepoek|zoutje|zoutjes|fritessticks|biscuit|koekje kaas|soepstengel|pepsels|cracker)", "🥨"),
        (r"^(kroket|bitterbal|kaassouffle|bamibal|nasischijf|kipkorn|berenklauw|viandel|soesje kaas|kipnuggets)", "🧆"),
        (r"^(frikandel|broodje (saucijzen|worsten|frikandel))", "🌭"), (r"^(loempia|broodje bapao)", "🥟"), (r"^broodje kaas", "🥐"), (r"^kikkererwten", "🫘"),
        (r"^peper zoete gevuld", "🫑"), (r"^(nuggets vegetarisch|gefrituurde peulvruchtensnack)", "🧆"),
        (r"^(pinda|noten|seroendeng|rempejek)", "🥜"),
    ],
    "Hartige sauzen": [(r"^(ketchup tomaten|saus tomaten|salsa)", "🍅"), (r"^(saus knoflook|aioli)", "🧄"), (r"^mosterd", "🫙")],
    "Vetten en oliën": [(r"^(olie olijf)", "🫒"), (r"^(boter|margarine|halvarine|bak en braadvet|vet|smeltjus|creme au beurre)", "🧈")],
    "Kruiden en specerijen": [
        (r"^(peterselie|kervel|basilicum|majoraan|oregano|rozemarijn|munt|kruiden tuin|selderij blad|bieslook|tijm|dragon|dille)", "🌿"),
        (r"^(peper|chilipoeder|paprikapoeder|sambal|kerrie)", "🌶️"), (r"^(knoflook)", "🧄"),
        (r"^(mosterd)", "🫙"), (r"^(azijn)", "🫗"),
    ],
    "Noten en zaden": [(r"^(kastanje)", "🌰"), (r"^(kokos)", "🥥")],
    "Samengestelde gerechten": [
        (r"^(pasta|lasagne|spaghetti|tortellini|macaroni|pastagerecht|manti|gnocchi)", "🍝"),
        (r"^(nasi|rijst|risotto|bobotie|bruine bonen m rijst)", "🍚"), (r"^(bami|mihoen|noodles)", "🍜"),
        (r"^(stamppot|aardappel|hutspot)", "🥔"), (r"^(omelet)", "🍳"), (r"^(quiche|taart hartige)", "🥧"),
        (r"^(chili con carne|goulash|ragout|stoofvlees|hachee)", "🍲"), (r"^(paprika gevuld)", "🫑"),
        (r"^(witlof)", "🥬"), (r"^kaasfondue", "🧀"), (r"^saus bolognese", "🍝"), (r"^(frites)", "🍟"), (r"^(sate)", "🍢"),
    ],
}
GROUP_ICON = {
    "Groente": "🥬", "Fruit": "🍎", "Aardappelen en knolgewassen": "🥔", "Niet-alcoholische dranken": "🧃",
    "Alcoholische dranken": "🥃", "Melk en melkproducten": "🥛", "Kaas": "🧀", "Vlees en gevogelte": "🥩",
    "Vleeswaren": "🥓", "Vis, schaal- en schelpdieren": "🐟", "Eieren": "🥚", "Brood": "🍞",
    "Gebak en koek": "🍪", "Graanproducten en meelsoorten": "🌾", "Suiker, snoep, zoet beleg en zoete sauzen": "🍬",
    "Hartige snacks en zoutjes": "🥨", "Hartige sauzen": "🫗", "Vetten en oliën": "🫗", "Kruiden en specerijen": "🧂",
    "Noten en zaden": "🥜", "Peulvruchten": "🫘", "Soepen": "🍲", "Samengestelde gerechten": "🍲",
    "Vleesvervangers en zuivelvervangers": "🌱", "Flesvoeding en preparaten": "🍼", "Hartig broodbeleg": "🥪", "_": "", "Diversen": "🍽️",
}
def icon_for(n, group):
    for pat, ic in COMMON:
        if re.search(pat, n): return ic
    for pat, ic in GROUPS.get(group, []):
        if re.search(pat, n): return ic
    return GROUP_ICON.get(group, "🍽️")
