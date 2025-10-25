# Checklist de Tareas - OptiTech System Optimizer

## 1. Estructura y Configuración Inicial
- [x] Autoelevación de privilegios
- [x] Configuración inicial (rutas, directorios, codificación)
- [x] Definir rutas base para logs, backups e informes
- [x] Crear directorios necesarios si no existen
- [x] Establecer codificación UTF-8

## 2. Funciones de Utilidad
- [x] Implementar Write-Log (Registro de eventos con niveles INFO, WARN y ERROR)
- [x] Implementar Show-Header
- [x] Implementar Show-ProgressBar
- [x] Implementar Confirm-Operation

## 3. Análisis del Sistema
- [x] Implementar Get-SystemSpecs (Recoge información de hardware y sistema operativo)
- [x] Implementar Get-PerformanceData (Mide uso de CPU y espacio libre en disco)
- [x] Implementar Get-ServiceStatus (Cuenta servicios activos)
- [x] Implementar Run-SystemAnalysis (Ejecuta un diagnóstico completo y genera un informe)

## 4. Limpieza del Sistema
- [x] Definir niveles de limpieza (Básico, Extendido, Avanzado)
- [x] Implementar Clear-TempFiles (Limpieza según nivel)
- [x] Implementar Clear-RecycleBinSafe
- [x] Implementar Clear-WinSxS
- [x] Implementar Clear-ShadowCopies
- [x] Implementar Run-Cleaner (Menú interactivo para elegir nivel o modo informe)

## 5. Optimización del Sistema
- [x] Implementar Optimize-VisualEffects (Ajusta efectos visuales)
- [x] Implementar Optimize-Services (Desactiva servicios no críticos)
- [x] Implementar Optimize-PowerPlan (Activa plan de energía de alto rendimiento)
- [x] Implementar Optimize-Network (Reinicia configuración de red)
- [x] Implementar Run-Optimizer (Permite optimización rápida o completa)

## 6. Mantenimiento y Backups
- [x] Implementar Backup-Registry / Restore-Registry
- [x] Implementar Backup-SystemRestore
- [x] Implementar Run-SFC
- [x] Implementar Run-DISM
- [ ] Implementar Run-CHKDSK
- [ ] Implementar Run-Maintenance (Menú para ejecutar tareas de mantenimiento)

## 7. Gestión de Logs
- [ ] Implementar View-Logs (Visualiza logs, permite rotación y eliminación)

## 8. Bucle Principal
- [ ] Implementar Menú principal con opciones (análisis, limpieza, optimización, mantenimiento, logs, salir)

## 9. Consideraciones Técnicas
- [ ] Asegurar Modularidad
- [ ] Implementar Seguridad (confirmaciones, puntos de restauración)
- [ ] Asegurar Compatibilidad con Windows 11
- [ ] Implementar Logging robusto
- [ ] Asegurar Interactividad (menús y confirmaciones)
