# ¿Qué es el data skew en Spark y cómo lo solucionas?

**Nivel:** 🟡 Mid
**Tags:** `spark`, `performance`, `joins`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

El **data skew** ocurre cuando los datos se reparten de forma desigual entre particiones: unas pocas claves concentran la mayoría de registros. Tras un *shuffle* (join, groupBy), unas pocas tareas procesan muchísimos más datos que el resto, el stage tarda lo que tarda la tarea más lenta y pueden aparecer errores de memoria (OOM) o *spill* a disco.

**Cómo detectarlo:** en la Spark UI, una o pocas tareas del stage tardan mucho más que la mediana o leen muchos más bytes de shuffle.

**Soluciones habituales:**

1. **Adaptive Query Execution (AQE)** — en Spark 3+, `spark.sql.adaptive.skewJoin.enabled=true` divide automáticamente las particiones sesgadas.
2. **Broadcast join** — si una tabla es pequeña, se envía a todos los executors y se evita el shuffle.
3. **Salting** — añadir un sufijo aleatorio a la clave sesgada para repartirla en N particiones, y replicar la otra tabla N veces.
4. **Tratar las claves calientes por separado** — p. ej. filtrar `NULL`s o claves por defecto y procesarlas aparte.

## Ejemplo

```python
from pyspark.sql import functions as F

N = 10  # número de "sales"

# Tabla grande con clave sesgada: añadimos un salt aleatorio
ventas_salted = ventas.withColumn("salt", (F.rand() * N).cast("int"))

# Tabla pequeña: la replicamos N veces, una por cada salt
clientes_salted = clientes.crossJoin(
    spark.range(N).withColumnRenamed("id", "salt")
)

resultado = ventas_salted.join(clientes_salted, on=["cliente_id", "salt"])
```

## Preguntas de seguimiento

- ¿Cuándo no conviene usar broadcast join? (tabla demasiado grande para la memoria del driver/executors)
- ¿Qué diferencia hay entre `repartition` y `coalesce`?

## Referencias

- [Spark — Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution)
