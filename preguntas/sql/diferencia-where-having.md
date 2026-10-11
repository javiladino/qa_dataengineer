# ¿Cuál es la diferencia entre WHERE y HAVING?

**Nivel:** 🟢 Junior
**Tags:** `sql`, `agregaciones`, `group-by`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Ambos filtran, pero en **momentos distintos** de la ejecución de la consulta:

| | `WHERE` | `HAVING` |
|---|---|---|
| Filtra | **Filas** individuales | **Grupos** ya agregados |
| Se evalúa | **Antes** del `GROUP BY` | **Después** del `GROUP BY` |
| Puede usar agregaciones (`SUM`, `COUNT`…) | ❌ No | ✅ Sí |

Orden lógico de ejecución de una consulta:

`FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`

**Buena práctica de rendimiento:** filtra todo lo que puedas en el `WHERE`, porque reduce las filas *antes* de agrupar. Usa `HAVING` solo para condiciones sobre agregados.

> **En una frase:** «`WHERE` filtra filas antes de agrupar; `HAVING` filtra grupos después de agregar».

## Ejemplo

```sql
-- Clientes con más de 5 pedidos completados en 2026
SELECT cliente_id, COUNT(*) AS num_pedidos
FROM pedidos
WHERE estado = 'completado'            -- filtra filas
  AND fecha >= '2026-01-01'
GROUP BY cliente_id
HAVING COUNT(*) > 5;                   -- filtra grupos
```

## Preguntas de seguimiento

- ¿Por qué no puedes usar un alias del `SELECT` en el `WHERE`? (el `SELECT` se evalúa después)
- ¿Se puede usar `HAVING` sin `GROUP BY`? (sí, trata toda la tabla como un único grupo)

## Referencias

- [PostgreSQL — GROUP BY and HAVING](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
