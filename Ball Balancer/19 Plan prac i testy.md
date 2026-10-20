---
title: Plan prac i testy
tags:
  - ball-balancer
  - plan
  - testy
created: 2026-10-20
---

# 19. Plan prac i testy

Poprzednia: [[18 Kalibracja i uruchomienie]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Zamiast kupić wszystko i dopiero potem odkryć problem, **najpierw sprawdzamy to, co najbardziej niepewne, najtańszym kosztem**. Dwie największe niewiadome to wizja (czy kamera 120° da użyteczną dokładność i szybkość) i cięgna Kardana (czy nie klinują). Obie sprawdzamy, zanim kupimy resztę i wydrukujemy bazę i tacę.

Każdy etap ma **kryterium przejścia dalej**. Nie przechodzimy do następnego, dopóki poprzedni go nie spełni.

## Etapy

- [ ] **Etap 0: walidacja na tym, co mamy.**
  - Serwa na stole: PWM z LEDC, kalibracja 1500 µs, pomiar µs/° dla ±35° ([[18 Kalibracja i uruchomienie]]).
  - Zmierz suwmiarką otwory w oryginalnych orczykach HS-422.
  - Wydrukuj kupon tolerancji i **1 zestaw cięgien** ([[16 Elementy do druku]]).
  - *Przejdź dalej, gdy:* cięgno nie klinuje się w ±35° orczyka, luz $\le0{,}3$ mm. Jeśli nie: popraw tolerancje albo plan B (łączniki kulowe, [[07 Cięgna i przeguby]]).

- [ ] **Etap 1: test wizji** (zakup części A, ok. 70–80 zł, [[03 Lista rzeczy do projektu]]).
  - Kartonowa taca ⌀210 mm, kamera na statywie na wysokości 170, 195 i 210 mm.
  - Zmierz: prawdziwy FPS (QQVGA i QVGA), kąt widzenia, skalę mm/px w środku i na brzegu, szum pozycji kulki w spoczynku, opóźnienie.
  - *Przejdź dalej, gdy:* szum $\sigma\le0{,}8$ mm, FPS $\ge45$, kulka widoczna na całej tacy. Wynik ustala wysokość kamery i rozdzielczość ([[09 Kamera i wizja]]).

- [ ] **Etap 2: zakup części B** (reszta listy).

- [ ] **Etap 3: CAD.** Baza i konsola, taca i pałąk. Parametry w jednym `params.scad`. Sprawdź kolizje ([[17 Taca, pałąk i baza]]).

- [ ] **Etap 4: druk i montaż mechaniki.** Kolejność: baza + serwa + cięgna → taca → pałąk → konsola. Po każdym kroku sprawdź ruch ręką.

- [ ] **Etap 5: elektronika na biurku.** Zasilanie 5 V w gwiazdę, kondensatory, konwerter poziomów dla LED, skręcona para UART, złącze JST ([[13 Zasilanie i elektronika]]). Zmierz prądy.

- [ ] **Etap 6: firmware** w kolejności: kinematyka + serwa → UI + NVS → kamera → UART → pętla PID ([[22 Firmware - Sterowanie]]).

- [ ] **Etap 7: integracja i strojenie.** Kalibracje, potem strojenie według procedury z [[11 Regulator PID]]. Mierz kryteria sukcesu.

- [ ] **Etap 8: wykończenie.** Folia, rant, okablowanie w tunelu, dyfuzor LED, etykiety.

## Ryzyka i jak je sprawdzamy

| Ryzyko | Kiedy sprawdzamy | Co robimy, jeśli się sprawdzi |
| :--- | :--- | :--- |
| Cięgna Kardana klinują lub mają zbyt duży luz | Etap 0 | Poprawka tolerancji; łączniki kulowe M3 |
| Kamera 120° nie daje dokładności | Etap 1 | QVGA; zmiana wysokości; obiektyw ok. 90° |
| Moduł S3 i taśma FPC nie pasują | Przy zamówieniu | Sprawdź opis oferty i zdjęcia gniazda |
| Główne ESP32 to WROVER | Przed lutowaniem | Zmień piny UART (GPIO 16/17 odpadają) |
| Zasilacz za słaby lub zakłócenia | Etap 5 | Dodaj kondensatory; wymień zasilacz |
| Za duże opóźnienia, regulator oscyluje | Etap 7 | Zmniejsz $K_p$; rozważ serwa cyfrowe |
| Taca się wygina | Po wydruku | Grubsza płyta (4 mm), brim, inny podkład |
| Drgania pałąka | Etap 4–7 | Wzmocnienie prętem, grubsze ścianki |

## Kryteria sukcesu (na koniec)

Taki sam zestaw jak w [[01 Jak to działa]]: odchylenie $\le3$ mm przez 60 s, powrót po szturchnięciu w $\le3$ s, okrąg $r=60$ mm przy $\omega=1{,}5$ rad/s z błędem $\le10$ mm, bezpieczne zachowanie po utracie kamery lub kulki, praca bez PC.
