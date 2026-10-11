# ¿Qué es Apache Kafka? Explica topics, particiones, offsets y consumer groups

**Nivel:** 🟢 Junior
**Tags:** `streaming`, `kafka`, `mensajeria`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**Apache Kafka** es una plataforma distribuida de **streaming de eventos**: un *log* distribuido, persistente y replicado donde los **productores** escriben eventos y los **consumidores** los leen, de forma desacoplada.

| Concepto | Qué es |
|---|---|
| **Broker** | Servidor de Kafka; un clúster tiene varios |
| **Topic** | Categoría o canal de eventos (p. ej. `pedidos`) |
| **Partición** | División de un topic. Es la unidad de **paralelismo**; el **orden solo se garantiza dentro de una partición** |
| **Offset** | Posición secuencial de cada mensaje dentro de una partición. El consumidor guarda hasta dónde ha leído |
| **Key** | Determina la partición: misma key → misma partición → orden garantizado para esa key |
| **Producer** | Aplicación que publica eventos |
| **Consumer group** | Conjunto de consumidores que se **reparten las particiones**: cada partición la lee un solo consumidor del grupo |
| **Replicación** | Cada partición tiene copias en varios brokers para tolerar fallos |
| **Retención** | Los mensajes se conservan un tiempo configurable aunque ya se hayan leído (se pueden releer) |

A diferencia de una cola tradicional, **leer no borra el mensaje**, y varios consumer groups pueden leer el mismo topic de forma independiente.

> **En una frase:** «Kafka es un log distribuido y persistente: los productores escriben en topics particionados y los consumer groups leen en paralelo controlando su posición con offsets».

## Ejemplo

```python
from confluent_kafka import Producer, Consumer

# Productor: key = cliente_id → los eventos de un cliente mantienen su orden
p = Producer({"bootstrap.servers": "broker:9092"})
p.produce("pedidos", key="C-001", value='{"pedido_id": 1, "importe": 50}')
p.flush()

# Consumidor dentro de un consumer group
c = Consumer({
    "bootstrap.servers": "broker:9092",
    "group.id": "carga-dwh",
    "auto.offset.reset": "earliest",
})
c.subscribe(["pedidos"])
msg = c.poll(1.0)
if msg is not None and msg.error() is None:
    print(msg.key(), msg.value(), msg.partition(), msg.offset())
```

## Preguntas de seguimiento

- Si un topic tiene 6 particiones y el grupo tiene 8 consumidores, ¿qué pasa? (2 quedan inactivos)
- ¿Qué es el *consumer lag* y por qué hay que monitorizarlo?

## Referencias

- [Apache Kafka — Introduction](https://kafka.apache.org/intro)
