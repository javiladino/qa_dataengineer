# ¿Cuál es la diferencia entre Data Lake, Data Warehouse y Lakehouse?

**Nivel:** 🟢 Junior
**Tags:** `cloud`, `data-lake`, `data-warehouse`, `lakehouse`, `arquitectura`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| | Data Warehouse | Data Lake | Lakehouse |
|---|---|---|---|
| Datos | **Estructurados**, limpios y modelados | **Cualquier formato**: crudos, semi y no estructurados | Cualquier formato, con capa de tablas gestionadas |
| Esquema | *Schema-on-write* (se define al cargar) | *Schema-on-read* (se interpreta al leer) | Ambos |
| Almacenamiento | Propietario del motor | Object storage barato (S3, GCS, ADLS) | Object storage + formato de tabla abierto |
| Transacciones ACID | ✅ | ❌ (solo ficheros) | ✅ (Delta Lake, Apache Iceberg, Hudi) |
| Usuarios típicos | Analistas, BI | Data engineers, data scientists | Todos |
| Ejemplos | BigQuery, Snowflake, Redshift, Synapse | S3 + Parquet, ADLS, GCS | Databricks, Iceberg sobre S3, Microsoft Fabric |

- El **Data Warehouse** es rápido y fiable para BI, pero más caro y rígido.
- El **Data Lake** es barato y flexible, pero sin gobierno puede convertirse en un *data swamp* (un "pantano" de datos sin control).
- El **Lakehouse** combina ambos: almacenamiento barato y abierto en el lake con fiabilidad de warehouse (ACID, esquema, *time travel*) gracias a formatos de tabla como **Delta** o **Iceberg**.

> **En una frase:** «El warehouse guarda datos estructurados listos para analizar, el lake guarda cualquier dato en crudo a bajo coste, y el lakehouse aporta garantías de warehouse sobre el almacenamiento del lake».

## Ejemplo

Arquitectura habitual:

```
Fuentes (BD, APIs, ficheros)
        │
        ▼
  Data Lake (S3/GCS/ADLS) ── crudo en Parquet/JSON
        │  transformación (Spark, dbt)
        ▼
  Data Warehouse / Lakehouse ── tablas modeladas
        │
        ▼
  BI (Power BI, Looker, Tableau) / ML
```

## Preguntas de seguimiento

- ¿Qué aporta Delta Lake o Iceberg sobre un Parquet normal? (ACID, `MERGE`, evolución de esquema, *time travel*)
- ¿Qué es la arquitectura medallion (bronze/silver/gold)?

## Referencias

- [Databricks — What is a data lakehouse?](https://docs.databricks.com/en/lakehouse/index.html)
- [AWS — Data Lake vs Data Warehouse](https://aws.amazon.com/compare/the-difference-between-a-data-warehouse-data-lake-and-data-mart/)
