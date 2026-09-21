"""Extrait les logos (Simple Icons + Devicon) vers logos.json.

À lancer UNIQUEMENT si tu ajoutes un nouvel outil dans content.py :
    npm install --no-save simple-icons devicon      (dans le dossier scripts/)
    python extract_logos.py
Le fichier logos.json généré est versionné : build.py n'a pas besoin de npm.
"""
import json
import re
import subprocess
from pathlib import Path

import content

ROOT = Path(__file__).resolve().parent
SI = ROOT / "node_modules" / "simple-icons"
DEV = ROOT / "node_modules" / "devicon" / "icons"

NODE = (
    "const si=require(process.argv[1]);"
    "const o={};for(const i of Object.values(si)){o[i.slug]={hex:i.hex,title:i.title,path:i.path}}"
    "console.log(JSON.stringify(o))"
)
si_all = json.loads(subprocess.check_output(["node", "-e", NODE, str(SI)], text=True))

out = {}
for key, spec in content.LOGOS.items():
    kind, ref = spec[0], spec[1]
    forced = spec[2] if len(spec) > 2 else None
    if kind == "si":
        icon = si_all[ref]
        out[key] = {"kind": "si", "vb": "0 0 24 24", "hex": "#" + icon["hex"],
                    "title": icon["title"], "inner": f'<path d="{icon["path"]}"/>'}
    else:
        svg = (DEV / ref).read_text(encoding="utf-8")
        vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
        inner = svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")].strip()
        ids = set(re.findall(r'\bid="([^"]+)"', inner))
        for i in ids:  # évite les collisions d'identifiants entre logos
            inner = inner.replace(f'id="{i}"', f'id="{key}-{i}"')
            inner = inner.replace(f"url(#{i})", f"url(#{key}-{i})")
            inner = inner.replace(f'href="#{i}"', f'href="#{key}-{i}"')
        out[key] = {"kind": "dev", "vb": vb, "inner": inner}
        if forced:
            out[key]["hex"] = forced

(ROOT / "logos.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{len(out)} logos -> logos.json ({(ROOT / 'logos.json').stat().st_size // 1024} Ko)")
