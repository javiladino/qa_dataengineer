# ¿Cómo encuentras y eliminas registros duplicados en una tabla?

**Nivel:** 🟢 Junior
**Tags:** `sql`, `calidad-datos`, `window-functions`
**Visto en:** Pregunta frecuente — entrevista técnica / live coding

## Respuesta

Primero hay que definir **qué es un duplicado**: ¿filas idénticas en todas las columnas, o filas con la misma *clave de negocio* (p. ej. mismo `email`)? A partir de ahí:

1. **Detectarlos** con `GROUP BY ... HAVING COUNT(*) > 1`.
2. **Quedarte con uno** usando `ROW_NUMBER()` particionando por la clave y ordenando por un criterio (normalmente el registro más reciente).
3. **Eliminarlos** de la tabla o, mejor en Data Engineering, **crear una tabla/vista deduplicada** sin borrar el dato original (trazabilidad).

> **En una frase:** «Defino la clave de duplicidad, los detecto con `GROUP BY + HAVING` y me quedo con uno por clave con `ROW_NUMBER()`».

## Ejemplo

```sql
-- 1. Detectar duplicados por email
SELECT email, COUNT(*) AS veces
FROM clientes
GROUP BY email
HAVING COUNT(*) > 1;

-- 2. Quedarse con el registro más reciente por email
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated_at DESC) AS rn
    FROM clientes
) t
WHERE rn = 1;

-- 3. Eliminar duplicados físicamente (PostgreSQL)
DELETE FROM clientes
WHERE id IN (
    SELECT id FROM (
        SELECT id,
               ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated_at DESC) AS rn
        FROM clientes
    ) t
    WHERE rn > 1
);
```

Si los duplicados son filas **exactamente iguales**, basta con `SELECT DISTINCT *`.

## Preguntas de seguimiento

- ¿Cómo evitarías que vuelvan a entrar duplicados? (restricción `UNIQUE`/`PRIMARY KEY`, `MERGE`/upsert en la carga, tests de unicidad)
- ¿Qué diferencia hay entre `DISTINCT` y `GROUP BY` para deduplicar?

## Referencias

- [PostgreSQL — Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
