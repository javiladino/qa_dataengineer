# ¿Qué diferencia hay entre Operators, Sensors y Hooks en Airflow?

**Nivel:** 🟢 Junior
**Tags:** `airflow`, `operators`, `sensors`, `hooks`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| Concepto | Qué es | Ejemplos |
|---|---|---|
| **Operator** | Plantilla de una **tarea**: define *qué* hace un paso del DAG | `BashOperator`, `PythonOperator`, `SQLExecuteQueryOperator`, `S3ToRedshiftOperator` |
| **Sensor** | Operator especial que **espera** a que se cumpla una condición | `FileSensor`, `S3KeySensor`, `ExternalTaskSensor`, `HttpSensor` |
| **Hook** | Interfaz reutilizable para **conectarse** a un sistema externo usando una *Connection* | `PostgresHook`, `S3Hook`, `HttpHook` |
| **Task** | Instancia de un operator dentro de un DAG | `extraer = PythonOperator(...)` |

Relación: los **operators** usan **hooks** por dentro para hablar con sistemas externos, y las credenciales viven en **Connections** de Airflow (nunca en el código).

**Buena práctica con sensors:** usa `mode="reschedule"` o sensores *deferrable* para que no ocupen un worker mientras esperan.

> **En una frase:** «El operator define qué hace una tarea, el sensor espera una condición y el hook encapsula la conexión con un sistema externo».

## Ejemplo

```python
from airflow.decorators import task
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.postgres.hooks.postgres import PostgresHook

esperar_fichero = S3KeySensor(
    task_id="esperar_fichero",
    bucket_name="raw-data",
    bucket_key="ventas/{{ ds }}/ventas.csv",
    mode="reschedule",
    poke_interval=300,
    timeout=6 * 60 * 60,
)

@task
def contar_ventas(ds=None):
    hook = PostgresHook(postgres_conn_id="dwh")          # credenciales en la Connection
    return hook.get_first("SELECT COUNT(*) FROM ventas WHERE fecha = %s", parameters=(ds,))[0]

esperar_fichero >> contar_ventas()
```

## Preguntas de seguimiento

- ¿Qué diferencia hay entre `mode="poke"` y `mode="reschedule"`?
- ¿Qué es la TaskFlow API (`@task`)?

## Referencias

- [Airflow — Operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html)
- [Airflow — Sensors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html)
