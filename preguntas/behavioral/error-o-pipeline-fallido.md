# Cuéntame un error que cometiste o una vez que algo falló en producción

**Nivel:** 🟢 Junior
**Tags:** `behavioral`, `errores`, `aprendizaje`, `star`
**Visto en:** Pregunta frecuente — entrevista con hiring manager

## Respuesta

Evalúan **responsabilidad, honestidad y capacidad de aprender**. En Data Engineering los fallos son habituales (datos duplicados, pipelines caídos, cambios de esquema en origen); lo importante es **cómo reaccionas**.

Estructura (STAR orientado al aprendizaje):
1. **Situación y error:** explícalo con honestidad, **asumiendo tu parte** sin culpar a otros.
2. **Acción inmediata:** cómo lo detectaste, a quién avisaste y cómo lo corregiste.
3. **Acción preventiva:** qué cambiaste para que **no vuelva a ocurrir** (tests, alertas, revisiones, documentación).
4. **Resultado y aprendizaje.**

**Evita:** decir que nunca te has equivocado, falsos defectos ("soy demasiado perfeccionista") o errores graves de ética o seguridad.

> **Claves:** reconoce el error, cuenta cómo lo resolviste y, sobre todo, qué cambiaste para evitarlo.

## Ejemplo

> **S:** *"Desarrollé una carga diaria de pedidos con `INSERT`. Un día el job falló a mitad, Airflow lo reintentó y el dashboard de ventas mostró el doble de ingresos de ese día."*
>
> **A (inmediata):** *"Un analista lo detectó por la mañana. Avisé al equipo de que el dato no era fiable, identifiqué la causa y corregí la partición de ese día."*
>
> **A (preventiva):** *"Cambié la carga a delete + insert por fecha para hacerla idempotente, añadí un test de unicidad sobre `pedido_id` que detiene el pipeline y una alerta si el volumen diario varía más de un 30 %."*
>
> **R:** *"No volvió a ocurrir, y desde entonces diseño cada pipeline pensando en qué pasa si se ejecuta dos veces."*

## Preguntas de seguimiento

- ¿Cómo comunicaste el problema a los usuarios afectados?
- ¿Qué harías si el error lo hubiera cometido un compañero?

## Referencias

- [Google SRE — Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
