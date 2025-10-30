# Guía de Usuario de OptiTech System Optimizer

¡Bienvenido a OptiTech System Optimizer! Esta guía te ayudará a entender qué hace cada función principal de la herramienta para que puedas usarla con confianza.

---

## Cómo Empezar

Para usar OptiTech System Optimizer, sigue estos pasos:

1.  **Descomprime la aplicación**: La herramienta se distribuye como una carpeta comprimida en un archivo `.zip`. Descomprime este archivo en la ubicación que prefieras.
2.  **Ejecuta la aplicación**: Dentro de la carpeta descomprimida, busca el archivo `OptiTechSystemOptimizer.exe` y haz doble clic en él.
3.  **Acepta los permisos de administrador**: La aplicación solicitará permisos de administrador (una ventana de UAC). Esto es **necesario y seguro**, ya que muchas funciones de optimización y limpieza requieren acceso a nivel de sistema. Sin estos permisos, la herramienta no podrá realizar sus tareas más importantes.
4.  **Consideraciones sobre Antivirus**: Es posible que tu antivirus (incluido Windows Defender) muestre una advertencia o bloquee la aplicación. Esto se debe a la forma en que se empaquetan las aplicaciones de Python y no significa que la herramienta sea maliciosa. Si esto ocurre, puedes añadir la carpeta de la aplicación a las exclusiones de tu antivirus.
5.  **Navega por el menú**: Una vez abierta, verás un menú principal con varias opciones. Simplemente escribe el número de la opción que deseas y presiona `Enter`.

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

*   **Opciones de Limpieza:**
    *   **Limpieza Básica:** Es la opción más rápida. Elimina archivos temporales de programas y del sistema.
    *   **Limpieza Extendida:** Hace todo lo del nivel básico y además busca archivos de pre-carga del sistema (`Prefetch`) y logs antiguos.
    *   **Vaciar Papelera de Reciclaje:** Vacía de forma segura la papelera.
    *   **Limpiar Almacén WinSxS:** Realiza una limpieza profunda de componentes de actualizaciones de Windows antiguas. Es una de las formas más efectivas de liberar una gran cantidad de espacio. La operación no se puede deshacer.
    *   **Eliminar Copias de Sombra:** Borra los puntos de restauración del sistema y el historial de archivos antiguos. Libera mucho espacio, pero ten en cuenta que no podrás volver a esos puntos de restauración específicos.

*   **¿Es seguro?**
    Sí, todas las opciones son seguras. Sin embargo, las opciones `WinSxS` y `Copias de Sombra` eliminan datos de recuperación del sistema, por lo que deben usarse a conciencia.

*   **Beneficio esperado:**
    Recuperarás espacio en tu disco duro, lo que puede ayudar a que el sistema funcione un poco más fluido.

---

## 3. Optimización del Sistema

Este módulo te ofrece un conjunto de herramientas para mejorar el rendimiento y la configuración de tu sistema.

*   **Optimizar Efectos Visuales:** Desactiva animaciones y efectos gráficos que consumen recursos para que la interfaz de Windows se sienta más ágil. Es un cambio cosmético y totalmente seguro.
*   **Optimizar Servicios No Esenciales:** Deshabilita ciertos servicios de Windows que no son críticos (telemetría, fax, etc.) para liberar una pequeña cantidad de memoria RAM y recursos.
*   **Activar Plan de Máximo Rendimiento:** Cambia el plan de energía de Windows para priorizar el rendimiento sobre el ahorro de energía. Ideal para ordenadores de sobremesa. En portátiles, consumirá la batería más rápido.
*   **Optimizar y Reiniciar Red:** Ejecuta comandos para reiniciar la configuración de red, lo que puede solucionar problemas de conexión a internet.

---

## 4. Mantenimiento del Sistema

Este módulo proporciona herramientas esenciales para mantener la salud de tu sistema.

*   **Backup y Restauración del Registro:** Permite crear una copia de seguridad de la configuración de tu usuario (`HKEY_CURRENT_USER`) y restaurarla si es necesario. La restauración es una operación crítica; úsala con precaución.
*   **Crear Punto de Restauración del Sistema:** Crea una "instantánea" del estado de tu sistema, permitiéndote revertir cambios importantes si algo sale mal.
*   **Ejecutar SFC (System File Checker):** Escanea y repara archivos corruptos o dañados del sistema operativo.
*   **Ejecutar DISM:** Repara la imagen de Windows, solucionando problemas más profundos que SFC no puede arreglar.
*   **Ejecutar CHKDSK (Check Disk):** Escanea el disco duro en busca de errores y los repara para prevenir la pérdida de datos.

---

## 5. Gestión de Logs

Esta opción te permite visualizar los registros de actividad generados por OptiTech System Optimizer.

*   **¿Qué hace?**
    Muestra el contenido del archivo de log principal de la aplicación, donde se registran todas las acciones, advertencias y errores.

*   **¿Para qué sirve?**
    Es útil para revisar el historial de operaciones realizadas por la herramienta, diagnosticar posibles problemas o verificar que las acciones se ejecutaron correctamente.

*   **¿Es seguro?**
    Sí, es **100% seguro**. Esta función solo lee información.