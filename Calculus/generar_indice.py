"""Regenera Calculus/index.html con la lista de pizarras (HTML) por tema e idioma.

Uso (desde cualquier sitio):  python Calculus/generar_indice.py
Estructura esperada: Calculus/<NN>_Videos/<IDIOMA>/<fichero>.html
"""
import html
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent

IDIOMAS = {  # orden de presentación y nombre en su propio idioma
    "ES": "Español", "EN": "English", "FR": "Français", "PT": "Português", "ZH": "中文",
    "HI": "हिन्दी", "AR": "العربية", "BN": "বাংলা", "ID": "Bahasa Indonesia", "UR": "اردو",
    "RU": "Русский",
}
RTL = {"AR", "UR"}


def titulo(f):
    m = re.search(r"<title>(.*?)</title>", f.read_text(encoding="utf-8"), re.S)
    return html.unescape(m.group(1).strip()) if m else f.stem


def main():
    temas = sorted(d for d in AQUI.glob("*_Videos") if d.is_dir())
    secciones = []
    for tema in temas:
        bloques = []
        for lang, nombre in IDIOMAS.items():
            ficheros = sorted((tema / lang).glob("*.html"))
            if not ficheros:
                continue
            items = "\n".join(
                f'      <li><a href="{tema.name}/{lang}/{f.name}">{html.escape(titulo(f))}</a></li>'
                for f in ficheros)
            d = ' dir="rtl"' if lang in RTL else ""
            bloques.append(f'    <section class="lang"{d}>\n    <h3>{nombre} <span>{lang}</span></h3>\n'
                           f'    <ul>\n{items}\n    </ul>\n    </section>')
        if bloques:
            num = tema.name.split("_")[0]
            secciones.append(f'  <h2>Topic {num}</h2>\n  <div class="grid">\n' + "\n".join(bloques) + "\n  </div>")

    pagina = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calculus · Interactive whiteboards</title>
<style>
:root{{--bg:#16231f;--fg:#f1efe4;--acc:#ffd166;--link:#7cc4ff;--mut:#9fb3aa;--card:#1d2e28}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:Georgia,'Times New Roman',serif;padding:32px 24px;max-width:1200px;margin:auto}}
h1{{margin:0 0 6px;color:var(--acc)}}
p.sub{{color:var(--mut);margin:0 0 28px}}
h2{{border-bottom:2px dashed #3d5a50;padding-bottom:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.lang{{background:var(--card);border-radius:12px;padding:12px 18px}}
.lang h3{{margin:4px 0 8px}} .lang h3 span{{color:var(--mut);font:13px sans-serif}}
ul{{margin:0;padding-inline-start:20px}} li{{margin:4px 0}}
a{{color:var(--link);text-decoration:none}} a:hover{{text-decoration:underline}}
</style></head><body>
  <h1>Calculus · Interactive whiteboards</h1>
  <p class="sub">C.O.S. Sorzano · Step-by-step narrated solutions. Open a page and press ▶ (or the space bar).</p>
{chr(10).join(secciones)}
</body></html>
"""
    (AQUI / "index.html").write_text(pagina, encoding="utf-8")
    print(f"index.html: {len(secciones)} tema(s)")


if __name__ == "__main__":
    main()
