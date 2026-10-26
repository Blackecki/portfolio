# Blackecki

Znak osobisty zbudowany z geometrycznej litery B oraz napisu „blackecki”. Dwa wycięcia w znaku nawiązują do promptu terminala `>`. Logo zostało przygotowane za pomocą kodu jako grafika wektorowa.

## Pliki

- `blackecki-logo-on-dark` — pełne logo na ciemne tło.
- `blackecki-logo-on-light` — pełne logo na jasne tło.
- `blackecki-logo-black` i `blackecki-logo-white` — wersje jednobarwne.
- `blackecki-mark` — sam znak B, bez napisu.
- `blackecki-avatar` — ikona na granatowym tle, odpowiednia do profilu i favicony.

Każda wersja jest dostępna jako SVG oraz PNG. Pełne logo w PNG ma szerokość 2400 px; znaki i ikony mają 1024 × 1024 px. Pliki SVG składają się z krzywych i nie wymagają instalowania fontów. Fonty nie są dołączone do zestawu.

## Stosowanie

- Wybierz wariant odpowiadający jasności tła.
- Zachowaj proporcje i wolną przestrzeń wokół znaku.
- Przy małych rozmiarach użyj samego B; dołączone pliki 16 i 32 px pokazują jego czytelność jako ikony.
- Do zmiany wielkości i przygotowania druku użyj SVG. Do profilu, dokumentu lub prezentacji użyj PNG.

## Konstrukcja

Symbol B jest własną konstrukcją geometryczną. Napis opiera się na kroju Bahnschrift o wadze 600, z indywidualnym dopasowaniem odstępów i konwersją do krzywych. Kolory: granat `#17233A`, niebieski `#4169A5`, jasny niebieski `#B4C7FF`.

Dołączone źródła: `tools/build_logo.py`, `tools/render_logo.cjs` i `tools/preview_logo.py`. Odtworzenie eksportów wymaga Pythona z fonttools i Pillow, Node.js z Sharp oraz zainstalowanego kroju Bahnschrift. Font nie jest potrzebny do korzystania z gotowych SVG i PNG.
