# ¿Cómo gestionas permisos y seguridad de los datos en la nube? (IAM y mínimo privilegio)

**Nivel:** 🟢 Junior
**Tags:** `cloud`, `iam`, `seguridad`, `gobierno`
**Visto en:** Pregunta frecuente — entrevista técnica

## Respuesta

**IAM** (*Identity and Access Management*) define **quién** (usuario, grupo o identidad de servicio) puede hacer **qué** (acciones) sobre **qué recurso**.

Principios básicos:
1. **Mínimo privilegio:** cada identidad tiene solo los permisos que necesita. Un pipeline que lee de `raw/` y escribe en `curated/` no necesita permisos de administrador.
2. **Identidades de servicio para procesos:** los pipelines usan *roles* (AWS), *service accounts* (GCP) o *managed identities* (Azure), **nunca credenciales personales**.
3. **Sin secretos en el código:** usar un gestor de secretos (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) o las Connections del orquestador.
4. **Permisos por grupos/roles**, no usuario a usuario.
5. **Cifrado** en reposo y en tránsito, y **auditoría** de accesos (CloudTrail, Cloud Audit Logs).
6. **Datos sensibles (PII):** enmascaramiento, seguridad a nivel de fila o columna y separación de entornos.

> **En una frase:** «Aplico mínimo privilegio con identidades de servicio para los pipelines, sin secretos en el código y con permisos asignados por roles y auditados».

## Ejemplo

Política de AWS de mínimo privilegio para un job que lee crudo y escribe datos curados:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::empresa-datalake", "arn:aws:s3:::empresa-datalake/raw/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": ["arn:aws:s3:::empresa-datalake/curated/*"]
    }
  ]
}
```

## Preguntas de seguimiento

- ¿Qué harías si encuentras una credencial subida a un repositorio Git? (revocarla y rotarla inmediatamente; después limpiar el historial)
- ¿Qué es la seguridad a nivel de fila (*row-level security*)?

## Referencias

- [AWS — Security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Google Cloud — IAM overview](https://cloud.google.com/iam/docs/overview)
