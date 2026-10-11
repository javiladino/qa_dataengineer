# ¿Cuál es la diferencia entre RDD, DataFrame y Dataset?

**Nivel:** 🟢 Junior
**Tags:** `spark`, `rdd`, `dataframe`, `api`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Son las tres APIs de datos de Spark, de más bajo a más alto nivel:

| | RDD | DataFrame | Dataset |
|---|---|---|---|
| Qué es | Colección distribuida de objetos | Tabla distribuida con **columnas con nombre y esquema** | DataFrame **tipado** |
| Esquema | ❌ No | ✅ Sí | ✅ Sí + tipos en compilación |
| Optimización (Catalyst/Tungsten) | ❌ No | ✅ Sí | ✅ Sí |
| Lenguajes | Python, Scala, Java | Python, Scala, Java, R, SQL | **Solo Scala y Java** |
| Uso hoy | Casos muy específicos de bajo nivel | **El estándar** | Proyectos Scala/Java que quieren tipado |

En PySpark trabajarás casi siempre con **DataFrames**: son más rápidos porque Spark conoce el esquema y optimiza el plan, y además puedes mezclar con Spark SQL.

> **En una frase:** «El RDD es la base de bajo nivel; el DataFrame añade esquema y optimización y es lo que se usa en la práctica; el Dataset añade tipado, solo en Scala/Java».

## Ejemplo

```python
# RDD: bajo nivel, sin esquema
rdd = spark.sparkContext.parallelize([("ES", 100), ("FR", 50), ("ES", 30)])
print(rdd.reduceByKey(lambda a, b: a + b).collect())

# DataFrame: con esquema y optimizado
df = spark.createDataFrame(rdd, ["pais", "importe"])
df.groupBy("pais").sum("importe").show()

# Mismo resultado con Spark SQL
df.createOrReplaceTempView("ventas")
spark.sql("SELECT pais, SUM(importe) FROM ventas GROUP BY pais").show()
```

## Preguntas de seguimiento

- ¿Por qué las UDFs de Python pueden ser lentas? (serialización entre JVM y Python; mejor funciones nativas o *pandas UDFs*)
- ¿Qué es Catalyst?

## Referencias

- [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
