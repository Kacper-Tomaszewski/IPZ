---
title: Projekt Fusion 360
tags:
  - ball-balancer
  - cad
  - fusion360
  - mechanika
created: 2026-10-20
---

# 26. Projekt Fusion 360 (model całości)

Powrót: [[Projekt Ball Balancer]]. Wymiary: [[05 Geometria i wymiary]]. Kinematyka: [[06 Kinematyka i zakres ruchu]]. Lista wydruków: [[16 Elementy do druku]].

## W skrócie

Cały stół jest zbudowany **skryptem Pythona dla Fusion 360**: baza z kieszeniami serw, konsola, taca z żebrami i rantem, cztery części nóg, pałąk C-Arm z regulacją kamery, serwa HS-422, kulka, pierścień LED i płytka kamery. Skrypt robi więcej niż model:

- **przechyla tacę** według tej samej kinematyki odwrotnej co firmware i ustawia wszystkie części nóg,
- **sprawdza kolizje** w zadanej pozycji i w całym zakresie ruchu, a wynik zapisuje do raportu,
- **eksportuje STL** wszystkich wydruków z nazwami z [[16 Elementy do druku]].

![[26_fusion_render.png]]
*Taca przechylona o 6° w stronę serwa 1, kulka poza środkiem (podgląd z testu skryptu).*

> [!warning] Status
> Skrypt sprawdziłem **poza Fusion**: na atrapie API Fusion z prawdziwymi operacjami na bryłach (biblioteka manifold3d). Wszystkie części się budują, każda jest jedną bryłą, przechylanie, test kolizji i eksport STL działają. W samym Fusion 360 skrypt **jeszcze nie był uruchamiany**. Jeśli przy pierwszym uruchomieniu pojawi się błąd, okno pokaże pełny komunikat.

## Pliki

```
cad/
  fusion/
    BallBalancer/
      BallBalancer.py        # skrypt (menu)
      BallBalancer.manifest
      bb_params.py           # WSZYSTKIE wymiary (odpowiednik params.scad)
      bb_kin.py              # kinematyka odwrotna i polozenia czesci (czysty Python)
      bb_geom.py             # ksztalty czesci
    raport_zakresu.txt       # tworzy opcja 3
  stl/                       # tworzy opcja 5
```

## Jak uruchomić

1. Fusion 360 → **Utilities → Add-Ins → Scripts and Add-Ins** (skrót Shift+S).
2. Zakładka **Scripts** → **+** obok „My Scripts” → wskaż folder `cad/fusion/BallBalancer`.
3. Zaznacz **BallBalancer** → **Run**. Pojawi się menu:

| Opcja | Co robi |
| :--- | :--- |
| **1** | Nowy dokument z całym modelem w pozycji neutralnej (ok. kilkanaście sekund). Zapisz go (Ctrl+S) |
| **2** | Przechyl tacę: `przechył X; przechył Y; zmiana wysokości; kulka x; kulka y` (stopnie, mm). Pokazuje kąty serw, przybliżone µs, skręt popychaczy i pyta o test kolizji |
| **3** | Test zakresu: maksymalny przechył w każdym kierunku, tabela kątów serw, skręt popychaczy, wymiary wydruków względem stołu 220 mm, kolizje przy 0°, 6° i 9° co 60°. Zapisuje `cad/fusion/raport_zakresu.txt` |
| **4** | Kolizje w bieżącej pozycji |
| **5** | Eksport STL do `cad/stl` |

Opcje 2–5 działają na otwartym dokumencie zbudowanym opcją 1. Przechył X > 0 podnosi stronę serwa 1 (tył), tak jak `rx` w [[22 Firmware - Sterowanie]].

> [!tip] Zmiana wymiaru
> Zmieniamy **tylko** `bb_params.py`, potem ponownie opcja 1 (nowy dokument). Stałe `R_BASE`, `L1`, `L2`, `Z_SERVO` muszą być takie same jak w firmware. Model jest w trybie bezpośrednim (bez osi czasu), bo źródłem prawdy jest skrypt, a nie historia w Fusion.

## Co jest w modelu

| Komponent | Szt. w modelu / do druku | Uwagi |
| :--- | :--- | :--- |
| `00_Kupon_Tolerancji` | 1 / 1 | Otwory 2,0/2,05/2,10/2,15, szczeliny 8,2/8,4/8,6. Leży obok stołu |
| `01_Baza_Glowna_HS422` | 1 / 1 | 205 × 215 mm. Trzy ściany z kieszenią 41,0 × 20,2 i otworami pilotowymi ⌀2,2 (48,5 × 10) pod wkręty samogwintujące z kompletu serwa, bez nakrętek, żebra, komora elektroniki 80 × 60 z 4 tulejami pod wkładki (płytka uniwersalna 70 × 50), 4 gniazda stopek, wkładki M3 pod pałąk i konsolę |
| `02_Panel_Konsoli_OLED` | 1 / 1 | Płyta 120 × 62 pod kątem 40°: okno OLED 24 × 13, krzyżak strzałek, DALEJ, enkoder; z boku gniazdo DC ⌀8 i włącznik 13 × 19; listwa z 2 śrubami M3 poza obrysem tacy |
| `03_Taca_Robocza_210mm` | 1 / 1 | Płyta 3 mm, 6 żeber 5 mm (0°, 60°…), **3 widełki wydrukowane razem z tacą** (`pivot_h = 10,5`); 210 × 210 × 19,8 mm, drukowana górą do stołu |
| `03b_Rant_210mm` | 1 / 1 | 2 × 3,5 mm |
| `04_Adapter_Orczyka_24mm` | 3 / 4 | Patrz zmiany niżej |
| `05_Popychacz_60mm` | 3 / 4 | Sworznie co 54,4 mm |
| `05b_Kostka_Kardana` | 6 / 8 | Jak w OpenSCAD |
| `05c_Uchwyt_Testowy` | — / 1 | Te same widełki jako osobny uchwyt, tylko do testu jednej nogi w Etapie 0 |
| `06_Palak_Dolny` | 1 / 1 | Stopa + słupek 20 × 20 do 218 mm, tunel 8 × 8, kanał do gniazda JST-XH, żebra, 2 wkładki M3 z każdej strony |
| `07_Palak_Gorny_Kamera` | 1 / 1 | Tuleja 90 mm ze szczeliną (regulacja 170–210 mm), ramię z tunelem, głowica ⌀60: pierścień LED ⌀50 od spodu, gniazdo modułu OV2640 8,6 × 8,6 z półką i stożkowym otworem na obiektyw (nie obcina pola 120°), kieszeń na płytkę od góry |
| `HS-422`, `Kulka_40mm`, `Pierscien_LED_12x`, `ESP32-S3_CAM` | — / 0 | Modele odniesienia, nie do druku |

## Co CAD zmienił lub ustalił (ważne)

> [!important] 1. Widełki adaptera i uchwytu są pochylone o 23,6°
> Sworzeń w adapterze orczyka i w uchwycie tacy jest **prostopadły do popychacza w pozycji neutralnej** (popychacz jest odchylony od pionu o $\arcsin(24/60)=23{,}6°$). Wtedy obie kostki Kardana leżą na osi popychacza i wymiar $L_2=54{,}4+2\cdot2{,}8=60$ mm jest dokładny. Dzięki temu model z [[06 Kinematyka i zakres ruchu]] i firmware zgadzają się z mechaniką, a góra tacy wychodzi **96,49 mm** (potwierdza 96,5 mm z [[05 Geometria i wymiary]]).
>
> W wersji z [[24 Kod OpenSCAD cięgien]] sworzeń orczyka jest pionowy, a uchwytu poziomy. Wtedy przesunięcia 2,8 mm w kostkach nie leżą na osi popychacza i taca usiądzie niżej. Mój szacunek to ok. 94 mm, **do sprawdzenia**. Jeśli drukujemy części z Fusion, ten problem znika.

> [!important] 2. Orczyk zahaczał o popychacz
> Pierwsza wersja adaptera (jak w OpenSCAD: szeroka nakładka pod oryginalny orczyk) **kolidowała z dolnym mostkiem popychacza przy kącie orczyka poniżej ok. −25°**. To już przy przechyle 6° w najgorszym kierunku. Poprawka: nakładka pod orczyk sięga tylko do 14,6 mm od osi, od strony popychacza ma 0,9 mm ścianki i fazkę. Mostek za szczeliną widełek ma 2,5 mm zamiast 4 mm. Po zmianie test nie pokazuje kolizji w **całym** osiągalnym zakresie (do ±35° orczyka, przechył do 10,2°).

**3. Serwa** leżą na boku, korpus skierowany do środka, orczyk na zewnątrz. Wałek jest 10 mm od końca korpusu, a ucho mocujące 7,9 mm pod górną ścianką. **Obie wartości trzeba zmierzyć** (`SERVO_SHAFT_FROM_END`, `SERVO_FLANGE_FROM_TOP`), bo od nich zależy położenie ściany z kieszenią.

**4. Konsola stoi przed bazą** (front 150 mm od środka), a nie pod tacą. Pod przednią krawędzią tacy jest korpus serwa 2, więc konsola by się nie zmieściła. Konsola ma maksymalnie 52 mm wysokości, a najniższy punkt tacy przy 10° to 73 mm.

**5. Pałąk:** słupek dolny ma 218 mm (mieści się na stole 220 mm także na leżąco). Wkładki M3 są na wysokości 190 i 210 mm. Dla każdej wysokości kamery 170–210 mm obie śruby trafiają w szczelinę, a tuleja zachodzi na słupek co najmniej 37 mm.

**6. Orczyk przy −35°** schodzi do 3,3 mm nad blatem. Dlatego baza nie ma podłogi w płaszczyźnie orczyków (ramiona bazy są tylko po stronie korpusu serwa), a stopa pałąka zaczyna się dalej niż zasięg orczyka serwa 1.

## Uproszczenia (2026-10-21)

Dwa uproszczenia bez straty jakości (wybrane z czterech propozycji):

| Było | Jest | Zysk |
| :--- | :--- | :--- |
| 3 uchwyty przykręcane do tacy (6 × M3 + nakrętki, łby pod folią) | Widełki drukowane razem z tacą | 3 wydruki i 12 elementów złącznych mniej, promień 90 mm i wysokość osi bez błędu montażu. Ryzyko: złamane widełki = nowa taca |
| Konwerter poziomów 74AHCT125 dla WS2812B | Dioda 1N4001 w zasilaniu pierścienia | Jeden element zamiast układu scalonego, ten sam efekt ([[13 Zasilanie i elektronika]]) |

Bez zmian (świadomie): dwa ESP32, regulacja wysokości kamery, osobny rant, osobna konsola, kostki Kardana (łączniki kulowe zostają planem B), strzałki w konsoli.

## Przegląd montażu (2026-10-21)

Sprawdziłem, czy całość da się złożyć i czy wszystko działa razem, nie tylko czy części się nie przenikają.

| Sprawdzenie | Wynik |
| :--- | :--- |
| Ruch tacy w całym osiągalnym zakresie (do 10,2°, orczyk ±35°), co 15° kierunku | brak kolizji |
| Wsuwanie każdego serwa przez okno w ścianie (od strony orczyka) | bez kolizji |
| Śruby stopy pałąka i konsoli: dostęp wkrętakiem pionowo z góry przy założonej tacy | OK (po poprawce) |
| Regulacja kamery 170–210 mm: obie śruby w szczelinie, tuleja zachodzi ≥ 37 mm | OK |
| Każdy wydruk to jedna bryła i mieści się na stole 220 mm | OK |

Poprawki z przeglądu:
- **Śruby konsoli były pod tacą** (promień 89 mm), więc nie dało się ich wkręcić. Przeniesione na skrzydełka bazy na promień 111 mm.
- **Śruby stopy pałąka** też były pod krawędzią tacy. Przeniesione na promień ≥ 110 mm.
- **Serwa przykręcamy wkrętami z kompletu** w otwory pilotowe ⌀2,2. Nakrętki od tyłu ściany zahaczałyby o żebro.
- **Kamera:** wcześniej moduł OV2640 nie miał w głowicy oparcia (otwór ⌀16 na wylot). Teraz ma gniazdo z półką, a otwór rozszerza się stożkowo, żeby nie obcinał pola widzenia 120°.
- **Prostszy kod:** wszystkie pozycje śrub i wymiary głowicy są w `bb_params.py`, a nie wpisane w kodzie części.

## Wyniki testu (opcja 3)

| Wielkość | Wynik | Zgodność z notatkami |
| :--- | :--- | :--- |
| Zakres przechyłu przy ±35° orczyka | 7,9° … 10,2° | jak w [[06 Kinematyka i zakres ruchu]] |
| Kąty serw przy 3° / 6° / 9° w stronę serwa 1 | +11,0/−5,7 · +21,7/−11,7 · +32,7/−18,0 | jak w [[06 Kinematyka i zakres ruchu]] |
| Skręt popychacza przy 2/4/6/8° | 0,81 / 1,65 / 2,52 / 3,42° | ok. jak w [[07 Cięgna i przeguby]] (0,8/1,6/2,4/3,2) |
| Odchyłka modelu punktowego od kostek przy 6° | do 0,26 mm | pomijalna |
| Kolizje 0°, 6°, 9° | brak | — |

## Do zmierzenia przed drukiem

Wszystko w `bb_params.py`, oznaczone `ZMIERZYC`:
- otwory w oryginalnym orczyku HS-422 (`HORN_HOLES`, teraz 8,0 i 12,5 mm),
- położenie wałka i uszu serwa (`SERVO_SHAFT_FROM_END`, `SERVO_FLANGE_FROM_TOP`),
- wysokość wałka serwa nad korpusem (`HORN_PLANE`),
- wymiary płytki ESP32-S3 CAM (`CAM_BOARD`), modułu kamery i obiektywu (`CAM_MODULE`, `CAM_LENS_D`) oraz pierścienia LED (`LED_RING_OD`),
- tolerancje z kuponu (`M2_HOLE`, `FORK_GAP`), jak w [[07 Cięgna i przeguby]].

## Ograniczenia

- Śruby, nakrętki, wkładki, kable i elektronika (poza płytką kamery) nie są modelowane, są tylko otwory.
- Popychacz w modelu ma sworznie równoległe; rzeczywisty skręt (tabela wyżej) jest dzielony po połowie na oba końce, dlatego test kolizji pokazuje stan „po sprężystym skręcie”. Klinowanie sprawdzamy na wydruku ([[19 Plan prac i testy]], Etap 0).
- Orientację wydruku ustawiamy w slicerze: tacę górną płaszczyzną do stołu, konsolę licem do stołu ([[16 Elementy do druku]]).
