---
title: Ball Balancer - Firmware
tags:
  - projekt
  - ball-balancer
  - esp32
  - firmware
created: 2026-10-20
---

# 💾 Ball Balancer: firmware (szkielet i ustalenia)

Wróć do: [[Projekt Ball Balancer]]. Wzory: [[Ball Balancer - Obliczenia]]. Ryzyka: [[Ball Balancer - Uwagi i ulepszenia]].

> [!warning] Status kodu
> Poniższe fragmenty to **szkielet ustaleń**, nie gotowy projekt. Matematyka kinematyki odwrotnej jest zweryfikowana numerycznie w Pythonie, ale kod C++ **nie był kompilowany ani uruchamiany na sprzęcie**. Pełny firmware powstanie w osobnych sesjach (zadania 3 i 4 z [[Projekt Ball Balancer]]).

---

## 1. Protokół UART (oko → mózg)

921 600 baud, 8N1, 3,3 V, wspólna masa. Ramka 9 B (czas transmisji ok. 0,1 ms):

| Bajt | Pole | Opis |
| :--- | :--- | :--- |
| 0 | `0xAA` | nagłówek |
| 1 | `0x55` | nagłówek |
| 2 | `seq` | licznik ramek (wykrywanie zgubień) |
| 3 | `flags` | bit0 = kulka znaleziona, bit1 = nasycenie, bit2 = błąd kamery |
| 4–5 | `x` | $x$ w 1/16 piksela, uint16 (QVGA: do 5120) |
| 6–7 | `y` | $y$ w 1/16 piksela, uint16 |
| 8 | `xor` | XOR bajtów 2–7 |

Odbiornik: maszyna stanów szukająca `AA 55`, odrzucenie przy błędnej sumie, synchronizacja po zgubionym bajcie. Kierunek odwrotny (mózg → oko): komendy tekstowe lub 1-bajtowe (jasność LED, tryb LED, `calibrate`).

---

## 2. Oko: ESP32-S3 CAM (zadania)

1. Konfiguracja kamery: `PIXFORMAT_GRAYSCALE`, `FRAMESIZE_QQVGA` (opcja QVGA), XCLK 20 MHz, `fb_count=2`, tryb `GRAB_LATEST`.
2. Wyłączone Wi-Fi i Bluetooth.
3. Sensor: `aec=0`, `agc=0`, `awb=0`, stała ekspozycja ($\le5$ ms), stałe wzmocnienie.
4. Progowanie (próg stały lub z kalibracji Otsu przy starcie, kulka jasna na ciemnym tle).
5. Centroid z wagami jasności: $x_c=\frac{\sum x\,w}{\sum w}$, $w=\max(I-\text{próg},0)$. Walidacja pola powierzchni (kulka ok. 17 px średnicy → ok. 230 px pola).
6. Wysyłka ramki UART po każdej klatce.
7. LED: biały pierścień ok. 25% jasności jako oświetlenie, statusy kolorem (zielony = kulka, żółty = brak, czerwony = błąd), bez zmiany jasności w trakcie pomiaru.

---

## 3. Mózg: ESP32 (podział na rdzenie)

| Rdzeń | Zadanie | Częstotliwość |
| :--- | :--- | :--- |
| Core 1 | Odbiór UART, filtr α-β, PID, IK, PWM | stałe 50 Hz (timer) |
| Core 0 | OLED, przyciski, enkoder, NVS | 10–15 Hz (UI) |

Wymiana danych: struktura `Params` (nastawy, setpoint) chroniona `portMUX` lub kolejką; telemetria Core 1 → Core 0 przez kolejkę 1-elementową (najnowsza wartość).

### Maszyna stanów sterowania
`INIT` (rampa do neutralnego) → `IDLE` (taca płasko, brak kulki) → `RUN` (kulka wykryta, PID aktywny) → `LOST` (brak kulki > 0,5 s, powrót do poziomu) → `FAULT` (brak kamery > 100 ms, taca w poziomie, komunikat).

---

## 4. Kinematyka odwrotna (C++)

Wzór z [[Ball Balancer - Obliczenia]], sekcja 2. Zwraca kąty orczyków w stopniach, `false` przy pozie poza zasięgiem.

```cpp
#include <math.h>

constexpr float R_BASE = 90.0f;   // promien osi serw = promien uchwytow tacy [mm]
constexpr float L1     = 24.0f;   // orczyk [mm]
constexpr float L2     = 60.0f;   // popychacz (os-os) [mm]
constexpr float ZS     = 28.0f;   // os serwa nad blatem [mm]
const float Z0 = ZS + sqrtf(L2 * L2 - L1 * L1);  // 83.0 mm: os uchwytu przy alpha=0

// kolejnosc: serwo1 (90), serwo2 (210), serwo3 (330)
const float PSI[3] = { 90.f * DEG_TO_RAD, 210.f * DEG_TO_RAD, 330.f * DEG_TO_RAD };

// z: wysokosc osi uchwytow, rx/ry: przechyl [rad], Rpose = Ry(ry)*Rx(rx)
bool inverseKinematics(float z, float rx, float ry, float alphaDeg[3]) {
  const float cx = cosf(rx), sx = sinf(rx), cy = cosf(ry), sy = sinf(ry);
  const float m[3][3] = {
    {  cy,  sy * sx,  sy * cx },
    {  0.f, cx,      -sx      },
    { -sy,  cy * sx,  cy * cx }
  };
  for (int i = 0; i < 3; i++) {
    const float ex = R_BASE * cosf(PSI[i]);
    const float ey = R_BASE * sinf(PSI[i]);
    const float Px = m[0][0] * ex + m[0][1] * ey;
    const float Py = m[1][0] * ex + m[1][1] * ey;
    const float Pz = m[2][0] * ex + m[2][1] * ey + z;

    const float pu = Px * cosf(PSI[i]) + Py * sinf(PSI[i]);    // skladowa radialna
    const float pt = -Px * sinf(PSI[i]) + Py * cosf(PSI[i]);   // skladowa styczna

    const float a = pu - R_BASE;
    const float b = Pz - ZS;
    const float c = (a * a + b * b + pt * pt + L1 * L1 - L2 * L2) / (2.f * L1);
    const float A = sqrtf(a * a + b * b);
    if (A < 1e-3f || fabsf(c / A) > 1.f) return false;          // poza zasiegiem

    alphaDeg[i] = (atan2f(b, a) - acosf(c / A)) * RAD_TO_DEG;
    if (fabsf(alphaDeg[i]) > 35.f) return false;                 // limit serwa
  }
  return true;
}
```

**Odwzorowanie sterowania na przechył** (do ustalenia znaków na sprzęcie): przyspieszenie kulki w $X$ wynika z przechyłu $\theta_y$, w $Y$ z przechyłu $\theta_x$ ze znakiem przeciwnym. Najpierw zrób test statyczny z komendą z enkodera: znaki i kierunki ustaw w parametrach `invX`, `invY`, `swapXY`.

**Serwo:** `pulse_us = 1500 + sign_i * alpha_deg * US_PER_DEG + trim_i`. Start: `US_PER_DEG ≈ 10`, a trim i skalę zapisz w NVS po kalibracji w ekranie 4.

---

## 5. Regulator

Dane startowe i procedura strojenia: [[Ball Balancer - Obliczenia#5. Regulator PID]].

```cpp
struct AlphaBeta {
  float x = 0, v = 0;
  float alpha = 0.5f, beta = 0.167f;
  bool init = false;
  void update(float z, float T) {
    if (!init) { x = z; v = 0; init = true; return; }
    const float xp = x + v * T;
    const float r  = z - xp;
    x = xp + alpha * r;
    v = v + (beta / T) * r;
  }
  void predict(float T) { x += v * T; }   // przy braku detekcji
};

struct Pid {
  float kp = 0.0229f, kd = 0.0229f, ki = 0.0015f;  // [stopnie/mm], [stopnie*s/mm], [stopnie/(mm*s)]
  float iLimit = 1.5f;                              // [stopnie]
  float integ = 0;
  float step(float setpoint, float pos, float vel, float T, float outLimit) {
    const float e = setpoint - pos;
    integ += ki * e * T;
    integ  = constrain(integ, -iLimit, iLimit);
    const float u = kp * e - kd * vel + integ;      // pochodna z pomiaru
    return constrain(u, -outLimit, outLimit);       // outLimit = 6 stopni
  }
};
```

Wyjście PID (stopnie przechyłu) przeliczamy na radiany i podajemy do `inverseKinematics`. Kolejność: wejście z kamery → mapowanie piksel → mm → filtr α-β → PID X i Y → IK → PWM.

Anty-windup dodatkowo przez zamrożenie całki, gdy wyjście jest nasycone lub kulka zgubiona.

---

## 6. Interfejs offline

| Ekran | Zawartość | Sterowanie |
| :--- | :--- | :--- |
| 1. Radar | podgląd pozycji kulki i setpointu na okręgu tacy, FPS, status | strzałki: setpoint X/Y |
| 2. Trajektorie | typ (stop, okrąg, ósemka, kwadrat), promień, prędkość | enkoder: promień/prędkość, SW: krok |
| 3. PID | $K_p$, $K_d$, $K_i$, profil kulki | enkoder: wartość, SW: krok 0,01 / 0,10 / 1,0, strzałki: wybór parametru |
| 4. Trim serw | offset i znak dla 3 serw, poziomowanie tacy | strzałki + enkoder |
| 5. Kalibracja kamery (nowy) | środek obrazu, $f_{px}$, obrót/odbicie osi, próg | strzałki + enkoder |

- **DALEJ** przełącza ekrany, długie przytrzymanie = STOP (taca w poziomie).
- **Zapis do NVS** tylko po potwierdzeniu (przytrzymanie SW), z numerem wersji i CRC. Zapis flash wstrzymuje cache, ale PWM z LEDC działa sprzętowo i nie ma przez to jitteru.
- Odświeżanie OLED 10–15 Hz (pełna klatka 128×64 przy 400 kHz to ok. 25 ms).

---

## 7. Plan testów

1. **Bez kamery:** komenda przechyłu z enkodera → IK → serwa. Sprawdź, że taca się nie klinuje w całym zakresie $\pm6^\circ$.
2. **Kamera osobno:** podgląd po USB, dobór progu, ekspozycji i oświetlenia, pomiar rzeczywistego FPS i czasu centroidu.
3. **UART:** odbiór ramek, wykrywanie zgubionych (`seq`), obsługa błędnej sumy.
4. **Kalibracja:** środek i skala kamery względem tacy (znany promień rantu), osie, trim serw.
5. **Pętla zamknięta:** najpierw samo $K_p$ i $K_d$ z małym zakresem przechyłu (3°), potem $K_i$ i pełny zakres.
6. **Trajektorie:** okrąg z feed-forward dla $\omega\le1{,}5$ rad/s.
7. **Odporność:** odłączenie kamery (FAULT), zasłonięcie kulki (LOST), zasilanie na granicy.
