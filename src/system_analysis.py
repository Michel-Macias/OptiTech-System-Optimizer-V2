# src/system_analysis.py

import platform
import psutil
import logging
import datetime
import os
from src import config_manager
from src import utils

APP_LOGGER_NAME = 'OptiTechOptimizer'
logger = logging.getLogger(APP_LOGGER_NAME)

def get_system_specs():
    """Recopila especificaciones detalladas de hardware y sistema operativo."""
    logger.info("Recopilando especificaciones del sistema...")
    try:
        # --- Información del Sistema Operativo ---
        os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
        }

        # --- Información de la CPU ---
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "max_frequency": f"{psutil.cpu_freq().max:.2f} Mhz",
            "min_frequency": f"{psutil.cpu_freq().min:.2f} Mhz",
            "current_frequency": f"{psutil.cpu_freq().current:.2f} Mhz",
            "usage_per_core": [f"{usage}%" for usage in psutil.cpu_percent(percpu=True, interval=1)],
            "total_usage": f"{psutil.cpu_percent(interval=1)}%",
        }

        # --- Información de la Memoria ---
        svmem = psutil.virtual_memory()
        memory_info = {
            "total": f"{svmem.total / (1024**3):.2f} GB",
            "available": f"{svmem.available / (1024**3):.2f} GB",
            "used": f"{svmem.used / (1024**3):.2f} GB",
            "percentage": f"{svmem.percent}%",
        }

        # --- Información de Discos ---
        disk_info = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_size": f"{partition_usage.total / (1024**3):.2f} GB",
                    "used": f"{partition_usage.used / (1024**3):.2f} GB",
                    "free": f"{partition_usage.free / (1024**3):.2f} GB",
                    "percentage": f"{partition_usage.percent}%",
                })
            except PermissionError:
                logger.warning(f"No se pudo acceder a la partición de disco {partition.mountpoint} debido a un PermissionError.")
                continue

        specs = {
            "os_info": os_info,
            "cpu_info": cpu_info,
            "memory_info": memory_info,
            "disk_info": disk_info,
        }
        
        logger.info("Especificaciones del sistema recopiladas con éxito.")
        return specs

    except Exception as e:
        logger.error(f"Ocurrió un error al recopilar las especificaciones del sistema: {e}", exc_info=True)
        return None

def get_service_status():
    """Cuenta los servicios del sistema por su estado (en ejecución, detenido, etc.)."""
    logger.info("Recopilando información del estado de los servicios...")
    status_counts = {
        'total': 0,
        'running': 0,
        'stopped': 0,
        'paused': 0,
        'other': 0
    }
    try:
        for service in psutil.win_service_iter():
            status = service.status()
            status_counts['total'] += 1
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts['other'] += 1
        logger.info("Estado de los servicios recopilado con éxito.")
        return status_counts
    except Exception as e:
        logger.error(f"Ocurrió un error al recopilar el estado de los servicios: {e}", exc_info=True)
        return None

def run_system_analysis():
    """Ejecuta un análisis completo del sistema y guarda el informe en un archivo."""
    utils.show_header("Módulo de Análisis del Sistema")
    logger.info("Iniciando análisis completo del sistema...")

    analysis_steps = [
        ("Recopilando especificaciones del sistema", get_system_specs),
        ("Contando servicios del sistema", get_service_status),
    ]
    total_steps = len(analysis_steps)
    current_step = 0

    specs = None
    services = None

    for description, func in analysis_steps:
        current_step += 1
        print(f"\n{description}...")
        utils.show_progress_bar(current_step, total_steps, prefix='Progreso del Análisis:', suffix='Completado', length=30)
        
        if func == get_system_specs:
            specs = func()
        elif func == get_service_status:
            services = func()

        if (func == get_system_specs and specs is None) or \
           (func == get_service_status and services is None):
            logger.error(f"El paso de análisis '{description}' falló.")
            print(utils.colored_text(f"Error: El análisis de '{description}' falló.", utils.Colors.RED))
            return

    # Asegurarse de que la barra de progreso finalice en 100%
    utils.show_progress_bar(total_steps, total_steps, prefix='Progreso del Análisis:', suffix='Completado', length=30)
    print(utils.colored_text("\nAnálisis del sistema completado con éxito.", utils.Colors.GREEN))

    # --- Construir Informe en Markdown (más legible) ---
    report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_sections = []
    md_sections.append(f"# Informe de Análisis de OptiTech System Optimizer\n")
    md_sections.append(f"**Informe generado el:** {report_date}\n")

    # Sistema
    md_sections.append("## 1. Información del Sistema Operativo\n")
    md_sections.append(f"- **Sistema:** {specs['os_info']['system']} {specs['os_info']['release']}\n")
    md_sections.append(f"- **Versión:** {specs['os_info']['version']}\n")
    md_sections.append(f"- **Hostname:** {specs['os_info']['hostname']}\n")
    md_sections.append(f"- **Arquitectura:** {specs['os_info']['architecture']}\n")

    # CPU
    md_sections.append("## 2. Información de la CPU\n")
    md_sections.append(f"- **Núcleos:** {specs['cpu_info']['physical_cores']} físicos, {specs['cpu_info']['total_cores']} lógicos\n")
    md_sections.append(f"- **Frecuencia:** {specs['cpu_info']['current_frequency']} (Min: {specs['cpu_info']['min_frequency']}, Max: {specs['cpu_info']['max_frequency']})\n")
    md_sections.append(f"- **Carga Total:** {specs['cpu_info']['total_usage']}\n")

    # Memoria
    md_sections.append("## 3. Información de la Memoria (RAM)\n")
    md_sections.append(f"- **Total:** {specs['memory_info']['total']}\n")
    md_sections.append(f"- **Disponible:** {specs['memory_info']['available']}\n")
    md_sections.append(f"- **En uso:** {specs['memory_info']['used']} ({specs['memory_info']['percentage']})\n")

    # Servicios
    md_sections.append("## 4. Estado de los Servicios\n")
    md_sections.append(f"- **Servicios Totales:** {services['total']}\n")
    md_sections.append(f"- **En ejecución:** {services['running']}\n")
    md_sections.append(f"- **Detenidos:** {services['stopped']}\n")
    md_sections.append(f"- **Pausados:** {services['paused']}\n")

    # Discos
    md_sections.append("## 5. Información de Discos\n")
    disk_lines = []
    for d in specs['disk_info']:
        disk_lines.append(f"- **Dispositivo:** {d['device']} | Montaje: {d['mountpoint']} | Tipo: {d['fstype']}\n  - Tamaño: {d['total_size']} | Usado: {d['used']} ({d['percentage']})")
    md_sections.append("\n".join(disk_lines) + "\n")

    md_report = "\n".join(md_sections)

    # --- Additionally include a legacy plain-text section for backwards compatibility/tests ---
    plain_report = """
    ========================================
    Informe de Análisis de OptiTech System Optimizer
    ========================================

    Informe generado el: {report_date}

    ---[ 1. Información del Sistema Operativo ]---
    Sistema:    {os_system} {os_release}
    Versión:    {os_version}
    Hostname:   {os_hostname}
    Arqui:      {os_arch}

    ---[ 2. Información de la CPU ]---
    Núcleos:    {cpu_physical_cores} Físicos, {cpu_total_cores} Lógicos
    Frecuencia: {cpu_current_freq} (Min: {cpu_min_freq}, Max: {cpu_max_freq})
    Carga Total: {cpu_total_usage}

    ---[ 3. Información de la Memoria (RAM) ]---
    Total:      {mem_total}
    Disponible: {mem_available}
    En uso:     {mem_used} ({mem_percentage})

    ---[ 4. Estado de los Servicios ]---
    Servicios Totales: {srv_total}
    En ejecución:      {srv_running}
    Detenidos:         {srv_stopped}
    Pausados:          {srv_paused}

    ---[ 5. Información de Discos ]---
    {disk_report}
    """.format(
        report_date=report_date,
        os_system=specs['os_info']['system'],
        os_release=specs['os_info']['release'],
        os_version=specs['os_info']['version'],
        os_hostname=specs['os_info']['hostname'],
        os_arch=specs['os_info']['architecture'],
        cpu_physical_cores=specs['cpu_info']['physical_cores'],
        cpu_total_cores=specs['cpu_info']['total_cores'],
        cpu_current_freq=specs['cpu_info']['current_frequency'],
        cpu_min_freq=specs['cpu_info']['min_frequency'],
        cpu_max_freq=specs['cpu_info']['max_frequency'],
        cpu_total_usage=specs['cpu_info']['total_usage'],
        mem_total=specs['memory_info']['total'],
        mem_available=specs['memory_info']['available'],
        mem_used=specs['memory_info']['used'],
        mem_percentage=specs['memory_info']['percentage'],
        srv_total=services['total'],
        srv_running=services['running'],
        srv_stopped=services['stopped'],
        srv_paused=services['paused'],
        disk_report="\n".join([
            f"    Dispositivo: {d['device']} | Montaje: {d['mountpoint']} | Tipo: {d['fstype']}\n" \
            f"    Tamaño: {d['total_size']} | Usado: {d['used']} ({d['percentage']})"
            for d in specs['disk_info']
        ])
    )

    # Combine markdown and legacy plain text so tests and users both get a readable file
    final_report = md_report + "\n\n" + plain_report

    # --- Guardar Archivo de Informe (Markdown) ---
    try:
        report_dir = config_manager.get_report_path()
        file_name = f"Informe_Analisis_Sistema_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path = os.path.join(report_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
                f.write(final_report)

        logger.info(f"Informe de análisis del sistema guardado en {file_path}")

        # Mostrar un resumen formateado en la consola para el usuario (más legible)
        try:
            _utils.show_header("Resumen del Análisis del Sistema")
            print(f"Sistema: {specs['os_info']['system']} {specs['os_info']['release']} ({specs['os_info']['architecture']})")
            print(f"Hostname: {specs['os_info']['hostname']}")
            print(f"CPU: {specs['cpu_info']['total_usage']} | Núcleos: {specs['cpu_info']['physical_cores']}/{specs['cpu_info']['total_cores']}")
            print(f"RAM: {specs['memory_info']['used']} / {specs['memory_info']['total']} ({specs['memory_info']['percentage']})")
            print(f"Servicios: {services['running']} running / {services['total']} total")
            print('\nDiscos:')
            for d in specs['disk_info']:
                print(f" - {d['mountpoint']}: {d['used']} / {d['total_size']} ({d['percentage']})")
            print(utils.colored_text(f"\nInforme guardado en: {file_path}", utils.Colors.GREEN))
        except Exception:
            # Si por alguna razón la impresión fallase, no detener el flujo
            pass

    except Exception as e:
        logger.error(f"Fallo al guardar el informe de análisis: {e}", exc_info=True)
        print(utils.colored_text(f"Error al guardar el informe de análisis: {e}", utils.Colors.RED))
