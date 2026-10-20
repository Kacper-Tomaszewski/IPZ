---
title: Firmware - Kamera
tags:
  - ball-balancer
  - firmware
  - kamera
created: 2026-10-20
---

# 21. Firmware: kamera (oko)

Powrót: [[Projekt Ball Balancer]]. Wcześniej: [[20 Firmware - Protokół UART]]. Wiedza o obrazie: [[09 Kamera i wizja]].

> [!warning] Status kodu
> Poniżej jest **opis zadań**, nie gotowy program. Kod powstanie po Etapie 1 testów ([[19 Plan prac i testy]]), bo ustawienia zależą od wyników.

## W skrócie

Płytka ESP32-S3 z kamerą robi wyłącznie to, co do niej należy: bierze obraz, znajduje na nim kulkę i wysyła pozycję. Nic poza tym, żeby nie było żadnych opóźnień.

## Zadania krok po kroku

1. **Konfiguracja kamery.** Skala szarości (`PIXFORMAT_GRAYSCALE`), rozdzielczość QQVGA ($160\times120$) z opcją QVGA, zegar XCLK 20 MHz, dwa bufory klatek, tryb "weź najnowszą" (`GRAB_LATEST`).
   *Dlaczego:* obraz bez kompresji JPEG jest szybszy i nie traci informacji, a tryb "najnowsza" zapobiega czytaniu starej klatki.
2. **Wyłączone Wi-Fi i Bluetooth.** *Dlaczego:* radio zajmuje procesor i wprowadza opóźnienia, a nie jest potrzebne.
3. **Ustawienia czujnika.** `aec=0`, `agc=0`, `awb=0`, stała ekspozycja $\le5$ ms (najlepiej wielokrotność okresu PWM WS2812B ok. 2,5 ms), stałe wzmocnienie. *Dlaczego:* automatyka zmienia czas klatki i jasność, a wtedy próg wykrywania "pływa".
4. **Maska.** Obszar spoza tacy (rant, pałąk) ignorujemy. *Dlaczego:* inaczej jasne elementy tła mogą wyglądać jak kulka.
5. **Progowanie.** Próg stały lub wyznaczony przy starcie (metoda Otsu). Piksele jaśniejsze niż próg należą do kulki.
6. **Centroid z wagami jasności.** $x_c=\frac{\sum x\,w}{\sum w}$, gdzie $w=\max(I-\text{próg},0)$. *Dlaczego z wagami:* daje dokładność ułamka piksela, ok. ±0,2–0,3 px.
7. **Sprawdzenie sensowności.** Pole plamy powinno wynosić ok. 230 px (kulka ⌀40 mm = ok. 17 px średnicy). Za małe lub za duże: odrzucamy jako błąd.
8. **Wysyłka ramki UART** po każdej klatce ([[20 Firmware - Protokół UART]]).
9. **Pierścień LED.**
   - Światło białe, jasność ok. 25%, stałe w trakcie pomiaru.
   - Status kolorem w osobnych przerwach lub na dedykowanych diodach: zielony = kulka widoczna, żółty = brak, czerwony = błąd.
   - Dane wprost z GPIO; pierścień zasilany przez diodę 1N4001 ([[13 Zasilanie i elektronika]]).

## Czego mierzymy w Etapie 1

- Prawdziwy FPS w QQVGA i QVGA.
- Czas przetwarzania klatki (centroid).
- Szum pozycji kulki w spoczynku (cel $\sigma\le0{,}8$ mm).
- Stabilność jasności tła przy dyfuzorze (histogram).
- Opóźnienie od błysku światła do wysłania ramki.
