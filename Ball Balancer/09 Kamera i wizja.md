---
title: Kamera i wizja
tags:
  - ball-balancer
  - kamera
  - obliczenia
created: 2026-10-20
---

# 09. Kamera i wizja

Poprzednia: [[08 Serwa i momenty]]. Dalej: [[10 Dynamika kulki]]. Powrót: [[Projekt Ball Balancer]]. Kod: [[21 Firmware - Kamera]].

## W skrócie

Kamera jest „oczami" układu, więc od niej zależy dokładność całego balansowania. Wybraliśmy obiektyw 120°, bo tylko taki obejmie całą tacę z 195 mm. Ma to swoją cenę: obraz jest zniekształcony i piksel oznacza ok. 2 mm. Poniżej pokazuję obliczenia i co z nimi robimy.

> [!info] Założenia
> Obliczenia zakładają obiektyw o kącie 120° po przekątnej i rzut równoodległy ($r=f\theta$), czyli typowy model dla szerokiego kąta. **Prawdziwy kąt widzenia tanich modułów bywa mniejszy**, dlatego wszystko sprawdzamy w Etapie 1 ([[19 Plan prac i testy]]).

## Dlaczego obiektyw 120°

Kamera widzi prostokąt 4:3. Żeby zobaczyć całą okrągłą tacę, krótszy bok obrazu musi obejmować ok. 210 mm.

| Obiektyw (kąt po przekątnej) | Co widzi krótszy bok z 195 mm | Czy obejmuje tacę 210 mm?  |
| :--------------------------- | ----------------------------: | :------------------------- |
| 65° (standardowy w zestawie) |                        138 mm | **Nie**                    |
| 90°                          |                        199 mm | Prawie                     |
| **120°**                     |                        283 mm | **Tak, z zapasem**         |
| 160°                         |                        433 mm | Tak, ale za zniekształcony |

Standardowy obiektyw 65° musiałby być ok. 300 mm nad tacą. Obiektyw 120° pozwala zostać przy 195 mm.

## Jak dokładny jest pomiar

W trybie QQVGA obraz ma $160\times120$ pikseli. Dla przekątnej 100 px (połowa) i kąta 60° (połowa 120°):

$$f_{px}=\frac{100\text{ px}}{1{,}047\text{ rad}}\approx95{,}5\text{ px/rad}$$

Skala w środku obrazu, na wysokości $H=195$ mm:

$$s_0=\frac{H}{f_{px}}=\frac{195}{95{,}5}=2{,}04\text{ mm/px}$$

Na krawędzi tacy (kąt $\theta=\arctan(105/195)=28{,}3^\circ$) skala rośnie:

$$s_{edge}=\frac{H}{f_{px}\cos^2\theta}\approx2{,}6\text{ mm/px}$$

Skala zmienia się o ok. 28% między środkiem a brzegiem. Bez korekcji pozycja byłaby przekłamana: ta sama odległość w pikselach oznaczałaby inną odległość w milimetrach zależnie od miejsca.

### Jak to naprawiamy

Przeliczamy piksele na milimetry wzorem:

$$r_{mm}=H\tan\!\left(\frac{r_{px}}{f_{px}}\right),\qquad x_{mm}=(x-x_c)\frac{r_{mm}}{r_{px}},\quad y_{mm}=(y-y_c)\frac{r_{mm}}{r_{px}}$$

gdzie $(x_c,y_c)$ to środek obrazu, $r_{px}$ to odległość od środka w pikselach. $f_{px}$ i środek wyznacza kalibracja ([[18 Kalibracja i uruchomienie]]).

> [!tip] Plan awaryjny, jeśli model nie pasuje
> Prawdziwy obiektyw może odbiegać od modelu równoodległego. Jeśli po kalibracji okręgi z arkusza nie zgadzają się z modelem (błąd większy niż ok. 1 mm), zamiast wzoru z tangensem używamy prostego wielomianu $r_{mm}=c_1\,r_{px}+c_3\,r_{px}^3$, którego dwa współczynniki dopasowujemy metodą najmniejszych kwadratów do czterech znanych okręgów arkusza (25, 50, 75, 100 mm). Jest też tańszy w obliczeniach, bo nie wymaga tangensa.

### Dokładność w praktyce

Kulka ma średnicę 40 mm, czyli ok. 17 px. Środek liczymy jako **średnią ważoną jasnością** (centroid subpikselowy), co daje dokładność rzędu 0,2–0,3 piksela, czyli około **±0,5–0,8 mm**. Do balansowania to wystarcza, ale pozycji **nie wolno** różniczkować wprost, bo pochodna z takiego szumu jest bezużyteczna. Dlatego prędkość liczy filtr α-β ([[11 Regulator PID]]).

## Wysokość kamery

Czy lepiej obniżyć kamerę? Policzone dla QQVGA, przechyłu 6° (krawędź tacy jest wtedy bliżej kamery, dlatego skala na brzegu jest nieco mniejsza niż 2,6 mm/px z wyliczenia dla płaskiej tacy) i krawędzi kulki na promieniu ok. 105 mm:

| Wysokość $H$ | mm/px w środku | mm/px na brzegu | Zapas kąta do krawędzi kadru |
| :--- | ---: | ---: | ---: |
| 170 mm | 1,78 | 2,36 | 2,0° |
| 185 mm | 1,94 | 2,46 | 4,4° |
| **195 mm** | 2,04 | 2,53 | 5,8° |
| 210 mm | 2,20 | 2,64 | 7,7° |

> [!success] Decyzja: 195 mm nominalnie, ale regulowana 170–210 mm
> Obniżenie z 195 do 170 mm poprawia skalę tylko o ok. 10%, a zapas kadru spada do ok. 2°. Jeśli rzeczywisty kąt obiektywu okaże się mniejszy niż 120°, kula na brzegu wypadnie z kadru. Dlatego zostajemy przy 195 mm, a w słupku pałąka robimy szczelinę z M3, żeby podnieść lub obniżyć głowicę po teście z prawdziwym obiektywem.

## Czy QVGA ($320\times240$) pomoże

Dwukrotnie więcej pikseli na bok to skala ok. 1,0–1,3 mm/px i dokładność subpikselowa ok. ±0,3 mm. Procesor ESP32-S3 (240 MHz) przeliczy 77 tys. pikseli w ok. 1–3 ms (oszacowanie). Nie wiemy jeszcze, czy kamera da w tym trybie 50 FPS. **Zaczynamy od QQVGA, a QVGA sprawdzamy w Etapie 1.** Wymagamy co najmniej 45 FPS.

## Ustawienia obrazu

- **Automatyka wyłączona.** Wyłączamy automatyczną ekspozycję (`aec`), wzmocnienie (`agc`) i balans bieli (`awb`). Automatyka zmienia czas klatki i jasność, a wtedy próg wykrywania kulki „pływa".
- **Ekspozycja krótka**, $\le 5$ ms. Kulka z prędkością 0,3 m/s przesunie się w tym czasie o ok. 1,5 mm, co jest akceptowalnym rozmyciem.
- **Obraz w skali szarości** (`PIXFORMAT_GRAYSCALE`). Nie potrzebujemy koloru, a surowy obraz oszczędza czas bez kompresji JPEG.

## Oświetlenie i kolor kulki

- **Pierścień LED** wokół obiektywu oświetla tacę równo, bez cieni. Jasność ok. 25%, żeby uniknąć odblasku.
- **Dyfuzor** (cienka biała kartka) rozprasza światło. Bez niego gładka kulka odbija punktowy błysk i środek plamy „ucieka".
- **Kulka matowa, jasna** (biała lub pomarańczowa) na **czarnej, matowej** tacy. Kontrast jest największy, a odblask najmniejszy. Ciemna kulka zniknęłaby na czarnej folii.
- **Migotanie LED.** Jasność WS2812B jest regulowana PWM-em o częstotliwości ok. 400 Hz (okres ok. 2,5 ms; wartość przybliżona). Przy krótkiej ekspozycji kolejne klatki mogą się różnić jasnością. Dlatego ekspozycja ma być **wielokrotnością okresu PWM** (np. 5 ms), a jasności i animacji LED **nie zmieniamy w trakcie pomiaru**.

## Czego nie ruszamy

Obszar poza tacą (rant, pałąk) maskujemy w oprogramowaniu, żeby nie był brany za kulkę ([[21 Firmware - Kamera]]).
