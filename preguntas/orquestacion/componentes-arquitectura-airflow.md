# ¿Cuáles son los componentes principales de la arquitectura de Airflow?

**Nivel:** 🟢 Junior
**Tags:** `airflow`, `arquitectura`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

| Componente | Función |
|---|---|
| **Scheduler** | Lee los DAGs, decide qué tareas deben ejecutarse según el calendario y las dependencias, y las envía al executor |
| **Executor** | Define **cómo y dónde** se ejecutan las tareas (`LocalExecutor`, `CeleryExecutor`, `KubernetesExecutor`) |
| **Workers** | Procesos que ejecutan realmente las tareas (en Celery/Kubernetes) |
| **Metadata database** | Base de datos (normalmente PostgreSQL) con el estado de DAGs, ejecuciones, tareas, conexiones y variables |
| **Webserver / API server** | Interfaz web para monitorizar, relanzar tareas y revisar logs |
| **DAG processor** | Parsea los ficheros Python de la carpeta de DAGs |
| **Triggerer** | Gestiona tareas *deferrable* (esperas asíncronas sin ocupar un worker) |

Flujo simplificado: el **DAG processor** parsea los DAGs → el **scheduler** decide qué toca ejecutar → el **executor** lo envía a los **workers** → el estado se guarda en la **metadata DB** → lo ves en la **UI**.

> **En una frase:** «El scheduler decide qué ejecutar, el executor y los workers lo ejecutan, la metadata DB guarda el estado y la UI permite monitorizarlo».

## Ejemplo

Elección de executor según el caso:

| Executor | Cuándo |
|---|---|
| `LocalExecutor` | Desarrollo o cargas pequeñas en una sola máquina |
| `CeleryExecutor` | Producción con un pool fijo de workers |
| `KubernetesExecutor` | Cada tarea en su propio pod, aislamiento y escalado elástico |

## Preguntas de seguimiento

- ¿Por qué no se debe hacer trabajo pesado (consultas, llamadas a API) en el código de nivel superior del fichero del DAG? (el DAG processor lo ejecuta en cada parseo)
- ¿Qué servicios gestionados de Airflow conoces? (Cloud Composer, Amazon MWAA, Astronomer)

## Referencias

- [Airflow — Architecture Overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
