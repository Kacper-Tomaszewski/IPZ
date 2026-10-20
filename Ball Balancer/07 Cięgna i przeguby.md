---
title: Cięgna i przeguby
tags:
  - ball-balancer
  - mechanika
  - przeguby
  - obliczenia
created: 2026-10-20
---

# 07. Cięgna i przeguby

Poprzednia: [[06 Kinematyka i zakres ruchu]]. Dalej: [[08 Serwa i momenty]]. Powrót: [[Projekt Ball Balancer]]. Kod do druku: [[24 Kod OpenSCAD cięgien]].

## W skrócie

Każde cięgno ma na obu końcach **kostkę Kardana** (dwa obroty w jednym przegubie). To tanie i drukowalne rozwiązanie, ale nie jest identyczne z przegubem kulowym, który zakłada model z [[06 Kinematyka i zakres ruchu]]. Liczby poniżej pokazują, że dla małych przechyłów to działa, a przy dużych zaczyna się klinować. Dlatego mamy limit przechyłu, test przed drukiem całości i plan B.

## Co to jest za przegub

Jedna noga to łańcuch: serwo (obrót) → widełki orczyka → kostka → widełki cięgna → cięgno → widełki cięgna → kostka → uchwyt pod tacą. Każda kostka ma dwie osie obrotu oddalone o 2,8 mm i pozwala widełkom wychylać się w dwóch płaszczyznach.

## Dlaczego przegub krzyżakowy może się klinować

W przegubie kulowym cięgno może się obracać dowolnie. Przegub krzyżakowy pozwala na obrót tylko wokół dwóch osi. Gdy dwa sworznie na końcach cięgna są równoległe, cięgno musi się **dodatkowo skręcić**, kiedy taca jest przechylona. Policzony skręt cięgna:

| Przechył tacy | 2° | 4° | 6° | 8° |
| :--- | ---: | ---: | ---: | ---: |
| Skręt cięgna | 0,8° | 1,6° | 2,4° | 3,2° |

Dla cięgna 54 mm skręt 3° to ok. 0,4 mm przesunięcia bocznego na końcu. Cały luz kostki w widełkach (szczelina 8,4 mm − kostka 8,0 mm) to też 0,4 mm.

> [!success] Co z tego wynika
> - Do **4°** wystarczy sprężystość i luz wydruku. Cięgno się nie klinuje.
> - Przy **8°** skręt zjada cały luz i konstrukcja zacznie się zacierać albo pracować z tarciem.
> - Dlatego przyjęliśmy **limit ±6°** ([[06 Kinematyka i zakres ruchu]]) oraz test przed drukiem całości.

## Luz i drżenie kulki

Luz kostki 0,4 mm daje błąd przechyłu rzędu 0,2–0,4° (oszacowanie). Przy regulatorze to przyczyna **cyklu granicznego**: kulka lekko drży wokół środka, bo luz powoduje "skok" w przechyle przy zmianie kierunku ruchu serwa.

## Test i plan B

1. **Wydrukuj jeden zestaw** (cięgno + 2 kostki + adapter + uchwyt) i złóż ręcznie z serwem.
2. Poruszaj orczykiem w całym zakresie ±35° i przechylaj uchwyt ręką. Ma chodzić płynnie, bez zacierania.
3. Zmierz luz. Cel: $\le0{,}3$ mm.
   - Zbyt luźno: zmniejsz `fork_gap` w kodzie z 8,4 na 8,2 mm.
   - Zbyt ciasno: zwiększ `m2_hole` z 2,05 na 2,15 mm.
4. Jeśli wciąż się klinuje: **plan B**, czyli gotowe łączniki kulowe M3 (używane w modelach RC) w miejscu górnych kostek lub na obu końcach.

> [!tip] Dlaczego kupujemy łączniki kulowe od razu
> To kilkanaście złotych, a dostawa tanich części potrafi trwać tygodnie. Lepiej mieć je w szufladzie, gdy test pokaże problem, niż czekać z całym projektem.

## Śruby i nakrętki

Szerokość widełek: 8,4 mm szczeliny + 2 × 2,8 mm ścianki = **14,0 mm**. Nakrętka samohamowna M2 ma ok. 2,5 mm wysokości. Śruba M2×16 wystaje poza widełki tylko o ok. 2 mm, więc nakrętka nie dochodzi do końca zwoju. Śruby **M2×18–20** dają zapas.

> [!warning] Nie dokręcaj do oporu
> Śruba w przegubie ma być **osią**, a nie zaciskiem. Dokręcenie powoduje tarcie i luz w innym miejscu. Używaj nakrętek samohamownych dokręconych tak, by nic nie kręciło się samo, ale ruch był swobodny.

## Zapas części

Cięgna i kostki to części, które najczęściej się psują przy montażu i kalibracji. Dlatego planujemy **4 zestawy zamiast 3**, a dodatkowo kupon tolerancji z otworami 2,0 / 2,05 / 2,1 / 2,15 mm i szczelinami 8,2 / 8,4 / 8,6 mm. Dzięki temu dobierzemy wartości do własnej drukarki, zanim wydrukujemy cały komplet.
