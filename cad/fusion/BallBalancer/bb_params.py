# BALL BALANCER 3-RRS - PARAMETRY GEOMETRII (Fusion 360)
# Jedno zrodlo prawdy dla skryptu Fusion. Wartosci przepisane z notatek v2
# (05 Geometria i wymiary, 24 Kod OpenSCAD ciegien). Wszystko w mm i stopniach.
# Plik w czystym ASCII (tak jak params.scad).

import math

# --- Kinematyka (musza sie zgadzac z firmware: R_BASE, L1, L2, ZS) ---
R_BASE = 90.0          # promien osi serw [mm]
R_PLATE = 90.0         # promien punktow podparcia tacy [mm]
L1 = 24.0              # orczyk: os serwa -> os przegubu [mm]
L2 = 60.0              # popychacz os-os (54.4 pret + 2 x 2.8 kostki) [mm]
Z_SERVO = 28.0         # os serwa nad blatem [mm]
PSI_DEG = (90.0, 210.0, 330.0)   # serwo 1 tyl, 2 przod-lewo, 3 przod-prawo
ALPHA_LIMIT = 35.0     # mechaniczny zakres orczyka [deg]
TILT_LIMIT = 6.0       # limit programowy przechylu [deg]

H0 = math.sqrt(L2 * L2 - L1 * L1)     # 55.0 mm
Z_PIVOT = Z_SERVO + H0                # 83.0 mm: os uchwytow przy alpha = 0

# --- Przeguby (z kodu OpenSCAD) ---
M2_HOLE = 2.05
M2_MOUNT = 2.15
M3_HOLE = 3.20
M3_INSERT = 4.00       # otwor pod wkladke heat-set M3
CUBE_W = 8.0
CUBE_H = 10.0
AXIS_OFFSET = 1.4      # osie kostki na +/-1.4 od srodka (2.8 mm miedzy osiami)
FORK_GAP = 8.4
FORK_WALL = 2.8
FORK_THICK = 7.6
FORK_DEPTH = 7.5
FORK_BRIDGE = 2.5      # mostek za szczelina (krotszy niz w OpenSCAD: mniej w dol przy -35 deg)
ROD_PIN_DIST = 54.4    # popychacz: odleglosc sworzni
PIVOT_H = 10.5         # uchwyt tacy: os sworznia pod plaszczyzna mocowania
BRACKET_BASE = (17.0, 28.0, 4.0)   # radialnie x stycznie x grubosc
BRACKET_SCREW = 10.0   # sruby M3 co +/-10 mm stycznie
HORN_HOLES = (8.0, 12.5)           # otwory w oryginalnym orczyku HS-422 (ZMIERZYC!)
HORN_BORE = 6.5
HORN_RECESS = (20.0, 6.2, 2.3)     # wglebienie na oryginalny orczyk

# --- Serwo Hitec HS-422 ---
SERVO_BODY = (40.6, 19.8, 36.6)    # dlugosc x szerokosc x wysokosc
SERVO_SHAFT_FROM_END = 10.0        # os walka od krotszego konca korpusu (ZMIERZYC)
SERVO_FLANGE_LEN = 54.6
SERVO_FLANGE_T = 2.5
SERVO_FLANGE_FROM_TOP = 7.9        # gorna (od strony orczyka) powierzchnia ucha pod gora korpusu
SERVO_SCREW = (48.5, 10.0)         # rozstaw srub
SERVO_SCREW_D = 2.2                # otwor pilotowy pod wkrety samogwintujace z kompletu serwa (bez nakretek)
SERVO_POCKET = (41.0, 20.2)        # kieszen = korpus + 0.4
HORN_PLANE = 7.8                   # srodek grubosci adaptera nad gora korpusu (walek 4 + 3.8, ZMIERZYC)

# --- Taca ---
PLATE_D = 210.0
PLATE_T = 3.0
RIB_H = 5.0
RIB_W = 2.4
RIB_ANGLES = (0.0, 60.0, 120.0, 180.0, 240.0, 300.0)  # omijaja uchwyty (90/210/330)
RIM_W = 2.0
RIM_H = 3.5
BALL_D = 40.0

Z_TOP = Z_PIVOT + PIVOT_H + PLATE_T   # 96.5 mm: gora tacy w pozycji neutralnej

# --- Kamera i palak ---
H_CAM = 195.0          # obiektyw nad gora tacy (regulacja 170..210)
H_CAM_MIN = 170.0
H_CAM_MAX = 210.0
ARM_REACH = 132.0      # przednia sciana slupka od srodka
POST_W = 20.0
POST_D = 20.0
TUNNEL = 8.0           # tunel kablowy 8 x 8
LOWER_POST_TOP = 218.0 # gora slupka dolnego nad blatem (<= 220, miesci sie w drukarce)
ARM_T = 16.0           # grubosc ramienia gornego
SLEEVE_LEN = 90.0
SLEEVE_WALL = 4.0
INSERT_Z = (190.0, 210.0)          # wkladki M3 w slupku dolnym (regulacja wysokosci)
HEAD_D = 60.0
HEAD_T = 8.0
LED_RING_OD = 50.0
LED_RING_ID = 36.0
LED_RING_T = 3.2
CAM_BOARD = (40.0, 28.0, 1.6)      # ESP32-S3 CAM (ZMIERZYC swoja plytke)
CAM_MODULE = 8.6                   # kwadratowy modul OV2640 (gniazdo od gory glowicy, ZMIERZYC)
CAM_LENS_D = 7.5                   # otwor na obiektyw (mniejszy niz modul, ZMIERZYC)

# --- Baza ---
FLOOR_T = 5.0
WALL_T = 5.0           # sciana z kieszenia serwa
BAY = (80.0, 60.0, 30.0)           # komora elektroniki (zewn.)
BAY_WALL = 2.4
ARM_BOLTS = ((13.0, 110.0), (33.0, 110.0))   # sruby stopy palaka: poza obrysem tacy (r > 110)
CONSOLE_BOLTS = ((-54.0, -97.0), (54.0, -97.0))  # sruby konsoli: poza obrysem tacy (r > 110)
FOOT_D = 10.5          # gniazdo stopki gumowej

# --- Konsola ---
CONSOLE_W = 120.0
CONSOLE_L = 62.0
CONSOLE_ANGLE = 40.0
CONSOLE_FRONT_Y = -150.0
CONSOLE_FRONT_H = 12.0
CONSOLE_WALL = 2.4
CONSOLE_FACE_T = 3.0
BTN_HOLE = 12.4        # przycisk tact 12x12 z nasadka
ENC_HOLE = 7.5         # tulejka enkodera KY-040
OLED_WIN = (24.0, 13.0)
DC_JACK_D = 8.0
ROCKER = (13.0, 19.0)

# --- Wydruk ---
PRINT_BED = 220.0
