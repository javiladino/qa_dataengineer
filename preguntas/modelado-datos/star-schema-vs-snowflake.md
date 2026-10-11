# ¿Qué diferencia hay entre un esquema estrella y un esquema copo de nieve?

**Nivel:** 🟢 Junior
**Tags:** `modelado`, `star-schema`, `snowflake-schema`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Ambos tienen una **tabla de hechos central** rodeada de dimensiones. La diferencia es si las dimensiones están normalizadas:

| | Estrella (*star*) | Copo de nieve (*snowflake*) |
|---|---|---|
| Dimensiones | **Desnormalizadas**: una tabla por dimensión | **Normalizadas**: divididas en subtablas |
| Joins en consultas | Pocos (hecho ↔ dimensión) | Más (dimensión ↔ subdimensión) |
| Redundancia | Mayor | Menor |
| Rendimiento de consulta | Mejor | Algo peor |
| Facilidad para analistas/BI | Más simple | Más complejo |

Ejemplo: en estrella, `dim_producto` incluye `categoria` y `subcategoria` como columnas; en copo de nieve, `dim_producto → dim_subcategoria → dim_categoria`.

**Recomendación habitual:** **esquema estrella**. En los data warehouses modernos el almacenamiento es barato y los motores columnares comprimen bien la redundancia, así que se prioriza la simplicidad y la velocidad de consulta.

> **En una frase:** «La estrella desnormaliza las dimensiones para consultar con menos joins; el copo de nieve las normaliza para reducir redundancia. Hoy se prefiere la estrella».

## Ejemplo

```
            ESTRELLA                              COPO DE NIEVE

  dim_fecha     dim_cliente            dim_fecha     dim_cliente ── dim_ciudad
        \         /                          \         /
         fct_ventas                           fct_ventas
        /         \                          /         \
  dim_tienda   dim_producto            dim_tienda   dim_producto ── dim_categoria
```

## Preguntas de seguimiento

- ¿Cuándo tendría sentido un copo de nieve? (dimensiones enormes con jerarquías muy reutilizadas)
- ¿Qué es una *One Big Table* (OBT) y cuándo se usa?

## Referencias

- [Kimball Group — Star Schemas and OLAP Cubes](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/)
