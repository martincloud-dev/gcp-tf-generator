# Terraform GCP Generator

Herramienta CLI para generar proyectos Terraform para Google Cloud Platform (GCP) de forma rápida y sencilla.

## Características

- Creación de proyectos Terraform con estructura organizada
- Generación automática de archivos base (backend, provider, variables, outputs)
- Soporte para múltiples servicios de GCP  
- Adición de servicios a proyectos existentes
- Utilización de abreviaturas para cada servicio

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/yourusername/terraform-gcp-generator.git

# Entrar al directorio
cd terraform-gcp-generator

# Instalar el paquete
pip install -e .
```

## Uso

### Crear un nuevo proyecto

```bash
# Crear un proyecto básico
tf-gcp create mi-proyecto --destino /ruta/donde/crear/proyecto

# Crear un proyecto con servicios específicos
tf-gcp create mi-proyecto --destino /ruta/donde/crear/proyecto --svc "cs,ce,lb"
```

### Añadir servicios a un proyecto existente

```bash
# Añadir un servicio a un proyecto existente
tf-gcp add /ruta/al/proyecto --svc vpc

# Añadir un servicio usando su abreviatura
tf-gcp add /ruta/al/proyecto --svc fw
```

### Listar servicios disponibles

```bash
# Ver todos los servicios disponibles con sus abreviaturas
tf-gcp services
```

## Servicios Disponibles

- **Compute Engine (VM)**: `compute-engine` (ce)
- **Cloud Storage**: `cloud-storage` (cs)
- **Cloud SQL**: `cloud-sql` (csql)
- **Cloud Run**: `cloud-run` (cr)
- **BigQuery**: `bigquery` (bq)
- **Kubernetes Engine (GKE)**: `kubernetes-engine` (gke)
- **Cloud Functions**: `cloud-functions` (cf)
- **Load Balancer**: `load-balancer` (lb)
- **VPC**: `vpc` (vpc)
- **IAM**: `iam` (iam)
- **Firewall**: `firewall` (fw)
- **DNS**: `dns` (dns)
- **Cloud Armor**: `cloud-armor` (armor)
- **CDN**: `cdn` (cdn)
- **Cloud NAT**: `cloud-nat` (nat)
- **SSL Certificate**: `ssl-certificate` (ssl)

## Desinstalación

Para desinstalar la herramienta, sigue estos pasos:

```bash
# Desinstalar el paquete
pip uninstall terraform-gcp-generator

# Opcionalmente, eliminar el directorio del repositorio
rm -rf /ruta/a/terraform-gcp-generator
```

## Licencia

MIT

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request. 