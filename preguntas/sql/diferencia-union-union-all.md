# ¿Cuál es la diferencia entre UNION y UNION ALL?

**Nivel:** 🟢 Junior
**Tags:** `sql`, `set-operations`, `performance`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Ambos apilan verticalmente el resultado de dos o más `SELECT`:

| | `UNION` | `UNION ALL` |
|---|---|---|
| Duplicados | **Los elimina** | **Los conserva** |
| Rendimiento | Más lento (tiene que ordenar/hashear para deduplicar) | Más rápido |
| Uso típico | Cuando necesitas valores únicos | Cuando sabes que no hay solapamiento o quieres todas las filas |

Requisitos: mismo **número de columnas**, en el **mismo orden** y con **tipos compatibles**. Los nombres de columnas los toma del primer `SELECT`.

**Regla práctica:** usa `UNION ALL` por defecto y `UNION` solo cuando realmente necesites deduplicar. En tablas grandes la diferencia de coste es significativa.

> **En una frase:** «`UNION` deduplica y es más costoso; `UNION ALL` concatena todo y es más eficiente».

## Ejemplo

```sql
-- Ventas de dos sistemas que no se solapan → UNION ALL
SELECT venta_id, importe, 'tienda' AS canal FROM ventas_tienda
UNION ALL
SELECT venta_id, importe, 'online' AS canal FROM ventas_online;

-- Lista única de emails de dos fuentes → UNION
SELECT email FROM clientes
UNION
SELECT email FROM suscriptores_newsletter;
```

## Preguntas de seguimiento

- ¿Qué otras operaciones de conjuntos conoces? (`INTERSECT`, `EXCEPT`/`MINUS`)
- ¿Cómo ordenas el resultado de un `UNION`? (un único `ORDER BY` al final)

## Referencias

- [PostgreSQL — Combining Queries](https://www.postgresql.org/docs/current/queries-union.html)
