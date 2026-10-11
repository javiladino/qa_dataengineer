# ¿Qué es Apache Airflow y qué es un DAG?

**Nivel:** 🟢 Junior
**Tags:** `airflow`, `orquestacion`, `dag`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**Apache Airflow** es una plataforma para **programar, ejecutar y monitorizar flujos de trabajo** definidos en código Python. No procesa los datos por sí mismo: **coordina** las tareas que lo hacen (consultas SQL, jobs de Spark, scripts, llamadas a APIs, `dbt run`…).

Un **DAG** (*Directed Acyclic Graph*) es la definición de un flujo:
- **Directed:** las tareas tienen un orden (A → B).
- **Acyclic:** no hay ciclos (B nunca puede volver a A).
- **Graph:** tareas (nodos) conectadas por dependencias (aristas).

Qué aporta un orquestador frente a un `cron`:
- Dependencias entre tareas.
- **Reintentos** automáticos y alertas ante fallos.
- Interfaz web con el estado e histórico de cada ejecución.
- *Backfills* (reprocesar fechas pasadas).
- Conectores con cientos de sistemas.

Alternativas: **Dagster**, **Prefect**, **Azure Data Factory**, **AWS Step Functions**, **Google Cloud Composer** (que es Airflow gestionado).

> **En una frase:** «Airflow orquesta tareas definidas como DAGs en Python: decide qué se ejecuta, cuándo y en qué orden, con reintentos y monitorización».

## Ejemplo

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="ventas_diarias",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2},
) as dag:

    extraer = BashOperator(task_id="extraer", bash_command="python extract.py {{ ds }}")
    cargar = BashOperator(task_id="cargar", bash_command="python load.py {{ ds }}")
    transformar = BashOperator(task_id="transformar", bash_command="dbt run --select ventas")

    extraer >> cargar >> transformar
```

## Preguntas de seguimiento

- ¿Por qué Airflow no debería usarse para procesar los datos dentro del propio worker?
- ¿Qué es `{{ ds }}`? (macro con la fecha lógica de la ejecución)

## Referencias

- [Airflow — Core Concepts: DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
