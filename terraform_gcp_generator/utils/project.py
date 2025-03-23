"""
Funciones para la creación y gestión de proyectos Terraform.
"""

import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from ..services.servicios import obtener_servicio_template

# Obtener la ruta base del paquete para acceder a las plantillas
BASE_DIR = Path(__file__).parent.parent


def crear_proyecto(nombre_proyecto, destino, region="us-central1", zona="us-central1-a"):
    """
    Crea un nuevo proyecto Terraform para GCP con la estructura
    de directorios y archivos necesarios.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto
        destino (str): Directorio de destino
        region (str): Región por defecto de GCP
        zona (str): Zona por defecto de GCP
    
    Returns:
        str: Ruta al directorio del proyecto creado
    """
    # Crear el directorio del proyecto
    ruta_proyecto = os.path.join(destino, f"{nombre_proyecto}")
    os.makedirs(ruta_proyecto, exist_ok=True)
    
    # Generar README
    with open(os.path.join(ruta_proyecto, "README.md"), "w") as f:
        f.write(generar_readme(nombre_proyecto))
    
    # Crear directorio de entornos
    ruta_entornos = os.path.join(ruta_proyecto, "environments")
    os.makedirs(ruta_entornos, exist_ok=True)
    
    # Crear entornos
    entornos = ["dev", "staging", "prod"]
    for entorno in entornos:
        ruta_entorno = os.path.join(ruta_entornos, entorno)
        os.makedirs(ruta_entorno, exist_ok=True)
        
        with open(os.path.join(ruta_entorno, "backend.tf"), "w") as f:
            f.write(generar_backend(nombre_proyecto, entorno))
            
        with open(os.path.join(ruta_entorno, "provider.tf"), "w") as f:
            f.write(generar_provider())
            
        with open(os.path.join(ruta_entorno, "variables.tf"), "w") as f:
            f.write(generar_variables())
            
        with open(os.path.join(ruta_entorno, "outputs.tf"), "w") as f:
            f.write(generar_outputs())
            
        with open(os.path.join(ruta_entorno, "main.tf"), "w") as f:
            f.write(generar_main(nombre_proyecto))
            
        with open(os.path.join(ruta_entorno, "terraform.tfvars"), "w") as f:
            f.write(generar_tfvars(nombre_proyecto, region, zona, entorno))
        
    return ruta_proyecto


def añadir_servicio(ruta_proyecto: str, servicio: str) -> None:
    """
    Añade un servicio GCP a un proyecto Terraform existente en todos sus entornos.
    
    Args:
        ruta_proyecto: Ruta al proyecto Terraform
        servicio: Nombre del servicio a añadir
    """
    if not os.path.exists(ruta_proyecto):
        raise ValueError(f"El directorio del proyecto '{ruta_proyecto}' no existe")
    
    # Verificar que exista el directorio de entornos
    environments_dir = os.path.join(ruta_proyecto, "environments")
    if not os.path.exists(environments_dir):
        raise ValueError(f"El directorio de entornos '{environments_dir}' no existe")
    
    # Obtener la plantilla para el servicio
    template_contenido = obtener_servicio_template(servicio)
    
    # Añadir el servicio a cada entorno
    entornos = ["dev", "staging", "prod"]
    for entorno in entornos:
        entorno_dir = os.path.join(environments_dir, entorno)
        if os.path.exists(entorno_dir):
            # Crear archivo .tf con configuración del servicio en el entorno
            ruta_archivo = os.path.join(entorno_dir, f"{servicio}.tf")
            with open(ruta_archivo, 'w') as f:
                f.write(template_contenido)


def crear_archivo(ruta_proyecto, nombre_archivo, contenido):
    """
    Crea un archivo con el contenido especificado en la ruta indicada.
    
    Args:
        ruta_proyecto (str): Ruta del directorio donde se creará el archivo
        nombre_archivo (str): Nombre del archivo a crear
        contenido (str): Contenido del archivo
    """
    with open(os.path.join(ruta_proyecto, nombre_archivo), 'w') as f:
        f.write(contenido)


def generar_backend(nombre_proyecto, entorno=None):
    """
    Genera el contenido del archivo backend.tf.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto
        entorno (str, opcional): Entorno del proyecto
        
    Returns:
        str: Contenido del archivo backend.tf
    """
    bucket_name = nombre_proyecto
    if entorno:
        bucket_name = f"{nombre_proyecto}-{entorno}"
        
    return f"""#=========================================================================#
#                           BACKEND CONFIG                            #
#=========================================================================#
terraform {{
  backend "gcs" {{
    bucket  = "{bucket_name}-tfstate"
    prefix  = "terraform/state"
  }}
}}
"""


def generar_provider():
    """
    Genera el contenido del archivo provider.tf.
    
    Returns:
        str: Contenido del archivo provider.tf
    """
    return """#=========================================================================#
#                           PROVIDER CONFIG                           #
#=========================================================================#
# Proveedor de Google Cloud
provider "google" {
  # La región y el proyecto se toman de las variables
  region  = var.region
  project = var.project_id
}

# Proveedor para recursos globales
provider "google-beta" {
  region  = var.region
  project = var.project_id
}

#=========================================================================#
#                         TERRAFORM CONFIG                          #
#=========================================================================#
# Especificar la versión mínima de Terraform
terraform {
  required_version = ">= 1.0.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.0"
    }
  }
}
"""


def generar_variables():
    """
    Genera el contenido del archivo variables.tf.
    
    Returns:
        str: Contenido del archivo variables.tf
    """
    return """#=========================================================================#
#                              VARIABLES                              #
#=========================================================================#
variable "project_id" {
  description = "ID del proyecto de Google Cloud"
  type        = string
}

variable "region" {
  description = "Región de Google Cloud para desplegar los recursos"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Zona de Google Cloud para desplegar los recursos"
  type        = string
  default     = "us-central1-a"
}

variable "environment" {
  description = "Entorno (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "labels" {
  description = "Etiquetas para los recursos"
  type        = map(string)
  default     = {}
}
"""


def generar_outputs():
    """
    Genera el contenido del archivo outputs.tf.
    
    Returns:
        str: Contenido del archivo outputs.tf
    """
    return """#=========================================================================#
#                              OUTPUTS                                #
#=========================================================================#
output "project_id" {
  description = "ID del proyecto de Google Cloud"
  value       = var.project_id
}

output "region" {
  description = "Región de Google Cloud"
  value       = var.region
}

output "zone" {
  description = "Zona de Google Cloud"
  value       = var.zone
}

output "environment" {
  description = "Entorno actual"
  value       = var.environment
}
"""


def generar_main(nombre_proyecto):
    """
    Genera el contenido del archivo main.tf.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto
        
    Returns:
        str: Contenido del archivo main.tf
    """
    return f"""#=========================================================================#
#                               LOCALS                                #
#=========================================================================#
# Definiciones de valores locales
locals {{
  project_name = "{nombre_proyecto}"
  common_labels = {{
    project     = "{nombre_proyecto}"
    environment = var.environment
    terraform   = "true"
  }}
  
  # Combinar etiquetas comunes con las específicas
  labels = merge(var.labels, local.common_labels)
}}

#=========================================================================#
#                      PROJECT CONFIGURATION                       #
#=========================================================================#
# Configuraciones relacionadas al proyecto
# Por ejemplo, configuraciones de IAM, APIs, etc.

# Habilitar APIs necesarias
# resource "google_project_service" "services" {{
#   for_each = toset([
#     "compute.googleapis.com",
#     "storage.googleapis.com",
#     "iam.googleapis.com"
#   ])
#   
#   project = var.project_id
#   service = each.value
#   
#   disable_dependent_services = false
#   disable_on_destroy         = false
# }}
"""


def generar_tfvars(nombre_proyecto, region, zona, entorno=None):
    """
    Genera el contenido del archivo terraform.tfvars.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto
        region (str): Región de GCP
        zona (str): Zona de GCP
        entorno (str, opcional): Entorno (dev, staging, prod)
        
    Returns:
        str: Contenido del archivo terraform.tfvars
    """
    # Crear un ID de proyecto único que incluya el entorno si está especificado
    project_id = f"{nombre_proyecto}"
    if entorno:
        project_id += f"-{entorno}"
    
    return f"""# Valores de las variables para el proyecto
project_id  = "{project_id}"
region      = "{region}"
zone        = "{zona}"
environment = "{entorno if entorno else 'dev'}"
"""


def generar_readme(nombre_proyecto):
    """
    Genera el contenido del archivo README.md.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto
        
    Returns:
        str: Contenido del archivo README.md
    """
    return f"""# {nombre_proyecto.capitalize()} - Proyecto Terraform para GCP

Este directorio contiene la infraestructura como código (IaC) utilizando Terraform para el proyecto {nombre_proyecto} en Google Cloud Platform.

## Estructura del Proyecto

```
{nombre_proyecto}/
├── README.md                   # Documentación del proyecto
└── environments/               # Directorio de entornos
    ├── dev/                    # Entorno de desarrollo
    │   ├── backend.tf          # Configuración del backend de Terraform para dev
    │   ├── provider.tf         # Configuración del proveedor de GCP
    │   ├── variables.tf        # Definición de variables
    │   ├── outputs.tf          # Outputs del proyecto
    │   ├── main.tf             # Recursos principales y valores locales
    │   ├── terraform.tfvars    # Valores de las variables para dev
    │   └── [servicios].tf      # Configuraciones de servicios específicos
    │
    ├── staging/                # Entorno de pruebas
    │   ├── backend.tf          # Configuración del backend de Terraform para staging 
    │   ├── provider.tf         # Configuración del proveedor de GCP
    │   ├── variables.tf        # Definición de variables
    │   ├── outputs.tf          # Outputs del proyecto
    │   ├── main.tf             # Recursos principales y valores locales
    │   ├── terraform.tfvars    # Valores de las variables para staging
    │   └── [servicios].tf      # Configuraciones de servicios específicos
    │
    └── prod/                   # Entorno de producción
        ├── backend.tf          # Configuración del backend de Terraform para prod
        ├── provider.tf         # Configuración del proveedor de GCP
        ├── variables.tf        # Definición de variables
        ├── outputs.tf          # Outputs del proyecto
        ├── main.tf             # Recursos principales y valores locales
        ├── terraform.tfvars    # Valores de las variables para prod
        └── [servicios].tf      # Configuraciones de servicios específicos
```

## Inicialización y Despliegue

### Entorno de Desarrollo (Dev)

```bash
# Inicializar Terraform
cd environments/dev
terraform init

# Planificar cambios
terraform plan

# Aplicar cambios
terraform apply
```

### Entorno de Pruebas (Staging)

```bash
# Inicializar Terraform
cd environments/staging
terraform init

# Planificar cambios
terraform plan

# Aplicar cambios
terraform apply
```

### Entorno de Producción (Prod)

```bash
# Inicializar Terraform
cd environments/prod
terraform init

# Planificar cambios
terraform plan

# Aplicar cambios
terraform apply
```

## Servicios Configurados

El proyecto incluye la configuración de los siguientes servicios de GCP:

- Infrastructure Base (configuración básica en todos los entornos)

## Licencia

Este proyecto está bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork del repositorio y envía un pull request.
""" 