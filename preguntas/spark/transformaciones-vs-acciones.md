# ¿Qué diferencia hay entre transformaciones y acciones en Spark? (lazy evaluation)

**Nivel:** 🟢 Junior
**Tags:** `spark`, `lazy-evaluation`, `dag`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Spark usa **evaluación perezosa**: las operaciones no se ejecutan en el momento, sino que se van anotando en un **plan (DAG)**. Solo cuando pides un resultado se optimiza y ejecuta todo el plan.

| | Transformaciones | Acciones |
|---|---|---|
| Qué hacen | Definen un **nuevo DataFrame** a partir de otro | **Disparan la ejecución** y devuelven un resultado o escriben datos |
| ¿Se ejecutan al llamarlas? | ❌ No (lazy) | ✅ Sí |
| Ejemplos | `select`, `filter`, `withColumn`, `join`, `groupBy`, `orderBy` | `count`, `show`, `collect`, `take`, `write`, `save` |

**Ventaja de la lazy evaluation:** el optimizador (**Catalyst**) ve el plan completo y puede reordenar operaciones, empujar filtros hacia la lectura (*predicate pushdown*) o leer solo las columnas necesarias (*column pruning*).

**Cuidado:** cada acción recalcula el plan desde el origen. Si reutilizas un DataFrame costoso en varias acciones, usa `cache()`/`persist()`.

> **En una frase:** «Las transformaciones construyen el plan y las acciones lo ejecutan; eso permite a Spark optimizar el trabajo completo antes de lanzarlo».

## Ejemplo

```python
df = spark.read.parquet("ventas/")                # lazy
df_ok = df.filter(df.estado == "completado")      # transformación → no ejecuta
df_sel = df_ok.select("pais", "importe")          # transformación → no ejecuta

df_sel.cache()                                    # se reutilizará
print(df_sel.count())                             # ACCIÓN → ejecuta (y cachea)
df_sel.show(5)                                    # ACCIÓN → reutiliza la caché

df_sel.explain()                                  # muestra el plan físico
```

## Preguntas de seguimiento

- ¿Por qué `collect()` es peligroso con datos grandes? (trae todo al driver y puede provocar OOM)
- ¿Qué diferencia hay entre `cache()` y `persist()`?

## Referencias

- [Spark — RDD Operations](https://spark.apache.org/docs/latest/rdd-programming-guide.html#rdd-operations)
