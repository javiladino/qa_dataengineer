# ¿Qué es la arquitectura medallion (bronze, silver, gold)?

**Nivel:** 🟢 Junior
**Tags:** `system-design`, `medallion`, `lakehouse`, `capas`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Es un patrón que organiza los datos en **capas de calidad creciente**:

| Capa | Contenido | Transformaciones | Consumidores |
|---|---|---|---|
| 🥉 **Bronze** (raw) | Datos **en crudo**, tal como llegan de la fuente, con metadatos de ingesta | Ninguna o mínima (solo añadir fecha de carga y origen) | Data engineers (reprocesos, auditoría) |
| 🥈 **Silver** (cleaned) | Datos **limpios y conformados** | Tipado, deduplicación, limpieza, joins, estandarización | Data engineers, data scientists |
| 🥇 **Gold** (curated) | Datos **de negocio**, agregados y modelados | Modelo dimensional, KPIs, agregaciones | Analistas, BI, dashboards |

**Ventajas:**
- **Trazabilidad:** siempre puedes volver al dato original.
- **Reprocesable:** si cambia una regla de negocio, regeneras silver y gold desde bronze sin volver a extraer.
- **Separación de responsabilidades** y depuración más sencilla.

Equivalencia con la nomenclatura de dbt: `staging` ≈ silver, `marts` ≈ gold.

> **En una frase:** «Bronze guarda el crudo, silver lo limpia y conforma, y gold lo modela para el negocio; así gano trazabilidad y puedo reprocesar sin volver a extraer».

## Ejemplo

```
bronze.ventas_raw          → JSON tal cual de la API + _ingested_at
        │  tipar, deduplicar, normalizar fechas y monedas
        ▼
silver.ventas              → una fila por venta, tipos correctos, sin duplicados
        │  unir con clientes y productos, agregar
        ▼
gold.fct_ventas / gold.ventas_diarias_por_pais   → listo para Power BI
```

## Preguntas de seguimiento

- ¿Dónde aplicarías el enmascaramiento de datos personales (PII)?
- ¿Es obligatorio tener siempre tres capas? (no, es una guía; hay equipos que añaden o fusionan capas)

## Referencias

- [Databricks — What is the medallion lakehouse architecture?](https://docs.databricks.com/en/lakehouse/medallion.html)
