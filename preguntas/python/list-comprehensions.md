# ¿Qué es una list comprehension y cuándo usarla?

**Nivel:** 🟢 Junior
**Tags:** `python`, `comprehensions`, `buenas-practicas`
**Visto en:** Pregunta frecuente — entrevista técnica / live coding

## Respuesta

Una **list comprehension** es una sintaxis compacta para crear una lista a partir de un iterable, aplicando opcionalmente una transformación y un filtro:

```python
[expresion for elemento in iterable if condicion]
```

Existen equivalentes para otras estructuras:
- **Dict comprehension:** `{k: v for k, v in ...}`
- **Set comprehension:** `{x for x in ...}`
- **Expresión generadora:** `(x for x in ...)` → no crea la lista en memoria.

**Ventajas:** más legible y concisa que un bucle `for` con `append`, y suele ser algo más rápida.
**Cuándo NO usarla:** si la lógica es compleja (varios `if/else` anidados, efectos secundarios). Ahí un bucle normal es más claro. Y si el resultado es enorme y solo lo vas a recorrer una vez, usa una expresión generadora.

> **En una frase:** «Es una forma concisa y pythónica de transformar y filtrar colecciones; la uso cuando la lógica cabe cómodamente en una línea».

## Ejemplo

```python
pedidos = [
    {"id": 1, "importe": 120.0, "estado": "ok"},
    {"id": 2, "importe": 35.5,  "estado": "cancelado"},
    {"id": 3, "importe": 80.0,  "estado": "ok"},
]

# Bucle tradicional
importes = []
for p in pedidos:
    if p["estado"] == "ok":
        importes.append(p["importe"])

# List comprehension equivalente
importes = [p["importe"] for p in pedidos if p["estado"] == "ok"]

# Dict comprehension: id → importe con IVA
con_iva = {p["id"]: round(p["importe"] * 1.21, 2) for p in pedidos}

# Expresión generadora: suma sin crear lista intermedia
total = sum(p["importe"] for p in pedidos if p["estado"] == "ok")
```

## Preguntas de seguimiento

- ¿Cuál es la diferencia entre `[x for x in ...]` y `(x for x in ...)`?
- ¿Cómo aplanarías una lista de listas? (`[x for sub in lista for x in sub]`)

## Referencias

- [Python Docs — List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
