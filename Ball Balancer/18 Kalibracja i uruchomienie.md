---
title: Kalibracja i uruchomienie
tags:
  - ball-balancer
  - kalibracja
  - testy
created: 2026-10-20
---

# 18. Kalibracja i uruchomienie

Poprzednia: [[17 Taca, pałąk i baza]]. Dalej: [[19 Plan prac i testy]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Żaden egzemplarz zbudowany ręcznie nie jest idealny: serwa mają inne środki, kamera nie jest dokładnie nad środkiem tacy, a obiektyw ma własne zniekształcenia. **Kalibracja** to mierzenie tych różnic i wpisanie ich do pamięci, żeby sterownik o nich wiedział. Poniżej cztery kalibracje i jeden pomiar opóźnienia.

## 1. Serwa (trym)

*Po co:* serwa nie mają dokładnie identycznych środków, a orczyk można nałożyć na wałek z rozdzielczością zębatki.

1. Zasilanie bez cięgien, orczyki luźno na wałkach.
2. Sygnał 1500 µs na wszystkich serwach. Nałóż orczyki tak, by były poziome.
3. Zmierz zakres: ile µs na stopień (zakładamy ok. 10 µs/°, do zmierzenia) dla ±35°.
4. Podłącz cięgna, na ekranie **Trim** ([[15 Konsola i obsługa]]) ustaw taką pozycję, żeby taca była płaska (poziomnica lub liniał).
5. Zapisz trymy w NVS.

## 2. Kamera (skala i środek)

*Po co:* obiektyw 120° zniekształca obraz i potrzebujemy współczynnika $f_{px}$ oraz środka obrazu do przeliczenia pikseli na milimetry ([[09 Kamera i wizja]]).

1. **Arkusz kalibracyjny**: wydruk A4 z okręgami $r=25/50/75/100$ mm i siatką 10 mm. Kładziemy go na tacy tak, by środek okręgów był w środku tacy.
2. Na ekranie **Kalibracja** znajdź środek obrazu i dopasuj $f_{px}$, aż okręgi z arkusza zgodzą się z okręgami modelu.
3. Ustaw obrót i odbicie osi (`swapXY`, `invX`, `invY`), aż strzałka "w prawo" przesuwa punkt zadany w prawo na tacy.
4. Zapisz.

## 3. Próg wykrywania kulki

*Po co:* próg jasności decyduje, które piksele należą do kulki. Zbyt niski doda tło, zbyt wysoki ukróci kulkę.

Z kulką w środku zrób zdjęcie i wyznacz próg (np. metodą Otsu) lub ustaw ręcznie na ekranie 5. Przy stałej ekspozycji i oświetleniu próg zostaje taki sam na długo.

## 4. Auto-trim (poziomowanie)

*Po co:* nawet po kalibracji trym serw bywa o ułamek stopnia niedokładny, a to wystarczy, by kulka spływała w jedną stronę.

Gdy kulka jest od ponad 10 s w odległości $<5$ mm od środka i porusza się wolniej niż 5 mm/s, sterownik zapamiętuje wartość całki PID jako poprawkę przechyłu i zeruje ją. Zapis do NVS po potwierdzeniu w UI. Dzięki temu nie trzeba ręcznie trymować serw do perfekcji.

## 5. Pomiar opóźnienia

*Po co:* nastawy PID ([[11 Regulator PID]]) opierają się na założonym opóźnieniu 40–60 ms. Warto je zmierzyć.

Prosty test: błysk diody LED w polu widzenia kamery i druga dioda lub oscyloskop na wyjściu PWM serwa. Czas od błysku do pierwszej zmiany sygnału to opóźnienie kamery + przetwarzania. Opóźnienie serwa mierzy się ruchem orczyka (odczyt z kamery lub nagranie wideo).

Jeśli wyjdzie większe niż założenie, zmniejszamy $K_p$, bo marża stabilności spada.

## Szum pozycji w spoczynku

Z nieruchomą kulką zapisz pozycję przez 10 s. Odchylenie standardowe powinno być $\le0{,}8$ mm. Jeśli jest większe: sprawdź oświetlenie (migotanie LED), mocowanie głowicy (drgania) i próg.
