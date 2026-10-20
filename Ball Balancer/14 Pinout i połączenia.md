---
title: Pinout i połączenia
tags:
  - ball-balancer
  - elektronika
  - pinout
created: 2026-10-20
---

# 14. Pinout i połączenia

Poprzednia: [[13 Zasilanie i elektronika]]. Dalej: [[15 Konsola i obsługa]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Tabele pinów obu płytek. Przyciski i enkoder używają wewnętrznych rezystorów podciągających (`INPUT_PULLUP`), a drugi styk każdego z nich idzie do wspólnej masy GND.

## Dolne ESP32 (baza)

| Funkcja | GPIO | Uwagi |
| :--- | :--- | :--- |
| OLED SDA | 21 | I²C, odświeżane na Core 0 |
| OLED SCL | 22 | 400 kHz |
| UART RX (z kamery) | 16 | Serial2. Do TX płytki S3 |
| UART TX (do kamery) | 17 | Serial2. Do RX płytki S3 |
| Serwo 1 (tył, 90°) | 25 | PWM 50 Hz |
| Serwo 2 (przód-lewo, 210°) | 26 | PWM 50 Hz |
| Serwo 3 (przód-prawo, 330°) | 27 | PWM 50 Hz |
| Enkoder CLK (A) | 32 | `INPUT_PULLUP` |
| Enkoder DT (B) | 33 | `INPUT_PULLUP` |
| Enkoder SW (klik) | 15 | `INPUT_PULLUP` |
| Strzałka GÓRA | 18 | Nawigacja / setpoint Y+ |
| Strzałka DÓŁ | 19 | Nawigacja / setpoint Y− |
| Strzałka LEWO | 23 | Nawigacja / setpoint X− |
| Strzałka PRAWO | 4 | Nawigacja / setpoint X+ |
| Przycisk DALEJ (MODE) | 13 | Przełącza ekrany |

### Uwagi

- **GPIO 16/17 działają tylko w module WROOM-32.** W module WROVER zajmuje je pamięć PSRAM. Sprawdź, jaki masz moduł, zanim zlutujesz ([[03 Lista rzeczy do projektu]]).
- **GPIO 15 to pin strappingowy.** Przytrzymanie klikniętego enkodera podczas włączania zmienia zachowanie logów bootu. Nic groźnego, ale nie trzymaj enkodera przy starcie.
- **Piny serw** (25/26/27) mają rezystory 10 kΩ do GND ([[13 Zasilanie i elektronika]]).
- **Serwa 2 i 3** mają zamienione etykiety względem pierwszej wersji planu. Powód: [[05 Geometria i wymiary]]. Piny są te same, zmieniły się tylko opisy.

## ESP32-S3 CAM (oko)

Dokładny pinout zależy od konkretnej płytki. **Sprawdź schemat własnej płytki przed lutowaniem.**

- Typowo wolne piny: GPIO 1, 2, 14, 47, 48 (zależnie od modelu).
- Na wariancie **N16R8** piny GPIO 35–37 są zajęte przez pamięć PSRAM i nie nadają się do niczego innego.
- Część pozostałych pinów jest zajęta przez kamerę.

Potrzebujemy dwóch pinów na UART (TX, RX) i jednego na dane diod LED:

| Funkcja | Pin | Uwagi |
| :--- | :--- | :--- |
| UART TX (do bazy) | wolny GPIO | Do RX bazy (GPIO 16) |
| UART RX (z bazy) | wolny GPIO | Do TX bazy (GPIO 17) |
| Dane WS2812B | wolny GPIO | Przez konwerter poziomów 74AHCT125 |

## Połączenia między płytkami (przez złącze pałąka)

| Przewód | Opis |
| :--- | :--- |
| 5 V | Zasilanie płytki S3 i pierścienia LED |
| GND | Wspólna masa (skręcona z TX i RX) |
| TX (S3) → RX (baza) | Pozycja kulki (ramka 9 B) |
| RX (S3) ← TX (baza) | Komendy: jasność LED, kalibracja |

TX z jednej strony zawsze idzie do RX z drugiej (połączenie krzyżowe). Ramka opisana w [[20 Firmware - Protokół UART]].
