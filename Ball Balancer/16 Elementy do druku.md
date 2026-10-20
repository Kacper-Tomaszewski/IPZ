---
title: Elementy do druku
tags:
  - ball-balancer
  - druk3d
  - stl
created: 2026-10-20
---

# 16. Elementy do druku

Poprzednia: [[15 Konsola i obsługa]]. Dalej: [[17 Taca, pałąk i baza]]. Powrót: [[Projekt Ball Balancer]].

## W skrócie

Lista wszystkich wydruków, ich stan (gotowe czy do zaprojektowania) i ustawienia. **Kolejność druku jest ważna**: najpierw drukujemy małe części do testów, a dopiero potem duże.

## Lista plików

| Plik | Szt. | Stan |
| :--- | :--- | :--- |
| `00_Kupon_Tolerancji.stl` | 1 | do zaprojektowania (prosty) |
| `01_Baza_Glowna_HS422.stl` | 1 | do zaprojektowania |
| `02_Panel_Konsoli_OLED.stl` | 1 | do zaprojektowania |
| `03_Taca_Robocza_210mm.stl` + `03b_Rant_210mm.stl` | 1 + 1 | do zaprojektowania |
| `04_Adapter_Orczyka_24mm.stl` | 4 | **gotowe**, kod w [[24 Kod OpenSCAD cięgien]] |
| `05_Popychacz_60mm.stl` | 4 | **gotowe** |
| `05b_Kostka_Kardana.stl` | 8 | **gotowe** |
| `05c_Uchwyt_Pod_Tace.stl` | 4 | **gotowe** (do potwierdzenia `pivot_h`) |
| `06_Palak_Dolny.stl` + `07_Palak_Gorny_Kamera.stl` | 1 + 1 | do zaprojektowania |
| Arkusz kalibracyjny (A4, papier) | 1 | do przygotowania |

Liczby sztuk przy cięgnach to zestawy **po 4** (3 użyte + 1 zapasowy), a nie po 3 jak w pierwszej wersji. Powód: [[07 Cięgna i przeguby]].

### Opisy wydruków

- **Baza główna.** Trzy ramiona z kieszeniami na serwa HS-422 (leżą na boku), komora na ESP32 i kondensator 1000 µF, gniazdo zasilania DC. Wkładki gwintowane M3 i stopki gumowe.
- **Panel konsoli.** Przód nachylony 40°, miejsce na ekran OLED, krzyżak strzałek po lewej, pokrętło i DALEJ po prawej. Drukowany licem do stołu.
- **Taca.** Płaska płyta 210 mm z 6 żebrami od spodu, drukowana górną płaszczyzną na gładkim stole. Rant jest osobnym pierścieniem doklejanym po założeniu folii.
- **Adapter orczyka.** Nakładka na oryginalny orczyk HS-422, mocowana dwiema śrubami M2, zakończona widełkami 24 mm od osi.
- **Popychacz + kostki.** Bezluzowe cięgna z przegubami krzyżakowymi na śrubach M2.
- **Uchwyt pod tacę.** Widełki przykręcane od spodu tacy w promieniu 90 mm, śruby M3 w rozstawie 20 mm.
- **Pałąk.** Dwuczęściowe ramię C-Arm z tunelem kablowym 8 × 8 mm, mocowaniem płytki S3-CAM, gniazdem pierścienia LED i regulacją wysokości głowicy ([[17 Taca, pałąk i baza]]).

## Ustawienia druku cięgien

| Parametr | Wartość | Dlaczego |
| :--- | :--- | :--- |
| Warstwa | 0,16–0,20 mm | Dokładność otworów i widełek |
| Obrysy | 4 | Mocne ścianki (części pracują na ścinanie) |
| Wypełnienie | 100% | Małe części, nie opłaca się oszczędzać, a są obciążone |
| Podpory | brak | Kształty są zaprojektowane tak, żeby ich nie potrzebować |

## Kolejność druku (dlaczego taka)

1. **Kupon tolerancji** i **jeden zestaw cięgien**. Sprawdzamy, jak drukarka radzi sobie z otworami 2,0–2,15 mm i szczelinami 8,2–8,6 mm. Jeśli luzy są złe, poprawiamy jedną liczbę w kodzie, zanim wydrukujemy resztę.
2. Pozostałe zestawy cięgien (łącznie 4).
3. Baza i konsola.
4. Taca (długi wydruk, więc dopiero wtedy, gdy wiemy, że wymiary są dobre).
5. Pałąk (po teście kamery, bo ostateczna wysokość głowicy zależy od obiektywu).

## Rzeczy do sprawdzenia po wydruku

- Płaskość tacy ($\le0{,}3$ mm, liniał na tacy, [[17 Taca, pałąk i baza]]).
- Czy kostki kręcą się swobodnie w widełkach, bez luzu większego niż 0,3 mm.
- Czy kieszenie serw przyjmują HS-422 bez siłowania.
