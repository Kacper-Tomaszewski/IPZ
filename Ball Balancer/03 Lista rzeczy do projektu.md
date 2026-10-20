---
title: Lista rzeczy do projektu
tags:
  - ball-balancer
  - zakupy
  - lista
created: 2026-10-20
---

# 03. Lista rzeczy do projektu

Wszystko, czego potrzebujemy, w jednym miejscu. Powrót: [[Projekt Ball Balancer]].

> [!tip] Jak to czytać
> Kupujemy **w dwóch turach**. Najpierw tylko zestaw kamery (część A), żeby sprawdzić, czy wizja działa, zanim wydamy resztę. Powód opisuje [[19 Plan prac i testy]].

## ✅ Już mamy (0 zł)

- [x] Drukarka 3D + filament PLA lub PETG
- [x] Płytka ESP32 (baza)
- [x] Wyświetlacz OLED I²C
- [x] 3× serwo Hitec HS-422 (zapas momentu 25–30 razy większy niż potrzeba, patrz [[08 Serwa i momenty]])
- [x] 3× SG90 (rezerwa)
- [x] Kondensatory elektrolityczne $\ge 1000\,\mu$F / 10 V
- [x] Śruby i nakrętki M2 oraz M3

## 🛒 Tura A: test wizji (ok. 70–80 zł)

- [ ] **ESP32-S3-WROOM N16R8 CAM** z 2× USB-C (~38–45 zł). To „oko".
- [ ] **Kamera OV2640 z obiektywem 120°**, taśma 24-pin, długość 20–50 mm (~15 zł). Standardowy obiektyw 65° nie obejmie całej tacy, uzasadnienie w [[09 Kamera i wizja]].
- [ ] **Pierścień LED 12× WS2812B**, średnica zewnętrzna 37–50 mm (~7 zł)
- [ ] **Piłeczki pingpongowe 40 mm**, matowe, białe lub pomarańczowe (~5 zł)
- [ ] **Czarna matowa folia samoprzylepna** lub czarna podkładka pod mysz (~5 zł)
- [ ] Zapasowa taśma FPC do kamery (łatwo ją uszkodzić)
- [ ] Biała kartka na dyfuzor pierścienia LED

## 🛒 Tura B: reszta (ok. 65–85 zł)

**Interfejs**
- [ ] Enkoder obrotowy KY-040 z gałką (~6 zł)
- [ ] 5× przycisk Tact 12×12×7,3 mm + 5 kolorowych nasadek (~5 zł): 4 strzałki i przycisk DALEJ

**Zasilanie i elektronika**
- [ ] **Zasilacz impulsowy 5 V / 4 A** + gniazdo DC 5,5/2,1 mm do obudowy (~20–25 zł). Wybieramy 4 A, nie 3 A, bo szczytowy pobór to ok. 2,3–3,3 A ([[13 Zasilanie i elektronika]]).
- [ ] Włącznik zasilania
- [ ] Bezpiecznik lub PTC ok. 5 A
- [ ] Konwerter poziomów **74AHCT125** (dla diod WS2812B)
- [ ] Rezystory 10 kΩ, 3 szt. (linie sygnałowe serw do masy)
- [ ] Kondensatory 100 µF i 100 nF (przy każdym serwie i każdym ESP32)
- [ ] Płytka uniwersalna, przewody silikonowe AWG26–28, goldpiny
- [ ] Złącze **JST-XH 4-pin** (para) do odłączanego pałąka

**Mechanika**
- [ ] Śruby **M2×18–20**, ok. 16 szt. (z zapasem)
- [ ] Nakrętki M2 **samohamowne**, ok. 16 szt.
- [ ] **8× łącznik kulowy M3** (plan B, jeśli kostki Kardana się zaklinują, patrz [[07 Cięgna i przeguby]])
- [ ] Cienkie podkładki M2
- [ ] Wkładki gwintowane M3 (heat-set), kilka sztuk
- [ ] Stopki gumowe, 4 szt.
- [ ] Klej do folii, ewentualnie nożyk do jej docinania

## 🖨️ Do wydrukowania

Pełna lista plików z uwagami: [[16 Elementy do druku]].
- Baza, panel konsoli, taca + rant, pałąk dolny i górny, 4 zestawy cięgien, kupon tolerancji, arkusz kalibracyjny (A4, papier).

## 🔧 Narzędzia

- [ ] Suwmiarka (potrzebna już w Etapie 0)
- [ ] Lutownica + cyna (także do wkładek heat-set)
- [ ] Multimetr
- [ ] Wkrętaki i klucze imbusowe M2/M3
- [ ] Szczypce tnące, szczypce do zdejmowania izolacji
- [ ] Liniał lub płyta szklana (kontrola płaskości tacy)

## 💻 Oprogramowanie

- [ ] OpenSCAD (kod w [[24 Kod OpenSCAD cięgien]])
- [ ] Slicer dla drukarki
- [ ] VS Code + PlatformIO ([[23 Firmware - Narzędzia i struktura]])
- [ ] Git (vault już jest repozytorium)
- [ ] Opcjonalnie Python do rysowania wykresów z telemetrii

## 💰 Budżet

| Pozycja | Koszt |
| :--- | ---: |
| Tura A (zestaw kamery, piłeczki, folia) | 70–80 zł |
| Tura B (interfejs, zasilanie, mechanika, dodatki) | 65–85 zł |
| **Razem** | **ok. 140–160 zł** |

W pierwszej wersji planu było 100–110 zł. Różnica to dodatki, których tamta lista nie zawierała (konwerter poziomów, łączniki kulowe, złącza, zapasowa taśma kamery, wkładki, stopki). Lepiej je kupić od razu niż dojeżdżać po jednej sztuce.

## ⚠️ Sprawdź przed zamówieniem

| Co | Dlaczego |
| :--- | :--- |
| Gniazdo FPC 24-pin 0,5 mm na płytce S3 pasuje do modułu OV2640 120° | Zdarzają się moduły z odwróconą kolejnością pinów lub innym złączem |
| Główne ESP32 to moduł **WROOM-32**, nie WROVER | UART jest na GPIO 16/17, a w WROVER zajmuje je pamięć PSRAM |
| Zasilanie S3 z pinu 5 V przy podłączonym USB-C | Sprawdź na schemacie płytki, czy jest dioda, inaczej nie łącz obu naraz |
| Rozstaw otworów w oryginalnym orczyku HS-422 (suwmiarką) | Adapter zakłada otwory na 8,0 i 12,5 mm od osi, trzeba to potwierdzić |
| Ostateczna wysokość kamery | Ustalimy po teście w Etapie 1, dlatego pałąk ma być regulowany |
