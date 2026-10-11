# ¿Qué es CDC (Change Data Capture) y por qué se usa?

**Nivel:** 🟢 Junior
**Tags:** `streaming`, `cdc`, `debezium`, `ingesta`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**CDC** es una técnica para **capturar los cambios** (`INSERT`, `UPDATE`, `DELETE`) de una base de datos y propagarlos a otros sistemas casi en tiempo real, sin tener que copiar la tabla entera cada vez.

| Método | Cómo funciona | Pros | Contras |
|---|---|---|---|
| **Basado en logs** | Lee el log de transacciones de la BD (WAL de PostgreSQL, binlog de MySQL) | Captura **todo**, incluidos los `DELETE`; mínimo impacto en la BD | Más complejo de configurar |
| **Basado en consultas** | Consulta periódica por `updated_at > último_valor` | Simple | **No detecta borrados**, depende de que exista y se mantenga `updated_at`, carga la BD |
| **Basado en triggers** | Triggers que escriben los cambios en una tabla de auditoría | Preciso | Penaliza las escrituras en la BD de origen |

Herramientas: **Debezium** (+ Kafka), **AWS DMS**, **Fivetran**, **Airbyte**, **Google Datastream**.

Ventajas frente a cargas completas: menos carga sobre la BD de origen, menor latencia y menos datos transferidos.

> **En una frase:** «CDC captura los cambios de la base de datos, idealmente leyendo su log de transacciones, y los replica casi en tiempo real sin recargar tablas completas».

## Ejemplo

Evento de Debezium simplificado para un `UPDATE`:

```json
{
  "op": "u",
  "ts_ms": 1760184000000,
  "before": { "cliente_id": 1, "ciudad": "Madrid" },
  "after":  { "cliente_id": 1, "ciudad": "Valencia" },
  "source": { "db": "crm", "table": "clientes" }
}
```

`op`: `c` = create, `u` = update, `d` = delete, `r` = read (snapshot inicial).

## Preguntas de seguimiento

- ¿Cómo aplicarías esos eventos en el data warehouse? (`MERGE` por clave primaria, respetando el orden de los eventos)
- ¿Cómo encaja CDC con un SCD tipo 2? (cada evento `u` puede generar una nueva versión de la dimensión)

## Referencias

- [Debezium — Documentation](https://debezium.io/documentation/)
