# ¿Qué son las transformaciones narrow y wide? ¿Qué es un shuffle?

**Nivel:** 🟢 Junior
**Tags:** `spark`, `shuffle`, `particiones`, `performance`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Spark divide los datos en **particiones** que se procesan en paralelo. Las transformaciones se clasifican según si necesitan mover datos entre particiones:

| | Narrow | Wide |
|---|---|---|
| Dependencia | Cada partición de salida depende de **una** partición de entrada | Una partición de salida depende de **muchas** particiones de entrada |
| Movimiento de datos | No (se procesa en el mismo executor) | **Shuffle**: redistribución por red |
| Coste | Barato | Caro (red, disco, serialización) |
| Ejemplos | `filter`, `select`, `withColumn`, `map`, `union` | `groupBy`, `join`, `distinct`, `orderBy`, `repartition` |

Un **shuffle** reorganiza los datos para que todos los registros con la misma clave acaben en la misma partición. Cada shuffle crea un **nuevo stage** en el plan de ejecución, y suele ser el principal cuello de botella de un job.

**Cómo reducir shuffles:** filtrar y seleccionar columnas antes de los joins, usar *broadcast join* con tablas pequeñas y evitar `orderBy`/`distinct` innecesarios.

> **En una frase:** «Narrow trabaja dentro de cada partición; wide necesita un shuffle por red, que es la operación más costosa en Spark».

## Ejemplo

```python
from pyspark.sql import functions as F

df = spark.read.parquet("ventas/")

# Narrow: sin shuffle
df2 = df.filter(F.col("importe") > 0).withColumn("anio", F.year("fecha"))

# Wide: provoca shuffle (Exchange en el plan)
resumen = df2.groupBy("pais").agg(F.sum("importe"))
resumen.explain()   # busca "Exchange hashpartitioning" en el plan

# Broadcast join: evita el shuffle de la tabla grande
paises = spark.read.parquet("dim_paises/")      # tabla pequeña
df2.join(F.broadcast(paises), "pais")
```

## Preguntas de seguimiento

- ¿Qué es un *stage* y qué es una *task* en Spark?
- ¿Qué controla `spark.sql.shuffle.partitions`? (número de particiones tras un shuffle, 200 por defecto)

## Referencias

- [Spark — Shuffle operations](https://spark.apache.org/docs/latest/rdd-programming-guide.html#shuffle-operations)
