---
title: Decyzje i uzasadnienia
tags:
  - ball-balancer
  - decyzje
created: 2026-10-20
---

# 04. Decyzje i uzasadnienia

Powrót: [[Projekt Ball Balancer]].

## W skrócie

Tu zebrane są wszystkie ważne wybory w projekcie, każdy z krótkim „dlaczego" i linkiem do notatki, gdzie jest pełne uzasadnienie. Pierwsza kolumna to to, co było w pierwszej wersji planu, druga to to, co jest teraz.

## Architektura

| Temat | Było | Jest | Dlaczego | Szczegóły |
| :--- | :--- | :--- | :--- | :--- |
| Mikrokontrolery | Dwa (ESP32 + ESP32-S3) | Bez zmian | Ekran i zapis nastaw nie mogą opóźniać regulatora | [[01 Jak to działa]] |
| Tryb pracy | Offline, bez PC | Bez zmian | Założenie projektu, mniej opóźnień (bez Wi-Fi) | [[01 Jak to działa]] |
| Układ nóg | 3-RRS, 3 serwa co 120° | Bez zmian | Sztywny, symetryczny, najprostszy do obliczenia | [[01 Jak to działa]] |

## Mechanika

| Temat | Było | Jest | Dlaczego | Szczegóły |
| :--- | :--- | :--- | :--- | :--- |
| Wysokość tacy w pozycji neutralnej | 92 mm | **96,5 mm** | Wynika z geometrii uchwytu. Zmiana uchwytu byłaby gorsza niż zmiana liczby | [[05 Geometria i wymiary]] |
| Limit przechyłu | ±9° | **±6°** (programowo) | Realny zakres to 7,9–10,2°, przeguby krzyżakowe kłopotliwe przy dużych kątach, a balansowanie potrzebuje 1–4° | [[06 Kinematyka i zakres ruchu]] |
| Etykiety serw 2 i 3 | 210° = prawo | 210° = **lewo** | Zgodność ze standardowym układem współrzędnych | [[05 Geometria i wymiary]] |
| Przeguby cięgien | Same kostki Kardana | Kostki + **8 łączników kulowych na plan B** | Kostki mogą się klinować przy dużych przechyłach | [[07 Cięgna i przeguby]] |
| Śruby w przegubach | M2×16 | **M2×18–20**, nakrętki samohamowne | Przy 16 mm nakrętka nie dochodzi do końca zwoju | [[07 Cięgna i przeguby]] |
| Zestawy cięgien | 3 | **4** | Zapas na uszkodzenia | [[07 Cięgna i przeguby]] |
| Wysokość kamery | 195 mm, stała | 195 mm, **regulowana 170–210 mm** | Obniżenie dałoby ok. 10% w skali, ale grozi wypadnięciem kulki z kadru | [[09 Kamera i wizja]] |
| Sztywność pałąka | nieomawiana | Grubsze ścianki, wzmocnienie prętem | Drżenie pałąka wygląda jak ruch kulki | [[17 Taca, pałąk i baza]] |
| Baza | bez uwag | Stopki, wkładki heat-set | Baza nie może wędrować | [[17 Taca, pałąk i baza]] |
| Uchwyty pod tacą | 3 osobne, przykręcane M3 | **Widełki drukowane razem z tacą** | 3 wydruki, 6 śrub i 6 nakrętek mniej; promień 90 mm i wysokość osi wynikają z jednego wydruku, bez błędu montażu. Złamane widełki = nowa taca | [[26 Projekt Fusion 360]] |
| Widełki orczyka i tacy | sworzeń pionowy / poziomy | **Sworzeń prostopadły do cięgna (pochylony o 23,6°)** | Kostki leżą na osi cięgna, więc $L_2=60$ mm i góra tacy 96,5 mm są dokładne | [[26 Projekt Fusion 360]] |

## Kamera i wizja

| Temat | Było | Jest | Dlaczego | Szczegóły |
| :--- | :--- | :--- | :--- | :--- |
| Obiektyw | 120° | Bez zmian | Standardowy 65° nie obejmuje tacy | [[09 Kamera i wizja]] |
| Przeliczenie pikseli | Wprost | **Korekcja dystorsji** | Skala zmienia się o 28% od środka do brzegu | [[09 Kamera i wizja]] |
| Pozycja kulki | Środek plamy | **Centroid z wagami (subpiksel)** | Dokładność ułamka piksela | [[09 Kamera i wizja]] |
| Ustawienia czujnika | Auto | **Ręczne**, stała ekspozycja | Automatyka zmienia FPS i jasność | [[09 Kamera i wizja]] |
| Rozdzielczość | QQVGA | QQVGA, test **QVGA** | Lepsza skala, jeśli FPS pozwoli | [[09 Kamera i wizja]] |
| Jasność LED | Dowolna | ok. 25%, stała w trakcie pomiaru | Migotanie PWM zmienia jasność klatek | [[09 Kamera i wizja]] |

## Sterowanie

| Temat | Było | Jest | Dlaczego | Szczegóły |
| :--- | :--- | :--- | :--- | :--- |
| Nastawy PID | do ustalenia | **Kp 0,0229 °/mm, Kd 0,0229 °·s/mm, Ki 0,0015** | Policzone z uwzględnieniem opóźnień | [[11 Regulator PID]] |
| Prędkość | Różnica pozycji | **Filtr α-β** | Różnicowanie szumu jest bezużyteczne | [[11 Regulator PID]] |
| Częstotliwość pętli | z kamerą (50–60 Hz) | **Stałe 50 Hz** | Serwo analogowe odświeża się co 20 ms | [[08 Serwa i momenty]] |
| Ramka UART | 5 B | **9 B z sumą** | Wykrywanie błędów i zgubionych ramek | [[20 Firmware - Protokół UART]] |
| Sterowanie po torze | tylko "feed-forward" jako pomysł | **Feed-forward obowiązkowy**, z wyprzedzeniem 0,1 s i współczynnikiem $k_{ff}$ | Sam PID dałby ok. 44 mm błędu na okręgu 60 mm przy 1,5 rad/s | [[12 Trajektorie]] |
| Limity toru | brak | **Przechył 3° na ff + 3° na regulator; najwyższa składowa ≤ 1,5 rad/s; wychylenie ≤ 70 mm** | Dwa niezależne ograniczenia (fizyka i pasmo pętli) | [[12 Trajektorie]] |
| Zmiana punktu i start toru | skok | **Płynny profil (minimum jerk), narastanie $\omega$** | Skoki szarpią tacą i pobudzają luzy | [[12 Trajektorie]] |
| Pomiar $K$ kulki | z teorii | **Zmierzony na tacy** | Dokładność $K$ decyduje o błędzie śledzenia | [[18 Kalibracja i uruchomienie]] |
| Poziomowanie | ręczne | **Auto-trim** | Mniej ręcznej pracy | [[18 Kalibracja i uruchomienie]] |

## Elektronika

| Temat | Było | Jest | Dlaczego | Szczegóły |
| :--- | :--- | :--- | :--- | :--- |
| Zasilacz | 5 V, 3 A (lub 4 A) | **5 V / 4 A** | Szczyt poboru 2,3–3,3 A | [[13 Zasilanie i elektronika]] |
| Napięcie serw | nieokreślone | **5 V** | Zapas momentu jest ogromny | [[08 Serwa i momenty]] |
| Enkoder KY-040 | nieokreślone | **zasilany z 3,3 V** | Moduł ma pull-upy do VCC | [[13 Zasilanie i elektronika]] |
| Dane WS2812B | wprost | **wprost, pierścień zasilany przez diodę 1N4001** (wcześniej 74AHCT125) | Przy ok. 4,25 V na pierścieniu próg „1” to ok. 3,0 V, więc 3,3 V wystarcza. Jeden element zamiast układu scalonego | [[13 Zasilanie i elektronika]] |
| Piny serw przy starcie | bez zabezpieczeń | **Rezystory 10 kΩ + rampa** | Pływające piny szarpią serwami | [[13 Zasilanie i elektronika]] |
| Okablowanie pałąka | nieokreślone | **JST-XH 4-pin, skręcona para** | Odłączalny pałąk, mniej zakłóceń | [[13 Zasilanie i elektronika]] |
| Ekran kalibracji | brak | **Ekran 5** | Kalibracja bez komputera | [[15 Konsola i obsługa]] |

## Proces

| Temat | Było | Jest | Dlaczego | Szczegóły |
| :--- | :--- | :--- | :--- | :--- |
| Kolejność | zakupy → CAD → druk | **walidacja → test wizji → reszta** | Najpierw sprawdzamy największe ryzyka | [[19 Plan prac i testy]] |
| Narzędzia kodu | dowolne | **PlatformIO, wspólny protocol.h, params.scad** | Spójność i powtarzalność | [[23 Firmware - Narzędzia i struktura]] |
| Budżet | 100–110 zł | **160–190 zł** (orientacyjnie) | Dodatki, których brakowało | [[03 Lista rzeczy do projektu]] |

## Czego świadomie nie robimy

- **Brak IMU na tacy.** Kamera daje wystarczającą informację, a IMU dodaje kod i usterki.
- **Brak Wi-Fi.** Założenie offline i mniej opóźnień.
- **Brak wymiany serw teraz.** HS-422 mają zapas momentu; cyfrowe serwa rozważamy dopiero, jeśli regulacja nie wyjdzie ([[08 Serwa i momenty]]).
- **Brak zmian wymiarów poza `params.scad`.** Jedno źródło prawdy ([[23 Firmware - Narzędzia i struktura]]).
