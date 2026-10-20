---
title: Dynamika kulki
tags:
  - ball-balancer
  - fizyka
  - obliczenia
created: 2026-10-20
---

# 10. Dynamika kulki

Poprzednia: [[09 Kamera i wizja]]. Dalej: [[11 Regulator PID]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Żeby dobrać regulator, musimy wiedzieć, **jak szybko kulka przyspiesza** na przechylonej tacy. To prosta fizyka: im większy przechył, tym większe przyspieszenie. Poniżej wzory i konkretne liczby.

## Wzór

Kulka toczy się bez poślizgu po płaszczyźnie przechylonej o kąt $\theta$. Część energii idzie w obrót, więc przyspieszenie jest mniejsze niż przy ślizganiu:

$$\ddot x=\frac{g\sin\theta}{1+I/(mr^2)}\approx k\,g\,\theta$$

Współczynnik $k$ zależy od budowy kulki:

| Kulka | $k$ | $K=kg$ (m/s² na radian) | Przyspieszenie przy 9° |
| :--- | ---: | ---: | ---: |
| Pingpongowa 2,7 g (cienka powłoka) | 0,6 | 5,89 | 0,92 m/s² |
| Pełna lub golfowa 45 g | 0,714 | 7,01 | 1,10 m/s² |

Dla małych kątów mamy więc układ, w którym **przechył daje przyspieszenie**, a pozycja to jego dwukrotne całkowanie. W języku regulacji to "podwójny integrator". Taki układ sam z siebie **nie ma tłumienia**: raz rozpędzona kulka jedzie, aż się coś stanie. Dlatego w regulatorze potrzebujemy członu D (prędkość), a nie tylko P ([[11 Regulator PID]]).

## Ile czasu zajmuje ruch

Czas przejechania odległości $d$ przy stałym przyspieszeniu: $t=\sqrt{2d/a}$.

| Sytuacja | Czas |
| :--- | ---: |
| 105 mm (od krawędzi do środka), przechył 9° | ok. 0,48 s |
| To samo przy przechyle 3° | ok. 0,83 s |

Prędkość kulki po przejechaniu 100 mm przy przechyle 5° to ok. 0,32 m/s, czyli ok. 6,4 mm na jedną klatkę przy 50 FPS (2–3 piksele). Wniosek: nie jest to wolny proces, ale i nie tak szybki, żeby kamera 50 FPS nie nadążyła.

## Kulka pingpongowa czy golfowa

Kulka pełna (np. golfowa) ma o ok. 19% większe $K$ niż pingpongowa, czyli przy tym samym przechyle przyspiesza mocniej. Wzmocnienie pętli rośnie o tyle samo, więc margines stabilności maleje. Konsekwencja: nastawy dobrane pod pingponga trzeba dla kulki pełnej zmniejszyć o ok. 15%. Dlatego w ustawieniach przechowujemy **osobne profile nastaw** dla każdej kulki ([[22 Firmware - Sterowanie]]).

> [!tip] Dlaczego zaczynamy od pingponga
> Jest najtańsza i najlżejsza, więc najmniej obciąża tacę i serwa, a wszystkie obliczenia w tych notatkach są policzone właśnie dla niej. Dopiero po stabilnej pracy z pingpongiem sprawdzamy inne kulki z osobnym profilem.
