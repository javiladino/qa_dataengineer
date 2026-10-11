# ¿Qué es un generador en Python y por qué es útil en Data Engineering?

**Nivel:** 🟢 Junior
**Tags:** `python`, `generadores`, `yield`, `memoria`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Un **generador** es una función que usa `yield` en lugar de `return`. En vez de construir y devolver todos los resultados a la vez, **produce los valores de uno en uno, bajo demanda** (*lazy evaluation*), y recuerda su estado entre llamadas.

| | Lista | Generador |
|---|---|---|
| Memoria | Guarda **todos** los elementos | Guarda **solo el estado actual** |
| Cuándo calcula | Todo de golpe | Elemento a elemento, al iterar |
| Se puede recorrer | Varias veces | **Una sola vez** |

**Por qué importa en datos:** permite procesar ficheros o respuestas de API mucho más grandes que la RAM disponible, leyendo y transformando registro a registro, y encadenar pasos como si fuera un pequeño pipeline.

> **En una frase:** «Un generador produce valores bajo demanda con `yield`, así proceso volúmenes grandes con memoria constante».

## Ejemplo

```python
def leer_lineas(ruta):
    with open(ruta, encoding="utf-8") as f:
        for linea in f:                      # el propio fichero es un iterador
            yield linea.rstrip("\n")

def filtrar_errores(lineas):
    for linea in lineas:
        if "ERROR" in linea:
            yield linea

# Pipeline perezoso: nada se lee hasta que iteramos
errores = filtrar_errores(leer_lineas("app.log"))
for e in errores:
    print(e)

# Expresión generadora (como una list comprehension pero con paréntesis)
total_bytes = sum(len(l) for l in leer_lineas("app.log"))
```

## Preguntas de seguimiento

- ¿Qué diferencia hay entre un iterable y un iterador? (`__iter__` vs `__next__`)
- ¿Qué pasa si intentas recorrer un generador por segunda vez? (está agotado, no devuelve nada)
- ¿Para qué sirve `yield from`?

## Referencias

- [Python Docs — Generators](https://docs.python.org/3/howto/functional.html#generators)
