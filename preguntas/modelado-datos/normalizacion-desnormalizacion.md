# ¿Qué es la normalización y cuándo conviene desnormalizar?

**Nivel:** 🟢 Junior
**Tags:** `modelado`, `normalizacion`, `formas-normales`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**Normalizar** es organizar las tablas para **eliminar redundancia** y evitar anomalías al insertar, actualizar o borrar. Las formas normales más preguntadas:

| Forma normal | Regla | Ejemplo de violación |
|---|---|---|
| **1NF** | Valores atómicos, sin grupos repetidos | Columna `telefonos = "600111, 600222"` |
| **2NF** | 1NF + cada atributo depende de **toda** la clave primaria | En `(pedido_id, producto_id)`, guardar `nombre_producto` (depende solo de `producto_id`) |
| **3NF** | 2NF + sin dependencias **transitivas** entre atributos no clave | Guardar `ciudad` y `pais` en `clientes` cuando `pais` depende de `ciudad` |

**Desnormalizar** es introducir redundancia a propósito para **leer más rápido** (menos joins).

| Normalizar | Desnormalizar |
|---|---|
| Sistemas OLTP | Data warehouses / OLAP |
| Muchas escrituras | Muchas lecturas y agregaciones |
| Integridad y consistencia | Rendimiento y simplicidad de consulta |

> **En una frase:** «Normalizo en sistemas transaccionales para garantizar integridad, y desnormalizo en analítica para consultar rápido con menos joins».

## Ejemplo

```sql
-- Normalizado (OLTP)
CREATE TABLE paises   (pais_id INT PRIMARY KEY, nombre VARCHAR(50));
CREATE TABLE ciudades (ciudad_id INT PRIMARY KEY, nombre VARCHAR(50),
                       pais_id INT REFERENCES paises(pais_id));
CREATE TABLE clientes (cliente_id INT PRIMARY KEY, nombre VARCHAR(100),
                       ciudad_id INT REFERENCES ciudades(ciudad_id));

-- Desnormalizado (dimensión analítica)
CREATE TABLE dim_cliente (
    cliente_key INT, nombre VARCHAR(100),
    ciudad VARCHAR(50), pais VARCHAR(50)     -- redundancia intencionada
);
```

## Preguntas de seguimiento

- ¿Qué es una anomalía de actualización?
- ¿Qué es BCNF (forma normal de Boyce-Codd)?

## Referencias

- [Microsoft — Database normalization description](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)
