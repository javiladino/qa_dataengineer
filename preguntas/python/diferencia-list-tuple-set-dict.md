# ¿Cuál es la diferencia entre list, tuple, set y dict?

**Nivel:** 🟢 Junior
**Tags:** `python`, `estructuras-de-datos`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| Estructura | Sintaxis | ¿Ordenada? | ¿Mutable? | ¿Duplicados? | Búsqueda `x in ...` | Uso típico |
|---|---|---|---|---|---|---|
| `list` | `[1, 2, 3]` | ✅ | ✅ | ✅ | O(n) | Colección ordenada que cambia |
| `tuple` | `(1, 2, 3)` | ✅ | ❌ | ✅ | O(n) | Registros fijos, claves de dict, retorno múltiple |
| `set` | `{1, 2, 3}` | ❌ | ✅ | ❌ | **O(1)** | Valores únicos, pertenencia, operaciones de conjuntos |
| `dict` | `{"a": 1}` | ✅ (orden de inserción, Python 3.7+) | ✅ | Claves ❌ | **O(1)** por clave | Mapear clave → valor, lookups |

Puntos clave:
- **Inmutable** (`tuple`) significa que es *hashable*, por lo que puede usarse como clave de un `dict` o elemento de un `set`; una `list` no.
- Para comprobar pertenencia en colecciones grandes, convierte la lista en `set`: pasa de O(n) a O(1).

> **En una frase:** «`list` para secuencias que cambian, `tuple` para datos fijos, `set` para unicidad y búsquedas rápidas, `dict` para relaciones clave-valor».

## Ejemplo

```python
ids_procesados = set()                       # búsqueda O(1)
registros = [("2026-01-01", 101), ("2026-01-01", 101), ("2026-01-02", 102)]

for fecha, cliente_id in registros:          # cada registro es una tupla
    if cliente_id in ids_procesados:
        continue                             # salta duplicados
    ids_procesados.add(cliente_id)

ventas_por_dia = {}                          # dict: clave → valor
for fecha, _ in registros:
    ventas_por_dia[fecha] = ventas_por_dia.get(fecha, 0) + 1

print(ventas_por_dia)  # {'2026-01-01': 2, '2026-01-02': 1}
```

## Preguntas de seguimiento

- ¿Por qué una `list` no puede ser clave de un diccionario? (no es hashable)
- ¿Qué es `collections.defaultdict` y `Counter`?
- ¿Cómo eliminas duplicados de una lista manteniendo el orden? (`list(dict.fromkeys(lista))`)

## Referencias

- [Python Docs — Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python Wiki — Time Complexity](https://wiki.python.org/moin/TimeComplexity)
