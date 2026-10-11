# ¿Qué tipos de JOIN existen y en qué se diferencian?

**Nivel:** 🟢 Junior
**Tags:** `sql`, `joins`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Un `JOIN` combina filas de dos tablas según una condición. La diferencia está en **qué hacer con las filas que no tienen coincidencia**:

| JOIN | Devuelve | Filas sin coincidencia |
|---|---|---|
| `INNER JOIN` | Solo las filas que coinciden en ambas tablas | Se descartan |
| `LEFT JOIN` | Todas las de la izquierda + coincidencias de la derecha | Columnas de la derecha a `NULL` |
| `RIGHT JOIN` | Todas las de la derecha + coincidencias de la izquierda | Columnas de la izquierda a `NULL` |
| `FULL OUTER JOIN` | Todas las filas de ambas tablas | `NULL` en el lado que no coincide |
| `CROSS JOIN` | Producto cartesiano (cada fila con cada fila) | No aplica (no hay condición) |
| `SELF JOIN` | Una tabla unida consigo misma (con alias) | Según el tipo de join usado |

En la práctica, `RIGHT JOIN` casi no se usa: se reescribe como `LEFT JOIN` invirtiendo el orden de las tablas, que es más legible.

> **En una frase:** «`INNER` se queda con la intersección, `LEFT/RIGHT` conservan todo un lado, `FULL` conserva ambos y `CROSS` combina todo con todo».

## Ejemplo

```sql
-- Clientes y sus pedidos, incluyendo clientes sin pedidos
SELECT c.cliente_id, c.nombre, p.pedido_id
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id;

-- Patrón "anti-join": clientes que NUNCA han hecho un pedido
SELECT c.cliente_id, c.nombre
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id
WHERE p.pedido_id IS NULL;
```

## Preguntas de seguimiento

- Si la tabla A tiene 3 filas con `id = 1` y la B tiene 2 filas con `id = 1`, ¿cuántas filas devuelve el `INNER JOIN`? (**6**: se multiplican; ojo con los duplicados en las claves)
- ¿Qué pasa con los `NULL` en la condición del join? (`NULL = NULL` no es verdadero, así que esas filas no coinciden)
- ¿Qué diferencia hay entre poner un filtro en el `ON` o en el `WHERE` de un `LEFT JOIN`?

## Referencias

- [PostgreSQL — Joined Tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
