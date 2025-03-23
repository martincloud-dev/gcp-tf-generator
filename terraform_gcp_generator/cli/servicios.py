from colorama import Fore, Style, Back
import os
import typer

# Lista de servicios disponibles con sus abreviaturas
servicios_disponibles = [
    # Computación
    ("compute-engine", "ce", "Máquinas virtuales escalables en la infraestructura de Google"),
    ("kubernetes-engine", "gke", "Servicio gestionado y optimizado de Kubernetes"),
    ("cloud-run", "run", "Plataforma de cómputo serverless para contenedores"),
    ("cloud-functions", "cf", "Plataforma serverless para ejecución de funciones"),
    ("app-engine", "gae", "Plataforma serverless para aplicaciones web y APIs"),

    # Almacenamiento
    ("cloud-storage", "cs", "Servicio de almacenamiento de objetos"),
    ("cloud-sql", "sql", "Servicio totalmente gestionado de bases de datos relacionales"),
    ("bigquery", "bq", "Servicio de almacenamiento de datos y análisis empresarial"),
    ("spanner", "spn", "Base de datos relacional global y escalable"),
    ("memorystore", "mem", "Servicio de Redis y Memcached totalmente gestionado"),

    # Red
    ("load-balancer", "lb", "Balanceadores de carga HTTP(S), TCP/SSL y de red"),
    ("vpc", "vpc", "Redes privadas virtuales definidas por software"),
    ("firewall", "fw", "Reglas de firewall para controlar el tráfico de red"),
    ("dns", "dns", "Servicio de nombres de dominio gestionado"),
    ("cloud-armor", "armor", "Servicio de protección contra DDoS y ataques web"),
    ("cdn", "cdn", "Red de distribución de contenido"),
    ("cloud-nat", "nat", "Servicio de traducción de direcciones de red"),
    ("ssl-certificate", "ssl", "Certificados SSL gestionados para aplicaciones web"),

    # Mensajería y Orquestación
    ("pubsub", "ps", "Servicio de mensajería en tiempo real para integraciones"),
    ("scheduler", "sch", "Servicio para programar tareas y trabajos en la nube"),

    # Procesamiento de Datos
    ("dataflow", "df", "Servicio para procesamiento de datos en tiempo real y por lotes"),
    
    # DevOps y CI/CD
    ("cloud-build", "cb", "Servicio de CI/CD para compilar, probar y desplegar"),
    ("artifact-registry", "ar", "Registro de artefactos para imágenes de contenedores y paquetes"),

    # IAM y Seguridad
    ("iam", "iam", "Gestión de identidades y accesos"),
]

def listar_servicios():
    """
    Devuelve un diccionario con los servicios disponibles
    """
    servicios = {}
    for nombre, abrev, descripcion in servicios_disponibles:
        servicios[nombre] = {
            'abreviatura': abrev,
            'descripcion': descripcion
        }
    return servicios

def encontrar_servicio_por_abreviatura(abreviatura):
    """
    Encuentra el nombre completo de un servicio por su abreviatura.
    
    Args:
        abreviatura (str): Abreviatura o nombre completo del servicio
        
    Returns:
        str: Nombre completo del servicio o None si no se encuentra
    """
    for nombre, abrev, _ in servicios_disponibles:
        if abreviatura == abrev or abreviatura == nombre:
            return nombre
    return None

app = typer.Typer(help="Administrar servicios de Terraform para GCP")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Muestra los servicios disponibles para Terraform en GCP.
    """
    if ctx.invoked_subcommand is None:
        mostrar_servicios()

def mostrar_servicios():
    """
    Muestra en pantalla los servicios disponibles con sus abreviaturas.
    """
    typer.echo(f"{Fore.BLUE}Servicios disponibles:{Style.RESET_ALL}")
    
    # Agrupar por categorías
    categorias = {
        "Computación": ["compute-engine", "kubernetes-engine", "cloud-run", "cloud-functions", "app-engine"],
        "Almacenamiento": ["cloud-storage", "cloud-sql", "bigquery", "spanner", "memorystore"],
        "Red": ["load-balancer", "vpc", "firewall", "dns", "cloud-armor", "cdn", "cloud-nat", "ssl-certificate"],
        "Mensajería y Orquestación": ["pubsub", "scheduler"],
        "Procesamiento de Datos": ["dataflow"],
        "DevOps y CI/CD": ["cloud-build", "artifact-registry"],
        "IAM y Seguridad": ["iam"]
    }
    
    for categoria, servicios_cat in categorias.items():
        typer.echo(f"\n{Fore.YELLOW}{categoria}:{Style.RESET_ALL}")
        for servicio in servicios_disponibles:
            if servicio[0] in servicios_cat:
                typer.echo(f"  {Fore.GREEN}{servicio[0]}{Style.RESET_ALL} ({Fore.CYAN}{servicio[1]}{Style.RESET_ALL})")

if __name__ == "__main__":
    app() 