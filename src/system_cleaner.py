# src/system_cleaner.py

import os
import logging

APP_LOGGER_NAME = 'OptiTechOptimizer'
logger = logging.getLogger(APP_LOGGER_NAME)

# Definición de rutas a limpiar, expandiendo variables de entorno de Windows
CLEANUP_PATHS = {
    'basico': [
        os.path.expandvars(r'%TEMP%'),
        os.path.expandvars(r'%SystemRoot%\Temp'),
        os.path.expandvars(r'%SystemRoot%\SoftwareDistribution\Download'),
    ],
    'extendido': [
        os.path.expandvars(r'%SystemRoot%\Prefetch'),
        os.path.expandvars(r'%SystemRoot%\Logs\CBS'),
    ],
    'avanzado': [
        # Rutas para limpieza avanzada (ej. WinSxS) requerirán comandos DISM
        # y se manejarán de forma especial.
    ]
}

def limpiar_archivos_temporales(nivel='basico', modo_informe=False):
    """Limpia archivos y directorios temporales según el nivel especificado."""
    logger.info(f"Iniciando limpieza de archivos temporales (Nivel: {nivel}, Modo Informe: {modo_informe})")
    
    rutas_a_limpiar = []
    if nivel == 'basico':
        rutas_a_limpiar.extend(CLEANUP_PATHS['basico'])
    elif nivel == 'extendido':
        rutas_a_limpiar.extend(CLEANUP_PATHS['basico'])
        rutas_a_limpiar.extend(CLEANUP_PATHS['extendido'])
    elif nivel == 'avanzado':
        # La limpieza avanzada incluirá todo lo anterior más operaciones especiales
        rutas_a_limpiar.extend(CLEANUP_PATHS['basico'])
        rutas_a_limpiar.extend(CLEANUP_PATHS['extendido'])
        logger.info("La limpieza avanzada se implementará con funciones adicionales (DISM, etc.).")

    total_eliminado = 0
    archivos_eliminados = 0

    for ruta in rutas_a_limpiar:
        if not os.path.exists(ruta):
            logger.warning(f"La ruta no existe, omitiendo: {ruta}")
            continue
        
        logger.info(f"Procesando ruta: {ruta}")
        for dirpath, dirnames, filenames in os.walk(ruta):
            for archivo in filenames:
                ruta_completa = os.path.join(dirpath, archivo)
                try:
                    tamaño_archivo = os.path.getsize(ruta_completa)
                    if modo_informe:
                        total_eliminado += tamaño_archivo
                        archivos_eliminados += 1
                    else:
                        os.remove(ruta_completa)
                        total_eliminado += tamaño_archivo
                        archivos_eliminados += 1
                        logger.debug(f"Eliminado archivo: {ruta_completa}")
                except FileNotFoundError:
                    logger.warning(f"Archivo no encontrado al intentar eliminar, puede haber sido eliminado por otro proceso: {ruta_completa}")
                    continue
                except PermissionError:
                    logger.warning(f"Permiso denegado para eliminar: {ruta_completa}")
                    continue
                except Exception as e:
                    logger.error(f"Error inesperado al eliminar {ruta_completa}: {e}")
                    continue
    
    resumen = f"Limpieza completada. Total de archivos procesados para eliminación: {archivos_eliminados}. Espacio total recuperado: {total_eliminado / (1024*1024):.2f} MB."
    logger.info(resumen)
    print(resumen)
    
    return total_eliminado, archivos_eliminados
