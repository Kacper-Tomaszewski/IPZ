---
title: Słowniczek
tags:
  - ball-balancer
  - słowniczek
created: 2026-10-20
---

# 02. Słowniczek

Krótkie wyjaśnienia słów, które padają w notatkach. Powrót: [[Projekt Ball Balancer]].

## Mechanika

- **3-RRS** to nazwa układu: trzy "nogi", każda ma dwa obrotowe przeguby (R, R) i jeden kulowy (S). U nas serwo obraca orczyk (R), a przeguby na końcach cięgna pozwalają mu się wychylać. Zamiast prawdziwych przegubów kulowych mamy kostki Kardana (patrz [[07 Cięgna i przeguby]]), które działają podobnie, ale mają ograniczenia.
- **Orczyk** to ramię przykręcone do wałka serwa. U nas ma 24 mm i nazywamy jego długość $L_1$.
- **Cięgno (popychacz)** to sztywny pręt łączący orczyk z tacą. Ma 60 mm (oś do osi) i długość $L_2$.
- **Kostka Kardana (przegub krzyżakowy)** to mały sześcian z dwoma prostopadłymi osiami. Pozwala cięgnu wychylać się w dwóch kierunkach.
- **Taca** to okrągła płyta, na której toczy się kulka.
- **Pałąk C-Arm** to ramię w kształcie litery C, które trzyma kamerę nad środkiem tacy.
- **Przechył** to kąt, o jaki taca odchyla się od poziomu.

## Sterowanie

- **Setpoint** to punkt, w którym kulka ma stać (albo punkt, po którym ma jechać).
- **Uchyb** to różnica między tym, gdzie kulka ma być, a tym, gdzie jest.
- **PID** to popularny regulator. **P** reaguje na uchyb, **D** na prędkość (tłumi drgania), **I** zbiera drobny, stały błąd i go likwiduje.
- **Kinematyka odwrotna** to obliczenie "jakie kąty serw dadzą taką pozycję tacy".
- **Filtr α-β** to prosty filtr, który z zaszumionych pozycji wylicza gładką pozycję i prędkość.
- **Anty-windup** to zabezpieczenie, żeby część I regulatora nie "nabijała" się za bardzo, gdy układ nie może zareagować.
- **Feed-forward** to podanie z góry przechyłu potrzebnego do jazdy po torze, zanim pojawi się uchyb.
- **Czas martwy (opóźnienie)** to czas między zdarzeniem a reakcją układu. Przeszkadza regulacji.
- **Marża fazowa** mówi, jak daleko regulator jest od niestabilności. Więcej niż 30–40° to rozsądny zapas.

## Wizja

- **Centroid** to środek ciężkości jasnej plamy, czyli środek kulki na obrazie.
- **Subpiksel** to pozycja z dokładnością ułamka piksela, wyliczona ze średniej ważonej jasnością.
- **Dystorsja** to zakrzywienie obrazu typowe dla obiektywów szerokokątnych (skala zmienia się od środka do brzegu).
- **FOV / DFOV** to kąt widzenia kamery (DFOV: po przekątnej).
- **FPS** to liczba klatek na sekundę.
- **Ekspozycja** to czas naświetlania jednej klatki.

## Elektronika

- **UART** to prosta szeregowa magistrala (dwa przewody TX i RX plus masa), tu między kamerą a bazą.
- **PWM** to sposób sterowania serwem: impuls co 20 ms, a jego długość (1–2 ms) oznacza kąt.
- **LEDC** to sprzętowy generator PWM w ESP32. Działa niezależnie od procesora.
- **NVS** to pamięć nieulotna, w której zapisujemy nastawy.
- **Konwerter poziomów (level shifter)** zamienia napięcie 3,3 V z ESP32 na 5 V potrzebne diodom WS2812B.
- **Pull-up** to rezystor podciągający wejście do plusa. Przyciski i enkoder używają go, żeby wiedzieć, kiedy styk jest otwarty.
- **Pin strappingowy** to nóżka układu, której stan przy starcie wpływa na zachowanie układu (np. logi bootu).
- **FPC** to płaska taśma łącząca moduł kamery z płytką.
