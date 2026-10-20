---
title: Ball Balancer - Uwagi i ulepszenia
tags:
  - projekt
  - ball-balancer
  - przeglad
  - ryzyka
created: 2026-10-20
---

# 🔍 Ball Balancer: przegląd dokumentacji, ryzyka i ulepszenia

Wróć do: [[Projekt Ball Balancer]]. Liczby i wzory: [[Ball Balancer - Obliczenia]].

> [!abstract] Wniosek ogólny
> Koncepcja (dwa MCU, kamera nad tacą, 3 serwa co 120°, praca offline) jest dobra i wykonalna. Wymiary i kinematyka z v1 się zgadzają. Znalazłem **kilka rzeczy, które by się zemściły dopiero na gotowej konstrukcji**: rozdzielczość i dystorsja kamery, nastawy PID, zasilanie, poziomy logiczne i piny oraz przeguby. Wszystkie dają się naprawić tanio i przed zakupem.

Priorytety: 🔴 napraw przed zakupem/drukiem, 🟠 ważne przed pierwszym uruchomieniem, 🟢 usprawnienia.

---

## 🔴 Krytyczne

### 1. Kamera: rozdzielczość i dystorsja
- Przy 120° i QQVGA piksel to **2,0–2,6 mm** zależnie od miejsca w kadrze, a kulka ma tylko ok. 17 px. Skala zmienia się o 28% od środka do krawędzi, więc surowe piksele dają zniekształconą pozycję.
- **Zrób:** (a) mapowanie piksel → mm z modelu obiektywu (wzór w [[Ball Balancer - Obliczenia]] sekcja 4), (b) centroid z wagami jasności (subpiksel), (c) test QVGA 320×240, jeśli FPS $\ge 50$, (d) kalibracja w UI (ekran 5).
- **Zablokuj automatykę** OV2640: `aec`, `agc`, `awb` wyłączone, stała ekspozycja $\le 5$ ms. Auto-ekspozycja zmienia czas klatki (FPS) i jasność, co psuje próg.
- **Oświetlenie:** pierścień LED nad kulką daje odblask na gładkiej kulce. Użyj matowej kulki i cienkiej białej kartki jako dyfuzora, jasność ok. 25%.
- **120° jest uzasadnione:** wbudowany obiektyw ok. 65° nie obejmie tacy z 195 mm (widzi ok. 138 mm krótszego boku).

### 2. Nastawy PID
v1 nie podaje nastaw. Typowe „szybkie" nastawy (pasmo 4 rad/s) przy opóźnieniach serwa i kamery mają marżę fazową poniżej 20° i kulka będzie oscylować. Policzone nastawy startowe (pasmo ok. 2,6 rad/s, marża ok. 40°) są w [[Ball Balancer - Obliczenia#5. Regulator PID]].

### 3. Zasilanie 5 V
- Prąd szczytowy ok. 2,3–3,3 A. **Zasilacz 3 A to za mało, bierz 4 A.**
- Moment 4,1 kg·cm dotyczy HS-422 przy **6 V**. Przy 5 V jest ok. 3,3 kg·cm. Zapas i tak jest 25–30-krotny (potrzebne ok. 0,12 kg·cm), więc zostajemy przy 5 V.
- Serwa analogowe powodują zapady napięcia. Dodaj kondensator $1000\,\mu$F przy serwach, $100\,\mu$F i $100$ nF przy obu ESP32, zasilanie w gwiazdę z jednego punktu, wspólna masa.

### 4. Poziomy logiczne i piny
- **KY-040** ma pull-upy do pinu `+`. Zasilany z 5 V podaje 5 V na GPIO 3,3 V ESP32. Zasilaj z **3,3 V**.
- **WS2812B** przy zasilaniu 5 V wymaga logicznej „1" $\ge 0{,}7\cdot V_{DD}=3{,}5$ V, a ESP32-S3 daje 3,3 V. Działa „czasem". Użyj 74AHCT125 albo diody szeregowej w zasilaniu pierścienia (ok. 4,3 V).
- **GPIO 16/17 na ESP32** działają tylko w module WROOM. W WROVER zajmuje je PSRAM. Sprawdź, jaki masz moduł.
- **ESP32-S3 N16R8:** GPIO 35–37 są zajęte przez octal PSRAM, a część pinów przez kamerę. Zaplanuj UART i dane LED według pinoutu **swojej** płytki.
- **GPIO 15** (enkoder SW) to pin strappingowy: wciśnięcie podczas startu zmienia zachowanie logów boot. Nieszkodliwe, ale warto wiedzieć.

---

## 🟠 Ważne

### 5. Przeguby: kostka Kardana zamiast kulowego
Model kinematyczny zakłada przeguby kulowe, a konstrukcja ma przeguby krzyżakowe (U) na obu końcach cięgna. Obliczony skręt cięgna wymagany przez to rozwiązanie wynosi ok. 1,6° przy przechyle 4° i ok. 3,2° przy 8° (tabela w [[Ball Balancer - Obliczenia]], sekcja 2). To tyle, ile wynosi cały luz kostki, więc przy dużych wychyleniach konstrukcja może się klinować lub pracować z tarciem.
- **Zrób:** limit programowy $\pm6^\circ$; wydrukuj najpierw 1 zestaw cięgien i sprawdź płynność ruchu w całym zakresie.
- **Plan B:** gotowe łączniki kulowe M3 (RC) na górze lub na obu końcach.
- Luz kostki 0,4 mm sprzyja cyklom granicznym. Jeśli wydruk ma luz większy niż 0,3 mm, zmniejsz `fork_gap` do 8,2 mm.

### 6. $Z_{neutral}$ i `pivot_h`
Oś górnego przegubu przy $\alpha=0$ leży na **83,0 mm**. Jeśli `pivot_h = 10.5` liczy się od spodu tacy, górna powierzchnia tacy wypada na ok. **96,5 mm**, a nie 92 mm. To nie błąd krytyczny, ale należy raz ustalić wartość w CAD i pozostałe wymiary wyliczyć z niej, w tym wysokość kamery.

### 7. Etykiety serw 2 i 3
Przy widoku z góry, serwie 1 z tyłu ($\psi=90^\circ$), x w prawo: $\psi=210^\circ$ leży **po lewej** z przodu, a $\psi=330^\circ$ po prawej. v1 ma je odwrotnie. Wpływa to tylko na podpisy i okablowanie, ale warto to ujednolicić, żeby uniknąć odwrócenia osi w sterowaniu.

### 8. Ramka UART
5-bajtowa ramka z nagłówkiem `0xFF` nie ma sumy kontrolnej, flagi „kulka znaleziona" ani numeru ramki. Przy zakłóceniu lub zgubionym bajcie ramki przesuwają się. Nowa ramka (9 B): `AA 55 seq flags xH xL yH yL xor`. Pozycja w 1/16 piksela. Opis w [[Ball Balancer - Firmware]].

### 9. Częstotliwość pętli i serwa analogowe
HS-422 jest serwem analogowym i dobrze przyjmuje 50 Hz. Kamera podaje 50–60 FPS. Zmiany częstsze niż co 20 ms nie dotrą do serwa, a jitter wzrośnie. **Zrób:** stała pętla 50 Hz, użyj najnowszej próbki z kamery, PWM z LEDC (sprzętowy, więc zapis do NVS nie powoduje jitteru).

### 10. Bezpieczeństwo i start
- Piny serw przy starcie ESP32 są pływające: serwa mogą szarpnąć. Podłączaj PWM po ustawieniu pozycji, dodaj rezystory 10 kΩ do GND na liniach sygnałowych.
- Rampa startowa do pozycji neutralnej (1–2 s). Przy utracie kamery (> 100 ms) lub kulki (> 0,5 s) płynny powrót do poziomu, bez gwałtownych ruchów.
- Przycisk „STOP" (np. długie DALEJ): poziomowanie tacy.

### 11. Śruby M2×16
Kostka 8 mm + dwie ścianki widełek po 2,8 mm = 13,6–14 mm, a 16 mm śruby zostawia w nakrętce 1–2 zwoje. Użyj **M2×18–20** i nakrętek samohamownych. Nakrętki muszą utrzymać się przy drganiach, a luz w śrubie to luz w całym układzie.

---

## 🟢 Usprawnienia

### Mechanika
- **Sztywność C-Arm:** kamera mierzy względem bazy, więc drganie pałąka wygląda jak ruch kulki. Drukuj z 4 obrysami i grubszą ścianką, żebro na podstawie, w razie potrzeby wzmocnij prętem węglowym lub aluminiowym 6–8 mm w osi tunelu kablowego.
- **Płaskość tacy:** duża cienka płyta z PLA ma tendencję do wyginania się (warping). Drukuj na szkle/PEI z brimem, sprawdź płaskość liniałem (cel: $\le0{,}3$ mm). Ewentualnie 4 mm zamiast 3 mm.
- **Folia:** czarna mata zmniejsza odblask. Białą lub pomarańczową kulkę wybierz na ciemnym tle (kontrast), kulka ciemna by zniknęła.
- **Rant:** 2×3,5 mm nie zatrzyma kulki lecącej z prędkością ok. 0,5 m/s. Warto go traktować jako ograniczenie wizualne, a nie fizyczne.
- **Kolizje:** zweryfikuj w CAD przy przechyle 9° kolizję tacy z konsolą i słupkiem pałąka (krawędź tacy opada lub unosi się o 16 mm).

### Elektronika i firmware
- **Filtr α-β lub Kalman** dla pozycji i prędkości. Pochodna z surowych pikseli jest zaszumiona.
- **Anty-windup** całki i martwa strefa serw (HS-422: 8 µs).
- **Enkoder:** użyj PCNT (`ESP32Encoder`) albo maszyny stanów, a nie przerwań na surowych zboczach. Mechaniczny KY-040 odbija.
- **NVS:** zapisuj tylko na wyraźne polecenie z UI (flash ma ograniczoną liczbę zapisów). Dodaj wersję struktury i sumę kontrolną.
- **Wspólny stan między rdzeniami:** kolejka FreeRTOS lub kopia struktury pod `portMUX` zamiast zmiennych `volatile`.
- **Telemetria:** na etapie strojenia wysyłaj pozycję, uchyb i przechył po USB (Serial Plotter, 50 Hz). Tryb standalone nie wyklucza logowania na biurku.
- **Kalibracja kamery w UI:** środek obrazu, obrót/odbicie osi (`swapXY`, `invX`, `invY`), skala $f_{px}$.

### Funkcje na później
- Trajektorie: okrąg, ósemka, kwadrat, Lissajous z feed-forward $\theta_{ff}=a/K$.
- Auto-strojenie przekaźnikowe (relay feedback).
- Wykrywanie utraty kulki z komunikatem na OLED i animacją LED.
- Profile nastaw per kulka (pingpong, golfowa) w NVS.

---

## Tabela zmian względem v1

| #   | Zmiana                                                      | Wpływ                     |
| :-- | :---------------------------------------------------------- | :------------------------ |
| 1   | Korekcja dystorsji + centroid subpikselowy, blokada AEC/AGC | dokładniejsza pozycja     |
| 2   | Nastawy PID i filtr α-β z obliczeń                          | stabilna pętla od startu  |
| 3   | Zasilacz 4 A, rozdzielone zasilanie, kondensatory           | brak resetów              |
| 4   | KY-040 z 3,3 V, konwerter poziomów dla WS2812B              | poprawne poziomy logiczne |
| 5   | Limit przechyłu $\pm6^\circ$, test cięgna, plan B kule      | mniej klinowania          |
| 6   | Przeliczenie $Z_{neutral}$ z modelu                         | spójne wymiary            |
| 7   | Poprawione etykiety serw 2/3                                | zgodne osie               |
| 8   | Nowa ramka UART (9 B, XOR, flagi)                           | odporność na zakłócenia   |
| 9   | Stałe 50 Hz zsynchronizowane z PWM                          | mniejszy jitter           |
| 10  | Rampa startowa, failsafe, rezystory 10 kΩ                   | bezpieczeństwo            |
| 11  | Śruby M2×18–20, nakrętki samohamowne                        | trwałe przeguby           |
| 12  | Budżet 130–140 zł (z dodatkami)                             | realne koszty             |
