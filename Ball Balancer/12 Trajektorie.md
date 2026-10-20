---
title: Trajektorie
tags:
  - ball-balancer
  - trajektorie
  - obliczenia
created: 2026-10-20
---

# 12. Trajektorie

Poprzednia: [[11 Regulator PID]]. Dalej: [[13 Zasilanie i elektronika]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Oprócz trzymania kulki w miejscu chcemy, żeby jeździła po okręgu, ósemce itp. Żeby kulka jechała po łuku, musi mieć przyspieszenie skierowane do środka okręgu. Wiemy, jak je wytworzyć (przechyłem), więc możemy to **podać regulatorowi z góry** (feed-forward), zamiast czekać aż pojawi się błąd.

## Wzór

Dla okręgu o promieniu $r$ i szybkości kątowej $\omega$ potrzebne jest przyspieszenie dośrodkowe $a=\omega^2 r$. Przechył z góry:

$$\theta_{ff}=\frac{\omega^2 r}{K}$$

gdzie $K=5{,}89$ m/s² na radian dla piłeczki pingpongowej.

## Ile trzeba przechylić

| Promień $r$ | $\omega=1{,}0$ rad/s | $\omega=1{,}5$ rad/s | $\omega=2{,}0$ rad/s |
| :--- | ---: | ---: | ---: |
| 40 mm | 0,39° | 0,88° | 1,56° |
| 60 mm | 0,58° | 1,31° | 2,34° |
| 80 mm | 0,78° | 1,75° | 3,12° |

Przykład: okrąg $r=60$ mm przy $\omega=1{,}5$ rad/s (jedno okrążenie w ok. 4,2 s) wymaga przechyłu tylko ok. 1,3°, a prędkość kulki to $\omega r=90$ mm/s.

## Jak szybko można jechać

- **Fizyczny limit.** Przy połowie maksymalnego przechyłu (4,5°, przyspieszenie 0,46 m/s²) kulka może jechać z $\omega_{max}=\sqrt{a/r}$: 3,4 / 2,8 / 2,4 rad/s dla promieni 40 / 60 / 80 mm.
- **Limit regulatora.** Pasmo pętli to ok. 2,6 rad/s ([[11 Regulator PID]]). Zamknięta pętla nie dotrzyma tak szybkiego toru, więc na początek **ograniczamy $\omega\le1{,}5$ rad/s**.

> [!tip] Dlaczego zaczynamy od wolnego toru
> Przy większej prędkości regulator zaczyna się spóźniać, a kulka „ścina" łuk. Lepiej zacząć od wolnego, dokładnego toru, potwierdzić kryterium sukcesu (błąd $\le10$ mm), a potem stopniowo zwiększać prędkość.

## Plan rodzajów trajektorii

Zaczynamy od: **stop** (punkt), **okrąg**. Później: ósemka, kwadrat, krzywe Lissajous. Wszystkie wybierane na ekranie 2 konsoli ([[15 Konsola i obsługa]]).
