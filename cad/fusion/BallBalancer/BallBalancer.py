# BALL BALANCER 3-RRS - SKRYPT FUSION 360
# Uruchom: Utilities > Add-Ins > Scripts and Add-Ins > + (ten folder) > Run.
# Menu: 1 buduj model, 2 ustaw pozycje tacy, 3 test zakresu i kolizji,
#       4 kolizje w biezacej pozycji, 5 eksport STL.

import adsk.core
import adsk.fusion
import importlib
import math
import os
import sys
import traceback

_HERE = os.path.dirname(os.path.realpath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import bb_params
import bb_kin
import bb_geom

STL_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", "stl"))
REPORT = os.path.normpath(os.path.join(_HERE, "..", "raport_zakresu.txt"))
TITLE = "Ball Balancer 3-RRS"
US_PER_DEG = 10.0      # start z notatki 22, do kalibracji

_app = None
_ui = None


def _reload():
    global bb_params, bb_kin, bb_geom
    bb_params = importlib.reload(bb_params)
    bb_kin = importlib.reload(bb_kin)
    bb_geom = importlib.reload(bb_geom)


# ---------- pomocnicze ----------
def _design(required=True):
    design = adsk.fusion.Design.cast(_app.activeProduct)
    if design is None or design.rootComponent.occurrences.count == 0 or \
            _occs(design, "03_Taca_Robocza_210mm") == []:
        if required:
            _ui.messageBox("Najpierw zbuduj model (opcja 1) albo otworz zapisany projekt Ball Balancer.", TITLE)
        return None
    return design


def _occs(design, comp_name):
    out = []
    root = design.rootComponent
    for i in range(root.occurrences.count):
        o = root.occurrences.item(i)
        if o.component.name == comp_name:
            out.append(o)

    def idx(o):
        try:
            return int(o.name.rsplit(":", 1)[1])
        except Exception:
            return 0
    return sorted(out, key=idx)


def _y_up():
    """Fusion ma domyslnie os Y w gore; model jest liczony z osia Z w gore."""
    try:
        return _app.preferences.generalPreferences.defaultModelingOrientation == \
            adsk.core.DefaultModelingOrientations.YUpModelingOrientation
    except Exception:
        return False


def _to_fusion(fr):
    """Obrot -90 deg wokol X (z -> y), gdy dokument ma os Y w gore."""
    if not _y_up():
        return fr
    r = lambda v: (v[0], v[2], -v[1])
    return bb_kin.Frame(r(fr.o), r(fr.x), r(fr.y), r(fr.z))


def _set_transform(occ, fr):
    m = bb_geom.matrix(_to_fusion(fr))
    try:
        occ.transform2 = m
    except Exception:
        occ.transform = m


def _apply(design, frames):
    for name, lst in frames.items():
        occs = _occs(design, name)
        for occ, fr in zip(occs, lst):
            _set_transform(occ, fr)


def _appearance(design, name, rgb):
    """Prosty kolor (kopia dowolnego wygladu z biblioteki). Bledy pomijamy - to tylko kosmetyka."""
    try:
        ap = design.appearances.itemByName(name)
        if ap:
            return ap
        base = None
        for li in range(_app.materialLibraries.count):
            lib = _app.materialLibraries.item(li)
            if "ppearance" not in lib.name:
                continue
            for cand in ("Plastic - Matte (Yellow)", "Plastic - Glossy (White)", "ABS (White)"):
                base = lib.appearances.itemByName(cand)
                if base:
                    break
            if base is None:
                for k in range(min(lib.appearances.count, 400)):
                    a = lib.appearances.item(k)
                    if "Plastic" in a.name:
                        base = a
                        break
            if base:
                break
        if base is None:
            return None
        ap = design.appearances.addByCopy(base, name)
        col = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
        for k in range(ap.appearanceProperties.count):
            prop = ap.appearanceProperties.item(k)
            if prop.objectType == adsk.core.ColorProperty.classType():
                try:
                    adsk.core.ColorProperty.cast(prop).value = col
                except Exception:
                    pass
        return ap
    except Exception:
        return None


# ---------- 1. budowa ----------
def build():
    doc = _app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(_app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    root = design.rootComponent

    frames, rep = bb_kin.layout()
    frames.update(bb_kin.static_frames())

    prog = _ui.createProgressDialog()
    prog.isCancelButtonShown = False
    prog.show(TITLE, "Buduje %v / %m", 0, len(bb_geom.PARTS), 0)
    for k, (name, builder, printable, qty, rgb) in enumerate(bb_geom.PARTS):
        prog.progressValue = k
        prog.message = "Buduje: " + name + "  (%v / %m)"
        adsk.doEvents()
        places = frames.get(name, [bb_kin.IDENTITY])
        occ = root.occurrences.addNewComponent(bb_geom.matrix(places[0]))
        comp = occ.component
        comp.name = name
        for j, body in enumerate(builder()):
            b = comp.bRepBodies.add(body)
            b.name = name if j == 0 else "%s_%d" % (name, j)
        ap = _appearance(design, "BB " + name, rgb)
        if ap:
            for j in range(comp.bRepBodies.count):
                comp.bRepBodies.item(j).appearance = ap
        for fr in places[1:]:
            root.occurrences.addExistingComponent(comp, bb_geom.matrix(fr))
    prog.hide()

    _apply(design, frames)
    _app.activeViewport.fit()
    try:
        doc.name = "Ball Balancer 3-RRS"
    except Exception:
        pass
    P = bb_params
    _ui.messageBox(
        "Model zbudowany (pozycja neutralna).\n\n"
        "Gora tacy: %.2f mm, os uchwytow: %.2f mm, kamera: %.1f mm nad blatem.\n"
        "Katy serw w neutrum: %s\n\n"
        "Dalej: 2 = przechyl tacy, 3 = test zakresu i kolizji, 5 = eksport STL.\n"
        "Zapisz projekt (Ctrl+S)."
        % (P.Z_TOP, P.Z_PIVOT, P.Z_TOP + P.H_CAM, ", ".join("%.1f" % a for a in rep["alpha"])),
        TITLE)


# ---------- 2. pozycja ----------
def _fmt_report(rep):
    P = bb_params
    lines = []
    for i, a in enumerate(rep["alpha"]):
        lines.append("Serwo %d (%3.0f deg): alfa = %+6.2f deg  ->  ok. %4.0f us (bez trymu)"
                     % (i + 1, P.PSI_DEG[i], a, 1500 + a * US_PER_DEG))
    lines.append("Skret popychaczy: " + ", ".join("%.2f" % t for t in rep["twist"]) + " deg")
    lines.append("Blad dlugosci (model punktowy vs kostki): " +
                 ", ".join("%+.3f" % e for e in rep["rod_len_err"]) + " mm")
    return "\n".join(lines)


def pose():
    design = _design()
    if design is None:
        return
    val, cancelled = _ui.inputBox(
        "Pozycja tacy:  przechyl X [deg]; przechyl Y [deg]; zmiana wysokosci [mm]; kulka x [mm]; kulka y [mm]\n"
        "Przechyl X > 0 podnosi strone serwa 1 (tyl). Limit programowy: %.0f deg." % bb_params.TILT_LIMIT,
        TITLE, "3; 0; 0; 0; 0")
    if cancelled:
        return
    try:
        v = [float(s.replace(",", ".")) for s in val.replace(" ", "").split(";") if s != ""]
    except ValueError:
        _ui.messageBox("Nie rozumiem: " + val, TITLE)
        return
    v += [0.0] * (5 - len(v))
    rx, ry, dz, bx, by = v[:5]
    frames, rep = bb_kin.layout(bb_params.Z_PIVOT + dz, math.radians(rx), math.radians(ry), (bx, by))
    if frames is None:
        _ui.messageBox("Pozycja nieosiagalna: " + rep, TITLE)
        return
    _apply(design, frames)
    _app.activeViewport.refresh()
    tilt = math.degrees(math.acos(max(-1.0, min(1.0, math.cos(math.radians(rx)) * math.cos(math.radians(ry))))))
    msg = "Przechyl calkowity %.2f deg%s\n\n%s\n\nSprawdzic kolizje w tej pozycji?" % (
        tilt, "  (POWYZEJ LIMITU PROGRAMOWEGO)" if tilt > bb_params.TILT_LIMIT + 1e-6 else "",
        _fmt_report(rep))
    r = _ui.messageBox(msg, TITLE, adsk.core.MessageBoxButtonTypes.YesNoButtonType)
    if r == adsk.core.DialogResults.DialogYes:
        collisions(design)


# ---------- kolizje ----------
def _ename(e):
    try:
        if e.objectType == adsk.fusion.Occurrence.classType():
            return e.name
        if e.objectType == adsk.fusion.BRepBody.classType():
            ctx = e.assemblyContext
            return ctx.name if ctx else e.name
    except Exception:
        pass
    return "?"


def _interference(design, min_mm3=0.5):
    root = design.rootComponent
    coll = adsk.core.ObjectCollection.create()
    for i in range(root.occurrences.count):
        o = root.occurrences.item(i)
        if o.component.name != "00_Kupon_Tolerancji":
            coll.add(o)
    inp = design.createInterferenceInput(coll)
    inp.areCoincidentFacesIncluded = False
    res = design.analyzeInterference(inp)
    out = []
    for i in range(res.count):
        r = res.item(i)
        vol = 0.0
        try:
            vol = r.interferenceBody.volume * 1000.0
        except Exception:
            pass
        if vol >= min_mm3:
            out.append((_ename(r.entityOne), _ename(r.entityTwo), vol))
    return sorted(out, key=lambda x: -x[2])


def collisions(design=None, show=True):
    design = design or _design()
    if design is None:
        return None
    hits = _interference(design)
    if show:
        if not hits:
            _ui.messageBox("Brak kolizji (prog 0.5 mm3).", TITLE)
        else:
            _ui.messageBox("Kolizje:\n" + "\n".join("%s  <->  %s : %.1f mm3" % h for h in hits[:30]), TITLE)
    return hits


# ---------- 3. test zakresu ----------
def range_test():
    design = _design()
    if design is None:
        return
    P = bb_params
    lines = ["RAPORT ZAKRESU I KOLIZJI - Ball Balancer 3-RRS", ""]
    lines.append(bb_kin.range_report())
    lines.append("")
    lines.append("Wymiary wydrukow (stol %.0f mm):" % P.PRINT_BED)
    for name, builder, printable, qty, rgb in bb_geom.PARTS:
        occs = _occs(design, name)
        if not printable or not occs:
            continue
        bb = occs[0].component.bRepBodies.item(0).boundingBox
        size = sorted(10.0 * (getattr(bb.maxPoint, a) - getattr(bb.minPoint, a)) for a in "xyz")
        ok = size[2] <= P.PRINT_BED
        lines.append("  %-26s %5.1f x %5.1f x %5.1f mm  %s" % (name, size[2], size[1], size[0],
                                                               "ok" if ok else "ZA DUZY"))
    lines.append("")
    lines.append("Kolizje (kierunek osi przechylu co 60 deg, prog 0.5 mm3):")
    prog = _ui.createProgressDialog()
    prog.isCancelButtonShown = True
    poses = [(th, k * 60.0) for th in (0.0, P.TILT_LIMIT, 9.0) for k in range(6 if th > 0 else 1)]
    prog.show(TITLE, "Pozycja %v / %m", 0, len(poses), 0)
    bad = 0
    for n, (th, phi) in enumerate(poses):
        if prog.wasCancelled:
            break
        prog.progressValue = n
        adsk.doEvents()
        rx = math.radians(th) * math.cos(math.radians(phi))
        ry = math.radians(th) * math.sin(math.radians(phi))
        frames, rep = bb_kin.layout(None, rx, ry)
        head = "  %4.1f deg, kierunek %3.0f: " % (th, phi)
        if frames is None:
            lines.append(head + "nieosiagalne (" + rep + ")")
            continue
        _apply(design, frames)
        hits = _interference(design)
        al = "alfa " + "/".join("%+.1f" % a for a in rep["alpha"])
        if hits:
            bad += 1
            lines.append(head + al + " -> KOLIZJE:")
            lines += ["      %s <-> %s : %.1f mm3" % h for h in hits]
        else:
            lines.append(head + al + " -> ok")
    prog.hide()
    frames, _ = bb_kin.layout()
    _apply(design, frames)
    _app.activeViewport.refresh()
    text = "\n".join(lines)
    try:
        with open(REPORT, "w") as f:
            f.write(text + "\n")
        where = "\n\nZapisano: " + REPORT
    except Exception:
        where = ""
    _ui.messageBox(text[:3500] + where, TITLE)


# ---------- 5. eksport STL ----------
def export_stl():
    design = _design()
    if design is None:
        return
    if not os.path.isdir(STL_DIR):
        os.makedirs(STL_DIR)
    em = design.exportManager
    done = []
    for name, builder, printable, qty, rgb in bb_geom.PARTS:
        if not printable:
            continue
        occs = _occs(design, name)
        if not occs:
            continue
        path = os.path.join(STL_DIR, name + ".stl")
        opts = em.createSTLExportOptions(occs[0].component, path)
        opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(opts)
        done.append("%-26s x%d" % (name, qty))
    _ui.messageBox("Zapisano STL w:\n%s\n\n%s\n\nUstaw orientacje w slicerze (notatka 16)."
                   % (STL_DIR, "\n".join(done)), TITLE)


MENU = ("Ball Balancer 3-RRS - wybierz:\n"
        "1 = zbuduj model (nowy dokument)\n"
        "2 = ustaw pozycje tacy (kinematyka odwrotna)\n"
        "3 = test zakresu i kolizji (raport)\n"
        "4 = kolizje w biezacej pozycji\n"
        "5 = eksport STL do cad/stl")


def run(context):
    global _app, _ui
    _app = adsk.core.Application.get()
    _ui = _app.userInterface
    try:
        _reload()
        val, cancelled = _ui.inputBox(MENU, TITLE, "1")
        if cancelled:
            return
        choice = val.strip()
        if choice == "1":
            build()
        elif choice == "2":
            pose()
        elif choice == "3":
            range_test()
        elif choice == "4":
            collisions()
        elif choice == "5":
            export_stl()
        else:
            _ui.messageBox("Nieznana opcja: " + choice, TITLE)
    except Exception:
        if _ui:
            _ui.messageBox("Blad:\n" + traceback.format_exc(), TITLE)
