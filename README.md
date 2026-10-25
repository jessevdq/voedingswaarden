# Voedingswaarden

Persoonlijke zoek-app voor caloriën en macro's van standaardproducten. Werkt als PWA (offline, op het beginscherm).

- `index.html` app · `data.js` NEVO-gegevens · `extra.js` Belgische gerechten en extra zoektermen · `sw.js` offline cache · `manifest.json` + iconen
- `source/build.py` maakt `data.js` uit `NEVO2025_v9.0.csv` (zelf aanvragen bij RIVM, niet in deze repo). `source/build_extra.py` berekent de extra gerechten uit NEVO-ingrediënten.

Bron: NEVO-online versie 2025/9.0, RIVM, Bilthoven (gegevens ongewijzigd overgenomen). Vlaamse zoektermen, iconen en de als niet-NEVO gemarkeerde gerechten zijn eigen toevoegingen.
