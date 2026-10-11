# Cuéntame un proyecto de datos del que estés orgulloso

**Nivel:** 🟢 Junior
**Tags:** `behavioral`, `proyecto`, `star`
**Visto en:** Pregunta frecuente — entrevista con hiring manager / técnica

## Respuesta

Quieren comprobar que has **construido algo real**, que entiendes las **decisiones técnicas** que tomaste y su **impacto**. Usa el método **STAR**:

| Paso | Qué contar | Peso aproximado |
|---|---|---|
| **S**ituación | Contexto y problema de negocio | 15 % |
| **T**area | Tu responsabilidad concreta | 10 % |
| **A**cción | **Qué hiciste tú** ("yo", no "nosotros"), tecnologías y **por qué** las elegiste | 50 % |
| **R**esultado | Impacto medible y qué aprendiste | 25 % |

**Si no tienes experiencia laboral:** un proyecto personal o de formación es perfectamente válido, siempre que sea un pipeline de extremo a extremo y esté publicado en GitHub.

**Prepárate para profundizar:** te preguntarán por qué elegiste cada herramienta, qué harías distinto y cómo escalaría.

> **Claves:** un problema real, decisiones justificadas, resultados con números y una lección aprendida.

## Ejemplo

> **S:** *"El equipo de ventas preparaba un informe semanal descargando 5 Excel de distintos sistemas; tardaban un día entero y había errores frecuentes."*
>
> **T:** *"Me encargaron automatizar el proceso y centralizar los datos."*
>
> **A:** *"Diseñé un pipeline con Python que extraía los datos de las APIs y los guardaba en crudo en GCS. Los cargué en BigQuery y modelé las tablas con dbt en un esquema estrella, con tests de unicidad y nulos. Lo orquesté con Airflow para que corriera a diario con alertas a Slack. Elegí dbt porque permitía que los analistas entendieran y revisaran la lógica en SQL."*
>
> **R:** *"El informe pasó de un día de trabajo manual a estar disponible cada mañana a las 7:00, y los tests detectaron dos problemas de calidad en origen que nadie había visto. Aprendí la importancia de hacer el pipeline idempotente desde el principio: la primera versión duplicaba datos al relanzarla."*

## Preguntas de seguimiento

- ¿Cuál fue la parte más difícil técnicamente?
- Si lo empezaras hoy, ¿qué harías diferente?
- ¿Cómo escalaría si el volumen se multiplicara por 100?

## Referencias

- [MIT Career Advising — Using the STAR method](https://capd.mit.edu/resources/the-star-method-for-behavioral-interviews/)
