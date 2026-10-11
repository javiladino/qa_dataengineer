# ¿Qué diferencia hay entre una carga completa (full) y una incremental?

**Nivel:** 🟢 Junior
**Tags:** `system-design`, `carga-incremental`, `watermark`, `merge`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| | Carga completa (*full load*) | Carga incremental (*incremental load*) |
|---|---|---|
| Qué carga | **Toda** la tabla en cada ejecución | Solo los registros **nuevos o modificados** desde la última carga |
| Complejidad | Muy simple | Mayor (hay que saber qué cambió) |
| Coste y tiempo | Crece con el tamaño total | Proporcional a los cambios |
| Borrados en origen | Se reflejan automáticamente | **Hay que gestionarlos** aparte (CDC, *soft deletes*) |
| Cuándo | Tablas pequeñas, dimensiones, primera carga | Tablas grandes de hechos, eventos, logs |

**Cómo detectar los cambios:**
- **Watermark (marca de agua):** guardar el máximo `updated_at` (o ID) cargado y pedir solo lo posterior.
- **CDC:** leer el log de transacciones de la base de datos.
- **Partición por fecha:** reprocesar solo la partición del día.

**Cómo aplicar los cambios en destino:** `MERGE` (upsert) por clave primaria, para que las actualizaciones no generen duplicados.

> **En una frase:** «La full recarga todo y es simple; la incremental carga solo lo nuevo o modificado usando un watermark o CDC y lo aplica con `MERGE`, más eficiente en tablas grandes».

## Ejemplo

```sql
-- 1. Extraer solo los cambios desde el último watermark
SELECT * FROM origen.pedidos
WHERE updated_at > :ultimo_watermark;

-- 2. Aplicarlos en destino con MERGE
MERGE INTO dwh.pedidos AS t
USING staging.pedidos_cambios AS s
  ON t.pedido_id = s.pedido_id
WHEN MATCHED THEN UPDATE SET
  estado = s.estado, importe = s.importe, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (pedido_id, estado, importe, updated_at)
  VALUES (s.pedido_id, s.estado, s.importe, s.updated_at);

-- 3. Guardar el nuevo watermark = MAX(updated_at) de lo cargado
```

En dbt se implementa con `materialized='incremental'` y el filtro `{% if is_incremental() %}`.

## Preguntas de seguimiento

- ¿Qué pasa con los registros que llegan tarde con un `updated_at` antiguo? (usar una ventana de solape, p. ej. watermark − 1 día)
- ¿Cómo detectarías los registros borrados en origen?

## Referencias

- [dbt — Incremental models](https://docs.getdbt.com/docs/build/incremental-models)
