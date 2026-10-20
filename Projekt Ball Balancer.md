---
title: Projekt Ball Balancer 3-RRS
tags:
  - projekt
  - esp32
  - druk3d
  - pid
  - robotyka
  - ball-balancer
status: v2 po przeglądzie, etap walidacji przed zakupami
created: 2026-10-20
version: 2
aliases:
  - Ball Balancer
  - Hub Ball Balancer
---

# 🎯 Projekt Ball Balancer 3-RRS

> [!abstract] W jednym zdaniu
> Autonomiczny (bez komputera i Wi-Fi) stół, który **utrzymuje piłeczkę w zadanym punkcie albo prowadzi ją po wybranym torze**. Okrągła taca 210 mm jest przechylana przez trzy serwa, a pozycję piłeczki widzi kamera na pałąku nad tacą. Nastawy zmieniamy lokalnie: ekran, strzałki i pokrętło.

To jest **spis treści** projektu. Każda notatka ma jeden temat, zaczyna się od krótkiego „w skrócie" i wyjaśnia, **dlaczego** podjęliśmy dane decyzje. Obliczenia są przy tych tematach, których dotyczą.

**Stan projektu:** wersja 2 (po przeglądzie ustaleń). Teraz jesteśmy przed etapem zakupów. Najpierw sprawdzamy największe ryzyka (cięgna i kamera) na małym, tanim zestawie ([[19 Plan prac i testy]]).

---

## Zacznij tutaj

| Notatka | O czym |
| :--- | :--- |
| [[01 Jak to działa]] | Opis projektu, schemat, kryteria sukcesu |
| [[02 Słowniczek]] | Wyjaśnienie trudnych słów |
| [[03 Lista rzeczy do projektu]] | **Wszystko, co mamy i co kupić**, budżet, narzędzia, rzeczy do sprawdzenia przed zamówieniem |
| [[04 Decyzje i uzasadnienia]] | Co zmieniliśmy względem pierwszego planu i dlaczego |
| [[19 Plan prac i testy]] | Etapy, kryteria przejścia dalej, ryzyka |

## Mechanika i obliczenia

| Notatka | O czym |
| :--- | :--- |
| [[05 Geometria i wymiary]] | Wszystkie wymiary, wysokość tacy, kolizje |
| [[06 Kinematyka i zakres ruchu]] | Jak z przechyłu tacy liczymy kąty serw, ile można przechylić |
| [[07 Cięgna i przeguby]] | Kostki Kardana, luz, test, plan B |
| [[08 Serwa i momenty]] | Czy serwa mają dość siły, szybkość, opóźnienie |
| [[17 Taca, pałąk i baza]] | Płaskość tacy, sztywność pałąka, stabilność bazy |
| [[16 Elementy do druku]] | Lista wydruków i ich kolejność |
| [[24 Kod OpenSCAD cięgien]] | Gotowy kod do druku cięgien |
| [[26 Projekt Fusion 360]] | **Model całości w Fusion 360** (skrypt): przechylanie, test kolizji, eksport STL |

## Wizja, fizyka i regulacja

| Notatka | O czym |
| :--- | :--- |
| [[09 Kamera i wizja]] | Obiektyw 120°, dokładność, oświetlenie, wysokość kamery |
| [[10 Dynamika kulki]] | Jak szybko kulka przyspiesza |
| [[11 Regulator PID]] | Nastawy, filtr prędkości, strojenie |
| [[12 Trajektorie]] | Jazda po okręgu, ile można przechylić |

## Elektronika i obsługa

| Notatka | O czym |
| :--- | :--- |
| [[13 Zasilanie i elektronika]] | Prąd, napięcia, zabezpieczenia, okablowanie |
| [[14 Pinout i połączenia]] | Piny obu płytek |
| [[15 Konsola i obsługa]] | Ekrany, przyciski, pokrętło, zapis nastaw |
| [[18 Kalibracja i uruchomienie]] | Kalibracje serw i kamery, auto-trim |

## Firmware

| Notatka | O czym |
| :--- | :--- |
| [[20 Firmware - Protokół UART]] | Format ramki z kamery do bazy |
| [[21 Firmware - Kamera]] | Zadania płytki z kamerą |
| [[22 Firmware - Sterowanie]] | Rdzenie, stany, kinematyka, filtr, PID |
| [[23 Firmware - Narzędzia i struktura]] | PlatformIO, struktura repo, biblioteki |
| [[25 Firmware - Generator trajektorii]] | Okrąg, ósemka, kwadrat, ruch między punktami, regulator z feed-forward |

---

## Kolejne sesje (co jeszcze trzeba wygenerować)

1. ~~OpenSCAD #2: baza główna i panel konsoli (z `params.scad`).~~ Zrobione w Fusion 360: [[26 Projekt Fusion 360]].
2. ~~OpenSCAD #3: taca z uchwytami, pałąk C-Arm z regulacją wysokości kamery.~~ Zrobione w Fusion 360: [[26 Projekt Fusion 360]]. Pierwsze uruchomienie w Fusion = sprawdzenie skryptu.
3. Firmware kamery (po Etapie 1 testów).
4. Firmware bazy (po Etapie 5).

> [!tip] Zasada dla kodu OpenSCAD
> Cały kod OpenSCAD jest w czystym ASCII, bez polskich znaków nawet w komentarzach (parser w przeglądarkowym `/playground.scad` bywa na nie wrażliwy).

## Prompt startowy do nowego czatu

```text
Kontynuujemy budowe projektu Ball Balancer 3-RRS wedlug notatek v2 z Obsidiana (folder "Ball Balancer", spis w "Projekt Ball Balancer"). Decyzje v2 (limit przechylu 6 stopni, gora tacy 96.5 mm, kamera 195 mm regulowana 170-210, ramka UART 9 B, PD + filtr alfa-beta, zasilacz 5V/4A) sa ustalone. Kod OpenSCAD generuj w 100% w czystym ASCII (bez polskich znakow, takze w komentarzach), parametry trzymaj w params.scad.
Oto notatki:
[TUTAJ WKLEJ POTRZEBNE NOTATKI]
```
