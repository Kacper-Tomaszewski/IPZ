# BALL BALANCER 3-RRS - KINEMATYKA I UKLAD CZESCI (czysty Python, bez Fusion)
# Ten sam wzor co inverseKinematics() w firmware (notatka 22), plus polozenia
# wszystkich ruchomych czesci dla danej pozycji tacy. Mozna testowac bez Fusion.

import math
import bb_params as P


# ---------- wektory (krotki 3-elementowe) ----------
def add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norm(a): return math.sqrt(dot(a, a))
def unit(a):
    n = norm(a)
    return (a[0] / n, a[1] / n, a[2] / n)
def lin(*pairs):
    """lin((s1, v1), (s2, v2), ...) = s1*v1 + s2*v2 + ..."""
    r = (0.0, 0.0, 0.0)
    for s, v in pairs:
        r = add(r, mul(v, s))
    return r
def perp(v, n):
    """Skladowa v prostopadla do n (n jednostkowy), znormalizowana."""
    return unit(sub(v, mul(n, dot(v, n))))

EX, EY, EZ = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)


class Frame:
    """Uklad lokalny czesci: poczatek + osie X, Y, Z (w mm, w ukladzie swiata)."""
    def __init__(self, o, x, y, z):
        self.o, self.x, self.y, self.z = o, x, y, z

    def pt(self, p):
        """Punkt z ukladu lokalnego do swiata."""
        return add(self.o, lin((p[0], self.x), (p[1], self.y), (p[2], self.z)))

    def vec(self, v):
        return lin((v[0], self.x), (v[1], self.y), (v[2], self.z))

    def moved(self, p):
        return Frame(self.pt(p), self.x, self.y, self.z)


IDENTITY = Frame((0.0, 0.0, 0.0), EX, EY, EZ)


def pose_matrix(rx, ry):
    """Rpose = Ry(ry) * Rx(rx), identycznie jak w firmware. Zwraca kolumny (osie)."""
    cx, sx, cy, sy = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry)
    m = ((cy, sy * sx, sy * cx),
         (0.0, cx, -sx),
         (-sy, cy * sx, cy * cx))
    col = lambda j: (m[0][j], m[1][j], m[2][j])
    return col(0), col(1), col(2)


def leg_axes(i):
    psi = math.radians(P.PSI_DEG[i])
    u = (math.cos(psi), math.sin(psi), 0.0)      # radialnie
    t = (-math.sin(psi), math.cos(psi), 0.0)     # stycznie
    return psi, u, t


def inverse_kinematics(z, rx, ry):
    """Kopia firmware. Zwraca (lista alfa [deg] lub None, komunikat)."""
    mx, my, mz = pose_matrix(rx, ry)
    alphas = []
    for i in range(3):
        psi, u, t = leg_axes(i)
        e = (P.R_PLATE * math.cos(psi), P.R_PLATE * math.sin(psi), 0.0)
        Pw = add(lin((e[0], mx), (e[1], my)), (0.0, 0.0, z))
        pu, pt, pz = dot(Pw, u), dot(Pw, t), Pw[2]
        a = pu - P.R_BASE
        b = pz - P.Z_SERVO
        c = (a * a + b * b + pt * pt + P.L1 * P.L1 - P.L2 * P.L2) / (2.0 * P.L1)
        A = math.sqrt(a * a + b * b)
        if A < 1e-6 or abs(c / A) > 1.0:
            return None, "noga %d poza zasiegiem" % (i + 1)
        alpha = math.degrees(math.atan2(b, a) - math.acos(c / A))
        if abs(alpha) > P.ALPHA_LIMIT:
            return None, "serwo %d: %.1f deg > limit %.0f deg" % (i + 1, alpha, P.ALPHA_LIMIT)
        alphas.append(alpha)
    return alphas, "ok"


def max_tilt(direction_deg, z=None, step=0.01):
    """Najwiekszy przechyl [deg] w danym kierunku osi przechylu, przy limicie orczyka."""
    z = P.Z_PIVOT if z is None else z
    lo, hi = 0.0, 20.0
    phi = math.radians(direction_deg)
    while hi - lo > step:
        mid = 0.5 * (lo + hi)
        th = math.radians(mid)
        ok, _ = inverse_kinematics(z, th * math.cos(phi), th * math.sin(phi))
        if ok is None:
            hi = mid
        else:
            lo = mid
    return lo


# Kierunki pinow w pozycji neutralnej, w plaszczyznie nogi (radialnie u, pionowo z).
# Pin jest prostopadly do osi popychacza, wiec przesuniecia 2 x 2.8 mm w kostkach
# leza na osi popychacza i model punktowy (|AP| = L2) jest dokladny w neutrum.
D0_U, D0_Z = -P.L1 / P.L2, P.H0 / P.L2      # kierunek popychacza A -> P
N0_U, N0_Z = P.H0 / P.L2, P.L1 / P.L2       # kierunek pinow orczyka i uchwytu


def layout(z=None, rx=0.0, ry=0.0, ball=(0.0, 0.0)):
    """Polozenia czesci ruchomych. Zwraca (slownik nazwa -> lista Frame, raport) lub (None, blad)."""
    z = P.Z_PIVOT if z is None else z
    alphas, msg = inverse_kinematics(z, rx, ry)
    if alphas is None:
        return None, msg

    mx, my, mz = pose_matrix(rx, ry)
    plate = Frame((0.0, 0.0, z), mx, my, mz)
    frames = {
        "03_Taca_Robocza_210mm": [plate],
        "03b_Rant_210mm": [plate],
        "Kulka_40mm": [plate.moved((ball[0], ball[1], P.PIVOT_H + P.PLATE_T + P.BALL_D / 2))],
        "HS-422": [], "04_Adapter_Orczyka_24mm": [],
        "05b_Kostka_Kardana": [], "05_Popychacz_60mm": [],
    }
    report = {"alpha": alphas, "rod_len_err": [], "twist": [], "pin_angle": []}

    for i in range(3):
        psi, u, t = leg_axes(i)
        a = math.radians(alphas[i])
        axis = add(mul(u, P.R_BASE), (0.0, 0.0, P.Z_SERVO))

        # serwo: X = u (korpus do srodka), Y = gora, Z = -t (strona orczyka)
        frames["HS-422"].append(Frame(add(axis, mul(t, P.HORN_PLANE)), u, EZ, mul(t, -1.0)))

        # adapter orczyka: X = ramie, obrot o alfa wokol osi serwa
        ax_x = lin((math.cos(a), u), (math.sin(a), EZ))
        ax_y = lin((-math.sin(a), u), (math.cos(a), EZ))
        horn = Frame(axis, ax_x, ax_y, mul(t, -1.0))
        frames["04_Adapter_Orczyka_24mm"].append(horn)
        A = horn.pt((P.L1, 0.0, 0.0))
        n_h = lin((N0_U, ax_x), (N0_Z, ax_y))

        # widelki tacy: X = radialnie tacy, Y = stycznie, Z = normalna tacy
        up = lin((math.cos(psi), mx), (math.sin(psi), my))
        Pp = plate.pt((P.R_PLATE * math.cos(psi), P.R_PLATE * math.sin(psi), 0.0))
        n_b = lin((N0_U, up), (N0_Z, mz))

        d = unit(sub(Pp, A))
        # kostka dolna: Y = pin orczyka, Z = w strone popychacza
        zl = perp(d, n_h)
        xl = cross(n_h, zl)
        # kostka gorna: Y = pin uchwytu, Z = w strone popychacza
        zu = perp(mul(d, -1.0), n_b)
        xu = cross(n_b, zu)
        frames["05b_Kostka_Kardana"].append(Frame(add(A, mul(zl, P.AXIS_OFFSET)), xl, n_h, zl))
        frames["05b_Kostka_Kardana"].append(Frame(add(Pp, mul(zu, P.AXIS_OFFSET)), xu, n_b, zu))

        # popychacz: sworznie w osiach X kostek
        lo_pin = add(A, mul(zl, 2 * P.AXIS_OFFSET))
        hi_pin = add(Pp, mul(zu, 2 * P.AXIS_OFFSET))
        rx_ax = unit(sub(hi_pin, lo_pin))
        xu_al = xu if dot(xu, xl) >= 0 else mul(xu, -1.0)
        ry_ax = perp(add(xl, xu_al), rx_ax)
        frames["05_Popychacz_60mm"].append(
            Frame(mul(add(lo_pin, hi_pin), 0.5), rx_ax, ry_ax, cross(rx_ax, ry_ax)))

        report["rod_len_err"].append(norm(sub(hi_pin, lo_pin)) - P.ROD_PIN_DIST)
        # skret popychacza = kat miedzy sworzniami dolnym i gornym (wokol osi popychacza)
        pl, pu_ = perp(xl, rx_ax), perp(xu_al, rx_ax)
        report["twist"].append(math.degrees(math.acos(max(-1.0, min(1.0, dot(pl, pu_))))))
        # jak bardzo sworzen odbiega od prostopadlosci do popychacza (luz katowy kostki)
        report["pin_angle"].append(max(abs(90.0 - math.degrees(math.acos(abs(dot(xl, rx_ax))))),
                                       abs(90.0 - math.degrees(math.acos(abs(dot(xu_al, rx_ax)))))))
    return frames, report


def static_frames(h_cam=None):
    """Czesci nieruchome (w ukladzie swiata)."""
    h_cam = P.H_CAM if h_cam is None else h_cam
    zc = P.Z_TOP + h_cam
    return {
        "01_Baza_Glowna_HS422": [IDENTITY],
        "02_Panel_Konsoli_OLED": [IDENTITY],
        "06_Palak_Dolny": [IDENTITY],
        "07_Palak_Gorny_Kamera": [IDENTITY.moved((0.0, 0.0, zc))],
        "Pierscien_LED_12x": [IDENTITY.moved((0.0, 0.0, zc))],
        "ESP32-S3_CAM": [IDENTITY.moved((0.0, 0.0, zc))],
        "00_Kupon_Tolerancji": [IDENTITY.moved((260.0, 0.0, 0.0))],
        "05c_Uchwyt_Testowy": [IDENTITY.moved((290.0, 60.0, 8.0))],
    }


def range_report(dirs=36):
    """Tekstowy raport zakresu ruchu (do porownania z notatka 06)."""
    lines = []
    tilts = [(k * 360.0 / dirs, max_tilt(k * 360.0 / dirs)) for k in range(dirs)]
    mn = min(tilts, key=lambda x: x[1])
    mx = max(tilts, key=lambda x: x[1])
    lines.append("Maks. przechyl przy orczyku +/-%.0f deg: od %.1f deg (kierunek %.0f) do %.1f deg (kierunek %.0f)"
                 % (P.ALPHA_LIMIT, mn[1], mn[0], mx[1], mx[0]))
    lines.append("Przechyl w strone serwa 1 (rx > 0): kat serwa 1 / serw 2 i 3")
    for th in (3, 5, 6, 7, 9):
        al, msg = inverse_kinematics(P.Z_PIVOT, math.radians(th), 0.0)
        if al is None:
            lines.append("  %d deg: %s" % (th, msg))
        else:
            lines.append("  %d deg: %+.1f / %+.1f / %+.1f deg" % (th, al[0], al[1], al[2]))
    lines.append("Skret popychacza (maks. po kierunkach):")
    for th in (2, 4, 6, 8):
        worst = 0.0
        for k in range(dirs):
            phi = math.radians(k * 360.0 / dirs)
            fr, rep = layout(None, math.radians(th) * math.cos(phi), math.radians(th) * math.sin(phi))
            if fr is not None:
                worst = max(worst, max(rep["twist"]))
        lines.append("  %d deg: %.2f deg" % (th, worst))
    return "\n".join(lines)
