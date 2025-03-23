# Guía de Contribución - Terraform GCP Generator

## Convenciones de Commits

Para mantener un historial de commits limpio y un seguimiento efectivo de los cambios, utilizamos la siguiente nomenclatura de commits basada en el tipo de rama:

### Prefijos por Rama

- **main**: Cambios en producción
  - `release: v1.x.x - descripción de la versión`

- **develop**: Desarrollo principal
  - `dev: descripción del cambio`

- **feature/xxx**: Nuevas funcionalidades
  - `feat(xxx): descripción de la funcionalidad`

- **bugfix/xxx**: Corrección de errores
  - `fix(xxx): descripción de la corrección`

- **hotfix/xxx**: Correcciones urgentes en producción
  - `hotfix(xxx): descripción de la corrección urgente`

- **docs/xxx**: Documentación
  - `docs(xxx): descripción de la documentación`

- **refactor/xxx**: Refactorización de código
  - `refactor(xxx): descripción de la refactorización`

- **test/xxx**: Pruebas
  - `test(xxx): descripción de las pruebas`

### Estructura del Mensaje de Commit

```
<tipo>(<ámbito>): <descripción corta>

[cuerpo opcional]

[pie opcional]
```

### Tipos de Commits

- **feat**: Nueva característica o funcionalidad
- **fix**: Corrección de un error
- **docs**: Cambios en la documentación
- **style**: Cambios que no afectan al código (formato, espacios en blanco, etc.)
- **refactor**: Cambios en el código que no corrigen errores ni añaden características
- **perf**: Cambios que mejoran el rendimiento
- **test**: Adición o corrección de pruebas
- **build**: Cambios en el sistema de construcción o dependencias externas
- **ci**: Cambios en la configuración de CI/CD
- **chore**: Otros cambios que no modifican archivos de código o pruebas

### Ámbitos Comunes

- **cli**: Interfaz de línea de comandos
- **core**: Funcionalidad central
- **template**: Plantillas de Terraform
- **service**: Servicios específicos de GCP
- **docs**: Documentación
- **deps**: Dependencias

### Ejemplos

```
feat(service): añadir soporte para Cloud Run

fix(cli): corregir error al mostrar la lista de servicios

docs(readme): actualizar instrucciones de instalación

refactor(core): mejorar estructura del generador de archivos

test(service): añadir pruebas para servicio Cloud Storage
```

## Flujo de Trabajo con Ramas

1. Crear una rama desde `develop` con el nombre apropiado (ej: `feature/cloud-run`)
2. Realizar cambios y commits siguiendo las convenciones
3. Crear un Pull Request hacia `develop`
4. Después de revisión, fusionar con `develop`
5. Periódicamente, fusionar `develop` con `main` para lanzar nuevas versiones

## Versiones

Utilizamos [Semantic Versioning](https://semver.org/) para nuestras versiones:

- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Cambios compatibles con versiones anteriores que añaden funcionalidad
- **PATCH**: Cambios compatibles con versiones anteriores que corrigen errores 