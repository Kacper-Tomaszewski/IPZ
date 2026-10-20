---
title: Taca, pałąk i baza
tags:
  - ball-balancer
  - mechanika
  - obliczenia
created: 2026-10-20
---

# 17. Taca, pałąk i baza

Poprzednia: [[16 Elementy do druku]]. Dalej: [[18 Kalibracja i uruchomienie]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Trzy duże elementy konstrukcji i to, na co w każdym uważamy. W tej notatce są głównie rady praktyczne i jedno ważne obliczenie: **dlaczego pałąk musi być sztywny**.

## Taca

- **Wymiary:** 210 mm, płyta 3 mm, 6 żeber 5 mm, rant 2 × 3,5 mm ([[05 Geometria i wymiary]]).
- **Płaskość.** Duża cienka płyta z PLA lubi się wyginać podczas studzenia. Drukuj na szkle lub PEI z brimem, sprawdź liniałem. Cel: nierówność $\le0{,}3$ mm. Jeśli wygina się za mocno, zwiększ grubość do 4 mm. *Dlaczego:* garb tacy to dla kulki górka i zakłóca ruch tak, jakby ktoś dopisał do modelu stałą siłę.
- **Folia.** Czarna matowa folia samoprzylepna daje stałe tarcie i mały odblask. Naklej ją przed rantem, bez pęcherzy. Rant doklejamy potem.
- **Rant.** Ma 3,5 mm wysokości. To za mało, żeby zatrzymać kulkę lecącą ok. 0,5 m/s, i traktujemy go jako ograniczenie wizualne, a nie fizyczne.
- **Kolor.** Czarna taca i jasna kulka dają największy kontrast dla kamery ([[09 Kamera i wizja]]).

## Pałąk C-Arm

### Dlaczego musi być sztywny

Kamera jest zamocowana do bazy, ale mierzy położenie kulki **względem swojego obrazu**. Jeśli głowica kamery drga lub ugina się, obraz przesuwa się tak, jakby kulka się poruszyła. Policzmy: przechył kamery o zaledwie $0{,}3^\circ$ przesuwa to, co widać pod nią, o:

$$195\cdot\tan0{,}3^\circ\approx1\text{ mm}$$

To jest tyle, ile cała dokładność pomiaru ([[09 Kamera i wizja]]). Szybkie, drobne drgania wprowadzą szum do regulatora.

### Co robimy

- **Grube ścianki:** 4 obrysy, żebro u podstawy słupka.
- **Wzmocnienie:** w razie potrzeby pręt aluminiowy lub węglowy 6–8 mm w osi tunelu kablowego.
- **Podstawa pałąka** jest zintegrowana z serwem 1 (tył), co daje mocne mocowanie w bazie.
- **Regulacja wysokości głowicy 170–210 mm:** szczelina z M3 w słupku. Powód: ostateczną wysokość ustala test z prawdziwym obiektywem ([[09 Kamera i wizja]]).
- **Tunel kablowy 8 × 8 mm** na 4 przewody (5 V, GND, TX, RX), złącze JST-XH przy podstawie.

### Kolizje

Słupek stoi 132 mm od środka, a krawędź tacy sięga 105 mm (plus rant 2 mm), czyli zapas 25–27 mm. Przechył tacy zmienia głównie wysokość krawędzi, a nie jej promień, więc słupka nie dosięgnie.

## Baza

- **Stabilność.** Serwa pracują dynamicznie. Jeśli baza jest lekka i ślizga się po stole, ruchy tacy ją przemieszczą, a kamera będzie "jeździć" względem tacy. Dlatego: stopki gumowe i ewentualnie obciążnik (np. blaszka).
- **Wkładki gwintowane M3 (heat-set).** Wciskane lutownicą, dają gwint, który nie wyrabia się po wielokrotnym skręcaniu (PLA bez wkładek wyrabia gwint po kilku razach).
- **Kieszenie serw** 41,0 × 20,2 mm. Po wydruku sprawdź, czy serwo wchodzi bez siłowania, ale też bez luzu.
- **Orczyk.** Adapter mocuje się dwiema śrubami M2 do oryginalnego orczyka na promieniach 8,0 i 12,5 mm od osi. **Zmierz suwmiarką rzeczywiste otwory** przed finalnym CAD.
- **Komora na elektronikę.** ESP32, kondensator 1000 µF, konwerter poziomów, rezystory 10 kΩ, gniazdo zasilania i włącznik.
- **Kabel do pałąka** wchodzi przez złącze JST, a nie jest wlutowany na stałe.

## Co sprawdzić w CAD

- Taca ↔ konsola przy przechyle 6° i 9° ([[05 Geometria i wymiary]]).
- Orczyk ↔ obudowa serwa przy ±35°.
- Czy wszystkie śruby M2 i M3 mają dostęp od strony montażu.
