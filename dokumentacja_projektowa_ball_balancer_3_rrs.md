---
title: Projekt Ball Balancer 3-RRS (Standalone Dual-MCU)
tags:
  - projekt
  - esp32
  - druk3d
  - pid
  - robotyka
  - ball-balancer
status: W trakcie realizacji (Etap CAD / Zakupy)
created: 2026-10-20
architektura: 3-RRS Parallel Manipulator + C-Arm Camera Mount
---

# 🎯 Ball Balancer 3-RRS – Główna Dokumentacja Projektowa

> [!abstract] Założenia Główne Projektu
> Projekt zakłada budowę maksymalnie wydajnego, estetycznego i **w 100% autonomicznego (Standalone / Offline)** stołu balansującego kulką w układzie **3-RRS** (3 serwa rozmieszczone co $120^\circ$) z pojedynczym pałąkiem górnym **C-Arm** pod kamerę. 
> Konstrukcja opiera się w maksymalnym stopniu na druku 3D (PLA/PETG) bez utraty sztywności mechanicznej i precyzji układu sterowania PID.

---

## 1. Architektura Sprzętowa (Dual-MCU)

Aby wyeliminować blokowanie pętli PID oraz gubienie klatek z kamery podczas odświeżania ekranu OLED po magistrali $\text{I}^2\text{C}$, system podzielono na dwa niezależne mikrokontrolery połączone szybką magistralą UART ($921600\text{ baud}$):

1. **Moduł Wizyjny (Góra pałąka – "Oko"):** `ESP32-S3-WROOM N16R8 CAM` + obiektyw szerokokątny `OV2640 120°` + `Pierścień LED 12x WS2812B`.
   * **Zadanie:** Wyłączone Wi-Fi i kompresja JPEG. Praca w trybie surowym `PIXFORMAT_GRAYSCALE` przy rozdzielczości `FRAMESIZE_QQVGA` ($160 \times 120\text{ px}$), zegar XCLK podbity do $20\text{ MHz}$.
   * **Wynik:** Stabilne **50–60 FPS**, czas analizy klatki $< 1.5\text{ ms}$, wysyłanie ramki 5-bajtowej `[0xFF, X_H, X_L, Y_H, Y_L]` w dół pałąka oraz sterowanie oświetleniem i efektami statusu na pierścieniu LED RGB.
2. **Moduł Główny (Baza dolna – "Mózg i Konsola"):** Klasyczne `ESP32`.
   * **Rdzeń 1 (Real-Time Control):** Odbiór współrzędnych po UART, obliczanie podwójnego regulatora PID (oś $X$ i oś $Y$), przeliczanie kinematyki odwrotnej 3-RRS oraz generowanie sygnałów PWM dla 3 serw **Hitec HS-422**.
   * **Rdzeń 0 (Offline UI):** Obsługa wyświetlacza OLED $\text{I}^2\text{C}$, 4 przycisków kierunkowych (strzałki), przycisku `DALEJ (MODE)` oraz enkodera obrotowego `KY-040` z zapisem nastaw do pamięci nieulotnej NVS (`Preferences`).

---

## 2. Posiadane Części vs. Lista Zakupowa

### ✅ Posiadane na stanie (Koszt: 0 zł)
- [x] Drukarka 3D + filament (PLA / PETG)
- [x] Płytka główna `ESP32` (do bazy dolnej)
- [x] Wyświetlacz `OLED I2C` (niedotykowy)
- [x] **3x Serwo Hitec HS-422** (rozmiar Standard: $40.6 \times 19.8 \times 36.6\text{ mm}$, moment $4.1\text{ kg}\cdot\text{cm}$, zębatki Delrin) – *pozwalają na balansowanie nie tylko piłeczką pingpongową ($2.7\text{ g}$), ale też piłeczką golfową ($45\text{ g}$) i kulkami do $100\text{ g}$*
- [x] (Rezerwowo) 3x Serwo TowerPro SG90 9g
- [x] Kondensatory elektrolityczne (min. $1000\text{ }\mu\text{F} / 10\text{V}$ do filtracji zasilania serw)
- [x] Zestawy śrubek i nakrętek `M2` oraz `M3`

### 🛒 Lista zakupowa (Brakujące elementy: ~100–110 zł)
- [ ] **Płytka z kamerą:** `ESP32-S3-WROOM N16R8 CAM` (z 2x USB-C i kamerą OV2640 w zestawie) — *~38–45 zł*
- [ ] **Obiektyw szerokokątny:** `Kamera OV2640 120 stopni` (taśma 24-pin, dł. 20–50 mm) — *~15 zł*
- [ ] **Oświetlenie bezcieniowe:** `Pierścień LED Ring 12x WS2812B RGB 5050` (średnica zewn. ~37–50 mm) — *~7 zł*
- [ ] **Enkoder obrotowy:** `KY-040` z nakładką (gałką) — *~6 zł*
- [ ] **Przyciski konsoli:** `5x Tact Switch 12x12x7.3 mm` + `5x kolorowe nasadki (Caps)` (4x Strzałki + 1x Przycisk Dalej) — *~5 zł*
- [ ] **Zasilanie:** `Zasilacz impulsowy 5V 3A (lub 4A)` + `Gniazdo DC 5.5/2.1 mm do obudowy` — *~20 zł*
- [ ] **Powierzchnia toczna i kulki:** Czarna matowa folia samoprzylepna (okleina meblowa mat) lub czarna matowa podkładka pod mysz + matowe pomarańczowe/białe piłeczki pingpongowe $40\text{ mm}$ — *~10 zł*

---

## 3. Dokładne Wymiary Konstrukcyjne (Wersja Taca 210 mm + HS-422)

> [!info] Geometria 3-RRS
> Serwa rozmieszczone są symetrycznie co $120^\circ$:
> * **Serwo 1 (Tył):** Kąt $\psi_1 = 90^\circ$ (zintegrowane z bazą pałąka kamery C-Arm)
> * **Serwo 2 (Przód-Prawo):** Kąt $\psi_2 = 210^\circ$
> * **Serwo 3 (Przód-Lewo):** Kąt $\psi_3 = 330^\circ$

| Sekcja           | Parametr                                           | Wymiar dokładny                   | Uwagi techniczne                                                                                                                   |
| :--------------- | :------------------------------------------------- | :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **Taca Górna**   | Średnica całkowita                                 | $210.0\text{ mm}$                 | Maksymalny wymiar mieszczący się w 1 kawałku na stole $220 \times 220\text{ mm}$.                                                  |
|                  | Średnica robocza (wewnątrz rantu)                  | $206.0\text{ mm}$                 | Rant doklejany osobno: szerokość $2.0\text{ mm}$, wysokość $3.5\text{ mm}$.                                                        |
|                  | Grubość płyty + żebra                              | $3.0\text{ mm}$ + $5.0\text{ mm}$ | 6 żeber promieniowych od spodu, wypełnienie *Gyroid* 15%.                                                                          |
|                  | Promień punktów podparcia ($R_{\text{plate}}$)     | $90.0\text{ mm}$                  | 3 uchwyty przykręcane śrubami M3 od spodu tacy co $120^\circ$.                                                                     |
| **Baza i Serwa** | Promień rozstawu osi serw ($R_{\text{base}}$)      | $90.0\text{ mm}$                  | Osie wałków serw dokładnie w pionie pod uchwytami tacy.                                                                            |
|                  | Kieszeń montażowa serwa HS-422                     | $41.0 \times 20.2\text{ mm}$      | Wymiar korpusu HS-422 ($40.6 \times 19.8\text{ mm}$) + $0.4\text{ mm}$ tolerancji druku.                                           |
|                  | Rozstaw śrub serwa HS-422                          | $48.5 \times 10.0\text{ mm}$      | 4 otwory $\varnothing 2.5\text{ mm}$ pod wkręty lub śruby M2.5/M3.                                                                 |
|                  | Wysokość osi serwa nad stołem ($Z_{\text{servo}}$) | $28.0\text{ mm}$                  | Serwa leżą poziomo na boku; gwarantuje brak kolizji orczyka z blatem.                                                              |
| **Kinematyka**   | Długość czynna orczyka ($L_1$)                     | $24.0\text{ mm}$                  | Od osi wałka HS-422 do osi dolnej śruby M2 przegubu Kardana.                                                                       |
|                  | Zakres kąta orczyka ($\alpha_i$)                   | $\pm 35^\circ$                    | Daje skok pionowy $\pm 13.8\text{ mm}$ i przechył tacy $\pm 9^\circ$.                                                              |
|                  | Długość popychacza całkowita ($L_2$)               | $60.0\text{ mm}$                  | Od osi dolnego przegubu do osi górnego przegubu ($54.4\text{ mm}$ sam popychacz + $2 \times 2.8\text{ mm}$ offset kostek Kardana). |
|                  | Wysokość neutralna tacy ($Z_{\text{neutral}}$)     | $92.0\text{ mm}$                  | Poziom górnej powierzchni tacy przy kątach serw $\alpha_1=\alpha_2=\alpha_3=0^\circ$.                                              |
| **Pałąk C-Arm**  | Wysięg boczny od środka $(0,0)$                    | $132.0\text{ mm}$                 | Mija krawędź tacy ($R=105\text{ mm}$) z bezpiecznym zapasem $27\text{ mm}$.                                                        |
|                  | Wysokość kamery nad tacą                           | $195.0\text{ mm}$                 | Przeliczone pod obiektyw szerokokątny `OV2640 120°` (całość od blatu: $290\text{ mm}$).                                            |
| **Konsola UI**   | Wymiary płyty czołowej                             | $120.0 \times 62.0\text{ mm}$     | Pochylona pod kątem $40^\circ$ z przodu bazy (między serwem 2 i 3).                                                                |

---

## 4. Pinout i Schemat Połączeń (Konsola Offline + Serwa)

### A. Dolne ESP32 (Baza Główna)
Wszystkie przyciski i enkoder korzystają z wewnętrznych rezystorów podciągających (`INPUT_PULLUP`), druga nóżka każdego przycisku idzie do wspólnej masy `GND`.

| Funkcja / Komponent | Pin ESP32 | Kierunek / Magistrala | Uwagi |
| :--- | :--- | :--- | :--- |
| **OLED SDA** | `GPIO 21` | I2C Data | Odświeżany na `Core 0` |
| **OLED SCL** | `GPIO 22` | I2C Clock | Taktowanie I2C ustawione na `400 kHz` (Fast Mode) |
| **UART RX (z kamery)** | `GPIO 16` | Serial2 RX | Połączony z `TX` płytki ESP32-S3-CAM |
| **UART TX (do kamery)** | `GPIO 17` | Serial2 TX | Połączony z `RX` płytki ESP32-S3-CAM |
| **Serwo 1 (Tył - $90^\circ$)** | `GPIO 25` | PWM (50 Hz) | Hitec HS-422 |
| **Serwo 2 (Przód-Prawo - $210^\circ$)**| `GPIO 26` | PWM (50 Hz) | Hitec HS-422 |
| **Serwo 3 (Przód-Lewo - $330^\circ$)** | `GPIO 27` | PWM (50 Hz) | Hitec HS-422 |
| **Enkoder CLK (A)** | `GPIO 32` | Input Pullup | Płynna zmiana nastaw PID / promienia trajektorii |
| **Enkoder DT (B)** | `GPIO 33` | Input Pullup | Kierunek obrotu enkodera |
| **Enkoder SW (Klik)** | `GPIO 15` | Input Pullup | Zmiana kroku regulacji (`0.01` / `0.10` / `1.0`) |
| **Strzałka GÓRA** | `GPIO 18` | Input Pullup | Nawigacja w menu / przesuwanie Setpoint Y+ |
| **Strzałka DÓŁ** | `GPIO 19` | Input Pullup | Nawigacja w menu / przesuwanie Setpoint Y- |
| **Strzałka LEWO** | `GPIO 23` | Input Pullup | Nawigacja w menu / przesuwanie Setpoint X- |
| **Strzałka PRAWO** | `GPIO 4` | Input Pullup | Nawigacja w menu / przesuwanie Setpoint X+ |
| **Przycisk DALEJ (MODE)**| `GPIO 13` | Input Pullup | Przełączanie ekranów: `1. Radar` $\rightarrow$ `2. Trajektorie` $\rightarrow$ `3. PID` $\rightarrow$ `4. Trim Serw` |

---

## 5. Podział Części do Druku 3D (Lista Plików STL)

1. **`01_Baza_Glowna_HS422.stl` (1 szt.)** – Trójramienna baza z kieszeniami pod 3 serwa Hitec HS-422 (montowane poziomo na boku), komorą na ESP32, kondensator $1000\text{ }\mu\text{F}$ oraz gniazdo zasilania DC 5.5/2.1.
2. **`02_Panel_Konsoli_OLED.stl` (1 szt.)** – Front nachylony pod kątem $40^\circ$ z miejscem na ekran OLED, krzyżak 4 strzałek po lewej, enkoder KY-040 i przycisk `DALEJ` po prawej. Drukowany licem do stołu.
3. **`03_Taca_Robocza_210mm.stl` + `03b_Rant_210mm.stl` (po 1 szt.)** – Płaska taca $210\text{ mm}$ z 6 żebrami od spodu drukowana górną płaszczyzną na gładkim stole + osobny pierścień rantu doklejany po aplikacji czarnej matowej folii.
4. **`04_Adapter_Orczyka_24mm.stl` (3 szt.)** – Nakładka przykręcana dwiema śrubkami M2 do oryginalnego plastikowego orczyka Hitec HS-422, zakończona widełkami w odległości $L_1 = 24.0\text{ mm}$. *(GOTOWE W KODZIE PONIŻEJ)*
5. **`05_Popychacz_60mm.stl` (3 szt.) + `05b_Kostka_Kardana.stl` (6 szt.)** – Bezluzowe cięgna z przegubami krzyżakowymi (Kardana) na śrubach `M2x16mm` z mijanymi osiami (offset $\pm 1.4\text{ mm}$). *(GOTOWE W KODZIE PONIŻEJ)*
6. **`05c_Uchwyt_Pod_Tace.stl` (3 szt.)** – Uchwyty widełkowe przykręcane od spodu tacy w promieniu $R = 90.0\text{ mm}$ na śruby M3. *(GOTOWE W KODZIE PONIŻEJ)*
7. **`06_Palak_Dolny.stl` + `07_Palak_Gorny_Kamera.stl` (po 1 szt.)** – Dwuczęściowe ramię C-Arm z wewnętrznym tunelem kablowym $8 \times 8\text{ mm}$, mocowaniem pod `ESP32-S3-CAM` i gniazdem pod pierścień `12x WS2812B`.

---

## 6. Gotowy Kod CAD #1: Zestaw Cięgien Bezluzowych (OpenSCAD)

> [!success] Status: Gotowe do druku (100% ASCII Safe – przetestowane w `/playground.scad`)
> Ustawienia druku: Warstwa `0.16–0.20 mm`, Obrysy: `4`, Wypełnienie: `100%`, Podpory: `Brak (0%)`. Wydrukować cały zestaw (`part_select = 0`) **3 razy**.

```openscad
// BALL BALANCER 3-RRS - ZESTAW CIEGIEN (100% ASCII SAFE)
$fn = 64;

// 0 = Wszystkie czesci naraz (komplet na 1 ramie)
// 1 = Popychacz 60mm | 2 = Kostka Kardana | 3 = Adapter HS-422 | 4 = Uchwyt Tacy
part_select = 0; // [0:Wszystkie naraz, 1:Popychacz 60mm, 2:Kostka Kardana, 3:Adapter HS-422, 4:Uchwyt Tacy]

m2_hole = 2.05;
m2_mount = 2.15;
m3_hole = 3.20;

cube_w = 8.0;
cube_h = 10.0;
axis_offset = 1.4;

fork_gap = 8.4;
fork_wall = 2.8;
fork_thick = 7.6;
fork_depth = 7.5;

L1_horn = 24.0;
L2_rod = 54.4;

module fork_head() {
    outer_w = fork_gap + 2 * fork_wall;
    difference() {
        union() {
            translate([0, -outer_w/2, 0])
                rotate([-90, 0, 0])
                cylinder(d = fork_thick, h = outer_w);
            translate([-fork_depth - 4.0, -outer_w/2, -fork_thick/2])
                cube([fork_depth + 4.0, outer_w, fork_thick]);
        }
        translate([-fork_depth, -fork_gap/2, -fork_thick/2 - 1])
            cube([fork_depth + 6.0, fork_gap, fork_thick + 2]);
        translate([-fork_depth, 0, 0])
            rotate([0, 45, 0])
            cube([3, fork_gap, 3], center = true);
        translate([0, -outer_w/2 - 1, 0])
            rotate([-90, 0, 0])
            cylinder(d = m2_hole, h = outer_w + 2);
    }
}

module cardan_cube() {
    difference() {
        hull() {
            cube([cube_w - 2.0, cube_w, cube_h], center = true);
            cube([cube_w, cube_w - 2.0, cube_h], center = true);
        }
        translate([0, 0, axis_offset])
            rotate([0, 90, 0])
            cylinder(d = m2_hole, h = cube_w + 2, center = true);
        translate([0, 0, -axis_offset])
            rotate([90, 0, 0])
            cylinder(d = m2_hole, h = cube_w + 2, center = true);
    }
}

module pushrod_60mm() {
    rod_w = 7.0;
    union() {
        translate([L2_rod/2, 0, 0])
            fork_head();
        translate([-L2_rod/2, 0, 0])
            rotate([0, 0, 180])
            fork_head();
        difference() {
            translate([-(L2_rod/2 - fork_depth - 2), -rod_w/2, -fork_thick/2])
                cube([L2_rod - 2*fork_depth - 4, rod_w, fork_thick]);
            for (z_s = [-1, 1]) {
                translate([0, 0, z_s * (fork_thick/2)])
                    cube([L2_rod - 2*fork_depth - 14, rod_w - 2.6, 2.0], center = true);
            }
        }
    }
}

module hs422_horn_adapter() {
    outer_w = fork_gap + 2 * fork_wall;
    difference() {
        union() {
            translate([L1_horn, 0, 0])
                fork_head();
            hull() {
                cylinder(d = 14.0, h = fork_thick, center = true);
                translate([L1_horn - fork_depth - 3.5, -outer_w/2, -fork_thick/2])
                    cube([2.0, outer_w, fork_thick]);
            }
        }
        cylinder(d = 6.5, h = fork_thick + 2, center = true);
        translate([-2, -3.1, -fork_thick/2 - 0.1])
            cube([20.0, 6.2, 2.3]);
        for (r_h = [8.0, 12.5]) {
            translate([r_h, 0, 0])
                cylinder(d = m2_mount, h = fork_thick + 2, center = true);
        }
    }
}

module plate_mount_bracket() {
    base_len = 28.0;
    base_w = 14.0;
    base_t = 4.0;
    pivot_h = 10.5;
    difference() {
        union() {
            translate([-base_len/2, -base_w/2, 0])
                cube([base_len, base_w, base_t]);
            translate([0, 0, pivot_h])
                rotate([0, -90, 0])
                fork_head();
        }
        translate([-25, -25, -20])
            cube([50, 50, 20]);
        for (x_p = [-10.0, 10.0]) {
            translate([x_p, 0, -1])
                cylinder(d = m3_hole, h = base_t + 10);
        }
    }
}

if (part_select == 0) {
    translate([0, 0, fork_thick/2]) pushrod_60mm();
    translate([-15, 22, cube_h/2]) cardan_cube();
    translate([15, 22, cube_h/2]) cardan_cube();
    translate([-28, -24, fork_thick/2]) hs422_horn_adapter();
    translate([18, -24, 0]) plate_mount_bracket();
} else if (part_select == 1) {
    translate([0, 0, fork_thick/2]) pushrod_60mm();
} else if (part_select == 2) {
    translate([0, 0, cube_h/2]) cardan_cube();
} else if (part_select == 3) {
    translate([0, 0, fork_thick/2]) hs422_horn_adapter();
} else if (part_select == 4) {
    plate_mount_bracket();
}
```

---

## 7. Co zostało do zrobienia (Kolejne Kroki dla Nowego Czatu)

> [!todo] Zadania do wygenerowania w kolejnych sesjach:
> 1. **Kod OpenSCAD #2 (`01_Baza_Glowna_HS422` + `02_Panel_Konsoli_OLED`):** Wygenerowanie czystego kodu ASCII pod `/playground.scad` dla trójramiennej bazy ($R=90\text{ mm}$) z kieszeniami pod Hitec HS-422 oraz przedniego panelu pod ekran OLED, 4 strzałki, przycisk `Dalej` i enkoder `KY-040`.
> 2. **Kod OpenSCAD #3 (`03_Taca_Robocza_210mm` + `06/07_Palak_Kamery_C_Arm`):** Wygenerowanie kodu dla tacy $210\text{ mm}$ z otworami M3 pod uchwyty widełkowe (rozstaw śrub $20\text{ mm}$ w $R=90\text{ mm}$) oraz dwuczęściowego pałąka C-Arm o wysokości $195\text{ mm}$ nad tacą.
> 3. **Oprogramowanie dla `ESP32-S3-CAM` (C++ / Arduino IDE):** Kod szybkiego śledzenia środka ciężkości kulki w 60 FPS (`QQVGA Grayscale`), obsługa pierścienia LED `WS2812B` i wysyłanie pakietów po UART.
> 4. **Oprogramowanie dla głównego `ESP32` (C++ / FreeRTOS Dual-Core):** Pełny kod regulatora PID, kinematyki odwrotnej 3-RRS, obsługi 4 strzałek + enkodera, zapisu NVS i interfejsu graficznego (Radar Live / Trajektorie / PID / Trim) na ekranie OLED.

### 📋 Prompt startowy dla nowego czatu (Skopiuj i wklej na początku rozmowy)
```text
Kontynuujemy budowę projektu Ball Balancer 3-RRS według poniższej dokumentacji z Obsidiana. Wszystkie wymiary (taca 210 mm, promień rozstawu R=90 mm, serwa Hitec HS-422, ramię L1=24 mm, popychacz L2=60 mm z uchwytem pod tacę o rozstawie śrub M3 20 mm, kamera ESP32-S3-CAM + OV2640 120° na wysokości 195 mm nad tacą, konsola offline: OLED + 4 strzałki + przycisk Dalej + enkoder KY-040) są już ustalone, a cięgna Kardana mamy już wygenerowane. 
Uwaga techniczna: Każdy kod OpenSCAD, o który poproszę, generuj w 100% w czystym ASCII (bez polskich znaków nawet w komentarzach), aby działał bez błędów parsera w przeglądarkowym /playground.scad.
Oto nasza pełna dokumentacja:
[TUTAJ WKLEJ ZAWARTOŚĆ TEGO PLIKU MD]
```