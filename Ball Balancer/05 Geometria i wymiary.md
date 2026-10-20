---
title: Geometria i wymiary
tags:
  - ball-balancer
  - mechanika
  - obliczenia
created: 2026-10-20
---

# 05. Geometria i wymiary

Powrót: [[Projekt Ball Balancer]]. Dalej: [[06 Kinematyka i zakres ruchu]].

## W skrócie

Wszystkie wymiary konstrukcji w jednym miejscu, razem z obliczeniami, które pokazują, że do siebie pasują. W tym pliku jest też **zmiana względem pierwszej wersji**: górna powierzchnia tacy w pozycji neutralnej ma być na 96,5 mm, nie 92 mm.

## Tabela wymiarów

| Część | Parametr | Wartość | Uwagi |
| :--- | :--- | :--- | :--- |
| **Taca** | Średnica całkowita | 210 mm | Maksimum, jakie mieści się w jednym kawałku na stole 220×220 mm |
| | Średnica robocza | 206 mm | W środku rantu |
| | Rant | 2,0 mm szer., 3,5 mm wys. | Drukowany osobno, doklejany po założeniu folii |
| | Płyta + żebra | 3 mm + 5 mm | 6 żeber promieniowych od spodu, wypełnienie Gyroid 15% |
| | Promień punktów podparcia $R_{plate}$ | 90 mm | 3 uchwyty M3, co 120° |
| **Baza i serwa** | Promień osi serw $R_{base}$ | 90 mm | Osie serw dokładnie pod uchwytami tacy |
| | Kieszeń na serwo HS-422 | 41,0 × 20,2 mm | Korpus 40,6 × 19,8 mm + 0,4 mm tolerancji druku |
| | Rozstaw śrub serwa | 48,5 × 10,0 mm | 4 otwory ⌀2,5 mm |
| | Wysokość osi serwa $Z_{servo}$ | 28 mm | Serwa leżą na boku |
| **Ruch** | Orczyk $L_1$ | 24 mm | Od osi serwa do osi przegubu |
| | Cięgno $L_2$ | 60 mm | 54,4 mm pręt + 2 × 2,8 mm na kostki Kardana |
| | Zakres orczyka | ±35° | Skok pionowy ±13,8 mm |
| **Pałąk C-Arm** | Wysięg od środka | 132 mm | Zapas 27 mm od krawędzi tacy |
| | Kamera nad tacą | **195 mm, regulacja 170–210 mm** | Patrz [[09 Kamera i wizja]] |
| **Konsola** | Płyta czołowa | 120 × 62 mm, nachylenie 40° | Z przodu, między serwami 2 i 3 |

### Kąty serw (widok z góry, serwo 1 z tyłu)

| Serwo | Kąt $\psi$ | Położenie |
| :--- | :--- | :--- |
| 1 | 90° | tył (zintegrowane z podstawą pałąka) |
| 2 | 210° | przód-**lewo** |
| 3 | 330° | przód-**prawo** |

> [!note] Dlaczego poprawiliśmy etykiety serw 2 i 3
> W pierwszej wersji kąt 210° był podpisany jako "przód-prawo". Przy zwykłym układzie współrzędnych (oś X w prawo, oś Y od patrzącego w głąb, serwo 1 z tyłu) kąt 210° ma ujemny X, czyli leży po **lewej**. Sam układ działa tak samo, ale pomylone etykiety łatwo zamieniają osie w kodzie albo przewody serw. Wolimy to ujednolicić na początku.

## Obliczenia

### Wysokość cięgna w pozycji neutralnej

Gdy orczyk jest poziomy, a górny przegub leży dokładnie nad osią serwa, poziomy dystans cięgna to długość orczyka. Z twierdzenia Pitagorasa:

$$h_0=\sqrt{L_2^2-L_1^2}=\sqrt{60^2-24^2}=\sqrt{3024}\approx 55{,}0\text{ mm}$$

Oś górnego przegubu jest więc na wysokości

$$Z_{pivot}=Z_{servo}+h_0=28+55{,}0=83{,}0\text{ mm}$$

### Skąd 96,5 mm zamiast 92 mm

W pierwszej wersji przyjęto górę tacy na 92 mm, czyli 9 mm nad osią przegubu. Uchwyt pod tacę (`plate_mount_bracket`) ma jednak oś przegubu 10,5 mm od swojej płaszczyzny mocowania (parametr `pivot_h = 10.5`). Gdy uchwyt przykręcimy do spodu tacy (płyta 3 mm):

$$Z_{top}=83{,}0+10{,}5+3{,}0=96{,}5\text{ mm}$$

> [!success] Dlaczego nie zmniejszamy `pivot_h`, żeby wrócić do 92 mm
> Kostka Kardana ma 10 mm wysokości i musi się zmieścić w widełkach uchwytu. Przy `pivot_h` około 6 mm zahaczałaby o podstawę uchwytu. Łatwiej zmienić jedną liczbę w planie (wysokość tacy) niż przerabiać gotowy, sprawdzony kształt uchwytu.
>
> To jest wartość **nominalna, do potwierdzenia w CAD** po obróceniu uchwytu pod tacę. Od niej liczymy wysokość pałąka. Kamera ma być regulowana, więc ewentualne różnice kilku milimetrów nie zepsują projektu.

Wysokość kamery nad blatem: $96{,}5+195=291{,}5$ mm.

### Skok i przesunięcie końcówki orczyka

Pionowy skok końcówki to $\Delta z=L_1\sin\alpha$:

$$\alpha=\pm35^\circ:\quad \Delta z=24\cdot\sin35^\circ=\pm13{,}77\text{ mm}$$

Końcówka przesuwa się też poziomo (do środka lub od środka), bo porusza się po łuku:

$$\Delta u=L_1(1-\cos35^\circ)=4{,}34\text{ mm}$$

To przesunięcie jest powodem, dla którego kinematyka nie jest zwykłym "serwo w górę = taca w górę". Dlatego liczymy ją dokładnie ([[06 Kinematyka i zakres ruchu]]).

### Gdzie może dojść do kolizji

Przy przechyle tacy krawędź (promień 105 mm) idzie w górę po jednej stronie i w dół po drugiej. Wysokość zmiany: $105\cdot\sin\theta$.

| Przechył $\theta$ | Zmiana wysokości krawędzi |
| :--- | ---: |
| 6° (limit programowy) | 11,0 mm |
| 9° (maksimum konstrukcji) | 16,4 mm |

Spód tacy jest na $96{,}5-3{,}0=93{,}5$ mm. Najniższy punkt spodu przy przechyle 6° to $93{,}5-11{,}0=82{,}5$ mm, a koniec żebra (5 mm niżej) to ok. 77,5 mm. Elementy bazy i konsola pod krawędzią tacy muszą mieć górę **poniżej** tej wysokości, albo leżeć dalej niż promień 105 mm.

Do sprawdzenia w CAD:
- taca ↔ konsola,
- taca ↔ słupek pałąka (poziomo 27 mm zapasu, ale warto sprawdzić z rantem),
- orczyk ↔ obudowa serwa przy ±35°.

## Dlaczego te wymiary

- **Taca 210 mm:** największa, jaka mieści się w jednym kawałku na stole 220×220 mm. Większa taca daje kulce więcej miejsca, a nie wymaga sklejania.
- **Promień 90 mm dla serw i uchwytów:** uchwyty są dokładnie nad osiami serw, więc cięgna stoją prawie pionowo, a siła z serwa idzie wprost do góry. Taka symetria upraszcza obliczenia.
- **Orczyk 24 mm, cięgno 60 mm:** krótki orczyk daje precyzję (mały ruch tacy na stopień serwa), a dostatecznie długie cięgno ogranicza zmianę jego kąta podczas pracy.
- **Serwa na boku, oś 28 mm nad blatem:** orczyk nie uderza w stół nawet przy $-35^\circ$.
