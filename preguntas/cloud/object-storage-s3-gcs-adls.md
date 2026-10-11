# ¿Qué es el almacenamiento de objetos (S3, GCS, ADLS) y por qué se usa tanto en datos?

**Nivel:** 🟢 Junior
**Tags:** `cloud`, `s3`, `gcs`, `adls`, `almacenamiento`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

El **almacenamiento de objetos** guarda datos como **objetos** (fichero + metadatos + clave única) dentro de **buckets/contenedores**, en lugar de en un sistema de ficheros jerárquico o en discos de bloques.

| Proveedor | Servicio |
|---|---|
| AWS | Amazon S3 |
| Google Cloud | Google Cloud Storage (GCS) |
| Azure | Azure Data Lake Storage Gen2 (ADLS) / Blob Storage |

Por qué es la base de los data lakes:
- **Escalabilidad prácticamente ilimitada** y alta durabilidad (S3 indica 11 nueves).
- **Barato**, con **clases de almacenamiento** por frecuencia de acceso (estándar, infrecuente, archivo).
- **Separa almacenamiento y cómputo:** Spark, Athena, BigQuery, Snowflake o Databricks leen los mismos ficheros.
- Políticas de **ciclo de vida** (mover a archivo o borrar tras N días) y **versionado**.

Matiz importante: las "carpetas" son en realidad **prefijos** de la clave (`ventas/2026/01/…`). Organizar bien esos prefijos (particionado tipo Hive: `fecha=2026-01-01/`) es clave para el rendimiento.

> **En una frase:** «Es almacenamiento escalable, duradero y barato que separa los datos del cómputo, por eso es la base de casi cualquier data lake».

## Ejemplo

```
s3://empresa-datalake/
├── raw/ventas/fecha=2026-10-01/ventas.json
├── raw/ventas/fecha=2026-10-02/ventas.json
└── curated/ventas/fecha=2026-10-01/part-0000.parquet
```

```bash
aws s3 cp ventas.json s3://empresa-datalake/raw/ventas/fecha=2026-10-01/
aws s3 ls s3://empresa-datalake/raw/ventas/ --recursive
```

## Preguntas de seguimiento

- ¿Cómo controlas costes en S3? (clases de almacenamiento, ciclo de vida, compresión, evitar muchos ficheros pequeños)
- ¿Cómo protegerías un bucket con datos sensibles? (bloquear acceso público, cifrado, IAM de mínimo privilegio)

## Referencias

- [Amazon S3 — User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [Google Cloud Storage — Documentation](https://cloud.google.com/storage/docs)
