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
    Diseño minimalista y profesional. Lista ordenada alfabéticamente.
    """
    import shutil
    
    # Obtener el ancho de la terminal
    ancho_terminal = shutil.get_terminal_size().columns
    
    # Definir caracteres para el diseño minimalista
    simbolo_servicio = "•"
    
    # Imprimir encabezado elegante
    typer.echo("\n" + "─" * ancho_terminal)
    titulo = "SERVICIOS GCP DISPONIBLES"
    padding = (ancho_terminal - len(titulo)) // 2
    typer.echo(" " * padding + f"{Style.BRIGHT}{Fore.WHITE}{titulo}{Style.RESET_ALL}")
    typer.echo("─" * ancho_terminal)
    
    # Preparar lista de servicios ordenada alfabéticamente
    servicios_ordenados = [(nombre, abrev) for nombre, abrev, _ in sorted(servicios_disponibles, key=lambda x: x[0])]
    
    # Determinar anchos para formato uniforme
    ancho_servicio = max([len(nombre) for nombre, _ in servicios_ordenados]) + 2
    ancho_abrev = max([len(abrev) for _, abrev in servicios_ordenados]) + 2
    
    # Determinar número óptimo de columnas
    ancho_elemento = ancho_servicio + ancho_abrev + 10  # Espacio para símbolos y márgenes
    num_columnas = max(1, min(3, ancho_terminal // ancho_elemento))
    
    # Calcular elementos por columna para distribución equilibrada
    servicios_por_columna = (len(servicios_ordenados) + num_columnas - 1) // num_columnas
    
    # Espacio antes de la lista
    typer.echo("")
    
    # Imprimir servicios en formato de columnas
    for i in range(servicios_por_columna):
        linea = "    "
        for j in range(num_columnas):
            idx = i + j * servicios_por_columna
            if idx < len(servicios_ordenados):
                nombre, abrev = servicios_ordenados[idx]
                elemento = f"{Fore.WHITE}{nombre.ljust(ancho_servicio)}{Style.RESET_ALL}{Fore.CYAN}({abrev}){Style.RESET_ALL}"
                if j < num_columnas - 1 and idx < len(servicios_ordenados) - 1:
                    elemento = elemento.ljust(ancho_elemento + 20)  # +20 para códigos de color
                linea += f"{simbolo_servicio} {elemento}  "
        typer.echo(linea)
    
    # Línea separadora
    typer.echo("\n" + "─" * ancho_terminal)
    
    # Información de uso
    typer.echo(f"\n{Style.BRIGHT}Uso:{Style.RESET_ALL}")
    typer.echo(f"  tf-gcp create <nombre> --destino <ruta> --svc \"<abr1>,<abr2>,...\"")
    typer.echo(f"  tf-gcp add <ruta-proyecto> --svc \"<abr1>,<abr2>,...\"")
    
    # Ejemplos
    typer.echo(f"\n{Style.BRIGHT}Ejemplos:{Style.RESET_ALL}")
    typer.echo(f"  tf-gcp create mi-proyecto --destino ./proyectos --svc \"cs,lb,vpc\"")
    typer.echo(f"  tf-gcp add ./mi-proyecto --svc \"iam,fw\"\n")

if __name__ == "__main__":
    app() 