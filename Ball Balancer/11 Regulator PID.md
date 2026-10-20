---
title: Regulator PID
tags:
  - ball-balancer
  - pid
  - obliczenia
created: 2026-10-20
---

# 11. Regulator PID

Poprzednia: [[10 Dynamika kulki]]. Dalej: [[12 Trajektorie]]. Powrót: [[Projekt Ball Balancer]]. Kod: [[22 Firmware - Sterowanie]].

> [!note] Dla torów regulator ma dodatkowe wejścia
> Ta notatka opisuje regulator dla **stałego punktu**. Gdy kulka ma jeździć po torze, dochodzą prędkość i przyspieszenie z generatora, a sam PID nie wystarcza (błąd ok. 44 mm na okręgu 60 mm przy 1,5 rad/s). Pełny wzór: [[12 Trajektorie]].

## W skrócie

Regulator przelicza błąd ("gdzie kulka jest" − "gdzie ma być") na przechył tacy. Nastawy, które policzyłem, są **celowo powolne** (pasmo ok. 0,4 Hz). Powód: kamera i serwo mają opóźnienia i szybszy regulator zacząłby oscylować. Poniżej pokazuję, jak do tego doszedłem.

## Model, który regulujemy

Regulowany obiekt to podwójny integrator z dwoma opóźnieniami:

$$G(s)=\frac{K}{s^2}\cdot\frac{e^{-T_d s}}{\tau_s s+1},\quad K=5{,}89\ \text{m/s}^2/\text{rad}$$

- $\tau_s\approx50$–70 ms: opóźnienie serwa HS-422 (założenie z danych katalogowych, do zmierzenia).
- $T_d\approx40$–60 ms: opóźnienie czysto transportowe, na które składają się: klatka kamery (ok. 20 ms), przetwarzanie, UART, próbkowanie co 20 ms i średnio 10 ms opóźnienia PWM.

## Struktura

Sterujemy przechyłem (w stopniach) w funkcji pozycji i prędkości kulki. Pochodną bierzemy z **pomiaru**, a nie z uchybu, żeby skok punktu zadanego nie wywołał gwałtownego szarpnięcia:

$$\theta=K_p(r-x)-K_d\,\hat v+K_i\!\int(r-x)\,dt$$

Zamykając pętlę i pomijając opóźnienia, dostajemy równanie $s^2+K K_d s+K K_p=0$, z którego widać dwa pokrętła:

$$\omega_n=\sqrt{K K_p},\qquad \zeta=\frac{K K_d}{2\omega_n}$$

Pierwsze to szybkość reakcji, drugie tłumienie (cel: ok. 0,7–1).

## Dlaczego nie „szybki" PID

Pierwsza myśl: ustawić $\omega_n=4$ rad/s i $\zeta=0{,}8$. W modelu idealnym to działa świetnie. Ale po dodaniu opóźnienia serwa i kamery **marża fazowa spada do ok. 10–20°**, czyli układ jest blisko niestabilności i kulka będzie oscylować.

Dlatego przeszukałem siatkę nastaw dla $T_i=15$ s i filtra pochodnej $N=10$ w poszukiwaniu największej marży:

| Opóźnienia (serwo / kamera) | Najlepsza marża fazowa |
| :--- | ---: |
| $\tau_s=50$ ms, $T_d=40$ ms | ok. 46° |
| $\tau_s=70$ ms, $T_d=60$ ms | ok. 42° |

Szybszy regulator **nie poprawi** sytuacji. Ograniczeniem jest fizyka toru (kamera + serwo), a nie sama liczba w sterowniku.

## Nastawy startowe (pingpong, 50 Hz)

| Parametr | W radianach | W praktyce |
| :--- | :--- | :--- |
| $K_p$ | 0,4 rad/m | **0,0229 °/mm** |
| $K_d$ ($T_d=1{,}0$ s) | 0,4 rad·s/m | **0,0229 °·s/mm** |
| $K_i$ ($T_i=15$ s) | 0,027 rad/(m·s) | **0,0015 °/(mm·s)** |
| Filtr pochodnej | $N=10$ lub filtr α-β | |
| Limit całki | | ±1,5° |
| Limit wyjścia | | ±6° |

Wyniki: $\omega_n\approx1{,}5$ rad/s, $\zeta\approx0{,}77$ (model idealny). Z opóźnieniami: przecięcie ok. 2,6 rad/s (0,4 Hz), marża 37–43°, czas ustalania **ok. 2–3 s**.

Ponieważ model ma założenia, **to są nastawy startowe, nie ostateczne.** Fizyczne strojenie zrobimy w Etapie 7.

## Procedura strojenia (krok po kroku)

1. Wyłącz całkę ($K_i=0$), ustaw $K_d=0{,}02$ °·s/mm. Zwiększaj $K_p$ aż kulka zacznie oscylować wokół środka, potem cofnij o ok. 30%.
2. Zwiększaj $K_d$, aż oscylacje szybko zanikną, ale nie pojawią się drgania z szumu kamery.
3. Dodaj $K_i$ tak, by kulka wracała do środka po wypoziomowaniu lub dociśnięciu w ciągu kilkunastu sekund.
4. Zapisz zestaw jako profil w pamięci (osobno dla pingponga i golfowej).

## Filtr α-β: skąd prędkość

Kamera podaje tylko pozycję, a nam potrzebna jest też prędkość. Gdybyśmy odjęli dwie kolejne pozycje i podzielili przez 20 ms, błąd ±0,6 mm dałby szum prędkości rzędu 30–40 mm/s, czyli więcej niż sama prędkość kulki. Filtr α-β wygładza to, utrzymując przy tym szybkość reakcji.

Krok co $T=20$ ms:

$$\hat x^-=\hat x+\hat v\,T,\qquad \hat x\leftarrow\hat x^-+\alpha(z-\hat x^-),\qquad \hat v\leftarrow\hat v+\frac{\beta}{T}(z-\hat x^-)$$

Dla $\alpha=0{,}5$ wybieramy $\beta=\alpha^2/(2-\alpha)=0{,}167$ (krytyczne tłumienie). Gdy kamera na chwilę nie widzi kulki, filtr **przewiduje** pozycję (przesuwa o $\hat v T$) przez 1–2 klatki. Po 5 klatkach (100 ms) zgłaszamy awarię.

## Anty-windup i wyjście

- **Limit całki ±1,5°**: gdy kulka długo nie może dojechać do punktu (np. utknęła), część I nie powinna rosnąć w nieskończoność.
- **Zamrożenie całki** przy nasyceniu wyjścia (±6°) lub utracie kulki.
- **Auto-trim**: po 10 s z kulką stojącą w środku zapamiętujemy wartość całki jako poprawkę poziomowania tacy ([[18 Kalibracja i uruchomienie]]).

## Dlaczego ten regulator

- **PD z wolnym I** zamiast pełnego, szybkiego PID, bo obiekt to podwójny integrator, który wymaga tłumienia, a całka służy tylko do usunięcia małego, stałego błędu.
- **Pętla 50 Hz** zamiast 100+ Hz: serwo analogowe i tak odświeża się co 20 ms ([[08 Serwa i momenty]]).
- **Dwa osobne regulatory (X i Y):** w tym układzie osie są niezależne, a kod jest prostszy.
