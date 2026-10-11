# ¿Cuál es la diferencia entre usar dbt Core y SQL puro?

**Nivel:** 🟡 Mid
**Tags:** `dbt`, `sql`, `transformacion`
**Visto en:** 2026 — entrevista técnica

## Respuesta

La respuesta corta y contundente para una entrevista es:

> **«dbt no reemplaza a SQL; dbt le da superpoderes de ingeniería de software a SQL.»**
> 
> 
> SQL es el *lenguaje* con el que transformas los datos; **dbt Core es el *framework/herramienta* que gestiona, compila, prueba, documenta y orquesta ese SQL** dentro de tu Data Warehouse o Data Lake.
> 

### La analogía para entenderlo de golpe

- **SQL tradicional:** Es como construir una casa poniendo ladrillos a mano uno por uno sin planos formales. Escribes scripts largos llenos de `CREATE OR REPLACE TABLE ... AS SELECT ...`, procedimientos almacenados (*stored procedures*) y tienes que acordarte tú mismo de qué tabla se debe crear primero antes que las demás.
- **dbt Core:** Es la constructora automatizada. Tú solo describes la habitación (`SELECT * FROM ...`), y dbt se encarga de crear las tablas o vistas, calcular las dependencias entre ellas, correr pruebas de calidad (que no haya nulos o duplicados) y generar los planos (documentación y linaje) en tiempo real.

### Las 5 diferencias técnicas clave

| **Característica** | **SQL Puro (Scripts / Stored Procedures)** | **dbt Core** |
| --- | --- | --- |
| **Materialización (DDL)** | Tienes que escribir manualmente `CREATE TABLE`, `CREATE VIEW`, `INSERT INTO`, o lidiar con lógica compleja de `MERGE` para cargas incrementales. | **Solo escribes `SELECT`**. En la cabecera o archivo config dices si quieres que sea `table`, `view` o `incremental`, y dbt genera el DDL óptimo para tu motor. |
| **Dependencias y Linaje (DAG)** | **Manual y frágil**. Tienes que recordar el orden: *«primero ejecuto script_1.sql, luego script_2.sql»*. Si cambias el nombre de una tabla, se rompen 10 consultas. | **Automático**. Usas la función `{{ ref('mi_modelo_previo') }}`. dbt lee las referencias, genera un grafo acíclico dirigido (**DAG**) y corre las consultas en paralelo respetando las dependencias. |
| **Calidad y Testing** | Manual o inexistente. Tienes que escribir consultas ad-hoc para buscar duplicados o nulos y revisarlas a ojo. | **Declarativo y automatizado**. En un archivo YAML defines: `unique`, `not_null`, `relationships` (integridad referencial). Si un test falla, dbt detiene la pipeline o te avisa en CI/CD. |
| **Entornos (Dev vs. Prod)** | Riesgoso. Si en tu SQL escribes `FROM production_db.raw_data`, corres el riesgo de sobreescribir o ensuciar tablas de producción mientras pruebas en local. | **Aislado por configuración**. dbt conmuta automáticamente el esquema según el entorno: en local corre contra `dev_usuario.mi_tabla` y en CI/CD o producción contra `analytics.mi_tabla`, sin tocar una sola línea de SQL. |
| **Documentación y Linaje** | Documentos de Confluence o Excel desactualizados a los dos días. | Un comando (`dbt docs generate`) crea un sitio web interactivo con el catálogo de datos, descripciones de columnas y el árbol gráfico de cómo fluye el dato de origen a fin. |

## Ejemplo
### Ejemplo práctico: Mira cómo cambia el código

#### ❌ Cómo se hace con SQL tradicional:

SQL

```
-- Tienes que gestionar permisos, si la tabla existe, cómo recrearla, etc.
DROP TABLE IF EXISTS analytics.fct_aves_nantes;

CREATE TABLE analytics.fct_aves_nantes AS
SELECT
    id,
    species_guess,
    latitude,
    longitude
FROM raw_datalake.nantes_aves_2026 -- Si este nombre cambia o la tabla no está cargada, fallas.
WHERE quality_grade = 'research';
```

#### ✅ Cómo se hace con dbt Core (`fct_aves_nantes.sql`):

SQL

```
-- Configuras cómo materializarlo sin escribir DDL
{{ config(materialized='table') }}

SELECT
    id,
    species_guess,
    latitude,
    longitude
-- dbt sabe exactamente qué tabla es y que este modelo depende de stg_inaturalist
FROM {{ ref('stg_inaturalist_observations') }}
WHERE quality_grade = 'research'
```

Y junto a ese archivo, agregas su test en `schema.yml`:

YAML

```
version: 2
models:
  - name: fct_aves_nantes
    columns:
      - name: id
        tests:
          - unique
          - not_null
```

### El guion exacto para decir en una entrevista

Si te vuelven a preguntar: *«¿Cuál es la diferencia entre usar dbt Core y SQL puro?»*, responde esto:

> *"SQL es el motor de cálculo y el estándar para consultar datos, pero cuando gestionas un Data Warehouse a escala empresarial, el SQL puro presenta problemas de mantenibilidad: lógica DDL repetitiva (`CREATE/MERGE`), dependencias manuales y falta de pruebas automatizadas.*
> 
> 
> *dbt Core incorpora las mejores prácticas del desarrollo de software a SQL. Con dbt:*
> 
> 1. *Nos enfocamos solo en la lógica de negocio mediante sentencias `SELECT`, abstrayendo la materialización (tablas, vistas o incrementales).*
> 2. *Gestionamos el linaje y las dependencias automáticamente mediante la función `ref()`, creando un grafo (DAG) ejecutable.*
> 3. *Aseguramos la calidad del dato antes de que llegue a Power BI mediante pruebas automatizadas (`tests`) de unicidad y no-nulos en archivos YAML.*
> 4. *Mantenemos entornos aislados (desarrollo y producción) y control de versiones con Git de forma nativa."*

Con esta respuesta demuestras que no solo sabes hacer consultas, sino que entiendes de **gobierno, calidad y ciclo de vida de los datos (Analytics Engineering)**.

## Preguntas de seguimiento

## Referencias
