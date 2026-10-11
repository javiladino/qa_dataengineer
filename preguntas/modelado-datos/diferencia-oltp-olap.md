# ¿Cuál es la diferencia entre OLTP y OLAP?

**Nivel:** 🟢 Junior
**Tags:** `modelado`, `oltp`, `olap`, `data-warehouse`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| | OLTP (*Online Transaction Processing*) | OLAP (*Online Analytical Processing*) |
|---|---|---|
| Propósito | Operar el negocio (transacciones) | Analizar el negocio (informes, BI) |
| Operaciones | Muchas lecturas/escrituras pequeñas (`INSERT`, `UPDATE`) | Pocas consultas grandes de lectura y agregación |
| Modelo | **Normalizado** (3NF) para evitar redundancia | **Desnormalizado** (esquema estrella) para consultar rápido |
| Datos | Estado actual | Histórico |
| Almacenamiento | Orientado a filas | Orientado a **columnas** |
| Usuarios | Aplicaciones, clientes | Analistas, BI, data science |
| Ejemplos | PostgreSQL, MySQL, SQL Server, Oracle | BigQuery, Snowflake, Redshift, Databricks SQL |

El trabajo típico de un Data Engineer es **mover datos de sistemas OLTP a un sistema OLAP**, transformándolos para el análisis sin cargar la base de datos operacional.

> **En una frase:** «OLTP registra las operaciones del día a día con un modelo normalizado; OLAP almacena el histórico desnormalizado para analizarlo de forma eficiente».

## Ejemplo

```sql
-- OLTP: transacción puntual, afecta a una fila
UPDATE cuentas SET saldo = saldo - 50 WHERE cuenta_id = 1234;

-- OLAP: escanea millones de filas para agregar
SELECT d.anio, d.mes, p.categoria, SUM(f.importe) AS ventas
FROM fct_ventas f
JOIN dim_fecha d    ON f.fecha_key = d.fecha_key
JOIN dim_producto p ON f.producto_key = p.producto_key
GROUP BY d.anio, d.mes, p.categoria;
```

## Preguntas de seguimiento

- ¿Por qué no lanzar los informes directamente contra la base de datos de producción?
- ¿Por qué el almacenamiento columnar es más eficiente para analítica?

## Referencias

- [AWS — OLTP vs OLAP](https://aws.amazon.com/compare/the-difference-between-olap-and-oltp/)
