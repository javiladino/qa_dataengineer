# ¿Qué diferencia hay entre event time y processing time? ¿Qué son las ventanas?

**Nivel:** 🟢 Junior
**Tags:** `streaming`, `windowing`, `watermarks`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

- **Event time:** momento en que el evento **ocurrió realmente** (lo registra el dispositivo o la aplicación de origen).
- **Processing time:** momento en que el sistema **procesa** el evento.

No coinciden por latencia de red, reintentos o dispositivos que estuvieron sin conexión. Para resultados correctos se agrega por **event time**.

**Ventanas (*windows*):** como el stream no termina, las agregaciones se hacen sobre intervalos de tiempo:

| Ventana | Descripción | Ejemplo |
|---|---|---|
| **Tumbling** (fija) | Intervalos consecutivos sin solapamiento | Ventas cada 5 minutos: 10:00–10:05, 10:05–10:10 |
| **Sliding / Hopping** (deslizante) | Intervalos de tamaño fijo que se solapan | Últimos 10 min, recalculado cada minuto |
| **Session** (sesión) | Se cierra tras un periodo de inactividad | Actividad de un usuario hasta 30 min sin eventos |

**Watermark:** umbral que indica hasta cuándo se esperan **eventos tardíos** antes de cerrar una ventana (p. ej. "acepto eventos con hasta 10 min de retraso"). Equilibra exactitud y latencia.

> **En una frase:** «Agrego por event time en ventanas y uso watermarks para decidir cuánto tiempo espero a los eventos que llegan tarde».

## Ejemplo

```python
from pyspark.sql import functions as F

ventas_5min = (
    eventos                                         # DataFrame en streaming
    .withWatermark("event_time", "10 minutes")      # tolera 10 min de retraso
    .groupBy(F.window("event_time", "5 minutes"), "pais")
    .agg(F.sum("importe").alias("total"))
)
```

## Preguntas de seguimiento

- ¿Qué pasa con un evento que llega después del watermark? (se descarta o se envía a una salida aparte)
- ¿Qué ventana usarías para calcular usuarios activos en los últimos 15 minutos actualizados cada minuto? (sliding)

## Referencias

- [Spark — Window Operations on Event Time](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#window-operations-on-event-time)
- [Apache Flink — Timely Stream Processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/)
