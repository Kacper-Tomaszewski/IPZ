---
title: Firmware - Protokół UART
tags:
  - ball-balancer
  - firmware
  - uart
created: 2026-10-20
---

# 20. Firmware: protokół UART

Powrót: [[Projekt Ball Balancer]]. Następne: [[21 Firmware - Kamera]], [[22 Firmware - Sterowanie]].

## W skrócie

Oko (kamera) wysyła bazie pozycję kulki po kablu UART. W pierwszej wersji ramka miała 5 bajtów i nic nie sprawdzała. Nowa ma 9 bajtów i pozwala wykryć błędy oraz zgubione ramki.

## Parametry

921 600 baud, 8N1, poziomy 3,3 V, wspólna masa. Przesłanie jednej ramki trwa ok. 0,1 ms ($9\cdot10/921600$), więc kabel praktycznie nie opóźnia pomiaru.

## Ramka (oko → baza)

| Bajt | Pole | Znaczenie |
| :--- | :--- | :--- |
| 0 | `0xAA` | nagłówek |
| 1 | `0x55` | nagłówek |
| 2 | `seq` | numer ramki (licznik 0–255) |
| 3 | `flags` | bit 0: kulka znaleziona; bit 1: nasycenie obrazu; bit 2: błąd kamery |
| 4–5 | `x` | pozycja X w 1/16 piksela (uint16) |
| 6–7 | `y` | pozycja Y w 1/16 piksela (uint16) |
| 8 | `xor` | XOR bajtów 2–7 |

Pozycja w 1/16 piksela mieści się w 16 bitach nawet dla QVGA ($320\cdot16=5120$). Ułamek piksela jest potrzebny, bo centroid daje dokładność subpikselową ([[09 Kamera i wizja]]).

## Dlaczego nowa ramka

| Brakowało w v1 | Co daje v2 |
| :--- | :--- |
| Brak sumy kontrolnej | Zakłócenie lub zgubiony bajt jest wykrywane i ramka odrzucana |
| Nagłówek jednobajtowy `0xFF` | Dwubajtowy nagłówek `AA 55` rzadziej "udaje się" pojawić w danych |
| Brak numeru ramki | Wiemy, że ramka została zgubiona (luka w numeracji) |
| Brak flag | Wiemy, czy kulka w ogóle jest widoczna i czy obraz nie jest prześwietlony |

## Odbiór po stronie bazy

Maszyna stanów szuka `AA 55`. Po odebraniu 9 bajtów sprawdza sumę XOR. Przy błędzie odrzuca ramkę i szuka kolejnego nagłówka od początku (nie "gubi się" na stałe po jednym złym bajcie).

Jeśli nie ma poprawnej ramki przez > 100 ms, baza przechodzi w stan awarii kamery i poziomuje tacę ([[22 Firmware - Sterowanie]]).

## Komendy (baza → oko)

Prosty kanał zwrotny, np. 1-bajtowe lub tekstowe komendy: ustaw jasność LED, ustaw tryb LED, uruchom kalibrację, zmień rozdzielczość. Dokładny format ustalimy przy pisaniu kodu; wspólna definicja leży w `protocol.h` ([[23 Firmware - Narzędzia i struktura]]).
