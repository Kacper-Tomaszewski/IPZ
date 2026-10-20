---
title: Konsola i obsługa
tags:
  - ball-balancer
  - interfejs
  - ui
created: 2026-10-20
---

# 15. Konsola i obsługa

Poprzednia: [[14 Pinout i połączenia]]. Dalej: [[16 Elementy do druku]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Konsola to panel z ekranem OLED, czterema strzałkami, przyciskiem DALEJ i pokrętłem. Dzięki niej zmieniamy nastawy **bez komputera**. To spełnia założenie, że całość ma być w pełni autonomiczna.

## Sterowanie

| Element | Funkcja |
| :--- | :--- |
| **DALEJ (MODE)**, krótkie | Przełącza ekrany 1 → 2 → 3 → 4 → 5 |
| **DALEJ**, długie przytrzymanie | **STOP**: taca wraca do poziomu |
| **Strzałki** | Wybór pozycji w menu, w ekranie 1: przesuwanie punktu zadanego |
| **Pokrętło** | Zmiana wartości |
| **Klik pokrętła** | Zmiana kroku: 0,01 / 0,10 / 1,0 |
| **Przytrzymanie kliku** | Zapis do pamięci (z potwierdzeniem) |

## Ekrany

| Ekran | Co pokazuje | Co robimy |
| :--- | :--- | :--- |
| **1. Radar** | Mapa tacy z punktem kulki i punktem zadanym, FPS, status | Strzałkami przesuwamy punkt zadany |
| **2. Trajektorie** | Rodzaj toru (stop, okrąg, ósemka, kwadrat), rozmiar, okres okrążenia, kierunek, $k_{ff}$, $t_{lead}$ | Strzałki wybierają parametr, pokrętło zmienia wartość. Menu samo przycina do limitów toru ([[12 Trajektorie]]) |
| **3. PID** | $K_p$, $K_d$, $K_i$, profil kulki | Pokrętłem zmieniamy wartość, strzałkami wybieramy parametr |
| **4. Trim serw** | Offset i kierunek dla 3 serw, poziomowanie | Strzałki + pokrętło |
| **5. Kalibracja kamery** | Środek obrazu, skala, obrót/odbicie osi, próg | Strzałki + pokrętło |

Ekran 5 jest nowy (nie było go w pierwszej wersji). Dodaliśmy go, bo kalibracja kamery jest niezbędna ([[09 Kamera i wizja]], [[18 Kalibracja i uruchomienie]]), a bez własnego ekranu trzeba by ją robić po kablu z komputera.

## Zapis nastaw

- Nastawy trzymamy w pamięci nieulotnej **NVS**.
- Zapisujemy **tylko na wyraźne polecenie** (przytrzymanie kliku). Pamięć flash ma ograniczoną liczbę zapisów, więc nie zapisujemy w pętli.
- Do zapisu dodajemy **numer wersji** i **sumę kontrolną**, żeby po zmianie struktury nastaw stary zapis nie zepsuł działania.
- Zapis do flash na chwilę wstrzymuje procesor, ale sygnał PWM do serw jest generowany sprzętowo (LEDC) i nie ulega zakłóceniu.

## Enkoder

Mechaniczny enkoder KY-040 odbija styki. Dlatego czytamy go sprzętowym licznikiem impulsów (PCNT, biblioteka `ESP32Encoder`) lub maszyną stanów, a nie surowymi przerwaniami na zboczach. Inaczej wartości będą "skakać".

## Ekran OLED: szybkość odświeżania

Pełna klatka $128\times64$ to 1024 bajty. Przy I²C 400 kHz (9 taktów na bajt) transmisja trwa:

$$\frac{1024\cdot9}{400000}\approx23\text{ ms}$$

Plus narzut, razem ok. 25 ms, czyli maksymalnie ok. 40 klatek/s. Odświeżamy **10–15 razy na sekundę**, na osobnym rdzeniu (Core 0), żeby sterowanie serwami (Core 1) nigdy nie czekało na ekran.

## Wymiary panelu

Płyta czołowa 120 × 62 mm, pochylona o 40° z przodu bazy, między serwami 2 i 3. Strzałki po lewej, pokrętło i DALEJ po prawej, ekran pośrodku. Drukowany licem do stołu ([[16 Elementy do druku]]).
