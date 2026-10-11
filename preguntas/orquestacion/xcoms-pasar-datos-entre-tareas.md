# ¿Cómo se pasan datos entre tareas en Airflow? ¿Qué son los XComs?

**Nivel:** 🟢 Junior
**Tags:** `airflow`, `xcom`, `buenas-practicas`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

Las tareas de Airflow se ejecutan de forma **aislada** (incluso en máquinas distintas), así que no comparten variables en memoria. Para comunicarse usan **XComs** (*cross-communications*): pequeños valores que una tarea guarda en la metadata DB y otra lee.

- Con la **TaskFlow API** (`@task`), el `return` de una tarea se guarda automáticamente como XCom y se pasa como argumento a la siguiente.
- Con operators clásicos: `ti.xcom_push(...)` / `ti.xcom_pull(...)`.

**Regla clave:** los XComs son para **metadatos pequeños** (rutas de ficheros, IDs, contadores, fechas), **no para datasets**. Para pasar datos reales, la tarea A escribe en almacenamiento externo (S3, GCS, una tabla) y pasa por XCom **la ruta**.

> **En una frase:** «Uso XComs para pasar metadatos pequeños como rutas o IDs; los datos en sí se escriben en almacenamiento externo».

## Ejemplo

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False)
def pipeline_ventas():

    @task
    def extraer(ds=None) -> str:
        ruta = f"s3://raw/ventas/{ds}/ventas.parquet"
        # ... descarga y escribe el fichero en S3 ...
        return ruta                      # ✅ XCom: solo la ruta

    @task
    def cargar(ruta: str):
        print(f"Cargando {ruta} en el DWH")

    cargar(extraer())

pipeline_ventas()
```

## Preguntas de seguimiento

- ¿Qué pasa si guardas un DataFrame de 1 GB en un XCom? (sobrecarga la metadata DB y degrada todo Airflow)
- ¿Qué es un *custom XCom backend*? (guarda los XComs en S3/GCS en lugar de en la base de datos)

## Referencias

- [Airflow — XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)
