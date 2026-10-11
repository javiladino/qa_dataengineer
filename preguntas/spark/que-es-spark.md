# ¿Qué es Apache Spark y cuándo lo usarías en lugar de Pandas?

**Nivel:** 🟢 Junior
**Tags:** `spark`, `pyspark`, `procesamiento-distribuido`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**Apache Spark** es un motor de **procesamiento distribuido** que reparte el trabajo entre varias máquinas (un clúster) y procesa los datos principalmente **en memoria**. Ofrece APIs en Python (PySpark), SQL, Scala y Java para batch, streaming y machine learning.

Arquitectura básica:
- **Driver:** el proceso que ejecuta tu programa, crea el plan de ejecución y coordina.
- **Executors:** procesos en los nodos del clúster que ejecutan las tareas sobre las particiones de datos.
- **Cluster manager:** asigna recursos (YARN, Kubernetes, Standalone, Databricks…).

| | Pandas | Spark |
|---|---|---|
| Ejecución | Una sola máquina | Distribuida en clúster |
| Volumen cómodo | Hasta lo que cabe en RAM (GBs) | GBs a TBs/PBs |
| Evaluación | Inmediata | **Perezosa** (*lazy*) |
| Overhead | Mínimo | Alto (arranque, coordinación) |

**Cuándo Spark:** cuando los datos no caben en una máquina o el procesamiento es demasiado lento en una sola. **Cuándo no:** para pocos GB, Pandas, Polars o DuckDB son más simples y a menudo más rápidos.

> **En una frase:** «Spark es un motor distribuido para procesar grandes volúmenes en paralelo; lo uso cuando el dato ya no cabe o no rinde en una sola máquina».

## Ejemplo

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("ventas").getOrCreate()

ventas = spark.read.parquet("s3://mi-bucket/ventas/")

resumen = (
    ventas
    .filter(F.col("estado") == "completado")
    .groupBy("pais")
    .agg(F.sum("importe").alias("total"))
)

resumen.write.mode("overwrite").parquet("s3://mi-bucket/resumen_ventas/")
```

## Preguntas de seguimiento

- ¿Qué diferencia hay entre Spark y Hadoop MapReduce? (Spark procesa en memoria y es mucho más rápido en cargas iterativas)
- ¿Qué es una partición en Spark?

## Referencias

- [Apache Spark — Cluster Mode Overview](https://spark.apache.org/docs/latest/cluster-overview.html)
