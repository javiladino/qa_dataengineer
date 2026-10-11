# Diseña un pipeline batch que cargue diariamente datos de una API a un data warehouse

**Nivel:** 🟢 Junior
**Tags:** `system-design`, `pipeline`, `batch`, `api`
**Visto en:** Pregunta frecuente — entrevista técnica / system design

## Respuesta

Estructura recomendada para responder (sirve para cualquier pregunta de diseño):

**1. Aclarar requisitos antes de diseñar**
- ¿Volumen de datos diario? ¿Frecuencia? ¿Qué latencia se necesita?
- ¿La API pagina? ¿Tiene límites de peticiones (*rate limits*)? ¿Permite filtrar por fecha de modificación?
- ¿Quién consume los datos y para qué?

**2. Diseño por capas**

| Paso | Qué hace | Herramienta ejemplo |
|---|---|---|
| **Extract** | Llama a la API por fecha, gestiona paginación, *rate limits* y reintentos con backoff | Python (`requests`) |
| **Land (raw)** | Guarda la respuesta **tal cual** en el lake, particionada por fecha | S3 / GCS → `raw/api_x/fecha=YYYY-MM-DD/` |
| **Load** | Carga el crudo en una tabla de staging | `COPY INTO`, carga de BigQuery |
| **Transform** | Limpia, tipa, deduplica y modela | dbt / SQL |
| **Test** | Valida unicidad, nulos y volumen esperado | dbt tests, Great Expectations |
| **Orchestrate** | Programa, reintenta y alerta ante fallos | Airflow |

**3. Requisitos no funcionales (los que diferencian una buena respuesta)**
- **Idempotencia:** relanzar un día sobrescribe esa partición, no duplica.
- **Carga incremental** si la API lo permite.
- **Monitorización y alertas** (Slack/email) en caso de fallo o de volumen anómalo.
- **Secretos** de la API en un gestor de secretos, nunca en el código.
- **Backfill** posible gracias a la partición por fecha.

> **En una frase:** «Extraigo de la API por fecha con reintentos, guardo el crudo en el lake, cargo y transformo en el warehouse con tests, y lo orquesto de forma idempotente con alertas».

## Ejemplo

```
         Airflow (diario, retries=3, alertas)
                     │
 API ──► extract.py ──► S3 raw/fecha=… ──► COPY ──► DWH.staging ──► dbt run + dbt test ──► DWH.marts ──► BI
```

## Preguntas de seguimiento

- ¿Qué harías si la API falla a mitad de la paginación?
- ¿Cómo detectarías que un día llegaron muchos menos registros de lo normal?
- ¿Cómo cambiaría el diseño si el volumen se multiplica por 100?

## Referencias

- [Airflow — Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
