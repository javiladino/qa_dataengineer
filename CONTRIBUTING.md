# Guía de contribución

¡Gracias por aportar! Sigue estas pautas para mantener el banco ordenado y útil.

## Reglas

1. **Anonimiza siempre a la empresa.** Usa el formato `Sector, año` (ej. `Fintech, 2026`). Nunca incluyas nombres de empresas, entrevistadores ni detalles bajo NDA.
2. **Una pregunta por archivo**, dentro de la carpeta del tema correspondiente en `preguntas/`.
3. **Nombre del archivo** en minúsculas y con guiones: `diferencia-rank-dense-rank.md`.
4. **Usa la [plantilla](templates/pregunta.md)** — mantiene el formato homogéneo.
5. **Revisa duplicados** antes de crear una pregunta nueva (busca en el repo). Si ya existe, mejora la respuesta existente.
6. **Respuestas propias**, claras y con ejemplos. Si citas fuentes, enlázalas.

## Flujo de trabajo

### Proponer una pregunta sin respuesta
Abre un Issue con la plantilla **Nueva pregunta**. Otra persona podrá responderla.

### Añadir o mejorar una respuesta
```bash
git checkout -b pregunta/sql-rank-vs-dense-rank
cp templates/pregunta.md preguntas/sql/diferencia-rank-dense-rank.md
# edita el archivo
git add .
git commit -m "sql: añade pregunta sobre RANK vs DENSE_RANK"
git push origin pregunta/sql-rank-vs-dense-rank
```
Antes del commit, regenera los índices de cada tema:
```bash
python scripts/generar_indices.py
```

Después abre un Pull Request hacia `main`.

## Convención de commits

`<tema>: <descripción breve>` — por ejemplo `spark: añade pregunta sobre data skew`.

## Temas

`sql`, `python`, `spark`, `modelado-datos`, `orquestacion`, `cloud`, `streaming`, `system-design`, `behavioral`.

¿Falta un tema? Propónlo en un Issue.
