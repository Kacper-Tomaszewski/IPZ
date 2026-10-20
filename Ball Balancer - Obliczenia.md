---
title: Ball Balancer - Obliczenia
tags:
  - projekt
  - ball-balancer
  - obliczenia
  - kinematyka
  - pid
created: 2026-10-20
---

# 🧮 Ball Balancer 3-RRS: obliczenia

Wróć do: [[Projekt Ball Balancer]]. Wnioski z przeglądu: [[Ball Balancer - Uwagi i ulepszenia]]. Implementacja: [[Ball Balancer - Firmware]].

> [!info] Jak powstały te liczby
> Kinematykę, zakres przechyłu, marginesy PID i skręt przegubów sprawdziłem skryptem numerycznym (Python/NumPy). Wartości **oznaczone „zał." to założenia lub dane katalogowe**, które trzeba potwierdzić pomiarem na gotowej konstrukcji.

Oznaczenia: $R=90$ mm (promień osi serw i uchwytów tacy), $L_1=24$ mm (orczyk), $L_2=60$ mm (popychacz), $Z_s=28$ mm (oś serwa nad blatem), $\psi_i\in\{90^\circ,210^\circ,330^\circ\}$.

---

## 1. Geometria w pozycji neutralnej

Orczyk poziomy ($\alpha=0$), górny przegub dokładnie nad osią serwa (odległość pozioma $L_1$):

$$h_0=\sqrt{L_2^2-L_1^2}=\sqrt{60^2-24^2}=\sqrt{3024}\approx 55{,}0\text{ mm}$$

$$Z_{pivot,0}=Z_s+h_0=28+55{,}0=83{,}0\text{ mm}$$

> [!warning] Do sprawdzenia: $Z_{neutral}=92$ mm
> Oś górnego przegubu leży na 83,0 mm. Górna powierzchnia tacy to 83,0 plus odległość od osi przegubu do góry tacy. W v1 przyjęto 92 mm, czyli 9 mm. W modelu uchwytu `plate_mount_bracket` parametr `pivot_h = 10.5` mierzy od płaszczyzny mocowania do osi. Jeśli uchwyt jest przykręcony do spodu tacy (3 mm), górna powierzchnia wypadnie na ok. $83{,}0+10{,}5+3{,}0=96{,}5$ mm. Różnica 4,5 mm nie przeszkadza w działaniu, ale zmienia wysokość kamery nad tacą i trzeba ją ustalić raz w CAD.

**Skok pionowy końcówki orczyka:**

$$\Delta z = L_1\sin\alpha \;\Rightarrow\; \alpha=\pm35^\circ:\ \pm 13{,}77\text{ mm}$$

**Przesuw poziomy końcówki** (zmienia efektywną odległość do uchwytu):

$$\Delta u = L_1(1-\cos 35^\circ)=4{,}34\text{ mm}$$

Zakres $\pm35^\circ$ wymaga rozpiętości sygnału serwa ok. $70^\circ$. HS-422 (ok. 900–2100 µs) w pełni to pokrywa. Szacunkowo 10 µs/° (zał.), do skalibrowania w ekranie Trim.

---

## 2. Kinematyka odwrotna (3 nogi, model kulowy)

Dla nogi $i$ przyjmuję lokalną bazę: $\mathbf{u}_i=(\cos\psi_i,\sin\psi_i,0)$ (radialnie), $\mathbf{t}_i=(-\sin\psi_i,\cos\psi_i,0)$ (stycznie). Orczyk wychyla się w płaszczyźnie $(\mathbf{u},\mathbf{z})$ i wskazuje **na zewnątrz** przy $\alpha=0$ (zał.):

$$\mathbf{A}_i(\alpha)=\big(R+L_1\cos\alpha\big)\mathbf{u}_i+\big(Z_s+L_1\sin\alpha\big)\mathbf{z}$$

Punkt zamocowania na tacy po przechyleniu i podniesieniu o $z$:

$$\mathbf{P}_i=\mathbf{R}_{pose}\,[R\cos\psi_i,\ R\sin\psi_i,\ 0]^T+[0,0,z]^T,\quad \mathbf{R}_{pose}=R_y(\theta_y)R_x(\theta_x)$$

Warunek stałej długości popychacza $|\mathbf{P}_i-\mathbf{A}_i|=L_2$ po rozwinięciu daje równanie:

$$a\cos\alpha+b\sin\alpha=c$$

$$a=p_u-R,\quad b=p_z-Z_s,\quad c=\frac{a^2+b^2+p_t^2+L_1^2-L_2^2}{2L_1}$$

gdzie $p_u=\mathbf{P}_i\cdot\mathbf{u}_i$, $p_t=\mathbf{P}_i\cdot\mathbf{t}_i$, $p_z=P_{i,z}$. Rozwiązanie:

$$\boxed{\alpha_i=\operatorname{atan2}(b,a)-\arccos\!\left(\frac{c}{\sqrt{a^2+b^2}}\right)}$$

Brak rozwiązania ($|c|>\sqrt{a^2+b^2}$) oznacza pozę poza zasięgiem. Kontrola w pozycji neutralnej: $\alpha_i=0^\circ$ dla $z=83{,}0$ mm. ✔

### Wyniki: kąty serw dla przechyłu w stronę serwa 1 (ψ = 90°), $z=Z_{pivot,0}$

| Przechył tacy | $\alpha_1$ (w górę) | $\alpha_{2,3}$ (w dół) |
| :--- | ---: | ---: |
| 3° | +11,0° | −5,7° |
| 5° | +18,2° | −9,7° |
| 7° | +25,4° | −13,8° |
| 9° | +32,7° | −18,0° |
| 10° | +36,5° (poza limitem) | −20,2° |

> [!success] Zakres przechyłu
> Przy limicie $|\alpha|\le35^\circ$ i stałym $z$ maksymalny przechył wynosi **7,9° (najgorszy kierunek) do 10,2° (najlepszy)**. Wartość „$\pm9^\circ$" z v1 jest więc osiągalna tylko w części kierunków. Do sterowania wystarczy ok. 3–5°, więc przyjmujemy **limit programowy $\pm6^\circ$** (daje $|\alpha|\lesssim 22^\circ$ i zapas na luzy oraz trim).

**Przybliżenie intuicyjne:** nogi leżą na okręgu $R$, więc przechył $\theta$ w kierunku nogi $i$ podnosi ją o $R\tan\theta$. Dla $9^\circ$ jest to $14{,}3$ mm, czyli zgodnie z maksymalnym skokiem 13,8 mm.

### Luz i rozdzielczość
- LEDC 14 bit przy 50 Hz: krok $20\text{ ms}/16384=1{,}22\,\mu$s ≈ $0{,}12^\circ$ serwa (zał. 10 µs/°).
- Przy ramieniu 24 mm zmiana o $0{,}12^\circ$ daje $\Delta z\approx0{,}05$ mm, czyli przechył $\approx0{,}03^\circ$. Dyskretyzacja PWM jest pomijalna.
- Luz kostki: szczelina 8,4 mm − kostka 8,0 mm = 0,4 mm na przegub. Przy dwóch przegubach na nogę może to dać ok. 0,2–0,4° błędu przechyłu. To wystarczy do powstania **cyklu granicznego** (kulka „drży"). Pierwszy wydruk ma pokazać, czy trzeba zmniejszyć szczelinę do ok. 8,2 mm.

### Przeguby U zamiast kulowych
Model powyżej zakłada przeguby kulowe. W konstrukcji są **przeguby krzyżakowe (kostka Kardana)** po obu stronach cięgna. Gdy oba sworznie cięgna są równoległe, każdy z nich musi być prostopadły do osi cięgna, więc nogi wymuszają dodatkowy warunek. Obliczony **skręt cięgna** potrzebny do jego spełnienia przy przechyle $\vartheta$ w najgorszym kierunku:

| Przechył | 2° | 4° | 6° | 8° |
| :--- | ---: | ---: | ---: | ---: |
| Skręt cięgna | 0,8° | 1,6° | 2,4° | 3,2° |

Przy typowej pracy (do 4°) wystarcza sprężystość i luzy wydruku. Przy 8° skręt rzędu 3° na cięgnie 54 mm to ok. 0,4 mm bocznego przesunięcia, czyli tyle, ile wynosi cały luz. To uzasadnia **limit $\pm6^\circ$** i test cięgna przed drukiem całości. Plan B: gotowe łączniki kulowe M3 (np. typu RC) w miejscu górnych kostek.

---

## 3. Dynamika kulki

Kulka toczy się bez poślizgu po płaszczyźnie przechylonej o $\theta$:

$$\ddot x=\frac{g\sin\theta}{1+I/(mr^2)}\approx k\,g\,\theta,\quad k=\begin{cases}3/5 & \text{piłeczka pingpongowa (cienka powłoka)}\\5/7 & \text{kulka pełna / golfowa}\end{cases}$$

Dla małych kątów model to **podwójny integrator**: $X(s)/\Theta(s)=K/s^2$.

| Kulka | $k$ | $K=kg$ [m/s²/rad] | $a$ przy 9° |
| :--- | ---: | ---: | ---: |
| Pingpong 2,7 g | 0,6 | 5,89 | 0,92 m/s² |
| Pełna / golfowa 45 g | 0,714 | 7,01 | 1,10 m/s² |

**Czasy:** przejazd 105 mm (od krawędzi do środka) przy pełnym przechyle 9°: $t=\sqrt{2\cdot0{,}105/0{,}92}\approx0{,}48$ s. Przy 3°: $\approx0{,}83$ s. Prędkość kulki po przejeździe 100 mm przy 5°: $\approx0{,}32$ m/s, czyli ok. 6,4 mm/klatkę przy 50 FPS.

> [!warning] Zmiana kulki zmienia $K$
> Przejście z pingponga na kulkę golfową zwiększa $K$ o ok. 19%, a więc proporcjonalnie wzmocnienie pętli. Nastawy z sekcji 5 dobrane są dla pingponga. Dla kulki pełnej zmniejsz $K_p$ i $K_d$ o ok. 15%.

---

## 4. Kamera i rozdzielczość pomiaru

Kamera patrzy pionowo z $H=195$ mm. Model obiektywu szerokokątnego 120° (DFOV, zał. rzut równoodległy $r=f\theta$):

$$f_{px}=\frac{r_{diag}}{\theta_{diag}}=\frac{100\text{ px}}{1{,}047\text{ rad}}\approx95{,}5\text{ px/rad}\quad(\text{QQVGA})$$

Skala w środku: $s_0=H/f=2{,}04$ mm/px. Na krawędzi tacy ($\theta=\arctan(105/195)=28{,}3^\circ$):

$$s_{edge}=\frac{H}{f\cos^2\theta}=\frac{195}{95{,}5\cdot0{,}775}\approx2{,}6\text{ mm/px}$$

Skala zmienia się o 28% między środkiem a krawędzią, więc **bez korekcji dystorsji pozycja kulki byłaby przeskalowana**. Zalecane mapowanie piksel → mm:

$$r_{px}=\sqrt{(x-x_c)^2+(y-y_c)^2},\qquad r_{mm}=H\tan\!\left(\frac{r_{px}}{f_{px}}\right)$$

$$x_{mm}=(x-x_c)\frac{r_{mm}}{r_{px}},\quad y_{mm}=(y-y_c)\frac{r_{mm}}{r_{px}}$$

$f_{px}$, $x_c$, $y_c$ wyznacza się w ekranie kalibracji (znany promień rantu, obwiednia tacy).

| Obiektyw (DFOV) | Krótszy bok tacy (120 px) | mm/px (średnio) | Średnica tacy w obrazie |
| :--- | ---: | ---: | ---: |
| 65° (standardowy) | 138 mm | 1,15 | 182 px, **ale nie obejmuje całej tacy** |
| 90° | 199 mm | 1,66 | 127 px |
| **120°** | 283 mm | 2,36 | 89 px |
| 160° | 433 mm | 3,61 | 58 px |

**Wniosek:** obiektyw 120° obejmuje cały $\varnothing210$ mm z zapasem, a standardowy 65° nie. Cena to ok. 2–2,6 mm/px w QQVGA. Kulka $\varnothing40$ mm ma wtedy ok. 17 px średnicy. Centroid z wagami jasności daje błąd subpikselowy rzędu 0,2–0,3 px, czyli **±0,5–0,8 mm**. Do stabilizacji to wystarcza, ale prędkość z różnicowania surowej pozycji byłaby zaszumiona. Stąd filtr α-β w [[Ball Balancer - Firmware]].

**QVGA ($320\times240$):** ok. 1,0–1,3 mm/px, ok. 77 tys. pikseli. Progowanie i centroid na ESP32-S3 (240 MHz) zajmują szacunkowo 1–3 ms. Uzyskiwalny FPS trzeba zmierzyć (zał. 40–50 FPS).

**Rozmycie ruchu:** przy ekspozycji 5 ms i prędkości 0,3 m/s kulka przesuwa się o 1,5 mm podczas naświetlania, co jest akceptowalne. Pierścień LED pozwala utrzymać krótką ekspozycję.

---

## 5. Regulator PID

### Model do strojenia
$$G(s)=\frac{K}{s^2}\cdot\frac{e^{-T_d s}}{\tau_s s+1},\quad K=5{,}89\ \text{m/s}^2/\text{rad}$$

- $\tau_s\approx50$–70 ms: opóźnienie pierwszego rzędu serwa HS-422 (zał., katalog: 0,21 s/60° przy 4,8 V).
- $T_d\approx40$–60 ms: czas martwy, czyli klatka kamery 20 ms, przetwarzanie, UART, próbkowanie 50 Hz i średnio 10 ms opóźnienia PWM.

### Struktura
Dla stałego punktu zadanego $r$ (pochodna z pomiaru, nie z uchybu):

$$\theta=K_p(r-x)-K_d\,\hat v+K_i\!\int(r-x)\,dt$$

Układ zamknięty bez opóźnień: $s^2+KK_ds+KK_p=0$, stąd

$$\omega_n=\sqrt{KK_p},\qquad \zeta=\frac{KK_d}{2\omega_n}$$

### Dlaczego nie „szybki" PID
Samo dobranie $\omega_n=4$ rad/s (typowa wartość z modelu idealnego) daje przy opóźnieniach marżę fazową tylko ok. 10–20°, czyli kulka by oscylowała. Przeszukanie siatki $(K_p,T_d)$ dla $T_i=15$ s, filtra pochodnej $N=10$:

| Warianty obciążenia | Najlepsza marża fazowa |
| :--- | ---: |
| $\tau_s=50$ ms, $T_d=40$ ms | ok. 46° |
| $\tau_s=70$ ms, $T_d=60$ ms | ok. 42° |

### Nastawy startowe (pingpong, 50 Hz)

| Parametr | Wartość | W jednostkach sterownika |
| :--- | :--- | :--- |
| $K_p$ | 0,4 rad/m | 0,0229 °/mm |
| $K_d$ ($T_d=1{,}0$ s) | 0,4 rad·s/m | 0,0229 °·s/mm |
| $K_i$ ($T_i=15$ s) | 0,027 rad/(m·s) | 0,0015 °/(mm·s) |
| Filtr pochodnej | $N=10$ (lub α-β) | |
| Ogranicznik całki | $\pm1{,}5^\circ$ | |

Wynik: $\omega_n\approx1{,}5$ rad/s, $\zeta\approx0{,}77$ (model idealny); z opóźnieniami przecięcie $\omega_c\approx2{,}6$ rad/s (0,4 Hz), marża fazowa 37–43°, czas ustalania ok. 2–3 s.

> [!tip] Procedura strojenia
> 1. $K_i=0$, $K_d=0{,}3$, podnoś $K_p$ aż kulka zaczyna oscylować wokół środka, potem cofnij o ok. 30%.
> 2. Zwiększaj $K_d$, aż oscylacje zanikną szybko bez drgań wysokiej częstotliwości (szum z kamery).
> 3. Dodaj $K_i$ tak, by kulka wracała do środka po dociśnięciu lub niedokładnym wypoziomowaniu w ciągu kilkunastu sekund.
> 4. Zapisz w NVS jako profil dla danej kulki.

**Czemu nie szybciej:** granica wynika z fizyki toru. Szybszy pomiar (wyższy FPS) i szybsze serwa (cyfrowe) podniosłyby osiągi, a samo „mocniejsze" PID nie.

### Filtr α-β (pozycja i prędkość), $T=20$ ms

$$\hat x_k^- = \hat x_{k-1}+\hat v_{k-1}T,\qquad \hat x_k = \hat x_k^- + \alpha(z_k-\hat x_k^-),\qquad \hat v_k = \hat v_{k-1}+\frac{\beta}{T}(z_k-\hat x_k^-)$$

Przy $\alpha=0{,}5$ przyjmujemy krytyczne tłumienie $\beta=\alpha^2/(2-\alpha)=0{,}167$. Przy braku detekcji przez 1–2 klatki: samo przewidywanie. Po 5 klatkach (100 ms): awaria, patrz bezpieczeństwo w [[Ball Balancer - Firmware]].

---

## 6. Trajektorie i sprzężenie w przód

Dla okręgu o promieniu $r$ i pulsacji $\omega$ potrzebne przyspieszenie dośrodkowe $a=\omega^2 r$, a więc przechył feed-forward:

$$\theta_{ff}=\frac{\omega^2 r}{K}$$

| $r$ | $\omega=1{,}0$ rad/s | $\omega=1{,}5$ rad/s | $\omega=2{,}0$ rad/s |
| :--- | ---: | ---: | ---: |
| 40 mm | 0,39° | 0,88° | 1,56° |
| 60 mm | 0,58° | 1,31° | 2,34° |
| 80 mm | 0,78° | 1,75° | 3,12° |

**Ograniczenie praktyczne:** pasmo pętli to ok. 2,6 rad/s, więc na początek ogranicz $\omega\le1{,}5$ rad/s (okres ≥ 4,2 s). Wtedy $r=60$ mm daje prędkość $v=\omega r=90$ mm/s i wystarcza przechył ok. 1,3° (sam feed-forward) plus korekta PID.

Teoretyczny limit przy 50% max przechyłu (4,5°, $a=0{,}46$ m/s²): $\omega_{max}=\sqrt{a/r}$ = 3,4 / 2,8 / 2,4 rad/s dla $r$ = 40 / 60 / 80 mm. Pętla zamknięta nie dotrzyma takiego tempa, więc to tylko górna granica fizyczna.

---

## 7. Siły, momenty, zasilanie

### Moment na serwie
Masa ruchomych elementów: taca PLA 210×3 mm (ok. 90–130 g, zał. zależnie od wypełnienia), żebra ok. 7 g, uchwyty, rant, folia. Razem **ok. 100–150 g** plus kulka. Na jedną nogę przypada ok. 40–50 g:

$$M_{serwo}\approx m\,L_1 \approx 0{,}05\text{ kg}\cdot2{,}4\text{ cm}=0{,}12\text{ kg·cm}$$

To jest **ok. 25–30 razy mniej** niż moment znamionowy HS-422 (3,3 kg·cm przy 4,8 V, 4,1 kg·cm przy 6 V). Serwa mają bardzo duży zapas. Nawet SG90 (1,6 kg·cm) by to uniosły, choć miałyby większy luz.

**Prędkość serwa:** 0,21 s/60° → ok. 285°/s. Przy paśmie 0,4 Hz i amplitudzie 10° wymagana prędkość to ok. 25°/s, więc jest duży zapas.

### Bilans prądu (wartości szacunkowe, zał.)

| Odbiornik | Szczyt |
| :--- | ---: |
| 3× HS-422 (ruch, szczytowo) | do ok. 1,5–2,4 A |
| ESP32 + OLED | ok. 0,25 A |
| ESP32-S3 CAM (Wi-Fi wyłączone) | ok. 0,3–0,4 A |
| Pierścień 12× WS2812B (przy 25% jasności) | ok. 0,2 A (pełna biel: 0,7 A) |
| **Suma** | **ok. 2,3–3,3 A** |

Zasilacz **5 V / 4 A** daje zapas. Wersja 3 A działałaby tylko na granicy przy szczytach. Zasilanie serw i elektroniki ze wspólnej szyny 5 V w gwiazdę, kondensator $1000\,\mu$F blisko serw, $100\,\mu$F i $100$ nF przy każdym ESP32. To ogranicza resety od przepięć przy ruszaniu serw.

---

## 8. Kolizje i wymiary pałąka

- **Krawędź tacy przy przechyle 9°:** podnosi się lub opada o $105\sin9^\circ=16{,}4$ mm. Sprawdź kolizję z konsolą i komorą bazy (dolna krawędź tacy przy maks. przechyle: ok. 89 − 16 = 73 mm nad blatem, bez żeber).
- **Słupek C-Arm:** na 132 mm od środka. Krawędź tacy sięga 105 mm (plus rant), a zapas 27 mm pochłania przechył i luzy. ✔
- **Wysokość kamery:** 195 mm nad tacą daje pole widzenia z sekcji 4. Zmiana $Z_{neutral}$ (patrz sekcja 1) przesuwa to o kilka mm, więc użyj mapowania z kalibracji.
- **Sztywność pałąka:** kamera jest mierzona względem bazy, więc każde ugięcie lub drganie końca pałąka wygląda jak ruch kulki. Przechył kamery o $0{,}3^\circ$ przesuwa obraz punktu pod nią o $195\tan0{,}3^\circ\approx1$ mm, czyli tyle co cała dokładność pomiaru. Pałąk musi być sztywny. Szczegóły w [[Ball Balancer - Uwagi i ulepszenia]].
