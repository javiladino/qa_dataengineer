# ¿Cómo garantizas la calidad de los datos en un pipeline?

**Nivel:** 🟢 Junior
**Tags:** `system-design`, `calidad-datos`, `testing`, `observabilidad`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**Dimensiones de calidad** que conviene nombrar:

| Dimensión | Pregunta | Ejemplo de test |
|---|---|---|
| **Completitud** | ¿Faltan datos? | `not_null` en columnas obligatorias; volumen ≥ mínimo esperado |
| **Unicidad** | ¿Hay duplicados? | `unique` en la clave primaria |
| **Validez** | ¿Los valores tienen sentido? | `importe >= 0`, valores dentro de una lista permitida |
| **Consistencia** | ¿Cuadra entre sistemas? | Total de ventas del DWH = total del sistema origen |
| **Integridad referencial** | ¿Las claves existen? | Cada `cliente_id` de hechos existe en `dim_cliente` |
| **Actualidad** (*freshness*) | ¿Están al día? | Último registro con menos de 24 h |

**Dónde aplicarlo:**
1. **En la ingesta:** validar el esquema y enviar los registros inválidos a una tabla de rechazos.
2. **En la transformación:** tests automáticos (dbt tests, Great Expectations, Soda).
3. **En CI/CD:** ejecutar los tests antes de desplegar cambios.
4. **En producción:** monitorización y alertas (freshness, volumen, anomalías).

**Decisión clave:** qué tests **bloquean** el pipeline (p. ej. claves duplicadas) y cuáles solo **avisan** (p. ej. una ligera variación de volumen).

> **En una frase:** «Defino tests de unicidad, nulos, validez, integridad y frescura en cada capa, automatizados y con alertas; los críticos detienen el pipeline antes de que el dato llegue al negocio».

## Ejemplo

```yaml
# dbt: models/marts/schema.yml
version: 2
models:
  - name: fct_ventas
    columns:
      - name: venta_id
        tests: [unique, not_null]
      - name: cliente_id
        tests:
          - relationships:
              to: ref('dim_cliente')
              field: cliente_id
      - name: estado
        tests:
          - accepted_values:
              values: ['completado', 'cancelado', 'pendiente']
```

## Preguntas de seguimiento

- ¿Qué es un *data contract*?
- ¿Qué harías si un test crítico falla a las 6:00 y el informe se consulta a las 9:00?

## Referencias

- [dbt — Data tests](https://docs.getdbt.com/docs/build/data-tests)
- [Great Expectations — Documentation](https://docs.greatexpectations.io/)
