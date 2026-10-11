# ¿Qué es una Slowly Changing Dimension (SCD)? Explica el tipo 1 y el tipo 2

**Nivel:** 🟢 Junior
**Tags:** `modelado`, `scd`, `dimensiones`, `historico`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Una **SCD** es una dimensión cuyos atributos cambian con el tiempo de forma poco frecuente (p. ej. un cliente cambia de ciudad). La pregunta es: **¿qué hacemos con el valor anterior?**

| Tipo | Estrategia | Histórico | Cuándo usarlo |
|---|---|---|---|
| **SCD 0** | No se cambia nunca | — | Atributos fijos (fecha de nacimiento) |
| **SCD 1** | **Sobrescribe** el valor | ❌ Se pierde | Correcciones de errores, atributos sin valor histórico |
| **SCD 2** | **Inserta una nueva fila** y cierra la anterior | ✅ Completo | Cuando hay que analizar los hechos con el valor vigente en su momento |
| **SCD 3** | Añade una columna `valor_anterior` | Parcial (solo el previo) | Poco habitual |

Columnas típicas de SCD 2: `valido_desde`, `valido_hasta` y `es_actual`, además de una **clave subrogada** distinta para cada versión.

> **En una frase:** «SCD 1 sobrescribe y pierde el histórico; SCD 2 crea una nueva versión con fechas de vigencia para conservarlo».

## Ejemplo

El cliente `C-001` se muda de Madrid a Valencia el 2026-03-01:

| cliente_key | cliente_id | ciudad | valido_desde | valido_hasta | es_actual |
|---|---|---|---|---|---|
| 1 | C-001 | Madrid | 2024-05-10 | 2026-02-28 | false |
| 7 | C-001 | Valencia | 2026-03-01 | 9999-12-31 | true |

```sql
-- SCD 2 simplificado: 1) cerrar la versión vigente
UPDATE dim_cliente
SET valido_hasta = DATE '2026-02-28', es_actual = FALSE
WHERE cliente_id = 'C-001' AND es_actual = TRUE;

-- 2) insertar la nueva versión
INSERT INTO dim_cliente (cliente_key, cliente_id, ciudad, valido_desde, valido_hasta, es_actual)
VALUES (7, 'C-001', 'Valencia', DATE '2026-03-01', DATE '9999-12-31', TRUE);
```

En dbt, el SCD 2 se implementa directamente con **snapshots**.

## Preguntas de seguimiento

- ¿Cómo unes una tabla de hechos con una SCD 2? (por clave subrogada, o por clave de negocio + fecha del hecho entre `valido_desde` y `valido_hasta`)
- ¿Cómo detectas qué registros han cambiado? (comparando columnas o un hash de los atributos)

## Referencias

- [Kimball Group — Slowly Changing Dimension Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/)
- [dbt — Snapshots](https://docs.getdbt.com/docs/build/snapshots)
