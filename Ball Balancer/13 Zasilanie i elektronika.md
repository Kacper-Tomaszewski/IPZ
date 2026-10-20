---
title: Zasilanie i elektronika
tags:
  - ball-balancer
  - elektronika
  - zasilanie
  - obliczenia
created: 2026-10-20
---

# 13. Zasilanie i elektronika

Poprzednia: [[12 Trajektorie]]. Dalej: [[14 Pinout i połączenia]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Najczęstsza przyczyna dziwnych, trudnych do znalezienia usterek w projektach z serwami to **zasilanie**: spadki napięcia przy ruszaniu serw resetują ESP32, a pływające piny szarpią serwami przy starcie. Tu opisuję, jak się przed tym zabezpieczamy i dlaczego wybraliśmy zasilacz 5 V / 4 A.

> [!info] Wartości prądów
> Prądy poniżej to **oszacowania** (nie zmierzone). Zmierzymy je multimetrem w Etapie 5 ([[19 Plan prac i testy]]).

## Bilans prądu

| Odbiornik | Szczyt |
| :--- | ---: |
| 3× HS-422 (w ruchu, szczyt) | 1,5–2,4 A |
| ESP32 + OLED | ok. 0,25 A |
| ESP32-S3 z kamerą (Wi-Fi wyłączone) | ok. 0,3–0,4 A |
| Pierścień 12× WS2812B przy jasności 25% | ok. 0,2 A (pełna biel: 0,7 A) |
| **Razem** | **ok. 2,3–3,3 A** |

> [!success] Dlaczego 4 A, a nie 3 A
> Zasilacz 3 A pracowałby na granicy przy szczytach. Zasilacz 4 A daje zapas, a różnica w cenie to kilka złotych. Za mały zasilacz objawia się zanikami napięcia i restartami, które trudno zdiagnozować.

## Napięcie: 5 V, nie 6 V

Serwa HS-422 mają większy moment przy 6 V, ale potrzebujemy tylko ok. 0,12 kg·cm z dostępnych ok. 3,3 kg·cm ([[08 Serwa i momenty]]). Zostajemy przy 5 V, bo jedno napięcie dla całości jest prostsze, a zasilanie ESP32 i diod LED z 5 V jest standardowe.

## Zakłócenia od serw

Serwa analogowe w czasie ruchu ciągną krótkie szczyty prądu, które zapadają napięcie. Zabezpieczenia:
- **Kondensator 1000 µF** blisko serw (mamy elektrolity $\ge1000\,\mu$F / 10 V).
- **100 µF + 100 nF** przy każdym z obu ESP32.
- **Zasilanie w gwiazdę** z jednego punktu: serwa mają własne przewody do zasilacza, nie "łańcuszkiem" przez płytkę ESP32.
- **Wspólna masa** między bazą i kamerą (przewód GND w złączu pałąka).

## Poziomy logiczne

| Element | Problem | Rozwiązanie |
| :--- | :--- | :--- |
| **Enkoder KY-040** | Moduł ma rezystory podciągające do pinu `+`. Zasilany z 5 V podawałby 5 V na wejścia ESP32 (3,3 V) | Zasilaj moduł z **3,3 V** |
| **Pierścień WS2812B** | Przy zasilaniu 5 V wymaga logicznej „1" co najmniej $0{,}7\cdot5=3{,}5$ V, a ESP32-S3 daje 3,3 V. Działa „czasem" | Konwerter poziomów **74AHCT125** albo dioda szeregowo w zasilaniu pierścienia (ok. 4,3 V) |
| **UART kamera ↔ baza** | Oba układy 3,3 V | Bez konwersji, tylko wspólna masa |

## Start i bezpieczeństwo

- **Rezystory 10 kΩ** z linii sygnałowej serwa do masy: bez nich pływający pin w pierwszych milisekundach po włączeniu może szarpnąć serwem.
- **Miękki rozruch.** Po włączeniu serwa płynnie dochodzą do pozycji środkowej w 1–2 s.
- **Utrata kamery** (> 100 ms): taca wraca do poziomu spokojnym ruchem, wyświetlacz pokazuje błąd.
- **Utrata kulki** (> 0,5 s): taca wraca do poziomu i czeka.
- **Długie DALEJ** = STOP: natychmiastowe poziomowanie tacy.
- **Zasilanie S3 z dwóch źródeł** (pin 5 V i USB-C naraz): sprawdź schemat płytki, czy jest dioda. Podczas programowania najbezpieczniej zasilać tylko przez USB-C i odłączyć zasilacz.

## Okablowanie pałąka

- **Złącze JST-XH 4-pin:** 5 V, GND, TX, RX.
- **UART jako skręcona para** z przewodem GND, żeby ograniczyć zakłócenia od serw.
- **Przewody silikonowe AWG26–28:** cienkie i elastyczne, mieszczą się w tunelu pałąka 8 × 8 mm (4 przewody).
- **Pałąk odłączany**, żeby można go było zdjąć do transportu i poprawek.
- **Zapasowa taśma FPC:** łatwo ją przerwać przy składaniu.

## Co z innymi napięciami

W projekcie występują tylko 5 V (serwa, LED, zasilanie obu płytek) i 3,3 V (logika, enkoder). Pierścień LED nie wymaga osobnego zasilacza, ale ma najwyższy szczytowy prąd, więc jasność ograniczamy do ok. 25%.
