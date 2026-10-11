# ¿Qué es el particionamiento y el clustering en un data warehouse cloud y por qué reduce costes?

**Nivel:** 🟢 Junior
**Tags:** `cloud`, `bigquery`, `snowflake`, `particionamiento`, `costes`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

En los data warehouses cloud pagas (directa o indirectamente) por **los datos que escaneas**. Particionar y agrupar la tabla permite que el motor **lea solo lo necesario**.

| | Particionamiento | Clustering |
|---|---|---|
| Qué hace | Divide la tabla en segmentos por una columna (normalmente **fecha**) | Ordena físicamente los datos dentro de cada partición por 1–4 columnas |
| Beneficio | **Partition pruning**: salta particiones enteras si filtras por esa columna | Salta bloques al filtrar o agrupar por las columnas de clustering |
| Columna ideal | Fecha/timestamp o entero con rango | Columnas muy usadas en `WHERE`/`JOIN` (`cliente_id`, `pais`) |

Equivalentes por plataforma:
- **BigQuery:** `PARTITION BY` + `CLUSTER BY`.
- **Snowflake:** micro-particiones automáticas + `CLUSTER BY` opcional.
- **Redshift:** `DISTKEY` + `SORTKEY`.
- **Databricks/Delta:** `PARTITIONED BY` + `CLUSTER BY` (liquid clustering) / Z-ORDER.

**Error típico:** particionar por una columna con demasiados valores distintos (p. ej. `cliente_id`), lo que genera miles de particiones diminutas.

> **En una frase:** «Particiono por fecha y hago clustering por las columnas de filtro habituales para que las consultas escaneen menos datos: más rápido y más barato».

## Ejemplo

```sql
-- BigQuery
CREATE TABLE analytics.fct_ventas
PARTITION BY DATE(fecha_venta)
CLUSTER BY pais, cliente_id
AS SELECT * FROM staging.ventas;

-- ✅ Escanea solo 7 particiones
SELECT pais, SUM(importe)
FROM analytics.fct_ventas
WHERE DATE(fecha_venta) BETWEEN '2026-10-01' AND '2026-10-07'
GROUP BY pais;

-- ❌ Sin filtro por la columna de partición → escanea toda la tabla
SELECT SUM(importe) FROM analytics.fct_ventas WHERE pais = 'ES';
```

## Preguntas de seguimiento

- ¿Por qué `SELECT *` es caro en BigQuery? (almacenamiento columnar: pagas por cada columna leída)
- ¿Cómo comprobarías cuántos datos va a escanear una consulta antes de lanzarla? (*dry run* o el estimador de la consola)

## Referencias

- [BigQuery — Partitioned tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
- [Snowflake — Clustering Keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
