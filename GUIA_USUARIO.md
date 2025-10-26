# Guía de Usuario de OptiTech System Optimizer

¡Bienvenido a OptiTech System Optimizer! Esta guía te ayudará a entender qué hace cada función principal de la herramienta para que puedas usarla con confianza.

---

## 1. Análisis del Sistema

Esta opción es como hacerle un chequeo médico a tu ordenador.

*   **¿Qué hace?**
    Recopila información importante sobre los componentes de tu PC (procesador, memoria RAM, discos duros) y sobre el sistema operativo. También mide el rendimiento actual, como el uso de la CPU y el espacio libre en disco.

*   **¿Para qué sirve?**
    Al finalizar, genera un informe de texto con todo el resumen. Este informe es muy útil para saber de un vistazo cómo está tu sistema o para compartirlo con personal técnico si necesitas ayuda.

*   **¿Es seguro?**
    Sí, es **100% seguro**. Esta función solo lee información y no realiza ningún cambio en tu sistema.

---

## 2. Limpieza del Sistema

Esta opción te ayuda a recuperar espacio en tu disco duro eliminando archivos innecesarios que se acumulan con el tiempo.

*   **¿Qué hace?**
    Ofrece varios niveles de limpieza para que elijas el que prefieras.

*   **Opciones de Limpieza:**
    *   **Nivel 1: Limpieza Básica:** Es la opción más rápida y segura. Elimina archivos temporales de programas y vacía la Papelera de Reciclaje. Ideal para un mantenimiento regular.
    *   **Nivel 2: Limpieza Extendida:** Hace todo lo del nivel básico y además busca archivos temporales del sistema más antiguos. Tarda un poco más pero puede liberar más espacio.
    *   **Nivel 3: Limpieza Avanzada:** Es la opción más potente. Realiza una limpieza profunda de componentes de actualizaciones de Windows (`WinSxS`) y copias de seguridad antiguas del sistema (`Shadow Copies`).

*   **¿Es seguro?**
    *   Los niveles **Básico y Extendido son muy seguros** para todos los usuarios.
    *   El nivel **Avanzado** es seguro, pero se recomienda para usuarios que necesiten liberar una gran cantidad de espacio. El proceso no se puede deshacer.

*   **Beneficio esperado:**
    Recuperarás espacio en tu disco duro, lo que puede ayudar a que el sistema funcione un poco más fluido.

---

## 4. Optimización del Sistema

Este módulo te ofrece un conjunto de herramientas para mejorar el rendimiento y la configuración de tu sistema. Puedes elegir qué optimizaciones aplicar desde un menú interactivo.

### 4.1. Optimización de Efectos Visuales

Esta opción ajusta la apariencia de Windows para que el sistema se sienta más ágil y rápido.

*   **¿Qué hace?**
    Desactiva animaciones y efectos gráficos que consumen recursos, como las animaciones al abrir o cerrar ventanas, los efectos de transparencia o las sombras debajo de las ventanas.

*   **¿Es seguro?**
    Sí, es **totalmente seguro**. Es un cambio cosmético y se puede revertir fácilmente desde la configuración de "Apariencia y rendimiento" de Windows si no te gusta el resultado.

*   **Beneficio esperado:**
    La interfaz de Windows responderá de forma más instantánea, dando una sensación de mayor velocidad, especialmente en equipos más modestos.

### 4.2. Optimización de Servicios No Esenciales

*   **¿Qué hace?**
    Deshabilita ciertos servicios de Windows que no son críticos para el funcionamiento diario de la mayoría de los usuarios (como la telemetría o servicios de fax). 

*   **¿Es seguro?**
    Sí, es una optimización **muy segura**. Los servicios seleccionados son conocidos por ser prescindibles en entornos de oficina típicos. En el improbable caso de que necesites uno de ellos, se pueden reactivar manualmente desde la consola de servicios de Windows.

*   **Beneficio esperado:**
    Liberar una pequeña cantidad de memoria RAM y recursos del procesador, contribuyendo a un sistema ligeramente más ágil.

### 4.3. Activar Plan de Máximo Rendimiento

*   **¿Qué hace?**
    Cambia el plan de energía de Windows al de "Máximo rendimiento". Este plan prioriza el rendimiento sobre el ahorro de energía.

*   **¿Es seguro?**
    Sí, es **totalmente seguro**. Es un ajuste estándar de Windows. Ten en cuenta que en portátiles, esto consumirá la batería más rápidamente.

*   **Beneficio esperado:**
    El procesador y otros componentes funcionarán a su máxima capacidad de forma más consistente, lo que puede mejorar la velocidad en tareas exigentes. Ideal para ordenadores de sobremesa.

### 4.4. Optimizar y Reiniciar Red

*   **¿Qué hace?**
    Ejecuta una serie de comandos estándar de Windows para reiniciar la configuración de red. Esto limpia la caché de DNS, reinicia la pila de red y renueva la dirección IP.

*   **¿Es seguro?**
    Sí, es **muy seguro**. Es el equivalente a ejecutar los comandos de solución de problemas de red más comunes. Perderás la conectividad a internet durante unos segundos mientras se ejecutan los comandos.

*   **Beneficio esperado:**
    Puede solucionar problemas de conexión a internet, como lentitud o páginas que no cargan. Es una buena primera medida ante cualquier problema de red.

---

## 5. Mantenimiento y Backups

Este módulo proporciona herramientas esenciales para mantener la salud de tu sistema y protegerte contra posibles problemas.

### 5.1. Backup y Restauración del Registro

*   **¿Qué hace?**
    Permite crear una copia de seguridad de una parte crítica del registro de Windows (HKEY_CURRENT_USER) en un archivo `.reg`. También puede restaurar el registro desde un archivo de copia de seguridad previamente creado.

*   **¿Es seguro?**
    La creación de backups es **segura**. La restauración es una operación **crítica** que debe usarse con precaución. Siempre se recomienda crear un punto de restauración del sistema antes de restaurar el registro.

*   **Beneficio esperado:**
    Protección contra configuraciones erróneas o corrupción del registro, permitiendo revertir a un estado anterior conocido.

### 5.2. Creación de Puntos de Restauración del Sistema

*   **¿Qué hace?**
    Crea un "punto de restauración" en Windows. Un punto de restauración es una instantánea del estado de los archivos del sistema, programas instalados y configuración del registro en un momento dado.

*   **¿Es seguro?**
    Sí, es **seguro**. Es una característica nativa de Windows diseñada para revertir el sistema a un estado anterior sin afectar tus archivos personales.

*   **Beneficio esperado:**
    Proporciona una red de seguridad para deshacer cambios importantes en el sistema, como la instalación de controladores o software problemático.

### 5.3. Ejecutar SFC (System File Checker)

*   **¿Qué hace?**
    Ejecuta la herramienta "Comprobador de archivos de sistema" de Windows (`sfc /scannow`). Esta herramienta escanea todos los archivos protegidos del sistema en busca de corrupciones y los reemplaza con versiones correctas de Microsoft.

*   **¿Es seguro?**
    Sí, es **seguro**. Es una herramienta de diagnóstico y reparación integrada en Windows.

*   **Beneficio esperado:**
    Ayuda a solucionar problemas relacionados con archivos del sistema dañados, que pueden causar inestabilidad o errores en Windows.

### 5.4. Ejecutar DISM (Deployment Image Servicing and Management)

*   **¿Qué hace?**
    Ejecuta el comando `DISM /Online /Cleanup-Image /RestoreHealth`. Esta herramienta repara la imagen de Windows, lo que puede solucionar problemas más profundos que SFC no puede resolver.

*   **¿Es seguro?**
    Sí, es **seguro**. Es una herramienta de mantenimiento avanzada de Windows. Puede tardar un tiempo en completarse.

*   **Beneficio esperado:**
    Repara componentes dañados del sistema operativo, mejorando la estabilidad y el rendimiento general.

### 5.5. Ejecutar CHKDSK (Check Disk)

*   **¿Qué hace?**
    Ejecuta el comando `chkdsk C: /F /R` (o la unidad que especifiques). Esta herramienta escanea el disco duro en busca de errores en el sistema de archivos y sectores defectuosos, intentando repararlos.

*   **¿Es seguro?**
    Sí, es **seguro**, pero puede requerir un reinicio del sistema para ejecutarse, especialmente si se corrigen errores en la unidad del sistema.

*   **Beneficio esperado:**
    Mantiene la integridad de tus discos duros, previniendo la pérdida de datos y mejorando la fiabilidad del almacenamiento.

### 5.6. Menú de Mantenimiento

*   **¿Qué hace?**
    Este es el punto de entrada principal para todas las herramientas de mantenimiento. Presenta un menú interactivo donde puedes seleccionar y ejecutar cualquiera de las funciones de mantenimiento descritas anteriormente (Backup/Restauración del Registro, Puntos de Restauración, SFC, DISM, CHKDSK).

*   **¿Es seguro?**
    El menú en sí es **seguro**. La seguridad de cada operación individual se describe en sus respectivas secciones.

*   **Beneficio esperado:**
    Centraliza y facilita el acceso a todas las herramientas de mantenimiento del sistema, permitiéndote realizar tareas de forma organizada y controlada.

---

## 6. Gestión de Logs

Esta opción te permite visualizar los registros de actividad generados por OptiTech System Optimizer.

*   **¿Qué hace?**
    Muestra el contenido del archivo de log principal de la aplicación, donde se registran todas las acciones, advertencias y errores.

*   **¿Para qué sirve?**
    Es útil para revisar el historial de operaciones realizadas por la herramienta, diagnosticar posibles problemas o verificar que las acciones se ejecutaron correctamente.

*   **¿Es seguro?**
    Sí, es **100% seguro**. Esta función solo lee información y no realiza ningún cambio en tu sistema.
