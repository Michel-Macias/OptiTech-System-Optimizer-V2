# OptiTech System Optimizer

## Descripción del Proyecto

**OptiTech System Optimizer** es una herramienta integral diseñada para la optimización y mantenimiento de equipos con **Windows 11**. Su objetivo principal es mejorar el rendimiento general del sistema y liberar espacio de almacenamiento, garantizando al mismo tiempo la seguridad y la integridad de los datos en un entorno empresarial.

Este proyecto se desarrolla utilizando **Python** con una arquitectura modular, y se distribuirá como un ejecutable autónomo (`.exe`) para facilitar su uso y distribución interna.

## Guía de Usuario

Para entender qué hace cada función en un lenguaje sencillo, consulta nuestra **[Guía de Usuario](GUIA_USUARIO.md)**.

## Progreso del Proyecto

*   [x] **Módulo 1: Estructura y Configuración Inicial**: Configuración de la estructura del proyecto, sistema de logging, gestión de configuración y auto-elevación de privilegios (UAC).
*   [x] **Módulo 2: Funciones de Utilidad**: Implementación de helpers para la interfaz de usuario como encabezados, barras de progreso y confirmaciones.
*   [x] **Módulo 3: Análisis del Sistema**: Implementación de la capacidad de recopilar y guardar informes detallados sobre el SO, hardware, servicios y uso de recursos.
*   [x] **Módulo 4: Limpieza del Sistema**: Implementación de funciones para limpiar archivos temporales, vaciar la papelera de reciclaje, limpiar WinSxS y eliminar copias de sombra.
*   [ ] **Módulo 5: Optimización del Sistema**
    *   [x] Optimización de Efectos Visuales
    *   [x] Optimización de Servicios
    *   [x] Optimización de Plan de Energía
    *   [x] Optimización de Red
*   [ ] **Módulo 6: Mantenimiento y Backups**
*   [ ] **Módulo 7: Interfaz Principal y Empaquetado**

## Funcionalidades Clave

La herramienta incluirá las siguientes funcionalidades principales:

*   **Diagnóstico del Sistema**: Recopilación de información de hardware, sistema operativo, uso de CPU y espacio en disco, y estado de servicios.
*   **Limpieza del Sistema**: Eliminación de archivos temporales, caché, logs, elementos de la papelera de reciclaje, y optimización de componentes como WinSxS.
*   **Optimización del Rendimiento**: Ajuste de servicios no críticos, efectos visuales, plan de energía y configuración de red.
*   **Mantenimiento y Backups**: Funciones para la gestión del registro, creación de puntos de restauración del sistema y ejecución de herramientas de integridad del sistema (SFC, DISM, CHKDSK).
*   **Gestión de Logs**: Visualización y rotación de logs generados por la propia herramienta.
*   **Interfaz Interactiva**: Un menú principal en consola para una interacción sencilla con el usuario.

## Consideraciones Técnicas

*   **Lenguaje de Programación**: Python
*   **Sistema Operativo Objetivo**: Exclusivamente Windows 11.
*   **Arquitectura**: Modular, facilitando el mantenimiento y la escalabilidad.
*   **Distribución**: Ejecutable autónomo (`.exe`) generado con `PyInstaller`.
*   **Seguridad**: Implementación robusta de elevación de privilegios (UAC), validación de entradas, confirmaciones explícitas para operaciones críticas y logging detallado.
*   **Rendimiento**: Optimización del código Python y, cuando sea necesario, invocación de comandos nativos de Windows o PowerShell para tareas de bajo nivel.

## Estado Actual del Desarrollo

El trabajo previo en los módulos 1 a 4 está completo y documentado. El desarrollo actual se centra en el **Módulo 5: Optimización del Sistema**. La próxima tarea es la implementación de la **función principal del optimizador (Run-Optimizer)**.

## Cómo Contribuir

(Se añadirán instrucciones detalladas sobre cómo contribuir al proyecto en el futuro.)

## Testing rápido

Pasos rápidos para preparar el entorno y ejecutar las pruebas en Windows (PowerShell):

- Crear y activar un virtualenv:

```powershell
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\.venv\Scripts\Activate.ps1
```

- Instalar dependencias:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

- Ejecutar tests unitarios:

```powershell
python -m unittest discover -v
```

- Ejecutar la aplicación (modo desarrollo, sin elevar UAC):

```powershell
python -m src.main --no-elevate
```

Logs e informes se escriben en `%LOCALAPPDATA%\\OptiTechOptimizer`.

## Licencia

(Se especificará la licencia del proyecto.)