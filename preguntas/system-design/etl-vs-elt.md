# ¿Cuál es la diferencia entre ETL y ELT?

**Nivel:** 🟢 Junior
**Tags:** `system-design`, `etl`, `elt`, `arquitectura`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Ambos mueven datos de las fuentes a un sistema analítico; cambia **dónde y cuándo se transforma**:

| | ETL (*Extract, Transform, Load*) | ELT (*Extract, Load, Transform*) |
|---|---|---|
| Orden | Extrae → **transforma fuera** → carga | Extrae → **carga en crudo** → transforma **dentro** del warehouse |
| Dónde se transforma | Servidor o herramienta intermedia (Spark, SSIS, Informatica) | En el propio DWH/lakehouse con SQL (dbt, BigQuery, Snowflake) |
| Dato crudo | No se conserva en destino | **Se conserva**: se puede reprocesar |
| Flexibilidad | Cambiar la lógica implica re-extraer | Cambiar la lógica es relanzar el SQL |
| Cuándo encaja | Datos sensibles que hay que anonimizar antes de cargar, sistemas legacy, transformaciones pesadas no SQL | Warehouses cloud con cómputo escalable (**enfoque moderno**) |

El **ELT** se ha impuesto con los warehouses cloud porque el cómputo es elástico, el almacenamiento barato, y conservar el crudo permite rehacer transformaciones. Stack típico: **Fivetran/Airbyte (EL) + Snowflake/BigQuery + dbt (T) + Airflow**.

> **En una frase:** «En ETL transformo antes de cargar; en ELT cargo el crudo y transformo dentro del warehouse, lo que da más flexibilidad y es el enfoque moderno».

## Ejemplo

```
ETL:  PostgreSQL ──► Spark (limpia, une, agrega) ──► DWH (solo tablas finales)

ELT:  PostgreSQL ──► DWH.raw (copia en crudo) ──► dbt (staging → marts) ──► DWH.analytics
```

## Preguntas de seguimiento

- ¿En qué caso elegirías ETL hoy? (PII que no puede llegar sin anonimizar, por cumplimiento normativo)
- ¿Qué es *reverse ETL*? (devolver datos del DWH a herramientas operativas como un CRM)

## Referencias

- [AWS — ETL vs ELT](https://aws.amazon.com/compare/the-difference-between-etl-and-elt/)
