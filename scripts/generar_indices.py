"""Genera un README.md con el índice de preguntas en cada carpeta de preguntas/.

Uso: python scripts/generar_indices.py
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "preguntas"
ORDEN_NIVEL = {"Junior": 0, "Mid": 1, "Senior": 2}
NOMBRES = {
    "sql": "SQL",
    "python": "Python",
    "spark": "Spark",
    "modelado-datos": "Modelado de datos",
    "orquestacion": "Orquestación",
    "cloud": "Cloud",
    "streaming": "Streaming",
    "system-design": "System Design",
    "behavioral": "Behavioral",
}


def leer_metadatos(ruta: Path) -> tuple[str, str]:
    texto = ruta.read_text(encoding="utf-8")
    titulo = re.search(r"^# (.+)$", texto, re.MULTILINE)
    nivel = re.search(r"^\*\*Nivel:\*\* (.+)$", texto, re.MULTILINE)
    return (
        titulo.group(1).strip() if titulo else ruta.stem,
        nivel.group(1).strip() if nivel else "—",
    )


def clave_orden(fila: tuple[str, str, str]) -> tuple[int, str]:
    _, nivel, titulo = fila
    rango = next((v for k, v in ORDEN_NIVEL.items() if k in nivel), 99)
    return rango, titulo.lower()


for carpeta in sorted(p for p in RAIZ.iterdir() if p.is_dir()):
    filas = []
    for md in carpeta.glob("*.md"):
        if md.name == "README.md":
            continue
        titulo, nivel = leer_metadatos(md)
        filas.append((md.name, nivel, titulo))
    filas.sort(key=clave_orden)

    nombre = NOMBRES.get(carpeta.name, carpeta.name.replace("-", " ").capitalize())
    lineas = [
        f"# {nombre}",
        "",
        f"[← Volver al índice general](../../README.md) · {len(filas)} preguntas",
        "",
        "| # | Pregunta | Nivel |",
        "|---|---|---|",
    ]
    lineas += [f"| {i} | [{t}]({f}) | {n} |" for i, (f, n, t) in enumerate(filas, 1)]
    (carpeta / "README.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"{carpeta.name}: {len(filas)} preguntas")
