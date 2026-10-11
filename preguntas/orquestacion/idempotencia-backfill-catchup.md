# ¿Qué significa que un pipeline sea idempotente? ¿Qué son backfill y catchup?

**Nivel:** 🟢 Junior
**Tags:** `airflow`, `idempotencia`, `backfill`, `buenas-practicas`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**Idempotencia:** un pipeline es idempotente si **ejecutarlo una o varias veces con la misma entrada produce el mismo resultado**. Es fundamental porque los pipelines se relanzan constantemente (reintentos, fallos, reprocesos).

Cómo conseguirlo:
- Procesar por **ventana de fecha lógica** (`{{ ds }}`), no por "ahora" (`datetime.now()`).
- **Sobrescribir la partición** de esa fecha, o usar `MERGE`/upsert, en lugar de `INSERT` a ciegas.
- Patrón **delete + insert** dentro de una transacción.

**Backfill:** ejecutar un DAG para **fechas pasadas**, p. ej. para reprocesar tras corregir un bug o cargar histórico. Solo es seguro si el pipeline es idempotente.

**Catchup:** parámetro del DAG. Con `catchup=True`, al activarlo Airflow lanza automáticamente todas las ejecuciones pendientes desde `start_date`. Normalmente se usa `catchup=False` y se hacen backfills de forma explícita.

> **En una frase:** «Idempotente significa que relanzarlo no duplica ni corrompe datos; eso es lo que permite hacer reintentos y backfills con seguridad».

## Ejemplo

```sql
-- ❌ No idempotente: cada reintento duplica las filas
INSERT INTO fct_ventas SELECT * FROM stg_ventas WHERE fecha = '{{ ds }}';

-- ✅ Idempotente: borra la partición y la vuelve a cargar
BEGIN;
DELETE FROM fct_ventas WHERE fecha = '{{ ds }}';
INSERT INTO fct_ventas SELECT * FROM stg_ventas WHERE fecha = '{{ ds }}';
COMMIT;
```

```bash
# Backfill de enero de 2026
airflow dags backfill ventas_diarias --start-date 2026-01-01 --end-date 2026-01-31
```

## Preguntas de seguimiento

- ¿Qué es la *logical date* (antes `execution_date`) y por qué no coincide con la hora real de ejecución?
- ¿Cómo harías idempotente una carga que lee de una API? (guardar el crudo por fecha y sobrescribir esa partición)

## Referencias

- [Airflow — DAG Runs: Catchup and Backfill](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html)
- [Airflow — Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
