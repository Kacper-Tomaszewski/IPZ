---
title: Kinematyka i zakres ruchu
tags:
  - ball-balancer
  - kinematyka
  - obliczenia
created: 2026-10-20
---

# 06. Kinematyka i zakres ruchu

Poprzednia: [[05 Geometria i wymiary]]. Dalej: [[07 Cięgna i przeguby]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Regulator mówi: "przechyl tacę o tyle w osi X i o tyle w osi Y". Serwa rozumieją tylko "obróć się o taki kąt". **Kinematyka odwrotna** to przeliczenie jednego na drugie. Poniżej pokazuję, jak to liczymy, jaki zakres przechyłu mamy naprawdę i dlaczego ograniczamy go do ±6°.

> [!info] Skąd te liczby
> Zakres przechyłu i kąty serw sprawdziłem skryptem numerycznym (Python). Kod C++ do sterownika jest w [[22 Firmware - Sterowanie]].

## Jak to liczymy

Dla każdej z trzech nóg ustawiamy własny układ: oś **radialna** (od środka na zewnątrz w stronę serwa), oś **styczna** i oś pionowa. Przyjmuję, że orczyk wskazuje **na zewnątrz** przy kącie 0° (założenie, do potwierdzenia przy montażu).

Końcówka orczyka (tam, gdzie zaczyna się cięgno) leży w:

$$\mathbf{A}(\alpha)=\big(R+L_1\cos\alpha\big)\,\mathbf{u}+\big(Z_{servo}+L_1\sin\alpha\big)\,\mathbf{z}$$

Punkt mocowania cięgna na tacy zależy od tego, jak taca jest przechylona (obrót $\mathbf{R}_{pose}$) i o ile podniesiona ($z$):

$$\mathbf{P}=\mathbf{R}_{pose}\,[R\cos\psi,\ R\sin\psi,\ 0]^T+[0,0,z]^T$$

Cięgno jest sztywne, więc odległość między $\mathbf{A}$ a $\mathbf{P}$ musi wynosić $L_2$. Z tego warunku wychodzi równanie, które da się rozwiązać dokładnie:

$$a\cos\alpha+b\sin\alpha=c$$

$$a=p_u-R,\quad b=p_z-Z_{servo},\quad c=\frac{a^2+b^2+p_t^2+L_1^2-L_2^2}{2L_1}$$

gdzie $p_u$, $p_t$, $p_z$ to składowe punktu $\mathbf{P}$: radialna, styczna i pionowa. Wynik:

$$\boxed{\alpha=\operatorname{atan2}(b,a)-\arccos\!\left(\frac{c}{\sqrt{a^2+b^2}}\right)}$$

Jeśli $|c|>\sqrt{a^2+b^2}$, to taka pozycja tacy jest poza zasięgiem. **Sprawdzenie:** dla płaskiej tacy na wysokości 83,0 mm wychodzi $\alpha=0^\circ$ dla wszystkich trzech serw.

## Wyniki: kąty serw przy przechyle

Przechył w stronę serwa 1 (tył), taca na wysokości neutralnej:

| Przechył tacy | Serwo przy którym taca idzie w górę | Pozostałe dwa serwa (w dół) |
| :--- | ---: | ---: |
| 3° | +11,0° | −5,7° |
| 5° | +18,2° | −9,7° |
| 6° | ok. +22° | ok. −12° |
| 7° | +25,4° | −13,8° |
| 9° | +32,7° | −18,0° |
| 10° | +36,5° (poza limitem) | −20,2° |

### Ile naprawdę możemy przechylić

Przy limicie orczyka ±35° maksymalny przechył zależy od kierunku: **od 7,9° (najgorszy kierunek) do 10,2° (najlepszy)**. Wartość "±9°" z pierwszej wersji planu jest więc osiągalna tylko w części kierunków.

Intuicyjnie: nogi leżą na okręgu o promieniu $R$, więc przechył $\theta$ w stronę nogi podnosi ją o $R\tan\theta$. Dla 9° to $90\cdot\tan9^\circ=14{,}3$ mm, a skok serwa wynosi tylko 13,8 mm.

## Decyzja: limit programowy ±6°

> [!success] Dlaczego ±6°, a nie pełne 8–10°
> 1. **Wystarcza do balansowania.** Piłeczka z przyspieszeniem $a=5{,}89\sin\theta$ m/s² przy 6° ma już prawie 0,6 m/s². Typowa praca to 1–4° ([[10 Dynamika kulki]]).
> 2. **Zostaje zapas serwa.** 6° zużywa ok. 22° z 35°, a pozostałe ok. 13° przydaje się na trym, wypoziomowanie i luzy.
> 3. **Przeguby pracują łagodniej.** Przy 6° cięgna muszą się skręcić tylko o ok. 2,4° ([[07 Cięgna i przeguby]]), a przy 8° o 3,2°, czyli tyle, ile wynosi cały luz kostki.
> 4. **Lepsza widoczność kulki.** Mniejszy przechył to mniej odchylonej tacy względem kamery.

## Rozdzielczość

- Sygnał PWM z LEDC (14 bitów, 50 Hz) ma krok $20\text{ ms}/16384=1{,}22\,\mu s$. Przy około 10 µs na stopień serwa (założenie, do zmierzenia w Etapie 0) to ok. 0,12° serwa.
- Przy ramieniu 24 mm to zmiana wysokości o ok. 0,05 mm, czyli zmiana przechyłu tacy o ok. 0,03°.

Dyskretyzacja PWM jest więc zaniedbywalna. Prawdziwe ograniczenia to luzy mechaniczne i martwa strefa serwa analogowego (ok. 8 µs).

## Co jeszcze liczymy

- Dopasowanie nogi do przegubów krzyżakowych, nie kulowych: [[07 Cięgna i przeguby]].
- Siły i prędkości serw: [[08 Serwa i momenty]].
