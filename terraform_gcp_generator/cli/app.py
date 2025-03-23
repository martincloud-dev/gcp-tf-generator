"""
Aplicación CLI principal para la generación de proyectos Terraform.
"""

import os
import sys
import typer
from typing import Optional, List
from colorama import Fore, Style, Back
from ..utils.project import crear_proyecto, añadir_servicio
from .servicios import servicios_disponibles, encontrar_servicio_por_abreviatura, mostrar_servicios

app = typer.Typer(help="Crear y gestionar proyectos Terraform para GCP")


@app.command()
def create(
    name: str,
    destino: str = typer.Option(
        None,
        "--destino",
        "-d",
        help="Directorio donde se creará el proyecto"
    ),
    region: str = typer.Option(
        "us-central1",
        "--region",
        "-r",
        help="Región de GCP donde se desplegarán los recursos"
    ),
    zona: str = typer.Option(
        "us-central1-a",
        "--zona",
        "-z",
        help="Zona de GCP donde se desplegarán los recursos"
    ),
    svc: List[str] = typer.Option(
        None,
        "--servicios",
        "--svc",
        help="Servicios de GCP para agregar al proyecto (separados por comas o múltiples flags)"
    )
):
    """
    Crea un nuevo proyecto de Terraform para GCP con los servicios especificados.
    """
    try:
        servicios_normalizados = []
        if svc:
            for item in svc:
                # Manejar valores separados por comas
                for s in item.split(','):
                    s = s.strip()
                    if s:  # Solo procesa si no está vacío
                        servicio_normalizado = encontrar_servicio_por_abreviatura(s)
                        if servicio_normalizado:
                            servicios_normalizados.append(servicio_normalizado)
                        else:
                            typer.echo(f"Servicio no reconocido: {s}")
                            return
        
        # Si no hay destino especificado, usar el directorio actual
        if not destino:
            typer.echo("Error: Debe especificar un directorio de destino con --destino")
            return
        
        # Crear el proyecto
        ruta_proyecto = crear_proyecto(name, destino, region, zona)
        
        # Añadir servicios si se especificaron
        servicios_añadidos = []
        for servicio in servicios_normalizados:
            añadir_servicio(ruta_proyecto, servicio)
            servicios_añadidos.append(servicio)
        
        # Actualizar README.md con la lista de servicios configurados
        if servicios_añadidos:
            actualizar_readme_con_servicios(os.path.join(ruta_proyecto, "README.md"), servicios_añadidos)
        
        typer.echo(f"✓ Proyecto '{name}' creado en {ruta_proyecto}")
        typer.echo(f"✓ Entornos creados: dev, staging, prod")
        for servicio in servicios_añadidos:
            typer.echo(f"✓ Servicio {servicio} añadido a todos los entornos: dev, staging, prod")
        typer.echo(f"\nPara inicializar el proyecto:")
        typer.echo(f"  cd {os.path.join(ruta_proyecto, 'environments/dev')}")
        typer.echo(f"  terraform init")
        
    except Exception as e:
        typer.echo(f"Error al crear el proyecto: {str(e)}")

# Función para actualizar el README con la lista de servicios
def actualizar_readme_con_servicios(readme_path, servicios):
    """
    Actualiza el archivo README.md con la lista de servicios configurados.
    
    Args:
        readme_path (str): Ruta al archivo README.md
        servicios (list): Lista de servicios configurados
    """
    try:
        with open(readme_path, 'r') as file:
            contenido = file.read()
        
        # Encuentra la sección de servicios configurados y actualízala
        if "## Servicios Configurados" in contenido:
            # Actualiza la lista de servicios
            nueva_seccion = "## Servicios Configurados\n\n"
            for servicio in servicios:
                # Obtener descripción del servicio
                for s in servicios_disponibles:
                    if s[0] == servicio:
                        nueva_seccion += f"- **{servicio}** - Configurado en todos los entornos\n"
                        break
            
            # Reemplaza la sección existente con la nueva
            partes = contenido.split("## Servicios Configurados")
            inicio = partes[0] + "## Servicios Configurados"
            # Encuentra el próximo encabezado ## si existe
            if len(partes) > 1:
                resto = partes[1]
                if "##" in resto:
                    fin = "##" + resto.split("##", 1)[1]
                    contenido_actualizado = inicio + nueva_seccion.replace("## Servicios Configurados\n\n", "\n\n") + fin
                else:
                    contenido_actualizado = inicio + nueva_seccion.replace("## Servicios Configurados\n\n", "\n\n")
            else:
                contenido_actualizado = inicio + nueva_seccion.replace("## Servicios Configurados\n\n", "\n\n")
        
            with open(readme_path, 'w') as file:
                file.write(contenido_actualizado)
    except Exception as e:
        typer.echo(f"Error al actualizar README con servicios: {str(e)}")

@app.command()
def add(
    proyecto: str,
    servicio: str = typer.Argument(None, help="Servicio de GCP para agregar al proyecto"),
    svc: List[str] = typer.Option(
        None,
        "--servicios",
        "--svc",
        help="Servicios de GCP para agregar al proyecto (separados por comas o múltiples flags)"
    )
):
    """
    Añade uno o varios servicios de GCP a un proyecto Terraform existente.
    """
    try:
        servicios_a_añadir = []
        
        # Procesar servicio por argumento principal
        if servicio:
            servicio_normalizado = encontrar_servicio_por_abreviatura(servicio)
            if servicio_normalizado:
                servicios_a_añadir.append(servicio_normalizado)
            else:
                typer.echo(f"Servicio no reconocido: {servicio}")
                return
        
        # Procesar servicios por opción --svc
        if svc:
            for item in svc:
                # Manejar valores separados por comas
                for s in item.split(','):
                    s = s.strip()
                    if s:  # Solo procesa si no está vacío
                        servicio_normalizado = encontrar_servicio_por_abreviatura(s)
                        if servicio_normalizado:
                            servicios_a_añadir.append(servicio_normalizado)
                        else:
                            typer.echo(f"Servicio no reconocido: {s}")
                            return
        
        # Verificar que se especificó al menos un servicio
        if not servicios_a_añadir:
            typer.echo("Error: Debe especificar al menos un servicio para añadir")
            return
            
        # Añadir los servicios al proyecto
        for servicio_normalizado in servicios_a_añadir:
            # Añadir el servicio al proyecto
            añadir_servicio(proyecto, servicio_normalizado)
            
            # Actualizar README.md con el nuevo servicio
            readme_path = os.path.join(proyecto, "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, 'r') as file:
                    contenido = file.read()
                
                # Añadir el servicio a la lista si no está ya
                if f"- **{servicio_normalizado}**" not in contenido:
                    servicios = [servicio_normalizado]
                    actualizar_readme_con_servicios(readme_path, servicios)
            
            typer.echo(f"✓ Servicio {servicio_normalizado} añadido a todos los entornos: dev, staging, prod")
    except Exception as e:
        typer.echo(f"Error al añadir servicio: {str(e)}")


def mostrar_servicios_disponibles():
    """
    Muestra la lista de servicios disponibles de forma elegante
    """
    typer.echo(f"\n{Fore.BLUE}{Style.BRIGHT}Servicios GCP disponibles:{Style.RESET_ALL}")
    
    from ..services.servicios import listar_servicios
    servicios_info = listar_servicios()
    
    # Calcular anchos máximos para la tabla
    max_nombre = max(len(s["nombre"]) for s in servicios_info)
    max_abrev = max(len(s["abreviatura"]) for s in servicios_info)
    max_id = max(len(s["id"]) for s in servicios_info)
    
    # Encabezado de la tabla
    separador = "+" + "-" * (max_nombre + 2) + "+" + "-" * (max_abrev + 2) + "+" + "-" * (max_id + 2) + "+"
    
    typer.echo(separador)
    typer.echo(f"| {Fore.YELLOW}{'Servicio'.ljust(max_nombre)}{Style.RESET_ALL} | {Fore.YELLOW}{'Abr.'.ljust(max_abrev)}{Style.RESET_ALL} | {Fore.YELLOW}{'ID'.ljust(max_id)}{Style.RESET_ALL} |")
    typer.echo(separador)
    
    # Contenido de la tabla
    for servicio in servicios_info:
        typer.echo(f"| {Fore.GREEN}{servicio['nombre'].ljust(max_nombre)}{Style.RESET_ALL} | {Fore.CYAN}{servicio['abreviatura'].ljust(max_abrev)}{Style.RESET_ALL} | {Fore.WHITE}{servicio['id'].ljust(max_id)}{Style.RESET_ALL} |")
    
    typer.echo(separador)


@app.command()
def services():
    """
    Muestra la lista de servicios GCP disponibles para añadir a proyectos.
    """
    mostrar_servicios()


def main():
    """
    Función principal para ejecutar la CLI.
    """
    app()


if __name__ == "__main__":
    main() 