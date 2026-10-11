# ¿Cómo manejas excepciones en Python? (try / except / else / finally)

**Nivel:** 🟢 Junior
**Tags:** `python`, `excepciones`, `robustez`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| Bloque | Se ejecuta… |
|---|---|
| `try` | Siempre: contiene el código que puede fallar |
| `except TipoError` | Solo si ocurre **esa** excepción |
| `else` | Solo si **no** hubo excepción |
| `finally` | **Siempre**, haya error o no (liberar recursos) |
| `raise` | Lanza (o relanza) una excepción |

Buenas prácticas en pipelines de datos:
1. **Captura excepciones específicas** (`ValueError`, `KeyError`…), nunca un `except:` vacío que oculte errores.
2. **No silencies errores**: registra con `logging` y decide si reintentar, enviar el registro a una tabla de rechazos (*dead letter*) o fallar.
3. **Falla rápido** si el error compromete la integridad del dato: es mejor que el orquestador marque la tarea como fallida que cargar datos corruptos.
4. Usa **context managers** (`with`) para ficheros y conexiones: cierran el recurso automáticamente.

> **En una frase:** «Capturo excepciones concretas, las registro, separo los registros erróneos y dejo que el pipeline falle si el dato no es fiable».

## Ejemplo

```python
import logging

logger = logging.getLogger(__name__)

def parsear_importe(valor: str) -> float:
    try:
        importe = float(valor)
    except ValueError:
        logger.warning("Importe inválido: %r", valor)
        raise                                   # relanza para que el llamador decida
    else:
        return round(importe, 2)

validos, rechazados = [], []
for fila in ["10.5", "abc", "20"]:
    try:
        validos.append(parsear_importe(fila))
    except ValueError:
        rechazados.append(fila)                 # dead letter: no se pierde el dato

print(validos, rechazados)  # [10.5, 20.0] ['abc']
```

## Preguntas de seguimiento

- ¿Cómo crearías una excepción personalizada? (`class DatosInvalidosError(Exception): ...`)
- ¿Cómo implementarías reintentos ante un error de red? (bucle con *backoff* exponencial o librerías como `tenacity`)

## Referencias

- [Python Docs — Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
