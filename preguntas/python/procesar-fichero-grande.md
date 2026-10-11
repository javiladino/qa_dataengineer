# ¿Cómo procesarías en Python un CSV más grande que la memoria disponible?

**Nivel:** 🟢 Junior
**Tags:** `python`, `pandas`, `memoria`, `csv`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Si intentas `pd.read_csv("10GB.csv")` en una máquina con 8 GB de RAM, el proceso se queda sin memoria. Opciones, de más simple a más escalable:

1. **Leer por bloques (*chunks*)** con `pd.read_csv(..., chunksize=N)`: procesas y agregas trozo a trozo.
2. **Leer solo lo necesario:** `usecols=[...]` para cargar únicamente las columnas útiles y `dtype={...}` para tipos más ligeros (p. ej. `int32`, `category`).
3. **Iterar línea a línea** con el módulo `csv` o un generador cuando la lógica es simple.
4. **Cambiar de formato:** convertir a **Parquet** (columnar y comprimido) y leer solo las columnas necesarias.
5. **Usar una herramienta adecuada al volumen:** **DuckDB** o **Polars** (procesan fuera de memoria en una sola máquina) o **Spark** si el volumen es realmente grande.

> **En una frase:** «Evito cargarlo entero: leo por chunks solo las columnas necesarias con tipos ajustados y, si el volumen crece, paso a Parquet + DuckDB/Polars o Spark».

## Ejemplo

```python
import pandas as pd

totales = {}
for chunk in pd.read_csv(
    "ventas_2026.csv",
    usecols=["pais", "importe"],
    dtype={"pais": "category", "importe": "float32"},
    chunksize=500_000,
):
    parcial = chunk.groupby("pais", observed=True)["importe"].sum()
    for pais, importe in parcial.items():
        totales[pais] = totales.get(pais, 0) + importe

print(totales)
```

Alternativa con DuckDB, en una línea y sin cargar el fichero en memoria:

```python
import duckdb
duckdb.sql("SELECT pais, SUM(importe) FROM 'ventas_2026.csv' GROUP BY pais").show()
```

## Preguntas de seguimiento

- ¿Por qué Parquet ocupa menos y se lee más rápido que CSV? (almacenamiento columnar + compresión + estadísticas por bloque)
- ¿Cómo calcularías una mediana leyendo por chunks? (no es agregable directamente: requiere otro enfoque)

## Referencias

- [pandas — Scaling to large datasets](https://pandas.pydata.org/docs/user_guide/scale.html)
- [DuckDB — Reading CSV files](https://duckdb.org/docs/data/csv/overview)
