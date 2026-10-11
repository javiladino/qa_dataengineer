# ¿Qué son las semánticas at-most-once, at-least-once y exactly-once?

**Nivel:** 🟢 Junior
**Tags:** `streaming`, `kafka`, `garantias`, `idempotencia`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Describen qué garantía tienes de que cada mensaje se procesa ante fallos (caídas, reintentos, reinicios):

| Semántica | Garantía | Riesgo | Cómo se consigue (consumidor) |
|---|---|---|---|
| **At-most-once** | Cada mensaje se procesa **0 o 1 vez** | **Pérdida** de datos | Confirmar el offset **antes** de procesar |
| **At-least-once** | Cada mensaje se procesa **1 o más veces** | **Duplicados** | Confirmar el offset **después** de procesar |
| **Exactly-once** | Cada mensaje afecta al resultado **exactamente 1 vez** | Más complejidad y algo de latencia | Transacciones + idempotencia de extremo a extremo |

En la práctica, lo más habitual es **at-least-once + escritura idempotente** en el destino (p. ej. `MERGE`/upsert por un ID único del evento). Así los duplicados no tienen efecto y se obtiene un resultado *efectivamente exactly-once*.

> **En una frase:** «At-most-once puede perder datos, at-least-once puede duplicarlos y exactly-once evita ambos. Lo habitual es at-least-once con un destino idempotente».

## Ejemplo

```python
consumer = Consumer({
    "bootstrap.servers": "broker:9092",
    "group.id": "carga-dwh",
    "enable.auto.commit": False,      # controlamos el commit manualmente
})
consumer.subscribe(["pedidos"])

while True:
    msg = consumer.poll(1.0)
    if msg is None or msg.error():
        continue
    upsert_en_dwh(msg.value())        # idempotente: MERGE por pedido_id
    consumer.commit(msg)              # commit DESPUÉS de procesar → at-least-once
```

## Preguntas de seguimiento

- ¿Qué es un productor idempotente en Kafka? (`enable.idempotence=true` evita duplicados al reintentar el envío)
- ¿Por qué exactly-once "de extremo a extremo" depende también del sistema de destino?

## Referencias

- [Confluent — Message Delivery Guarantees](https://docs.confluent.io/kafka/design/delivery-semantics.html)
