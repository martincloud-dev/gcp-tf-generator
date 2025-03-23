"""
Definiciones de servicios de GCP disponibles para generación.
"""

import os
from pathlib import Path

# Obtener la ruta base del paquete para acceder a las plantillas
BASE_DIR = Path(__file__).parent.parent

# Lista de servicios GCP disponibles
SERVICIOS_DISPONIBLES = [
    "compute-engine",
    "cloud-storage",
    "cloud-sql",
    "cloud-run",
    "bigquery",
    "kubernetes-engine",
    "cloud-functions",
    "load-balancer",
    "vpc",
    "iam",
    "firewall",
    "dns",
    "cloud-armor",
    "cdn",
    "cloud-nat",
    "ssl-certificate",
    "pubsub",
    "scheduler",
    "memorystore",
    "spanner",
    "dataflow",
    "app-engine",
    "cloud-build",
    "artifact-registry"
]

# Información detallada de cada servicio
SERVICIOS_INFO = {
    "compute-engine": {
        "descripcion": "Máquinas virtuales escalables en la infraestructura de Google",
        "archivo": "compute_engine.tf.tpl",
        "abreviatura": "ce"
    },
    "cloud-storage": {
        "descripcion": "Servicio de almacenamiento de objetos",
        "archivo": "cloud_storage.tf.tpl",
        "abreviatura": "cs"
    },
    "cloud-sql": {
        "descripcion": "Servicio de base de datos relacional totalmente gestionado",
        "archivo": "cloud_sql.tf.tpl",
        "abreviatura": "csql"
    },
    "cloud-run": {
        "descripcion": "Plataforma de computación serverless para contenedores",
        "archivo": "cloud_run.tf.tpl",
        "abreviatura": "cr"
    },
    "bigquery": {
        "descripcion": "Almacén de datos empresarial y servicio de análisis",
        "archivo": "bigquery.tf.tpl",
        "abreviatura": "bq"
    },
    "kubernetes-engine": {
        "descripcion": "Servicio Kubernetes gestionado y optimizado",
        "archivo": "kubernetes_engine.tf.tpl",
        "abreviatura": "gke"
    },
    "cloud-functions": {
        "descripcion": "Plataforma de ejecución de funciones serverless",
        "archivo": "cloud_functions.tf.tpl",
        "abreviatura": "cf"
    },
    "load-balancer": {
        "descripcion": "Balanceadores de carga HTTP(S), TCP/SSL y de red",
        "archivo": "load_balancer.tf.tpl",
        "abreviatura": "lb"
    },
    "vpc": {
        "descripcion": "Redes privadas virtuales definidas por software",
        "archivo": "vpc.tf.tpl",
        "abreviatura": "vpc"
    },
    "iam": {
        "descripcion": "Gestión de identidades y accesos",
        "archivo": "iam.tf.tpl",
        "abreviatura": "iam"
    },
    "firewall": {
        "descripcion": "Reglas de firewall para controlar el tráfico de red",
        "archivo": "firewall.tf.tpl",
        "abreviatura": "fw"
    },
    "dns": {
        "descripcion": "Servicio de resolución de nombres de dominio",
        "archivo": "dns.tf.tpl",
        "abreviatura": "dns"
    },
    "cloud-armor": {
        "descripcion": "Protección contra ataques DDoS y amenazas web",
        "archivo": "cloud_armor.tf.tpl",
        "abreviatura": "armor"
    },
    "cdn": {
        "descripcion": "Red de distribución de contenido",
        "archivo": "cdn.tf.tpl",
        "abreviatura": "cdn"
    },
    "cloud-nat": {
        "descripcion": "Traducción de direcciones de red para GCP",
        "archivo": "cloud_nat.tf.tpl",
        "abreviatura": "nat"
    },
    "ssl-certificate": {
        "descripcion": "Certificados SSL/TLS para balanceadores de carga",
        "archivo": "ssl_certificate.tf.tpl",
        "abreviatura": "ssl"
    },
    "pubsub": {
        "descripcion": "Servicio de mensajería en tiempo real para integraciones",
        "archivo": "pubsub.tf.tpl",
        "abreviatura": "ps"
    },
    "scheduler": {
        "descripcion": "Servicio para programar tareas y trabajos en la nube",
        "archivo": "scheduler.tf.tpl",
        "abreviatura": "sch"
    },
    "memorystore": {
        "descripcion": "Servicio de Redis y Memcached totalmente gestionado",
        "archivo": "memorystore.tf.tpl",
        "abreviatura": "mem"
    },
    "spanner": {
        "descripcion": "Base de datos relacional global y escalable",
        "archivo": "spanner.tf.tpl",
        "abreviatura": "spn"
    },
    "dataflow": {
        "descripcion": "Servicio para procesamiento de datos en tiempo real y por lotes",
        "archivo": "dataflow.tf.tpl",
        "abreviatura": "df"
    },
    "app-engine": {
        "descripcion": "Plataforma serverless para aplicaciones web y APIs",
        "archivo": "app_engine.tf.tpl",
        "abreviatura": "gae"
    },
    "cloud-build": {
        "descripcion": "Servicio de CI/CD para compilar, probar y desplegar",
        "archivo": "cloud_build.tf.tpl",
        "abreviatura": "cb"
    },
    "artifact-registry": {
        "descripcion": "Registro de artefactos para imágenes de contenedores y paquetes",
        "archivo": "artifact_registry.tf.tpl",
        "abreviatura": "ar"
    }
}

# Definición de servicios disponibles
SERVICIOS = {
    # COMPUTE ENGINE
    "compute-engine": {
        "nombre": "Compute Engine",
        "abreviatura": "ce",
        "template": """#=========================================================================#
#                          COMPUTE ENGINE VM                           #
#=========================================================================#
# Instancia de Compute Engine
resource "google_compute_instance" "vm" {
  name         = "${local.project_name}-vm"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 20
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    ssh-keys = "debian:ssh-rsa AAAA... user@example.com"
  }

  metadata_startup_script = "echo 'Hello, World!' > /var/www/html/index.html"

  tags = ["http-server", "https-server"]

  labels = local.labels
}

#=========================================================================#
#                          HTTP FIREWALL                          #
#=========================================================================#
# Firewall para permitir HTTP
resource "google_compute_firewall" "allow_http" {
  name    = "${local.project_name}-allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"]
}

#=========================================================================#
#                             OUTPUTS                             #
#=========================================================================#
# Outputs
output "vm_name" {
  value = google_compute_instance.vm.name
}

output "vm_external_ip" {
  value = google_compute_instance.vm.network_interface[0].access_config[0].nat_ip
}
"""
    },
    
    # CLOUD STORAGE
    "cloud-storage": {
        "nombre": "Cloud Storage",
        "abreviatura": "cs",
        "template": """#=========================================================================#
#                          CLOUD STORAGE                            #
#=========================================================================#
# Bucket de almacenamiento estándar
resource "google_storage_bucket" "storage" {
  name          = "${local.project_name}-storage"
  location      = "US"
  storage_class = "STANDARD"
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
  
  uniform_bucket_level_access = true
  
  labels = local.labels
}

#=========================================================================#
#                          BUCKET OBJECT                           #
#=========================================================================#
# Objeto en el bucket
resource "google_storage_bucket_object" "example" {
  name   = "example-object"
  bucket = google_storage_bucket.storage.name
  source = "path/to/local/file" # Reemplazar con la ruta del archivo
  
  content_type = "text/plain"
  
  # Para contenido en lugar de archivo
  # content = "Este es el contenido del objeto"
}

#=========================================================================#
#                           IAM POLICY                            #
#=========================================================================#
# Política de IAM para el bucket
resource "google_storage_bucket_iam_binding" "binding" {
  bucket = google_storage_bucket.storage.name
  role   = "roles/storage.objectViewer"
  
  members = [
    "allUsers", # Acceso público
  ]
}

#=========================================================================#
#                             OUTPUTS                             #
#=========================================================================#
# Outputs
output "bucket_name" {
  value = google_storage_bucket.storage.name
}

output "bucket_url" {
  value = google_storage_bucket.storage.url
}
"""
    },
    
    # LOAD BALANCER
    "load-balancer": {
        "nombre": "Load Balancer",
        "abreviatura": "lb",
        "template": """#=========================================================================#
#                          LOAD BALANCER                            #
#=========================================================================#
# Grupo de instancias para el backend
resource "google_compute_instance_group" "webservers" {
  name        = "${local.project_name}-webservers"
  description = "Grupo de instancias para el balanceador de carga"
  zone        = var.zone
  
  # Referencia a instancias existentes
  # instances = [google_compute_instance.vm.id]
  
  named_port {
    name = "http"
    port = 80
  }
  
  named_port {
    name = "https"
    port = 443
  }
}

#=========================================================================#
#                          HEALTH CHECK                            #
#=========================================================================#
# Health check
resource "google_compute_health_check" "http_health_check" {
  name               = "${local.project_name}-http-health-check"
  timeout_sec        = 5
  check_interval_sec = 10
  
  http_health_check {
    port         = 80
    request_path = "/health"
  }
}

#=========================================================================#
#                        BACKEND SERVICE                          #
#=========================================================================#
# Backend service
resource "google_compute_backend_service" "backend" {
  name          = "${local.project_name}-backend-service"
  protocol      = "HTTP"
  port_name     = "http"
  timeout_sec   = 10
  health_checks = [google_compute_health_check.http_health_check.id]
  
  backend {
    group = google_compute_instance_group.webservers.id
  }
}

#=========================================================================#
#                             URL MAP                             #
#=========================================================================#
# URL map
resource "google_compute_url_map" "url_map" {
  name            = "${local.project_name}-url-map"
  default_service = google_compute_backend_service.backend.id
  
  host_rule {
    hosts        = ["*"]
    path_matcher = "main"
  }
  
  path_matcher {
    name            = "main"
    default_service = google_compute_backend_service.backend.id
    
    path_rule {
      paths   = ["/api/*"]
      service = google_compute_backend_service.backend.id
    }
  }
}

#=========================================================================#
#                        SSL CERTIFICATE                          #
#=========================================================================#
# Certificado SSL gestionado
resource "google_compute_managed_ssl_certificate" "managed" {
  name = "${local.project_name}-ssl-cert"
  
  managed {
    domains = ["example.com", "www.example.com"]
  }
}

#=========================================================================#
#                          HTTPS PROXY                            #
#=========================================================================#
# Proxy HTTPS
resource "google_compute_target_https_proxy" "https_proxy" {
  name             = "${local.project_name}-https-proxy"
  url_map          = google_compute_url_map.url_map.id
  ssl_certificates = [google_compute_managed_ssl_certificate.managed.id]
}

#=========================================================================#
#                        FORWARDING RULES                         #
#=========================================================================#
# Regla de reenvío HTTPS
resource "google_compute_global_forwarding_rule" "https" {
  name       = "${local.project_name}-https-lb"
  target     = google_compute_target_https_proxy.https_proxy.id
  port_range = "443"
  ip_protocol = "TCP"
}

#=========================================================================#
#                     HTTP TO HTTPS REDIRECT                      #
#=========================================================================#
# Redirección HTTP a HTTPS
resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "${local.project_name}-http-proxy"
  url_map = google_compute_url_map.url_map.id
}

resource "google_compute_global_forwarding_rule" "http" {
  name       = "${local.project_name}-http-lb"
  target     = google_compute_target_http_proxy.http_proxy.id
  port_range = "80"
  ip_protocol = "TCP"
}

#=========================================================================#
#                             OUTPUTS                             #
#=========================================================================#
# Outputs
output "load_balancer_ip" {
  value = google_compute_global_forwarding_rule.https.ip_address
}

output "managed_cert_name" {
  value = google_compute_managed_ssl_certificate.managed.name
}
"""
    },
    
    # FIREWALL
    "firewall": {
        "nombre": "Firewall",
        "abreviatura": "fw",
        "template": """#=========================================================================#
#                         FIREWALL RULES                           #
#=========================================================================#
# Regla para permitir SSH
resource "google_compute_firewall" "allow_ssh" {
  name    = "${local.project_name}-allow-ssh"
  network = "default"
  
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  
  source_ranges = ["0.0.0.0/0"] # Considere restringir a rangos específicos
  description   = "Permite SSH desde Internet"
}

#=========================================================================#
#                         HTTPS ACCESS                            #
#=========================================================================#
# Regla para permitir HTTPS
resource "google_compute_firewall" "allow_https" {
  name    = "${local.project_name}-allow-https"
  network = "default"
  
  allow {
    protocol = "tcp"
    ports    = ["443"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  description   = "Permite HTTPS desde Internet"
}

#=========================================================================#
#                       INTERNAL TRAFFIC                          #
#=========================================================================#
# Regla para permitir tráfico interno
resource "google_compute_firewall" "allow_internal" {
  name    = "${local.project_name}-allow-internal"
  network = "default"
  
  allow {
    protocol = "icmp"
  }
  
  allow {
    protocol = "tcp"
  }
  
  allow {
    protocol = "udp"
  }
  
  source_ranges = ["10.0.0.0/8"]
  description   = "Permite todo el tráfico interno"
}

#=========================================================================#
#                         BLOCK TRAFFIC                           #
#=========================================================================#
# Regla para bloquear tráfico específico
resource "google_compute_firewall" "deny_specific" {
  name    = "${local.project_name}-deny-specific"
  network = "default"
  
  deny {
    protocol = "tcp"
    ports    = ["135", "137-139", "445"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  description   = "Deniega puertos específicos desde Internet"
  priority      = 1000
}

#=========================================================================#
#                             OUTPUTS                             #
#=========================================================================#
# Outputs
output "firewall_rules" {
  value = [
    google_compute_firewall.allow_ssh.name,
    google_compute_firewall.allow_https.name,
    google_compute_firewall.allow_internal.name,
    google_compute_firewall.deny_specific.name
  ]
}
"""
    },
    
    # PUBSUB
    "pubsub": {
        "nombre": "Cloud Pub/Sub",
        "abreviatura": "ps",
        "template": """################################################
################## CLOUD PUB/SUB ##################
################################################
# Tema de Pub/Sub
resource "google_pubsub_topic" "topic" {
  name = "${local.project_name}-topic"
  
  labels = local.labels
  
  message_retention_duration = "86600s"  # 24 horas
}

################################################
################ PUBSUB SUBSCRIPTION ##############
################################################
# Suscripción al tema
resource "google_pubsub_subscription" "subscription" {
  name  = "${local.project_name}-subscription"
  topic = google_pubsub_topic.topic.name
  
  ack_deadline_seconds = 20
  
  message_retention_duration = "604800s"  # 7 días
  
  expiration_policy {
    ttl = "2592000s"  # 30 días
  }
  
  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
  
  enable_message_ordering = false
  
  labels = local.labels
}

################################################
################### DEAD LETTER ###################
################################################
# Tema para dead letter (mensajes fallidos)
resource "google_pubsub_topic" "dead_letter" {
  name = "${local.project_name}-dead-letter"
  
  labels = local.labels
}

# Configuración de Dead Letter para la suscripción
resource "google_pubsub_subscription" "subscription_with_dl" {
  name  = "${local.project_name}-subscription-with-dl"
  topic = google_pubsub_topic.topic.name
  
  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dead_letter.id
    max_delivery_attempts = 5
  }
  
  labels = local.labels
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "pubsub_topic_id" {
  value = google_pubsub_topic.topic.id
}

output "pubsub_subscription_id" {
  value = google_pubsub_subscription.subscription.id
}
"""
    },
    
    # SCHEDULER
    "scheduler": {
        "nombre": "Cloud Scheduler",
        "abreviatura": "sch",
        "template": """################################################
################## CLOUD SCHEDULER ##################
################################################
# Trabajo de Cloud Scheduler con destino HTTP
resource "google_cloud_scheduler_job" "http_job" {
  name             = "${local.project_name}-http-job"
  description      = "Trabajo programado con destino HTTP"
  schedule         = "0 */3 * * *"  # Cada 3 horas
  time_zone        = "America/Los_Angeles"
  attempt_deadline = "320s"
  
  http_target {
    uri         = "https://example.com/api/task"
    http_method = "POST"
    
    headers = {
      "Content-Type" = "application/json"
    }
    
    body = base64encode(jsonencode({
      action = "process",
      data   = "example"
    }))
    
    oauth_token {
      service_account_email = "service-account@${var.project_id}.iam.gserviceaccount.com"
    }
  }
}

################################################
################ PUBSUB SCHEDULER ################
################################################
# Trabajo de Cloud Scheduler con destino Pub/Sub
resource "google_cloud_scheduler_job" "pubsub_job" {
  name             = "${local.project_name}-pubsub-job"
  description      = "Trabajo programado con destino Pub/Sub"
  schedule         = "0 0 * * *"  # Cada día a medianoche
  time_zone        = "UTC"
  attempt_deadline = "320s"
  
  pubsub_target {
    topic_name = "projects/${var.project_id}/topics/example-topic"
    data       = base64encode("Datos de mensaje programado")
  }
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "scheduler_http_job_name" {
  value = google_cloud_scheduler_job.http_job.name
}

output "scheduler_pubsub_job_name" {
  value = google_cloud_scheduler_job.pubsub_job.name
}
"""
    },
    
    # MEMORYSTORE
    "memorystore": {
        "nombre": "Memorystore",
        "abreviatura": "mem",
        "template": """################################################
################## MEMORYSTORE REDIS ##################
################################################
# Instancia de Redis
resource "google_redis_instance" "redis" {
  name           = "${local.project_name}-redis"
  tier           = "STANDARD_HA"
  memory_size_gb = 1
  
  region             = var.region
  location_id        = var.zone
  alternative_location_id = "us-central1-b"
  
  redis_version     = "REDIS_6_X"
  display_name      = "Instancia Redis para ${local.project_name}"
  redis_configs     = {
    "maxmemory-policy" = "allkeys-lru"
  }
  
  auth_enabled      = true
  transit_encryption_mode = "SERVER_AUTHENTICATION"
  
  maintenance_policy {
    weekly_maintenance_window {
      day = "TUESDAY"
      start_time {
        hours   = 0
        minutes = 30
      }
    }
  }
  
  labels = local.labels
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "redis_host" {
  value = google_redis_instance.redis.host
}

output "redis_port" {
  value = google_redis_instance.redis.port
}

output "redis_current_location_id" {
  value = google_redis_instance.redis.current_location_id
}
"""
    },
    
    # SPANNER
    "spanner": {
        "nombre": "Cloud Spanner",
        "abreviatura": "spn",
        "template": """################################################
################## CLOUD SPANNER ##################
################################################
# Instancia de Spanner
resource "google_spanner_instance" "instance" {
  name          = "${local.project_name}-spanner"
  config        = "regional-us-central1"
  display_name  = "Instancia Spanner para ${local.project_name}"
  processing_units = 100  # 1000 processing units = 1 node
  
  labels = local.labels
}

################################################
################## SPANNER DATABASE ##################
################################################
# Base de datos Spanner
resource "google_spanner_database" "database" {
  instance = google_spanner_instance.instance.name
  name     = "${local.project_name}-db"
  
  deletion_protection = false  # Para entornos de producción, establecer en true
  
  ddl = [
    "CREATE TABLE Users (UserId INT64 NOT NULL, Name STRING(100), Email STRING(100)) PRIMARY KEY(UserId)",
    "CREATE TABLE Posts (PostId INT64 NOT NULL, UserId INT64 NOT NULL, Title STRING(200), Content STRING(MAX)) PRIMARY KEY(PostId)",
    "CREATE INDEX PostsByUser ON Posts(UserId)"
  ]
  
  version_retention_period = "3d"
  
  encryption_config {
    kms_key_name = null  # Usar clave de google gestionada, para CMEK especificar la clave
  }
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "spanner_instance_id" {
  value = google_spanner_instance.instance.id
}

output "spanner_database_id" {
  value = google_spanner_database.database.id
}
"""
    },
    
    # DATAFLOW
    "dataflow": {
        "nombre": "Dataflow",
        "abreviatura": "df",
        "template": """################################################
################## DATAFLOW JOB ##################
################################################
# Job de Dataflow
resource "google_dataflow_job" "batch_job" {
  name              = "${local.project_name}-dataflow-job"
  template_gcs_path = "gs://dataflow-templates/latest/Word_Count"
  temp_gcs_location = "gs://${local.project_name}-dataflow-tmp"
  
  parameters = {
    inputFile = "gs://dataflow-samples/shakespeare/kinglear.txt"
    output    = "gs://${local.project_name}-dataflow-output/wordcount"
  }
  
  service_account_email = "service-account@${var.project_id}.iam.gserviceaccount.com"
  
  max_workers        = 5
  on_delete          = "cancel"
  region             = var.region
  zone               = var.zone
  machine_type       = "n1-standard-2"
  
  labels = local.labels
}

################################################
############## SERVICE ACCOUNT SETUP ##############
################################################
# Cuenta de servicio para Dataflow
resource "google_service_account" "dataflow_sa" {
  account_id   = "${local.project_name}-dataflow-sa"
  display_name = "Cuenta de servicio para Dataflow"
}

# Permisos para la cuenta de servicio
resource "google_project_iam_member" "dataflow_worker" {
  project = var.project_id
  role    = "roles/dataflow.worker"
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}

resource "google_project_iam_member" "storage_object_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "dataflow_job_id" {
  value = google_dataflow_job.batch_job.id
}

output "dataflow_job_state" {
  value = google_dataflow_job.batch_job.state
}

output "dataflow_service_account" {
  value = google_service_account.dataflow_sa.email
}
"""
    },
    
    # APP ENGINE
    "app-engine": {
        "nombre": "App Engine",
        "abreviatura": "gae",
        "template": """################################################
################## APP ENGINE ##################
################################################
# Aplicación de App Engine
resource "google_app_engine_application" "app" {
  project     = var.project_id
  location_id = "us-central"  # Ubicación de la app (no se puede cambiar después de crear)
  
  database_type = "CLOUD_FIRESTORE"
  
  # Usar feature_settings para habilitar ciertas características
  feature_settings {
    split_health_checks = true
  }
}

################################################
############### APP ENGINE VERSION ###############
################################################
# Versión de App Engine
resource "google_app_engine_standard_app_version" "default" {
  version_id = "v1"
  service    = "default"
  runtime    = "python39"
  
  entrypoint {
    shell = "gunicorn -b :$PORT main:app"
  }
  
  deployment {
    zip {
      source_url = "https://storage.googleapis.com/${google_storage_bucket.app_bucket.name}/${google_storage_bucket_object.app_zip.name}"
    }
  }
  
  env_variables = {
    ENVIRONMENT = var.environment
    DEBUG       = "false"
  }
  
  automatic_scaling {
    max_concurrent_requests = 50
    min_idle_instances = 0
    max_idle_instances = 2
    min_pending_latency = "1s"
    max_pending_latency = "5s"
  }
  
  delete_service_on_destroy = false
  
  noop_on_destroy = true
}

################################################
############### STORAGE FOR APP ################
################################################
# Bucket para almacenar el código de la aplicación
resource "google_storage_bucket" "app_bucket" {
  name          = "${local.project_name}-app-bucket"
  location      = "US"
  force_destroy = true
  
  versioning {
    enabled = true
  }
  
  labels = local.labels
}

resource "google_storage_bucket_object" "app_zip" {
  name   = "app-${formatdate("YYYYMMDDhhmmss", timestamp())}.zip"
  bucket = google_storage_bucket.app_bucket.name
  source = "path/to/source.zip"  # Reemplazar con la ruta del archivo zip
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "app_engine_url" {
  value = "https://${var.project_id}.appspot.com"
}

output "app_bucket_name" {
  value = google_storage_bucket.app_bucket.name
}
"""
    },
    
    # CLOUD BUILD
    "cloud-build": {
        "nombre": "Cloud Build",
        "abreviatura": "cb",
        "template": """################################################
################## CLOUD BUILD ##################
################################################
# Disparador de Cloud Build
resource "google_cloudbuild_trigger" "git_trigger" {
  name        = "${local.project_name}-build-trigger"
  description = "Disparador de build para ${local.project_name}"
  
  github {
    owner = "github-owner"
    name  = "github-repo"
    push {
      branch = "^main$"
    }
  }
  
  included_files = ["**/*.tf"]
  
  filename = "cloudbuild.yaml"  # Usar archivo de configuración dentro del repo
  
  # O definir los pasos directamente:
  build {
    step {
      name = "gcr.io/cloud-builders/docker"
      args = ["build", "-t", "gcr.io/${var.project_id}/${local.project_name}", "."]
    }
    
    step {
      name = "gcr.io/cloud-builders/docker"
      args = ["push", "gcr.io/${var.project_id}/${local.project_name}"]
    }
    
    step {
      name = "gcr.io/google.com/cloudsdktool/cloud-sdk"
      entrypoint = "gcloud"
      args = [
        "run", "deploy", "${local.project_name}-service",
        "--image", "gcr.io/${var.project_id}/${local.project_name}",
        "--region", var.region,
        "--platform", "managed",
        "--allow-unauthenticated"
      ]
    }
    
    tags = ["${local.project_name}", "build"]
    
    timeout = "900s"
  }
  
  tags = local.labels
}

################################################
############# SERVICE ACCOUNT SETUP #############
################################################
# Cuenta de servicio para Cloud Build
resource "google_service_account" "cloudbuild_sa" {
  account_id   = "${local.project_name}-cloudbuild-sa"
  display_name = "Cuenta de servicio para Cloud Build"
}

# Permisos para la cuenta de servicio
resource "google_project_iam_member" "cloudbuild_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}

resource "google_project_iam_member" "cloudbuild_storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "cloudbuild_trigger_id" {
  value = google_cloudbuild_trigger.git_trigger.id
}

output "cloudbuild_service_account" {
  value = google_service_account.cloudbuild_sa.email
}
"""
    },
    
    # ARTIFACT REGISTRY
    "artifact-registry": {
        "nombre": "Artifact Registry",
        "abreviatura": "ar",
        "template": """################################################
################# ARTIFACT REGISTRY #################
################################################
# Repositorio de Artifact Registry
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "${local.project_name}-repo"
  description   = "Repositorio de ${local.project_name} para imágenes de Docker"
  format        = "DOCKER"
  
  # Políticas de limpieza para la gestión del ciclo de vida
  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    condition {
      tag_state    = "TAGGED"
      tag_prefixes = ["release", "stable"]
      older_than   = "2592000s"  # 30 días
    }
  }
  
  cleanup_policies {
    id     = "delete-old-versions"
    action = "DELETE"
    condition {
      tag_state  = "UNTAGGED"
      older_than = "604800s"  # 7 días
    }
  }
  
  labels = local.labels
}

################################################
################## IAM POLICY ##################
################################################
# Política de IAM para el repositorio
resource "google_artifact_registry_repository_iam_member" "repo_admin" {
  project    = var.project_id
  location   = google_artifact_registry_repository.repo.location
  repository = google_artifact_registry_repository.repo.name
  role       = "roles/artifactregistry.repoAdmin"
  member     = "serviceAccount:${var.project_id}@cloudbuild.gserviceaccount.com"
}

resource "google_artifact_registry_repository_iam_member" "repo_reader" {
  project    = var.project_id
  location   = google_artifact_registry_repository.repo.location
  repository = google_artifact_registry_repository.repo.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${var.project_id}-compute@developer.gserviceaccount.com"
}

################################################
##################### OUTPUTS #####################
################################################
# Outputs
output "artifact_registry_repository_id" {
  value = google_artifact_registry_repository.repo.id
}

output "artifact_registry_repository_url" {
  value = "${google_artifact_registry_repository.repo.location}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}"
}
"""
    },
    
    # IAM
    "iam": {
        "nombre": "Identity and Access Management",
        "abreviatura": "iam",
        "template": """#=========================================================================#
#                    IDENTITY AND ACCESS MANAGEMENT                   #
#=========================================================================#
# Cuenta de servicio
resource "google_service_account" "service_account" {
  account_id   = "${local.project_name}-sa"
  display_name = "Cuenta de servicio para ${local.project_name}"
  description  = "Cuenta de servicio para acceso a recursos de GCP"
}

#=========================================================================#
#                       PROJECT IAM BINDINGS                       #
#=========================================================================#
# Asignación de roles a nivel de proyecto
resource "google_project_iam_member" "project_iam" {
  project = var.project_id
  role    = "roles/viewer"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

# Asignación de roles específicos
resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_project_iam_member" "logging_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

#=========================================================================#
#                      CUSTOM IAM ROLE                           #
#=========================================================================#
# Rol personalizado a nivel de proyecto
resource "google_project_iam_custom_role" "custom_role" {
  role_id     = "${replace(local.project_name, "-", "_")}_custom_role"
  title       = "${local.project_name} Custom Role"
  description = "Rol personalizado para ${local.project_name} con permisos específicos"
  permissions = [
    "storage.buckets.get",
    "storage.objects.get",
    "storage.objects.list",
    "compute.instances.get",
    "compute.instances.list"
  ]
}

# Asignación de rol personalizado
resource "google_project_iam_member" "custom_role_binding" {
  project = var.project_id
  role    = google_project_iam_custom_role.custom_role.id
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

#=========================================================================#
#                             OUTPUTS                             #
#=========================================================================#
# Outputs
output "service_account_email" {
  value = google_service_account.service_account.email
}

output "custom_role_id" {
  value = google_project_iam_custom_role.custom_role.id
}
"""
    },
    
    # VPC
    "vpc": {
        "nombre": "Virtual Private Cloud",
        "abreviatura": "vpc",
        "template": """#=========================================================================#
#                     VIRTUAL PRIVATE CLOUD (VPC)                    #
#=========================================================================#
# Red VPC principal
resource "google_compute_network" "vpc" {
  name                    = "${local.project_name}-vpc"
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
  description             = "Red VPC principal para ${local.project_name}"
}

#=========================================================================#
#                           SUBNETS                              #
#=========================================================================#
# Subred en la región primaria
resource "google_compute_subnetwork" "subnet_primary" {
  name          = "${local.project_name}-subnet-primary"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
  
  private_ip_google_access = true
  
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
  
  secondary_ip_range {
    range_name    = "services-range"
    ip_cidr_range = "10.0.1.0/24"
  }
  
  secondary_ip_range {
    range_name    = "pods-range"
    ip_cidr_range = "10.0.2.0/24"
  }
}

# Subred en la región secundaria
resource "google_compute_subnetwork" "subnet_secondary" {
  name          = "${local.project_name}-subnet-secondary"
  ip_cidr_range = "10.1.0.0/24"
  region        = "us-east1"  # Ajustar según necesidad
  network       = google_compute_network.vpc.id
  
  private_ip_google_access = true
}

#=========================================================================#
#                       CLOUD ROUTER & NAT                        #
#=========================================================================#
# Cloud Router para NAT
resource "google_compute_router" "router" {
  name    = "${local.project_name}-router"
  region  = var.region
  network = google_compute_network.vpc.id
  
  bgp {
    asn = 64514
  }
}

# Cloud NAT
resource "google_compute_router_nat" "nat" {
  name                               = "${local.project_name}-nat"
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  
  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

#=========================================================================#
#                       FIREWALL RULES                           #
#=========================================================================#
# Regla para tráfico interno
resource "google_compute_firewall" "allow_internal" {
  name    = "${local.project_name}-allow-internal"
  network = google_compute_network.vpc.id
  
  allow {
    protocol = "tcp"
  }
  
  allow {
    protocol = "udp"
  }
  
  allow {
    protocol = "icmp"
  }
  
  source_ranges = ["10.0.0.0/16", "10.1.0.0/16"]
  description   = "Permite tráfico interno entre subredes"
}

# Regla para SSH bastion host
resource "google_compute_firewall" "allow_ssh_bastion" {
  name    = "${local.project_name}-allow-ssh-bastion"
  network = google_compute_network.vpc.id
  
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  
  source_ranges = ["35.235.240.0/20"]  # Rango de Cloud IAP para SSH
  target_tags   = ["bastion"]
  description   = "Permite SSH desde Cloud IAP"
}

#=========================================================================#
#                             OUTPUTS                             #
#=========================================================================#
# Outputs
output "vpc_id" {
  value = google_compute_network.vpc.id
}

output "subnet_primary_id" {
  value = google_compute_subnetwork.subnet_primary.id
}

output "subnet_secondary_id" {
  value = google_compute_subnetwork.subnet_secondary.id
}

output "nat_ip" {
  value = google_compute_router_nat.nat.nat_ips
}
"""
    }
}


def listar_servicios():
    """
    Devuelve la información de todos los servicios disponibles.
    
    Returns:
        list: Lista de diccionarios con la información de cada servicio
    """
    servicios = []
    for clave, info in SERVICIOS.items():
        servicios.append({
            "nombre": info["nombre"],
            "abreviatura": info["abreviatura"],
            "id": clave
        })
    return servicios


def obtener_servicio_template(servicio_id):
    """
    Obtiene la plantilla de un servicio por su ID.
    
    Args:
        servicio_id (str): ID del servicio
        
    Returns:
        str: Plantilla del servicio o None si no existe
    """
    if servicio_id in SERVICIOS:
        return SERVICIOS[servicio_id]["template"]
    return None


def obtener_servicio_por_abreviatura(abreviatura):
    """
    Obtiene el ID de un servicio por su abreviatura.
    
    Args:
        abreviatura (str): Abreviatura del servicio
        
    Returns:
        str: ID del servicio o None si no existe
    """
    for servicio_id, info in SERVICIOS.items():
        if info["abreviatura"] == abreviatura:
            return servicio_id
    return None
