# Terraform GCP Generator

Herramienta de línea de comandos para generar proyectos de Terraform para Google Cloud Platform (GCP).

## Características

- **Generación Rápida:** Crea la estructura base para proyectos Terraform de GCP en segundos.
- **Entornos Múltiples:** Cada proyecto incluye entornos separados para desarrollo, pruebas y producción.
- **Modular:** Añade solo los servicios que necesitas.
- **Abreviaturas:** Usa abreviaturas intuitivas para los servicios (ej: "cs" para Cloud Storage).
- **Mejores Prácticas:** Implementa automáticamente las mejores prácticas de Terraform para GCP.

## Instalación

```bash
# Clona el repositorio
git clone https://github.com/usuario/terraform-gcp-generator.git
cd terraform-gcp-generator

# Instala el paquete en modo desarrollo
pip install -e .
```

## Uso

### Crear un nuevo proyecto

```bash
# Crear un proyecto básico
tf-gcp create mi-proyecto --destino ./proyectos

# Crear un proyecto con servicios específicos
tf-gcp create mi-proyecto --destino ./proyectos --svc "cs,lb,vpc"
```

### Añadir servicios a un proyecto existente

```bash
# Añadir un servicio a un proyecto existente
tf-gcp add ./mi-proyecto --svc "sql"

# Añadir múltiples servicios
tf-gcp add ./mi-proyecto --svc "iam,gke"
```

### Ver servicios disponibles

```bash
# Listar todos los servicios disponibles
tf-gcp services
```

## Servicios Disponibles

### Computación
- **compute-engine (ce)**: Máquinas virtuales escalables
- **kubernetes-engine (gke)**: Servicio gestionado de Kubernetes
- **cloud-run (run)**: Plataforma serverless para contenedores
- **cloud-functions (cf)**: Plataforma serverless para funciones
- **app-engine (gae)**: Plataforma serverless para aplicaciones web

### Almacenamiento
- **cloud-storage (cs)**: Servicio de almacenamiento de objetos
- **cloud-sql (sql)**: Bases de datos relacionales gestionadas
- **bigquery (bq)**: Almacenamiento de datos y análisis
- **spanner (spn)**: Base de datos relacional global
- **memorystore (mem)**: Servicio Redis/Memcached gestionado

### Red
- **load-balancer (lb)**: Balanceadores de carga
- **vpc (vpc)**: Redes privadas virtuales
- **firewall (fw)**: Reglas de firewall
- **dns (dns)**: Servicio de nombres de dominio
- **cloud-armor (armor)**: Protección contra DDoS y ataques web
- **cdn (cdn)**: Red de distribución de contenido
- **cloud-nat (nat)**: Servicio de traducción de direcciones
- **ssl-certificate (ssl)**: Certificados SSL gestionados

### Mensajería
- **pubsub (ps)**: Servicio de mensajería en tiempo real
- **scheduler (sch)**: Programación de tareas y trabajos

### Procesamiento de Datos
- **dataflow (df)**: Procesamiento de datos en tiempo real/lotes

### DevOps
- **cloud-build (cb)**: Servicio de CI/CD
- **artifact-registry (ar)**: Registro de artefactos

### Seguridad
- **iam (iam)**: Gestión de identidades y accesos

## Estructura del Proyecto

Cada proyecto generado incluye:

```
proyecto/
├── README.md                   # Documentación del proyecto
└── environments/               # Directorio de entornos
    ├── dev/                    # Entorno de desarrollo
    │   ├── backend.tf          # Configuración del backend
    │   ├── provider.tf         # Configuración del proveedor
    │   ├── variables.tf        # Definición de variables
    │   ├── outputs.tf          # Outputs del proyecto
    │   ├── main.tf             # Recursos principales 
    │   ├── terraform.tfvars    # Valores de variables
    │   └── [servicios].tf      # Servicios específicos
    │
    ├── staging/                # Entorno de pruebas
    │   └── ...
    │
    └── prod/                   # Entorno de producción
        └── ...
```

## Desinstalación

Para desinstalar la herramienta:

```bash
pip uninstall terraform-gcp-generator
```

## Control de Versiones y Contribuciones

Este proyecto sigue convenciones de commit y ramas específicas para facilitar el desarrollo colaborativo:

### Convenciones de Commit

Usamos una nomenclatura estandarizada para los mensajes de commit basada en el tipo de rama:

```
feat(servicio): añadir soporte para Cloud Run
fix(cli): corregir error en comando de ayuda
docs(readme): actualizar instrucciones de instalación
```

Para más detalles, consulta el archivo [CONTRIBUTING.md](CONTRIBUTING.md).

### Flujo de Trabajo de Ramas

- **main**: Código en producción
- **develop**: Desarrollo principal
- **feature/xxx**: Nuevas funcionalidades
- **bugfix/xxx**: Corrección de errores
- **hotfix/xxx**: Correcciones urgentes
- **docs/xxx**: Documentación

## Licencia

Este proyecto está bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork del repositorio y envía un pull request. 