---
title: Serwa i momenty
tags:
  - ball-balancer
  - serwa
  - obliczenia
created: 2026-10-20
---

# 08. Serwa i momenty

Poprzednia: [[07 Cięgna i przeguby]]. Dalej: [[09 Kamera i wizja]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Hitec HS-422 jest dla nas **bardzo mocny** (zapas ok. 25–30 razy), więc mocy nie musimy się obawiać. Ograniczeniem nie jest siła, tylko to, że to serwo analogowe: reaguje z opóźnieniem i dobrze przyjmuje sygnał co 20 ms (50 Hz).

## Dane serwa

| Parametr | Wartość |
| :--- | :--- |
| Wymiary | 40,6 × 19,8 × 36,6 mm |
| Moment przy 4,8 V | ok. 3,3 kg·cm |
| Moment przy 6 V | ok. 4,1 kg·cm |
| Prędkość przy 4,8 V | ok. 0,21 s na 60° (ok. 285°/s) |
| Martwa strefa | ok. 8 µs |

> [!warning] Wartość 4,1 kg·cm z pierwszej wersji
> Ten moment dotyczy zasilania **6 V**. My zasilamy z **5 V**, więc liczmy z ok. 3,3 kg·cm. Zapas i tak jest ogromny (niżej), więc zostajemy przy 5 V. Jedno napięcie dla wszystkich układów jest prostsze i bezpieczniejsze dla ESP32.

## Obliczenie: ile naprawdę potrzeba

Ruchoma część to taca z PLA (210 mm × 3 mm, ok. 90–130 g zależnie od wypełnienia), żebra (ok. 7 g), uchwyty, rant i folia. Razem **ok. 100–150 g** plus kulka. Na jedną nogę przypada ok. 40–50 g.

Moment w najgorszym przypadku (orczyk poziomy, cały ciężar nogi na końcu orczyka):

$$M\approx m\cdot L_1\approx 0{,}05\text{ kg}\cdot2{,}4\text{ cm}=0{,}12\text{ kg·cm}$$

To jest ok. **25–30 razy mniej** niż 3,3 kg·cm. Dokładna masa zależy od wydruku (to oszacowanie), ale nawet dwukrotnie cięższa taca nie zmienia wniosku.

> [!info] Czy SG90 by wystarczył?
> SG90 (1,6 kg·cm) też by uniósł taką tacę. Zostawiamy go jako rezerwę. HS-422 jest większy i zwykle ma mniejszy luz w przekładni niż SG90 (do potwierdzenia na własnych egzemplarzach), a dla precyzji luz jest ważniejszy niż sam moment.

## Prędkość

Pasmo regulatora to ok. 2,6 rad/s, czyli 0,4 Hz ([[11 Regulator PID]]). W najgorszym razie orczyk wykonuje ruch o amplitudzie ok. 22° (przechył 6°, [[06 Kinematyka i zakres ruchu]]) z częstotliwością pasma, co daje prędkość szczytową $22^\circ\cdot2{,}6\approx57^\circ$/s. Serwo potrafi ok. 285°/s, więc zapas to ok. 5-krotny. W normalnej pracy (przechyły 1–4°) jest znacznie większy.

## Opóźnienie serwa a regulacja

Serwo nie robi ruchu natychmiast. Szacuję opóźnienie pierwszego rzędu na 50–70 ms (założenie, do zmierzenia). To jedno z dwóch opóźnień (drugie to kamera), które **ograniczają szybkość regulatora**, a nie moc serwa. Dlatego szybsze PID nie pomaga bez szybszego serwa lub kamery ([[11 Regulator PID]]).

## Dlaczego 50 Hz

Serwo analogowe odświeża się wewnętrznie co 20 ms. Wysyłanie sygnału częściej niż 50 Hz nie przyspiesza reakcji, a może wprowadzić drżenie. Dlatego pętla sterowania chodzi na **stałe 50 Hz** zsynchronizowane z PWM, niezależnie od tego, czy kamera daje 50 czy 60 klatek.

## Decyzja: nie zmieniamy serw teraz

Cyfrowe serwa dałyby szybszą reakcję, ale kosztują i nie wiemy jeszcze, czy będą potrzebne. Jeśli po strojeniu nie uda się ustabilizować kulki w paśmie ok. 0,4 Hz, to będzie pierwszy kandydat do zmiany.

## Start serw

Przy włączeniu zasilania piny ESP32 są chwilę "pływające" i serwa mogą szarpnąć. Dlatego:
- rezystory **10 kΩ** z linii sygnałowej każdego serwa do masy,
- włączenie PWM dopiero po ustawieniu pozycji neutralnej,
- miękki rozruch (1–2 s) do pozycji środkowej.

Więcej: [[13 Zasilanie i elektronika]] i [[22 Firmware - Sterowanie]].
