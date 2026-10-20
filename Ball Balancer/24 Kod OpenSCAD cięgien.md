---
title: Kod OpenSCAD cięgien
tags:
  - projekt
  - ball-balancer
  - druk3d
  - openscad
created: 2026-10-20
---

# 🛠️ Ball Balancer: kod OpenSCAD cięgien (gotowy)

Powrót: [[Projekt Ball Balancer]]. Opis części: [[16 Elementy do druku]], [[07 Cięgna i przeguby]]. Kod jest przeniesiony bez zmian z pierwotnej dokumentacji (zestaw cięgien, adapter orczyka, kostka Kardana, uchwyt pod tacę).

> [!success] Status: gotowe do druku (100% ASCII, przetestowane w `/playground.scad`)
> Ustawienia druku: warstwa 0,16–0,20 mm, 4 obrysy, wypełnienie 100%, bez podpór. Wydrukować cały zestaw (`part_select = 0`) **3 razy** (wg v2: **4 razy**, jeden zestaw zapasowy).

> [!warning] Przed drukiem całości (decyzje v2)
> - Najpierw wydrukuj **jeden zestaw** i sprawdź płynność ruchu w całym zakresie $\pm35^\circ$ orczyka oraz luz (cel $\le 0{,}3$ mm). Przy zbyt dużym luzu zmniejsz `fork_gap` do 8,2 mm. Dla zbyt ciasnych sworzni zwiększ `m2_hole` do 2,15 mm.
> - `plate_mount_bracket`: `pivot_h = 10.5` oznacza górną powierzchnię tacy na ok. **96,5 mm** (nie 92). Potwierdź po obróceniu uchwytu pod tacę. Patrz [[05 Geometria i wymiary]].
> - W projekcie Fusion ([[26 Projekt Fusion 360]]) widełki uchwytu są **wbudowane w tacę**; `plate_mount_bracket` służy już tylko do testu jednej nogi.
> - Używaj śrub **M2×18–20** i nakrętek samohamownych (nie M2×16).
> - Zmierz rzeczywiste otwory w oryginalnym orczyku HS-422 (adapter zakłada 8,0 i 12,5 mm od osi).
> - Plan B przy klinowaniu: łączniki kulowe M3 w miejscu górnych kostek.

```openscad
// BALL BALANCER 3-RRS - ZESTAW CIEGIEN (100% ASCII SAFE)
$fn = 64;

// 0 = Wszystkie czesci naraz (komplet na 1 ramie)
// 1 = Popychacz 60mm | 2 = Kostka Kardana | 3 = Adapter HS-422 | 4 = Uchwyt Tacy
part_select = 0; // [0:Wszystkie naraz, 1:Popychacz 60mm, 2:Kostka Kardana, 3:Adapter HS-422, 4:Uchwyt Tacy]

m2_hole = 2.05;
m2_mount = 2.15;
m3_hole = 3.20;

cube_w = 8.0;
cube_h = 10.0;
axis_offset = 1.4;

fork_gap = 8.4;
fork_wall = 2.8;
fork_thick = 7.6;
fork_depth = 7.5;

L1_horn = 24.0;
L2_rod = 54.4;

module fork_head() {
    outer_w = fork_gap + 2 * fork_wall;
    difference() {
        union() {
            translate([0, -outer_w/2, 0])
                rotate([-90, 0, 0])
                cylinder(d = fork_thick, h = outer_w);
            translate([-fork_depth - 4.0, -outer_w/2, -fork_thick/2])
                cube([fork_depth + 4.0, outer_w, fork_thick]);
        }
        translate([-fork_depth, -fork_gap/2, -fork_thick/2 - 1])
            cube([fork_depth + 6.0, fork_gap, fork_thick + 2]);
        translate([-fork_depth, 0, 0])
            rotate([0, 45, 0])
            cube([3, fork_gap, 3], center = true);
        translate([0, -outer_w/2 - 1, 0])
            rotate([-90, 0, 0])
            cylinder(d = m2_hole, h = outer_w + 2);
    }
}

module cardan_cube() {
    difference() {
        hull() {
            cube([cube_w - 2.0, cube_w, cube_h], center = true);
            cube([cube_w, cube_w - 2.0, cube_h], center = true);
        }
        translate([0, 0, axis_offset])
            rotate([0, 90, 0])
            cylinder(d = m2_hole, h = cube_w + 2, center = true);
        translate([0, 0, -axis_offset])
            rotate([90, 0, 0])
            cylinder(d = m2_hole, h = cube_w + 2, center = true);
    }
}

module pushrod_60mm() {
    rod_w = 7.0;
    union() {
        translate([L2_rod/2, 0, 0])
            fork_head();
        translate([-L2_rod/2, 0, 0])
            rotate([0, 0, 180])
            fork_head();
        difference() {
            translate([-(L2_rod/2 - fork_depth - 2), -rod_w/2, -fork_thick/2])
                cube([L2_rod - 2*fork_depth - 4, rod_w, fork_thick]);
            for (z_s = [-1, 1]) {
                translate([0, 0, z_s * (fork_thick/2)])
                    cube([L2_rod - 2*fork_depth - 14, rod_w - 2.6, 2.0], center = true);
            }
        }
    }
}

module hs422_horn_adapter() {
    outer_w = fork_gap + 2 * fork_wall;
    difference() {
        union() {
            translate([L1_horn, 0, 0])
                fork_head();
            hull() {
                cylinder(d = 14.0, h = fork_thick, center = true);
                translate([L1_horn - fork_depth - 3.5, -outer_w/2, -fork_thick/2])
                    cube([2.0, outer_w, fork_thick]);
            }
        }
        cylinder(d = 6.5, h = fork_thick + 2, center = true);
        translate([-2, -3.1, -fork_thick/2 - 0.1])
            cube([20.0, 6.2, 2.3]);
        for (r_h = [8.0, 12.5]) {
            translate([r_h, 0, 0])
                cylinder(d = m2_mount, h = fork_thick + 2, center = true);
        }
    }
}

module plate_mount_bracket() {
    base_len = 28.0;
    base_w = 14.0;
    base_t = 4.0;
    pivot_h = 10.5;
    difference() {
        union() {
            translate([-base_len/2, -base_w/2, 0])
                cube([base_len, base_w, base_t]);
            translate([0, 0, pivot_h])
                rotate([0, -90, 0])
                fork_head();
        }
        translate([-25, -25, -20])
            cube([50, 50, 20]);
        for (x_p = [-10.0, 10.0]) {
            translate([x_p, 0, -1])
                cylinder(d = m3_hole, h = base_t + 10);
        }
    }
}

if (part_select == 0) {
    translate([0, 0, fork_thick/2]) pushrod_60mm();
    translate([-15, 22, cube_h/2]) cardan_cube();
    translate([15, 22, cube_h/2]) cardan_cube();
    translate([-28, -24, fork_thick/2]) hs422_horn_adapter();
    translate([18, -24, 0]) plate_mount_bracket();
} else if (part_select == 1) {
    translate([0, 0, fork_thick/2]) pushrod_60mm();
} else if (part_select == 2) {
    translate([0, 0, cube_h/2]) cardan_cube();
} else if (part_select == 3) {
    translate([0, 0, fork_thick/2]) hs422_horn_adapter();
} else if (part_select == 4) {
    plate_mount_bracket();
}
```
