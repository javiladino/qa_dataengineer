# ¿Cuál es la diferencia entre ROW_NUMBER, RANK y DENSE_RANK?

**Nivel:** 🟢 Junior
**Tags:** `sql`, `window-functions`
**Visto en:** Ejemplo, 2026 — entrevista técnica

## Respuesta

Las tres son *window functions* que numeran filas según un `ORDER BY`, pero difieren en cómo tratan los **empates**:

| Función | Empates | Huecos tras empate | Ejemplo (valores 100, 90, 90, 80) |
|---|---|---|---|
| `ROW_NUMBER()` | Asigna números distintos (orden arbitrario) | — | 1, 2, 3, 4 |
| `RANK()` | Mismo número | Sí, salta posiciones | 1, 2, 2, 4 |
| `DENSE_RANK()` | Mismo número | No | 1, 2, 2, 3 |

## Ejemplo

```sql
SELECT
    empleado,
    salario,
    ROW_NUMBER() OVER (ORDER BY salario DESC) AS row_num,
    RANK()       OVER (ORDER BY salario DESC) AS rnk,
    DENSE_RANK() OVER (ORDER BY salario DESC) AS dense_rnk
FROM empleados;
```

Caso típico — **deduplicar** quedándote con el registro más reciente por clave:

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY cliente_id ORDER BY updated_at DESC) AS rn
    FROM clientes_raw
) t
WHERE rn = 1;
```

## Preguntas de seguimiento

- ¿Cómo obtendrías el segundo salario más alto por departamento? (`DENSE_RANK` + `PARTITION BY`)
- ¿Por qué `ROW_NUMBER` puede dar resultados no deterministas? (empates sin desempate en el `ORDER BY`)

## Referencias

- [PostgreSQL — Window Functions](https://www.postgresql.org/docs/current/functions-window.html)
