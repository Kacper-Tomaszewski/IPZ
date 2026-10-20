# BALL BALANCER 3-RRS - GEOMETRIA CZESCI (Fusion 360, TemporaryBRepManager)
# Kazda funkcja part_* zwraca liste cial w ukladzie lokalnym komponentu (mm).
# Uklady lokalne sa opisane przy funkcjach i zgadzaja sie z bb_kin.layout().

import math
import adsk.core
import adsk.fusion

import bb_params as P
import bb_kin as K
from bb_kin import EX, EY, EZ, Frame

CM = 0.1   # Fusion API liczy w cm
_tbm = None


def tbm():
    global _tbm
    if _tbm is None:
        _tbm = adsk.fusion.TemporaryBRepManager.get()
    return _tbm


# ---------- prymitywy ----------
def p3(p):
    return adsk.core.Point3D.create(p[0] * CM, p[1] * CM, p[2] * CM)


def v3(v):
    return adsk.core.Vector3D.create(v[0], v[1], v[2])


def matrix(fr):
    m = adsk.core.Matrix3D.create()
    m.setWithCoordinateSystem(p3(fr.o), v3(fr.x), v3(fr.y), v3(fr.z))
    return m


def obox(center, xdir, ydir, sx, sy, sz):
    """Prostopadloscian o srodku center, osiach xdir, ydir (z = x * y), wymiarach sx, sy, sz."""
    obb = adsk.core.OrientedBoundingBox3D.create(p3(center), v3(K.unit(xdir)), v3(K.unit(ydir)),
                                                 sx * CM, sy * CM, sz * CM)
    return tbm().createBox(obb)


def box(x0, x1, y0, y1, z0, z1):
    return obox(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), EX, EY,
                abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def fbox(fr, x0, x1, y0, y1, z0, z1):
    """Prostopadloscian zadany w ukladzie fr."""
    c = fr.pt(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    return obox(c, fr.x, fr.y, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def cyl(a, b, r, r2=None):
    return tbm().createCylinderOrCone(p3(a), r * CM, p3(b), (r if r2 is None else r2) * CM)


def zcyl(x, y, z0, z1, r, r2=None):
    return cyl((x, y, z0), (x, y, z1), r, r2)


def sphere(c, r):
    return tbm().createSphere(p3(c), r * CM)


def union(target, *tools):
    for t in tools:
        tbm().booleanOperation(target, t, adsk.fusion.BooleanTypes.UnionBooleanType)
    return target


def cut(target, *tools):
    for t in tools:
        tbm().booleanOperation(target, t, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return target


def inter(target, tool):
    tbm().booleanOperation(target, tool, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return target


def place(body, fr):
    tbm().transform(body, matrix(fr))
    return body


def wedge(axis, a0, a1, corner, p1, p2):
    """Graniastoslup trojkatny (zebro). Trojkat prostokatny corner-p1-p2 w plaszczyznie
    prostopadlej do osi 'x' lub 'y', przyprostokatne rownolegle do osi ukladu."""
    def to3(q, s):
        return (s, q[0], q[1]) if axis == "x" else (q[0], s, q[1])
    pts = [corner, p1, p2]
    lo = (min(q[0] for q in pts), min(q[1] for q in pts))
    hi = (max(q[0] for q in pts), max(q[1] for q in pts))
    b0, b1 = to3(lo, a0), to3(hi, a1)
    body = box(min(b0[0], b1[0]), max(b0[0], b1[0]), min(b0[1], b1[1]), max(b0[1], b1[1]),
               min(b0[2], b1[2]), max(b0[2], b1[2]))
    # polprzestrzen po stronie wierzcholka kata prostego
    h = (p2[0] - p1[0], p2[1] - p1[1])
    hl = math.hypot(*h)
    h = (h[0] / hl, h[1] / hl)
    n = (-h[1], h[0])
    if (corner[0] - p1[0]) * n[0] + (corner[1] - p1[1]) * n[1] < 0:
        n = (-n[0], -n[1])
    mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    big = 4 * hl + 100
    c = (mid[0] + n[0] * big / 2, mid[1] + n[1] * big / 2)
    am = (a0 + a1) / 2
    hs = obox(to3(c, am), to3(h, 0.0), to3(n, 0.0), big, big, abs(a1 - a0) + 2)
    return inter(body, hs)


# ---------- przeguby (kod OpenSCAD przeniesiony do ukladow lokalnych) ----------
def fork_solid(fr):
    """Widelki: sworzen w osi Y ukladu fr, otwarte w strone +X, mostek w -X."""
    w = P.FORK_GAP / 2 + P.FORK_WALL
    r = P.FORK_THICK / 2
    body = place(cyl((0, -w, 0), (0, w, 0), r), fr)
    return union(body, fbox(fr, -(P.FORK_DEPTH + P.FORK_BRIDGE), 0, -w, w, -r, r))


def fork_cutters(fr):
    w = P.FORK_GAP / 2 + P.FORK_WALL
    zt = P.FORK_THICK / 2 + 1.0
    slot = fbox(fr, -P.FORK_DEPTH, 20.0, -P.FORK_GAP / 2, P.FORK_GAP / 2, -zt, zt)
    pin = place(cyl((0, -w - 2, 0), (0, w + 2, 0), P.M2_HOLE / 2), fr)
    return [slot, pin]


def part_cube():
    """05b Kostka Kardana. Srodek w (0,0,0); otwor wzdluz X na z=+1.4, wzdluz Y na z=-1.4."""
    s, h = P.CUBE_W, P.CUBE_H
    body = box(-s / 2, s / 2, -s / 2, s / 2, -h / 2, h / 2)
    d45 = K.unit((1, 1, 0))
    side = 2 * (s - 1.0) / math.sqrt(2)          # fazki 1 mm na pionowych krawedziach
    inter(body, obox((0, 0, 0), d45, (-d45[1], d45[0], 0), side, side, h + 2))
    a = P.AXIS_OFFSET
    cut(body, cyl((-s, 0, a), (s, 0, a), P.M2_HOLE / 2), cyl((0, -s, -a), (0, s, -a), P.M2_HOLE / 2))
    return [body]


def part_rod():
    """05 Popychacz. Os X wzdluz preta, sworznie wzdluz Y w x = +/-27.2."""
    xp = P.ROD_PIN_DIST / 2
    f1 = Frame((xp, 0, 0), EX, EY, EZ)
    f2 = Frame((-xp, 0, 0), (-1, 0, 0), (0, -1, 0), EZ)
    xb = xp - P.FORK_DEPTH - P.FORK_BRIDGE
    r = P.FORK_THICK / 2
    body = box(-xb - 0.5, xb + 0.5, -3.5, 3.5, -r, r)
    union(body, fork_solid(f1), fork_solid(f2))
    cut(body, *(fork_cutters(f1) + fork_cutters(f2)))
    # odchudzenie srodka (jak w OpenSCAD)
    for zs in (-1, 1):
        cut(body, box(-xb + 5, xb - 5, -2.2, 2.2, zs * r - 1.0, zs * r + 1.0))
    return [body]


def horn_fork_frame():
    d = (K.D0_U, K.D0_Z, 0.0)
    n = (K.N0_U, K.N0_Z, 0.0)
    return Frame((P.L1, 0.0, 0.0), d, n, K.cross(d, n))


def part_horn_adapter():
    """04 Adapter orczyka. Poczatek na osi serwa w srodku grubosci, X = ramie,
    Z = os serwa (od korpusu na zewnatrz). Strona serwa to z < 0."""
    r = P.FORK_THICK / 2
    ff = horn_fork_frame()
    body = zcyl(0, 0, -r, r, 7.0)
    # plaskownik pod oryginalny orczyk; od gory (+y) tylko 0.9 mm scianki i skrocony,
    # bo przy alfa < -25 deg dolny mostek popychacza schodzi nad ramie
    hx = max(P.HORN_HOLES) + P.M2_MOUNT / 2 + 1.0
    union(body, box(0, hx, -5.0, P.HORN_RECESS[1] / 2 + 0.9, -r, r))
    cut(body, obox((hx, P.HORN_RECESS[1] / 2 + 0.9, 0), K.unit((1, 1, 0)), K.unit((-1, 1, 0)), 5.0, 5.0,
                   2 * r + 2))
    q = ff.pt((-(P.FORK_DEPTH + P.FORK_BRIDGE / 2), -(P.FORK_GAP / 2 + P.FORK_WALL / 2), 0.0))
    qd = K.unit(q)
    union(body, obox(K.mul(q, 0.5), qd, (-qd[1], qd[0], 0), K.norm(q), 8.0, P.FORK_THICK))
    union(body, fork_solid(ff))
    cut(body, *fork_cutters(ff))
    cut(body, zcyl(0, 0, -r - 1, r + 1, P.HORN_BORE / 2))
    rl, rw, rd = P.HORN_RECESS
    cut(body, box(-2.0, rl - 2.0, -rw / 2, rw / 2, -r - 0.1, -r + rd))
    for hx in P.HORN_HOLES:
        cut(body, zcyl(hx, 0, -r - 1, r + 1, P.M2_MOUNT / 2))
    return [body]


def bracket_fork_frame():
    d = (-K.D0_U, 0.0, -K.D0_Z)
    n = (K.N0_U, 0.0, K.N0_Z)
    return Frame((0.0, 0.0, 0.0), d, n, K.cross(d, n))


def bracket_body(screws):
    """Widelki pod tace. Poczatek w osi sworznia, X = radialnie, Y = stycznie,
    Z = normalna tacy. Plaszczyzna styku ze spodem tacy na z = PIVOT_H."""
    ff = bracket_fork_frame()
    bx, by, bt = P.BRACKET_BASE
    top = P.PIVOT_H
    body = box(-bx + 6.0, 6.0, -by / 2, by / 2, top - bt, top)
    union(body, fork_solid(ff))
    cut(body, box(-30, 30, -30, 30, top, top + 30))
    cut(body, *fork_cutters(ff))
    if screws:
        for s in (-1, 1):
            cut(body, zcyl(0, s * P.BRACKET_SCREW, top - bt - 1, top + 1, P.M3_HOLE / 2))
    return body


def part_bracket():
    """05c Uchwyt testowy: tylko do testu jednej nogi w Etapie 0 (w tacy widelki sa wbudowane)."""
    return [bracket_body(True)]


# ---------- taca ----------
def part_plate():
    """03 Taca z wbudowanymi widelkami. Poczatek = srodek plaszczyzny osi sworzni."""
    z0 = P.PIVOT_H
    z1 = z0 + P.PLATE_T
    R = P.PLATE_D / 2
    body = zcyl(0, 0, z0, z1, R)
    zr = z0 - P.RIB_H
    hub = zcyl(0, 0, zr, z0, 14.4)
    cut(hub, zcyl(0, 0, zr - 1, z0 + 1, 12.0))
    union(body, hub)
    for a in P.RIB_ANGLES:
        d = (math.cos(math.radians(a)), math.sin(math.radians(a)), 0.0)
        c = K.mul(d, 55.0)
        union(body, obox((c[0], c[1], zr + P.RIB_H / 2), d, (-d[1], d[0], 0), 86.0, P.RIB_W, P.RIB_H))
    for psi in P.PSI_DEG:                        # widelki drukowane razem z taca
        ps = math.radians(psi)
        u = (math.cos(ps), math.sin(ps), 0.0)
        t = (-math.sin(ps), math.cos(ps), 0.0)
        union(body, place(bracket_body(False), Frame(K.mul(u, P.R_PLATE), u, t, EZ)))
    return [body]


def part_rim():
    z0 = P.PIVOT_H + P.PLATE_T
    R = P.PLATE_D / 2
    ring = zcyl(0, 0, z0, z0 + P.RIM_H, R)
    return [cut(ring, zcyl(0, 0, z0 - 1, z0 + P.RIM_H + 1, R - P.RIM_W))]


def part_ball():
    return [sphere((0, 0, 0), P.BALL_D / 2)]


# ---------- serwo (model odniesienia, nie do druku) ----------
def part_servo():
    """HS-422. Poczatek na osi walka w plaszczyznie gory korpusu, Z = walek na zewnatrz,
    X = dlugosc korpusu (walek blizej konca +X)."""
    L, W, H = P.SERVO_BODY
    xe = P.SERVO_SHAFT_FROM_END
    xc = xe - L / 2
    body = box(xe - L, xe, -W / 2, W / 2, -H, 0)
    ft = -P.SERVO_FLANGE_FROM_TOP
    fl = box(xc - P.SERVO_FLANGE_LEN / 2, xc + P.SERVO_FLANGE_LEN / 2, -W / 2, W / 2, ft - P.SERVO_FLANGE_T, ft)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cut(fl, zcyl(xc + sx * P.SERVO_SCREW[0] / 2, sy * P.SERVO_SCREW[1] / 2, ft - 5, ft + 1,
                         P.SERVO_SCREW_D / 2))
    union(body, fl)
    union(body, zcyl(0, 0, 0, P.HORN_PLANE - P.FORK_THICK / 2, 3.0))
    return [body]


# ---------- baza ----------
def _leg_frame(i):
    _, u, t = K.leg_axes(i)
    return Frame((0.0, 0.0, 0.0), u, t, EZ)


def part_base():
    """01 Baza glowna. Uklad swiata: srodek tacy nad (0,0), blat z = 0."""
    ft = P.FLOOR_T
    body = zcyl(0, 0, 0, ft, 62.0)
    union(body, box(6, 40, 40, 115, 0, ft))          # podkladka pod palak (tyl)
    union(body, box(-30, 30, -100, -50, 0, ft))      # jezyk pod konsole (przod)
    union(body, box(-60, 60, -100, -90, 0, ft))      # skrzydla pod sruby konsoli
    xe = P.SERVO_SHAFT_FROM_END
    L = P.SERVO_BODY[0]
    xc = xe - L / 2
    t_wall = P.HORN_PLANE + P.SERVO_FLANGE_FROM_TOP + P.SERVO_FLANGE_T   # 18.2
    pw, ph = P.SERVO_POCKET
    holes = []
    for i in range(3):
        lf = _leg_frame(i)
        union(body, fbox(lf, 40, 112, 9.5, 32, 0, ft))                   # ramie
        wall = fbox(lf, 50, 112, t_wall, t_wall + P.WALL_T, 0, 48)
        cut(wall, fbox(lf, P.R_BASE + xc - pw / 2, P.R_BASE + xc + pw / 2, t_wall - 1,
                       t_wall + P.WALL_T + 1, P.Z_SERVO - ph / 2, P.Z_SERVO + ph / 2))
        for sx in (-1, 1):
            for sz in (-1, 1):
                uu = P.R_BASE + xc + sx * P.SERVO_SCREW[0] / 2
                zz = P.Z_SERVO + sz * P.SERVO_SCREW[1] / 2
                holes.append(cyl(lf.pt((uu, t_wall - 1, zz)), lf.pt((uu, t_wall + P.WALL_T + 1, zz)),
                                 P.SERVO_SCREW_D / 2))
        union(body, wall)
        for u0 in (50, 108):                                              # zebra sciany
            union(body, wedge_leg(lf, u0, u0 + 4, t_wall + P.WALL_T, 31.0, ft, 40.0))
        holes.append(zcyl(*lf.pt((104, 21, 0))[:2], -0.1, 1.0, P.FOOT_D / 2))   # stopka
    # komora elektroniki
    bx, by, bz = P.BAY
    bw = P.BAY_WALL
    bay = box(-bx / 2, bx / 2, -by / 2, by / 2, ft, bz)
    cut(bay, box(-bx / 2 + bw, bx / 2 - bw, -by / 2 + bw, by / 2 - bw, ft - 1, bz + 1))
    cut(bay, box(-7, 7, -by / 2 - 1, by / 2 + 1, 12, bz + 1), box(-bx / 2 - 1, bx / 2 + 1, -7, 7, 12, bz + 1))
    union(body, bay)
    for sx in (-1, 1):
        for sy in (-1, 1):
            union(body, zcyl(sx * 33, sy * 23, ft, ft + 5, 3.0))
            holes.append(zcyl(sx * 33, sy * 23, ft + 1, ft + 5.1, P.M3_INSERT / 2))
    for (x, y) in P.ARM_BOLTS + P.CONSOLE_BOLTS:                            # wkladki M3
        holes.append(zcyl(x, y, 1.0, ft + 0.1, P.M3_INSERT / 2))
    holes.append(zcyl(0, -92, -0.1, 1.0, P.FOOT_D / 2))
    cut(body, *holes)
    return [body]


def wedge_leg(lf, u0, u1, t0, t1, z0, z1):
    """Zebro trojkatne w ukladzie nogi: kat prosty przy (t0, z0)."""
    w = wedge("x", u0, u1, (t0, z0), (t0, z1), (t1, z0))
    return place(w, lf)


# ---------- palak C-Arm ----------
def part_lower_arm():
    """06 Palak dolny (stopa + slupek). Uklad swiata."""
    pw = P.POST_W / 2
    y0, y1 = P.ARM_REACH, P.ARM_REACH + P.POST_D
    yc = (y0 + y1) / 2
    tn = P.TUNNEL / 2
    zt = 15.0
    body = box(8, 38, 70, 124, P.FLOOR_T, zt)
    union(body, box(-14, 40, 124, 165, 0, zt))
    union(body, box(-pw, pw, y0, y1, zt, P.LOWER_POST_TOP))
    union(body, wedge("x", -pw, pw, (y1, zt), (y1, zt + 60), (165, zt)))
    union(body, wedge("y", y0 + 4, y1 - 4, (pw, zt), (pw, zt + 50), (38, zt)))
    cut(body, box(-tn, tn, yc - tn, yc + tn, 5, P.LOWER_POST_TOP + 1))     # tunel kablowy
    cut(body, box(-tn, 23, yc - tn, yc + tn, 5, 13))
    cut(body, box(19, 27, 69, yc + tn, 7, 13))
    cut(body, box(16, 30, 69, 80, 7, 13.5))                                # gniazdo JST-XH
    for (x, y) in P.ARM_BOLTS:
        cut(body, zcyl(x, y, P.FLOOR_T - 1, zt + 1, 1.7), zcyl(x, y, zt - 4, zt + 1, 3.25))
    for z in P.INSERT_Z:
        for s in (-1, 1):
            cut(body, cyl((s * (pw + 0.1), yc, z), (s * (pw - 5.0), yc, z), P.M3_INSERT / 2))
    for x in (-8, 34):
        cut(body, zcyl(x, 158, -0.1, 1.0, P.FOOT_D / 2))
    return [body]


def part_upper_arm():
    """07 Palak gorny z glowica kamery. Poczatek: os obiektywu, z = 0 w plaszczyznie
    spodu glowicy (= wysokosc kamery nad tacka)."""
    pw = P.POST_W / 2
    y0, y1 = P.ARM_REACH, P.ARM_REACH + P.POST_D
    yc = (y0 + y1) / 2
    tn = P.TUNNEL / 2
    at = P.ARM_T
    sw = P.SLEEVE_WALL
    st = -36.0                                   # gora tulei (spod slupka gornego)
    sb = st - P.SLEEVE_LEN
    body = box(-pw, pw, 28, y1, 0, at)
    union(body, box(-pw, pw, y0, y1, st, at))
    sleeve = box(-pw - sw, pw + sw, y0, y1 + sw, sb, st)
    cut(sleeve, box(-pw - 0.25, pw + 0.25, y0 - 1, y1 + 0.25, sb - 1, st))
    # szczelina regulacji wysokosci (170..210 mm), obie scianki boczne
    zc_nom = P.Z_TOP
    s_lo = min(P.INSERT_Z) - (zc_nom + P.H_CAM_MAX)
    s_hi = max(P.INSERT_Z) - (zc_nom + P.H_CAM_MIN)
    slot = box(-pw - sw - 1, pw + sw + 1, yc - 1.7, yc + 1.7, s_lo, s_hi)
    union(slot, cyl((-pw - sw - 1, yc, s_lo), (pw + sw + 1, yc, s_lo), 1.7),
          cyl((-pw - sw - 1, yc, s_hi), (pw + sw + 1, yc, s_hi), 1.7))
    cut(sleeve, slot)
    union(body, sleeve)
    ht = P.HEAD_T
    union(body, zcyl(0, 0, 0, ht, P.HEAD_D / 2))
    cut(body, box(-tn, tn, yc - tn, yc + tn, st - 1, at - 4))              # tunel w slupku
    cut(body, box(-tn, tn, 27, yc + tn, 4, at - 4))                        # tunel w ramieniu
    led = zcyl(0, 0, -0.1, P.LED_RING_T + 0.4, P.LED_RING_OD / 2 + 0.3)     # gniazdo pierscienia LED
    cut(led, zcyl(0, 0, -1, 5, P.LED_RING_ID / 2 - 1.0))
    cut(body, led)
    cm = P.CAM_MODULE / 2
    cut(body, box(-cm, cm, -cm, cm, 2.0, ht + 1))                        # gniazdo modulu OV2640
    # obiektyw: modul lezy na waskiej polce, otwor rozszerza sie stozkowo (pole widzenia 120 deg)
    rl = P.CAM_LENS_D / 2
    cut(body, zcyl(0, 0, 2.01, -0.1, rl, rl + 2.11 * math.tan(math.radians(62))))
    bl, bw_, _ = P.CAM_BOARD
    cut(body, box(-bl / 2 - 0.5, bl / 2 + 0.5, -bw_ / 2 - 0.5, bw_ / 2 + 0.5, ht - 1.5, ht + 0.1))
    for sx in (-1, 1):
        for sy in (-1, 1):
            cut(body, zcyl(sx * 17, sy * 11, -1, ht + 1, 1.1))
    return [body]


def part_led_ring():
    ring = zcyl(0, 0, 0.4, 0.4 + P.LED_RING_T, P.LED_RING_OD / 2)
    return [cut(ring, zcyl(0, 0, 0, 5, P.LED_RING_ID / 2))]


def part_cam_board():
    bl, bw_, bt = P.CAM_BOARD
    ht = P.HEAD_T
    cm = P.CAM_MODULE / 2 - 0.1
    b = box(-bl / 2, bl / 2, -bw_ / 2, bw_ / 2, ht - 1.5, ht - 1.5 + bt)
    return [union(b, box(-cm, cm, -cm, cm, 2.0, ht - 1.5), zcyl(0, 0, 0.5, 2.0, P.CAM_LENS_D / 2 - 0.5))]


# ---------- konsola ----------
def console_frame():
    a = math.radians(P.CONSOLE_ANGLE)
    return Frame((0.0, P.CONSOLE_FRONT_Y, P.CONSOLE_FRONT_H), EX,
                 (0.0, math.cos(a), math.sin(a)), (0.0, -math.sin(a), math.cos(a)))


def part_console():
    """02 Panel konsoli. Uklad swiata, plyta czolowa 120 x 62 pochylona o 40 deg."""
    S = console_frame()
    a = math.radians(P.CONSOLE_ANGLE)
    W, Lf = P.CONSOLE_W, P.CONSOLE_L
    yb = P.CONSOLE_FRONT_Y + Lf * math.cos(a)
    zmax = P.CONSOLE_FRONT_H + Lf * math.sin(a)
    w = P.CONSOLE_WALL
    body = box(-W / 2, W / 2, P.CONSOLE_FRONT_Y, yb, 0, zmax)
    inter(body, fbox(S, -150, 150, -100, 160, -150, 0))
    cav = box(-W / 2 + w, W / 2 - w, P.CONSOLE_FRONT_Y + w, yb - w, -1, zmax)
    inter(cav, fbox(S, -150, 150, -100, 160, -150, -P.CONSOLE_FACE_T))
    cut(body, cav)
    # jezyk do bazy (na podkladce bazy, z = FLOOR_T)
    tongue = box(-58, 58, yb - 12, -90, P.FLOOR_T, P.FLOOR_T + 4)
    for (x, y) in P.CONSOLE_BOLTS:
        cut(tongue, zcyl(x, y, 0, 20, 1.7))
    union(body, tongue)
    # otwory w plycie czolowej (s, w w ukladzie plyty)
    b = P.BTN_HOLE / 2
    dpad = (-36.0, 31.0)
    for (s, wv) in ((dpad[0], dpad[1] + 14), (dpad[0], dpad[1] - 14), (dpad[0] - 14, dpad[1]),
                    (dpad[0] + 14, dpad[1]), (46.0, 20.0)):
        cut(body, fbox(S, s - b, s + b, wv - b, wv + b, -8, 2))
    ow, oh = P.OLED_WIN
    cut(body, fbox(S, -ow / 2, ow / 2, 34 - oh / 2, 34 + oh / 2, -8, 2))
    cut(body, cyl(S.pt((30, 42, -8)), S.pt((30, 42, 2)), P.ENC_HOLE / 2))
    # gniazdo DC i wlacznik w bokach, przepust kabli z tylu
    cut(body, cyl((W / 2 - 4, -130, 9), (W / 2 + 1, -130, 9), P.DC_JACK_D / 2))
    rw, rh = P.ROCKER
    cut(body, box(-W / 2 - 1, -W / 2 + 4, -120 - rw / 2, -120 + rw / 2, 7, 7 + rh))
    cut(body, box(-15, 15, yb - w - 1, yb + 1, 11, 21))
    return [body]


# ---------- kupon tolerancji ----------
def part_coupon():
    """00 Kupon tolerancji: otwory 2.0/2.05/2.10/2.15 i szczeliny 8.2/8.4/8.6."""
    body = box(0, 66, 0, 16, 0, 3)
    for k, d in enumerate((2.0, 2.05, 2.10, 2.15)):
        cut(body, zcyl(6 + k * 8, 8, -1, 4, d / 2))
    x = 38.0
    for gap in (8.2, 8.4, 8.6):
        blk = box(x - 4, x + 4, 16, 16 + gap + 2 * P.FORK_WALL, 0, P.FORK_THICK)
        cut(blk, box(x - 5, x + 5, 16 + P.FORK_WALL, 16 + P.FORK_WALL + gap, 3, P.FORK_THICK + 1))
        union(body, blk)
        x += 10.0
    return [body]


# Nazwa komponentu -> (budowniczy, do druku?, sztuk do druku, kolor RGB)
PARTS = [
    ("00_Kupon_Tolerancji", part_coupon, True, 1, (230, 160, 40)),
    ("01_Baza_Glowna_HS422", part_base, True, 1, (70, 70, 80)),
    ("02_Panel_Konsoli_OLED", part_console, True, 1, (60, 110, 170)),
    ("03_Taca_Robocza_210mm", part_plate, True, 1, (25, 25, 25)),
    ("03b_Rant_210mm", part_rim, True, 1, (200, 60, 50)),
    ("04_Adapter_Orczyka_24mm", part_horn_adapter, True, 4, (240, 200, 40)),
    ("05_Popychacz_60mm", part_rod, True, 4, (240, 200, 40)),
    ("05b_Kostka_Kardana", part_cube, True, 8, (60, 170, 90)),
    ("05c_Uchwyt_Testowy", part_bracket, True, 1, (240, 200, 40)),
    ("06_Palak_Dolny", part_lower_arm, True, 1, (70, 70, 80)),
    ("07_Palak_Gorny_Kamera", part_upper_arm, True, 1, (70, 70, 80)),
    ("HS-422", part_servo, False, 0, (20, 20, 20)),
    ("Kulka_40mm", part_ball, False, 0, (250, 140, 30)),
    ("Pierscien_LED_12x", part_led_ring, False, 0, (240, 240, 240)),
    ("ESP32-S3_CAM", part_cam_board, False, 0, (20, 90, 40)),
]
