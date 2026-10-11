# ¿Qué es una tabla de hechos y qué es una tabla de dimensiones?

**Nivel:** 🟢 Junior
**Tags:** `modelado`, `kimball`, `hechos`, `dimensiones`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Son las dos piezas del **modelado dimensional** (Kimball):

| | Tabla de hechos (*fact*) | Tabla de dimensiones (*dim*) |
|---|---|---|
| Contiene | **Medidas** numéricas de un evento de negocio | **Contexto** descriptivo: quién, qué, dónde, cuándo |
| Ejemplos de columnas | `importe`, `cantidad`, `descuento` + claves foráneas | `nombre_cliente`, `ciudad`, `categoria_producto` |
| Tamaño | Muy grande (millones de filas), crece rápido | Más pequeña, crece despacio |
| Forma | Estrecha y larga | Ancha (muchos atributos) |
| Uso en la consulta | Lo que **agregas** (`SUM`, `AVG`) | Lo que usas para **filtrar y agrupar** |

Concepto clave: **la granularidad (*grain*)** de la tabla de hechos, es decir, qué representa exactamente una fila (p. ej. «una línea de pedido»). Es lo primero que se define al diseñar.

Tipos de hechos más comunes: **transaccionales** (un evento por fila), **snapshot periódico** (foto diaria/mensual, p. ej. stock) y **acumulativos** (ciclo de vida de un proceso, p. ej. un pedido).

> **En una frase:** «Los hechos guardan las métricas de los eventos de negocio y las dimensiones el contexto para filtrarlas y agruparlas».

## Ejemplo

```sql
CREATE TABLE dim_cliente (
    cliente_key   INT PRIMARY KEY,   -- clave subrogada
    cliente_id    VARCHAR(20),       -- clave de negocio
    nombre        VARCHAR(100),
    ciudad        VARCHAR(50),
    segmento      VARCHAR(20)
);

CREATE TABLE fct_ventas (            -- grain: una línea de pedido
    fecha_key     INT,
    cliente_key   INT REFERENCES dim_cliente(cliente_key),
    producto_key  INT,
    cantidad      INT,
    importe       DECIMAL(12,2)
);
```

## Preguntas de seguimiento

- ¿Qué es una clave subrogada y por qué usarla en lugar de la clave de negocio?
- ¿Qué es una medida aditiva, semiaditiva y no aditiva? (p. ej. el saldo no se suma en el tiempo)

## Referencias

- [Kimball Group — Dimensional Modeling Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
