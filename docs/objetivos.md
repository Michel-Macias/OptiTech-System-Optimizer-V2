Mi objetivo es conseguir un script que me ayude con la optimización y mantenimiento del equipo especialmente centrado en: Mejorar rendimiento general y liberar espacio. El script tiene que ser muy seguro y no comprometer la integridad del sistema ni de sus datos ya que es para un entorno empresarial:
🧾 Resumen General
Nombre: OptiTech System Optimizer
Versión: 1.1
Autor: Jesús Macías Durán
Objetivo: Herramienta integral para:

Diagnóstico del sistema
Limpieza de archivos temporales
Optimización de rendimiento
Mantenimiento del sistema (backups, restauración, integridad)
🧰 Estructura y Funcionalidades
🔐 1. Autoelevación de privilegios
Verifica si el script se ejecuta con privilegios de administrador.
Si no es así, relanza el script con runas para obtener permisos elevados mediante UAC.
⚙️ 2. Configuración inicial
Define rutas base para logs, backups e informes.
Crea directorios necesarios si no existen.
Establece codificación UTF-8 para salida y archivos.
🧩 3. Funciones de utilidad
Write-Log: Registro de eventos con niveles INFO, WARN y ERROR.
Show-Header, Show-ProgressBar, Confirm-Operation: Utilidades para mejorar la experiencia del usuario.
🖥️ 4. Análisis del sistema
Get-SystemSpecs: Recoge información de hardware y sistema operativo.
Get-PerformanceData: Mide uso de CPU y espacio libre en disco.
Get-ServiceStatus: Cuenta servicios activos.
Run-SystemAnalysis: Ejecuta un diagnóstico completo y genera un informe en texto.
🧹 5. Limpieza del sistema
Niveles de limpieza:
Básico: TEMP, SoftwareDistribution, etc.
Extendido: Prefetch, CBS logs, descargas públicas.
Avanzado: WinSxS, WER, puntos de restauración antiguos.
Funciones clave:
Clear-TempFiles: Limpieza según nivel.
Clear-RecycleBinSafe, Clear-WinSxS, Clear-ShadowCopies: Limpiezas específicas.
Run-Cleaner: Menú interactivo para elegir nivel o modo informe.
🚀 6. Optimización del sistema
Optimize-Services: Desactiva servicios no críticos (ej. Xbox, Fax, RemoteRegistry).
Optimize-VisualEffects: Ajusta efectos visuales para mejorar rendimiento.
Optimize-PowerPlan: Activa el plan de energía de alto rendimiento.
Optimize-Network: Reinicia configuración de red.
Run-Optimizer: Permite optimización rápida o completa.
🛠️ 7. Mantenimiento y backups
Backup-Registry / Restore-Registry: Exporta y restaura claves del registro.
Backup-SystemRestore: Crea punto de restauración del sistema.
Run-SFC, Run-DISM, Run-CHKDSK: Ejecuta herramientas de integridad del sistema.
Run-Maintenance: Menú para ejecutar tareas de mantenimiento.
📁 8. Gestión de logs
View-Logs: Visualiza logs generados, permite rotación automática y eliminación manual.
🔁 9. Bucle principal
Menú principal con opciones para ejecutar análisis, limpieza, optimización, mantenimiento, ver logs o salir.
🧠 Consideraciones Técnicas
Modularidad: El script está bien estructurado en bloques funcionales, lo que facilita su mantenimiento y ampliación.
Seguridad: Incluye confirmaciones antes de operaciones críticas y crea puntos de restauración antes de tareas potencialmente destructivas.
Compatibilidad: Diseñado específicamente para Windows 11.
Logging: Implementa un sistema de logs robusto para trazabilidad.
Interactividad: Uso de menús y confirmaciones para evitar errores del usuario.