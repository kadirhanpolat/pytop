"""TikZ -> PNG uretim hatti (kilavuz sekilleri).

latex/figures/*.tikz dosyalarini standalone sablonuna sarip xelatex ile
derler, pdftoppm (yoksa Ghostscript) ile 300 dpi beyaz zeminli PNG'ye
cevirir ve assets/chNN/ altina yazar. Yalniz stdlib kullanir.

Kullanim:
    py -3.14 docs/user_guide/tools/build_figures.py                  # tum sekiller
    py -3.14 docs/user_guide/tools/build_figures.py fig_ch04_baz_tanimi
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[1]
FIGURES = GUIDE / "latex" / "figures"
ASSETS = GUIDE / "assets"
DPI = "300"

TEMPLATE = """\\documentclass[tikz,border=2pt]{standalone}
\\usepackage{fontspec}
\\setmainfont{Latin Modern Roman}
\\usetikzlibrary{arrows.meta, positioning, calc, patterns, decorations.pathmorphing}
\\begin{document}
<<TIKZ>>
\\end{document}
"""


def fail(msg: str) -> None:
    sys.exit(f"HATA: {msg}")


def find_raster() -> tuple[str, str]:
    exe = shutil.which("pdftoppm")
    if exe:
        return ("pdftoppm", exe)
    for name in ("gswin64c", "gs"):
        exe = shutil.which(name)
        if exe:
            return ("gs", exe)
    fail("pdftoppm (Poppler) veya Ghostscript bulunamadi. "
         "MiKTeX'in miktex-poppler-bin paketini ya da Ghostscript'i kurun.")
    raise AssertionError  # fail() cikar; tip denetleyici icin


def run(cmd: list[str], cwd: Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"{cmd[0]} basarisiz oldu:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")


def build(tikz: Path, xelatex: str, raster: tuple[str, str]) -> Path:
    m = re.match(r"fig_(ch\d+)_", tikz.stem)
    if not m:
        fail(f"{tikz.name}: ad 'fig_chNN_<ad>.tikz' kalibina uymali")
    out_dir = ASSETS / m.group(1)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / (tikz.stem + ".png")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        body = tikz.read_text(encoding="utf-8")
        (tmp / "fig.tex").write_text(TEMPLATE.replace("<<TIKZ>>", body), encoding="utf-8")
        run([xelatex, "-interaction=nonstopmode", "-halt-on-error", "fig.tex"], tmp)
        pdf = tmp / "fig.pdf"
        if not pdf.exists():
            fail(f"{tikz.name}: PDF uretilemedi")
        kind, exe = raster
        if kind == "pdftoppm":
            run([exe, "-png", "-r", DPI, "-singlefile", str(pdf), str(tmp / "out")], tmp)
        else:
            run([exe, "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m",
                 f"-r{DPI}", f"-sOutputFile={tmp / 'out.png'}", str(pdf)], tmp)
        shutil.copyfile(tmp / "out.png", out_png)
    return out_png


def main() -> None:
    xelatex = shutil.which("xelatex")
    if not xelatex:
        fail("xelatex bulunamadi (MiKTeX veya TeX Live kurun)")
    raster = find_raster()
    istenen = set(sys.argv[1:])
    tikzler = sorted(FIGURES.glob("*.tikz"))
    if istenen:
        tikzler = [t for t in tikzler if t.stem in istenen]
        if not tikzler:
            fail("eslesen .tikz dosyasi yok: " + ", ".join(sorted(istenen)))
    if not tikzler:
        fail(f"{FIGURES} altinda .tikz dosyasi yok")
    for t in tikzler:
        png = build(t, xelatex, raster)
        print(f"  {t.name} -> {png.relative_to(GUIDE)}")
    print(f"Tamam: {len(tikzler)} sekil.")


if __name__ == "__main__":
    main()
