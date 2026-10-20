---
title: Firmware - Narzędzia i struktura
tags:
  - ball-balancer
  - firmware
  - narzędzia
created: 2026-10-20
---

# 23. Firmware: narzędzia i struktura projektu

Powrót: [[Projekt Ball Balancer]].

## W skrócie

Mamy dwa osobne programy (kamera i baza), które muszą się „rozumieć" w ramce UART, i modele CAD, których wymiary muszą się zgadzać z liczbami w kodzie. Uporządkowana struktura sprawia, że zmieniamy każdą wartość tylko w jednym miejscu.

## Proponowana struktura

Vault jest już repozytorium git. Gdy zaczniemy pisać kod, zakładamy foldery:

```
cad/
  params.scad        # wszystkie wymiary: R, L1, L2, Z_servo, Z_top, H_cam
  stl/
firmware/
  eye/               # ESP32-S3 CAM (PlatformIO)
  brain/             # ESP32 (PlatformIO)
  shared/protocol.h  # wspolna definicja ramki UART
docs/                # te notatki
```

## Narzędzia i dlaczego

| Narzędzie | Po co |
| :--- | :--- |
| **PlatformIO** (w VS Code) | Wersje bibliotek zablokowane w `platformio.ini`. Za pół roku projekt zbuduje się tak samo, jak dziś |
| **Wspólny `protocol.h`** | Obie strony ramki UART czytają ten sam plik, więc nie ma ryzyka, że jedna zmieni format bez drugiej |
| **`params.scad`** | Jedno źródło prawdy dla geometrii, a stałe w kodzie (`R_BASE`, `L1`...) kopiujemy stamtąd |
| **Git, commit po każdym etapie** | Możliwość cofnięcia się, gdy zmiana pogorszy działanie |
| **Telemetria po USB** | Podczas strojenia wysyłamy z płytki linie CSV (czas, pozycja, prędkość, uchyb, przechył, kąty serw), zapisujemy do pliku i porównujemy nastawy. Tryb standalone nie wyklucza logowania na biurku |

## Biblioteki (propozycja)

- Serwa: LEDC bezpośrednio (14 bit, 50 Hz) lub `ESP32Servo`.
- OLED: biblioteka dla SSD1306/SH1106 w trybie, który nie blokuje (U8g2 lub Adafruit). Sprawdź, jaki sterownik ma Twój wyświetlacz.
- Enkoder: `ESP32Encoder` (sprzętowy licznik PCNT).
- Diody LED: `FastLED` lub `Adafruit_NeoPixel`.
- Zapis nastaw: `Preferences` (NVS).

## Jak nazywamy rzeczy

Kod, komentarze i nazwy zmiennych w programach piszemy po angielsku lub bez polskich znaków, a w kodzie OpenSCAD **wyłącznie w czystym ASCII**, bo parser przeglądarkowego `/playground.scad` bywa wrażliwy na polskie znaki, nawet w komentarzach.
