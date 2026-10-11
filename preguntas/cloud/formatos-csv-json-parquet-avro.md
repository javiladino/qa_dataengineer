# ¿Qué diferencia hay entre CSV, JSON, Parquet y Avro? ¿Cuándo usarías cada uno?

**Nivel:** 🟢 Junior
**Tags:** `cloud`, `formatos`, `parquet`, `avro`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| Formato | Orientación | Esquema | Compresión | Legible | Uso típico |
|---|---|---|---|---|---|
| **CSV** | Filas (texto) | ❌ | Baja | ✅ | Intercambio simple, exportaciones |
| **JSON** | Filas (texto) | ❌ (semi-estructurado) | Baja | ✅ | APIs, datos anidados, logs |
| **Avro** | **Filas** (binario) | ✅ Embebido, con evolución de esquema | Buena | ❌ | Streaming (Kafka), ingesta, escrituras rápidas |
| **Parquet** | **Columnas** (binario) | ✅ Embebido | **Muy alta** | ❌ | **Analítica**, data lakes, lectura de pocas columnas |

**Por qué Parquet es el estándar en analítica:**
- Lee **solo las columnas necesarias** (*column pruning*).
- Guarda **estadísticas** (min/max) por bloque y permite saltarse bloques (*predicate pushdown*).
- Comprime mucho mejor, porque los valores de una misma columna se parecen.

**Regla práctica:** formatos de filas (Avro, JSON) para **escribir y mover** registros completos; formato de columnas (Parquet, ORC) para **consultar y agregar**.

> **En una frase:** «CSV y JSON son de texto y sin esquema; Avro es binario por filas, ideal para streaming; Parquet es columnar y comprimido, ideal para analítica».

## Ejemplo

```python
import pandas as pd

df = pd.read_csv("ventas.csv")
df.to_parquet("ventas.parquet", compression="snappy")   # suele ocupar mucho menos que el CSV

# Leer solo 2 columnas: con Parquet no se lee el resto del fichero
pd.read_parquet("ventas.parquet", columns=["pais", "importe"])
```

## Preguntas de seguimiento

- ¿Qué es la evolución de esquema y por qué es importante en Avro?
- ¿Qué diferencia hay entre Parquet y Delta Lake/Iceberg? (Delta e Iceberg son formatos de *tabla* que usan Parquet por debajo)

## Referencias

- [Apache Parquet — Documentation](https://parquet.apache.org/docs/)
- [Apache Avro — Specification](https://avro.apache.org/docs/)
