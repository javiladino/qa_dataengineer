# ¿Cuál es la diferencia entre procesamiento batch y streaming?

**Nivel:** 🟢 Junior
**Tags:** `streaming`, `batch`, `arquitectura`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| | Batch | Streaming |
|---|---|---|
| Datos | Conjunto **acotado** procesado de golpe | Flujo **continuo**, sin fin |
| Latencia | Minutos u horas | Milisegundos a segundos |
| Ejecución | Programada (cada hora, cada día) | Siempre en marcha |
| Complejidad | Menor | Mayor (orden, duplicados, estado, eventos tardíos) |
| Coste | Normalmente menor | Mayor (infraestructura 24/7) |
| Herramientas | Spark, dbt, SQL, Airflow | Kafka, Flink, Spark Structured Streaming, Kinesis, Pub/Sub |
| Casos de uso | Informes diarios, cierres contables, entrenamiento de modelos | Detección de fraude, alertas, IoT, personalización en tiempo real |

**Micro-batch** (p. ej. Spark Structured Streaming): punto intermedio que procesa pequeños lotes cada pocos segundos.

**Criterio de decisión:** pregunta *¿qué latencia necesita realmente el negocio?* Si un dashboard se consulta una vez al día, el streaming añade complejidad y coste sin aportar valor.

> **En una frase:** «Batch procesa bloques acotados de datos con latencia de minutos u horas; streaming procesa eventos continuos en tiempo casi real. Elijo según la latencia que necesite el negocio».

## Ejemplo

```python
# Batch: lee todos los ficheros del día y termina
df = spark.read.parquet("s3://lake/eventos/fecha=2026-10-11/")

# Streaming: lee de Kafka indefinidamente
stream = (spark.readStream
          .format("kafka")
          .option("kafka.bootstrap.servers", "broker:9092")
          .option("subscribe", "eventos")
          .load())
```

## Preguntas de seguimiento

- ¿Qué son las arquitecturas Lambda y Kappa?
- ¿Por qué el streaming es más difícil de operar?

## Referencias

- [Spark — Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
