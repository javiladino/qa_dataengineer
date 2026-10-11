# ¿Cuál es la diferencia entre repartition y coalesce?

**Nivel:** 🟢 Junior
**Tags:** `spark`, `particiones`, `performance`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Ambos cambian el número de particiones de un DataFrame:

| | `repartition(n)` | `coalesce(n)` |
|---|---|---|
| Puede | **Aumentar o reducir** particiones | Solo **reducir** |
| Shuffle | ✅ Sí, completo | ❌ No (fusiona particiones existentes) |
| Distribución resultante | Equilibrada | Puede quedar desequilibrada |
| Coste | Alto | Bajo |
| Por columna | ✅ `repartition("pais")` | ❌ |

**Cuándo usar cada uno:**
- `coalesce` → reducir particiones **antes de escribir** para no generar miles de ficheros pequeños (*small files problem*).
- `repartition` → aumentar paralelismo, equilibrar particiones desiguales o agrupar por una columna antes de escribir particionado.

> **En una frase:** «`coalesce` reduce particiones sin shuffle y es barato; `repartition` hace shuffle completo pero reparte de forma equilibrada y permite aumentar».

## Ejemplo

```python
df = spark.read.parquet("eventos/")
print(df.rdd.getNumPartitions())          # p. ej. 400

# Tras un filtro fuerte quedan muchas particiones casi vacías → coalesce
df.filter("pais = 'ES'").coalesce(10).write.parquet("eventos_es/")

# Escribir particionado por fecha con pocos ficheros por carpeta
(df.repartition("fecha")
   .write.partitionBy("fecha")
   .mode("overwrite")
   .parquet("eventos_por_fecha/"))
```

## Preguntas de seguimiento

- ¿Qué es el *small files problem* y por qué afecta al rendimiento?
- ¿Qué diferencia hay entre `repartition("fecha")` y `write.partitionBy("fecha")`? (uno organiza particiones en memoria, el otro carpetas en disco)

## Referencias

- [PySpark — DataFrame.coalesce](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.coalesce.html)
- [PySpark — DataFrame.repartition](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.repartition.html)
