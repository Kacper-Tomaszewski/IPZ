---
title: Trajektorie
tags:
  - ball-balancer
  - trajektorie
  - obliczenia
  - sterowanie
created: 2026-10-20
---

# 12. Trajektorie

Poprzednia: [[11 Regulator PID]]. Dalej: [[13 Zasilanie i elektronika]]. Powrót: [[Projekt Ball Balancer]]. Kod generatora: [[25 Firmware - Generator trajektorii]].

## W skrócie

Oprócz trzymania kulki w miejscu chcemy, żeby jeździła po okręgu, ósemce czy kwadracie. Żeby kulka jechała po łuku, musi mieć przyspieszenie skierowane do środka łuku. Wiemy, jak je wytworzyć (przechyłem tacy), więc podajemy ten przechył regulatorowi **z góry**, zamiast czekać, aż pojawi się błąd. To się nazywa **feed-forward** (sprzężenie w przód).

> [!warning] Feed-forward nie jest dodatkiem, tylko warunkiem
> Policzyłem, co zrobiłby sam regulator PID bez feed-forward ([[11 Regulator PID]]): przy okręgu $r=60$ mm i $\omega=1{,}5$ rad/s błąd śledzenia wyszedłby **ok. 44 mm**, czyli o wiele więcej niż wymagane 10 mm. Powód: pętla ma ograniczone pasmo (ok. 2,6 rad/s) i przy tej częstotliwości reaguje już z dużym opóźnieniem. Dopiero przechył policzony z góry sprawia, że regulator tylko poprawia małe odchyłki.

## Jak działa sterowanie po torze

Dotychczas regulator miał punkt zadany stały. Dla toru punkt zadany się porusza, więc generator torów podaje w każdym kroku (co 20 ms) trzy rzeczy:

- $p_{ref}$: gdzie kulka ma być teraz,
- $v_{ref}$: z jaką prędkością ma się tam poruszać,
- $a_{ref}$: z jakim przyspieszeniem.

Przechył tacy to suma czterech składników:

$$\theta=\underbrace{K_p\,(p_{ref}-\hat x)}_{\text{poprawka położenia}}+\underbrace{K_d\,(v_{ref}-\hat v)}_{\text{poprawka prędkości}}+\underbrace{K_i\!\int(p_{ref}-\hat x)\,dt}_{\text{całka}}+\underbrace{k_{ff}\,\frac{a_{ref}(t+t_{lead})}{K}}_{\text{feed-forward}}$$

- Dla punktu stałego $v_{ref}=0$ i $a_{ref}=0$, więc wzór sprowadza się do zwykłego PID z [[11 Regulator PID]].
- **Feed-forward nie zmienia stabilności pętli.** Działa tylko jak dodatkowe wejście, więc nastawy z [[11 Regulator PID]] zostają bez zmian.
- $k_{ff}$ to współczynnik korekcji feed-forward (domyślnie 1,0). Poprawia błąd, jeśli rzeczywiste $K$ kulki różni się od założonego.
- $t_{lead}$ to wyprzedzenie. Feed-forward przechodzi przez to samo opóźnienie serwa i kamery co sygnał regulatora, więc liczymy go dla chwili $t+t_{lead}$ zamiast $t$ (domyślnie 0,1 s, do strojenia).

## Dlaczego feed-forward z wyprzedzeniem

Policzyłem, ile z tego sygnału "dojdzie" do kulki, gdyby serwo i kamera były idealne, a ile dochodzi realnie. Sygnał przechodzi przez opóźnienie serwa $\tau_s\approx0{,}06$ s i czas martwy $T_d\approx0{,}05$ s, więc dociera z lekkim spóźnieniem. Dla okręgu $r=60$ mm szacowany błąd śledzenia wynosi:

| $\omega$ | Okres okrążenia | Sam PID | Z feed-forward bez wyprzedzenia | Z wyprzedzeniem 0,1 s | Z wyprzedzeniem 0,1 s i błędem $K$ o ±20% |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1,0 rad/s | 6,3 s | 23 mm | 2,5 mm | 0,2 mm | 4,6 mm |
| 1,5 rad/s | 4,2 s | 44 mm | 7,3 mm | 0,7 mm | **9 mm** (8,7 / 9,1) |
| 2,0 rad/s | 3,1 s | 66 mm | 14,5 mm | 1,4 mm | 13–14 mm |

> [!info] Jak to czytać
> Liczby pochodzą z liniowego modelu z [[11 Regulator PID]], który zakłada idealnie znane $K$, brak luzów i brak tarcia. **Prawdziwy błąd będzie większy.** Tabela pokazuje wniosek jakościowy: (1) samo PID nie wystarcza, (2) wyprzedzenie czasowe pomaga bardzo, (3) po zastosowaniu obu **dokładność $K$ decyduje o wyniku**. Błąd $K$ o 20% (w którąkolwiek stronę) daje już ok. 9 mm przy 1,5 rad/s, czyli praktycznie granicę 10 mm, a w prawdziwym układzie dojdą luzy i tarcie.
>
> Dlatego $K$ trzeba **zmierzyć**, a nie zakładać ([[18 Kalibracja i uruchomienie]]), i dlatego w menu jest współczynnik $k_{ff}$. Jeśli kryterium 10 mm przy 1,5 rad/s nie zostanie spełnione, bezpiecznie schodzimy do 1,0 rad/s, gdzie błąd jest ok. 2 razy mniejszy.

## Rodzaje trajektorii

Wszystkie tory są zdefiniowane względem środka $(x_0,y_0)$, który domyślnie leży w środku tacy. $\varphi$ to faza, rosnąca z prędkością $\omega$.

| Tor | Definicja | Szczytowe przyspieszenie | Najwyższa składowa częstotliwości |
| :--- | :--- | :--- | :--- |
| **Punkt (stop)** | stały punkt zadany ($\mathbf{p}=$ const) | 0 | – |
| **Okrąg** | $x=r\cos\varphi,\ y=r\sin\varphi$ | $\omega^2 r$ | $\omega$ |
| **Ósemka** | $x=A\sin\varphi,\ y=\tfrac{A}{2}\sin 2\varphi$ | $2{,}125\,\omega^2 A$ | $2\omega$ |
| **Kwadrat z zaokrąglonymi rogami** | półbok $A$, promień rogu $r_c$, stała prędkość $v$ po torze | $v^2/r_c$ na rogach | ok. $v/r_c$ |
| **Lissajous $a{:}b$** | $x=A\sin(a\varphi),\ y=A\sin(b\varphi+\delta)$ | do ok. $\sqrt{a^4+b^4}\,\omega^2 A$ | $\max(a,b)\,\omega$ |

Szczytowe przyspieszenie ósemki ($2{,}125\,\omega^2A$) wyznaczyłem numerycznie. Jej szczytowa prędkość to $1{,}41\,\omega A$.

### Kierunek

Okrąg i ósemka można puszczać w obie strony (zgodnie z ruchem wskazówek zegara lub przeciwnie). Znak $\omega$ zmienia kierunek.

## Limity: ile naprawdę można

Mamy dwa niezależne ograniczenia i **stosujemy to, które jest ostrzejsze**.

### 1. Limit przechyłu (fizyka)

Całkowity przechył to ±6°. Dzielimy go: **3° na feed-forward i 3° na regulator** (poprawki). Przy 3° dostępne przyspieszenie to

$$a_{ff,max}=K\sin3^\circ\approx5{,}89\cdot0{,}0523=0{,}31\text{ m/s}^2$$

Stąd dla okręgu: $\omega\le\sqrt{a_{ff,max}/r}$:

| Promień $r$ | 40 mm | 60 mm | 70 mm |
| :--- | ---: | ---: | ---: |
| $\omega_{max}$ z limitu przechyłu | 2,8 rad/s | 2,3 rad/s | 2,1 rad/s |

### 2. Limit pasma pętli

Pętla zamknięta ma pasmo ok. 2,6 rad/s ([[11 Regulator PID]]). Tor zawiera składowe o różnych częstotliwościach, a najszybsza z nich nie powinna przekraczać **1,5 rad/s**. Stąd:

| Tor | Limit prędkości |
| :--- | :--- |
| Okrąg | $\omega\le1{,}5$ rad/s |
| Ósemka | $2\omega\le1{,}5$, czyli $\omega\le0{,}75$ rad/s (okrążenie w ok. 8,4 s) |
| Kwadrat | $v\le\min(1{,}5\,r_c,\ \sqrt{a_{ff,max}\,r_c})$ |
| Lissajous $a{:}b$ | $\omega\le1{,}5/\max(a,b)$ |

Przykład kwadratu: dla $r_c=30$ mm limit pasma daje $v\le45$ mm/s, a limit przechyłu $\sqrt{0{,}31\cdot0{,}03}=96$ mm/s. Wygrywa pierwszy: **45 mm/s**.

> [!tip] Dlaczego dzielimy 3° + 3°
> Gdyby sam feed-forward zużył cały przechył, regulator nie miałby już zapasu na poprawianie błędu i kulka w zakręcie uciekałaby. Połowa dla każdego to bezpieczny punkt wyjścia.

### 3. Rozmiar toru

Kulka o średnicy 40 mm może dotykać rantu, gdy jej środek jest 83 mm od środka tacy (promień roboczy 103 mm minus promień kulki 20 mm). Dla zapasu na błąd śledzenia (do 10 mm) przyjmujemy:

- **maksymalne wychylenie toru od środka ≤ 70 mm** (w menu: promień 20–70 mm, krok 5 mm),
- dla kwadratu: odległość narożnika od środka $(A-r_c)\sqrt2+r_c\le70$ mm.

## Tabela przechyłu feed-forward dla okręgu

Wartość $\theta_{ff}=\omega^2 r/K$:

| Promień $r$ | $\omega=1{,}0$ rad/s | $\omega=1{,}5$ rad/s | $\omega=2{,}0$ rad/s |
| :--- | ---: | ---: | ---: |
| 40 mm | 0,39° | 0,88° | 1,56° |
| 60 mm | 0,58° | 1,31° | 2,34° |
| 70 mm | 0,68° | 1,53° | 2,73° |

Przykład: okrąg $r=60$ mm przy $\omega=1{,}5$ rad/s wymaga ok. 1,3° przechyłu, a kulka jedzie z prędkością $\omega r=90$ mm/s. Po prawej stronie tabeli ($\omega=2$) sam feed-forward zbliża się do 3° przydzielonych temu składnikowi.

## Zmiana punktu zadanego (strzałki, start toru)

Gdy przesuwamy punkt zadany strzałkami albo każemy kulce dojechać do początku toru, **nie wolno skakać skokiem** (regulator by szarpał tacą). Płynny ruch z punktu $p_0$ do $p_1$ zapewnia profil o minimalnym szarpnięciu (*minimum jerk*):

$$p(t)=p_0+\Delta\,(10\tau^3-15\tau^4+6\tau^5),\qquad \tau=\frac{t}{T},\ \Delta=p_1-p_0$$

Szczytowa prędkość to $1{,}875\,\Delta/T$, a szczytowe przyspieszenie $5{,}77\,\Delta/T^2$. Czas ruchu dobieramy z prędkości ok. 30 mm/s:

$$T=\operatorname{clamp}\!\left(\frac{\Delta}{30\text{ mm/s}},\ 0{,}8\text{ s},\ 4\text{ s}\right)$$

| Dystans $\Delta$ | Czas $T$ | Szczyt. prędkość | Szczyt. przyspieszenie | Przechył ff |
| :--- | ---: | ---: | ---: | ---: |
| 20 mm | 0,8 s | 47 mm/s | 0,18 m/s² | 1,8° |
| 60 mm | 2,0 s | 56 mm/s | 0,09 m/s² | 0,8° |
| 100 mm | 3,3 s | 57 mm/s | 0,05 m/s² | 0,5° |

Dla małych dystansów czas 0,8 s jest dolnym limitem, żeby przyspieszenie nie rosło.

## Start, zmiana parametrów i stop

Każde nagłe przejście w torze (skok prędkości lub zmiana kierunku) to szarpnięcie. Dlatego:

1. **Start toru.** Najpierw punkt zadany płynnie dojeżdża do początku toru (powyżej). Gdy uchyb jest $<8$ mm przez 0,5 s, zaczynamy narastanie prędkości $\omega$ od 0 do wartości docelowej w ciągu ok. 3 s.
2. **Faza ciągła.** Fazę liczymy przyrostowo ($\varphi\leftarrow\varphi+\omega\,\Delta t$), a nie jako $\omega t$. Dzięki temu zmiana $\omega$ w trakcie jazdy nie powoduje skoku położenia na torze.
3. **Zmiany parametrów na żywo** (pokrętło) ograniczamy: $|\dot\omega|\le0{,}3$ rad/s², $|\dot r|\le15$ mm/s. Gwałtowne przekręcenie gałki nie wyrzuci kulki z toru.
4. **Zmiana rodzaju toru** w trakcie jazdy: najpierw płynne wyhamowanie do punktu (ramp $\omega\to0$), potem nowy start.
5. **Stop.** $\omega$ spada do 0 w ciągu ok. 3 s, po czym kulka płynnie wraca do środka tacy.
6. **Połączenia fragmentów** (np. proste i łuki kwadratu) łagodzimy filtrem pierwszego rzędu na $\theta_{ff}$ ze stałą ok. 50 ms. Skok krzywizny na styku prostej i łuku daje skok przyspieszenia, a taki sygnał pobudza luzy w przegubach.

## Strojenie feed-forward

Dwa parametry stroimy na torze, który znamy: okrąg $r=60$ mm, $\omega=1{,}0$ rad/s.

1. **Zmierz $K$** (przed pierwszą jazdą). Procedura w [[18 Kalibracja i uruchomienie]]. Wpisz zmierzoną wartość, a $k_{ff}=1$.
2. **Dobierz $t_{lead}$.** Zacznij od 0,1 s. Zmieniaj o 0,02 s i patrz na RMS błędu w telemetrii z jednego okrążenia. Za mało wyprzedzenia: kulka spóźnia się za punktem zadanym. Za dużo: wyprzedza go.
3. **Dobierz $k_{ff}$.** Zmieniaj od 0,8 do 1,2 co 0,05, szukając minimum RMS błędu. Jeśli minimum wychodzi poza 0,8–1,2, to znaczy, że $K$ jest źle zmierzone albo tarcie jest duże. Wróć do kroku 1.
4. Zwiększ $\omega$ do 1,5 rad/s i sprawdź kryterium (błąd $\le10$ mm).
5. Zapisz parametry w profilu kulki ([[15 Konsola i obsługa]]).

## Co widzi użytkownik (ekran 2)

Parametry toru ([[15 Konsola i obsługa]]):

| Parametr | Zakres | Domyślnie |
| :--- | :--- | :--- |
| Tor | stop / okrąg / ósemka / kwadrat | stop |
| Rozmiar (promień lub półbok) | 20–70 mm, krok 5 mm | 40 mm |
| Okres jednego okrążenia | od 4,2 s (okrąg, 1,5 rad/s) wzwyż | 8 s |
| Kierunek | zgodnie / przeciwnie | zgodnie |
| $k_{ff}$ | 0,5–1,5 | 1,0 |
| $t_{lead}$ | 0–0,2 s | 0,1 s |

Okres wygodniej jest wyświetlać w sekundach: $T=2\pi/\omega$. Menu samo przycina wartości do limitów z poprzedniej sekcji. Gdy ustawiony rozmiar i okres przekraczają limit toru, pokazujemy komunikat „zwolnij" i przycinamy $\omega$.

## Testy akceptacyjne

Tory sprawdzamy w Etapie 7 ([[19 Plan prac i testy]]) w tej kolejności i przechodzimy dalej dopiero, gdy poprzedni wyszedł:

1. **Punkt** w środku, potem przesunięty strzałkami o 30 mm. Kulka dojeżdża płynnie, bez przeregulowania powyżej 10 mm.
2. **Okrąg $r=40$ mm, $\omega=1{,}0$** rad/s: RMS błędu $\le5$ mm.
3. **Okrąg $r=60$ mm, $\omega=1{,}5$** rad/s: błąd $\le10$ mm przez całe okrążenie. To jest kryterium sukcesu z [[01 Jak to działa]].
4. **Ósemka** $A=50$ mm, $\omega=0{,}6$ rad/s.
5. **Kwadrat** $A=50$ mm, $r_c=30$ mm, $v=40$ mm/s.
6. **Zmiana parametrów na żywo** (pokrętło podczas jazdy): kulka nie wypada z toru.
7. **Stop w trakcie jazdy:** płynny powrót do środka.

## Dlaczego tak

- **Feed-forward zamiast "mocniejszego PID".** Szybszy regulator oscylowałby, bo ograniczeniem są opóźnienia serwa i kamery. Feed-forward omija ten problem, bo nie czeka na błąd.
- **Dwa limity naraz** (przechył i pasmo pętli). Pierwszy wynika z fizyki, drugi z regulatora. Pominięcie któregoś dałoby tor, którego układ nie utrzyma.
- **Najwyższa składowa częstotliwości, a nie $\omega$ toru.** Ósemka ma w osi Y składową $2\omega$, więc obowiązuje ją ostrzejszy limit niż okrąg.
- **Płynne starty i stopy.** Skok punktu zadanego wymusiłby skok przechyłu, a luzy w przegubach ([[07 Cięgna i przeguby]]) zamieniają taki skok w drżenie.
- **Zaczynamy od okręgu.** Najprostszy tor, jedna częstotliwość, łatwy do zmierzenia błąd. Pozostałe dodajemy po tym, jak okrąg działa.
