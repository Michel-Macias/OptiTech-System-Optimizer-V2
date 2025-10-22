# src/system_cleaner.py

import os
import logging
import winshell
import subprocess
from src import utils

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

def limpiar_papelera_reciclaje_seguro(confirmar=False, mostrar_progreso=True, sonido=False):
    """Vacía la papelera de reciclaje de Windows de forma segura usando winshell."""
    logger.info(f"Iniciando limpieza segura de la papelera de reciclaje (Confirmar: {confirmar}, Progreso: {mostrar_progreso}, Sonido: {sonido})")
    try:
        if not list(winshell.recycle_bin()):
            logger.info("La papelera de reciclaje ya está vacía.")
            print("La papelera de reciclaje ya está vacía.")
            return True # Considerar éxito si ya está vacía

        winshell.recycle_bin().empty(confirm=confirmar, show_progress=mostrar_progreso, sound=sonido)
        logger.info("La papelera de reciclaje ha sido vaciada con éxito.")
        print("La papelera de reciclaje ha sido vaciada con éxito.")
        return True
    except Exception as e:
        logger.error(f"Ocurrió un error al intentar vaciar la papelera de reciclaje: {e}", exc_info=True)
        print(f"Error al vaciar la papelera de reciclaje: {e}")
        return False

def limpiar_winsxs():
    """Limpia el almacén de componentes WinSxS usando DISM."""
    logger.info("Iniciando limpieza del almacén de componentes WinSxS...")
    try:
        # El comando DISM requiere privilegios de administrador
        comando = ["Dism.exe", "/online", "/Cleanup-Image", "/StartComponentCleanup"]
        
        # Ejecutar el comando y capturar la salida
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, shell=True)
        
        logger.info("Comando DISM ejecutado con éxito.")
        logger.debug(f"Salida DISM: {resultado.stdout}")
        print("Limpieza de WinSxS completada con éxito.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando DISM para WinSxS: {e}", exc_info=True)
        logger.error(f"Salida de error DISM: {e.stderr}")
        print(f"Error al limpiar WinSxS: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado al limpiar WinSxS: {e}", exc_info=True)
        print(f"Error inesperado al limpiar WinSxS: {e}")
        return False

def limpiar_copias_sombra():
    """Elimina todas las copias de sombra (Shadow Copies) del sistema."""
    logger.info("Iniciando eliminación de copias de sombra...")
    try:
        # El comando vssadmin requiere privilegios de administrador
        comando = ["vssadmin", "delete", "shadows", "/all", "/quiet"]
        
        # Ejecutar el comando y capturar la salida
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, shell=True)
        
        logger.info("Comando vssadmin ejecutado con éxito.")
        logger.debug(f"Salida vssadmin: {resultado.stdout}")
        print("Eliminación de copias de sombra completada con éxito.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando vssadmin para copias de sombra: {e}", exc_info=True)
        logger.error(f"Salida de error vssadmin: {e.stderr}")
        print(f"Error al eliminar copias de sombra: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado al eliminar copias de sombra: {e}", exc_info=True)
        print(f"Error inesperado al eliminar copias de sombra: {e}")
        return False

def ejecutar_limpiador():
    """Presenta un menú interactivo para realizar diferentes tipos de limpieza del sistema."""
    utils.show_header("Módulo de Limpieza del Sistema")
    logger.info("Iniciando módulo de limpieza del sistema.")

    opciones_limpieza = {
        '1': {'nombre': 'Limpieza Básica (Archivos Temporales)', 'nivel': 'basico'},
        '2': {'nombre': 'Limpieza Extendida (Archivos Temporales y Prefetch)', 'nivel': 'extendido'},
        '3': {'nombre': 'Vaciar Papelera de Reciclaje', 'funcion': limpiar_papelera_reciclaje_seguro},
        '4': {'nombre': 'Limpiar Almacén WinSxS', 'funcion': limpiar_winsxs},
        '5': {'nombre': 'Eliminar Copias de Sombra', 'funcion': limpiar_copias_sombra},
    }

    while True:
        print("\nSeleccione una opción de limpieza:")
        for key, value in opciones_limpieza.items():
            print(f"  {key}. {value['nombre']}")
        print("  0. Volver al menú principal")

        opcion = input("Ingrese su opción: ").strip()

        if opcion == '0':
            logger.info("Saliendo del módulo de limpieza.")
            break
        elif opcion in opciones_limpieza:
            tarea = opciones_limpieza[opcion]
            
            modo_informe = False
            if 'nivel' in tarea: # Solo para limpieza de archivos temporales
                if not utils.confirm_operation("¿Desea ejecutar en modo informe (solo mostrar qué se limpiaría sin eliminar)?"): 
                    if not utils.confirm_operation("ADVERTENCIA: Esta acción eliminará archivos permanentemente. ¿Está seguro de continuar?"):
                        logger.info("Operación de limpieza de archivos temporales cancelada por el usuario.")
                        continue
                else:
                    modo_informe = True
                
                total_recuperado, num_archivos = limpiar_archivos_temporales(nivel=tarea['nivel'], modo_informe=modo_informe)
                logger.info(f"Limpieza de archivos temporales ({tarea['nivel']}) - Recuperado: {total_recuperado / (1024*1024):.2f} MB, Archivos: {num_archivos}")

            elif 'funcion' in tarea: # Para otras funciones de limpieza
                if not utils.confirm_operation(f"¿Está seguro de ejecutar \'{tarea['nombre']}\'? (Esta acción es irreversible)"):
                    logger.info(f"Operación '{tarea['nombre']}' cancelada por el usuario.")
                    continue
                
                tarea['funcion']()

        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            logger.warning(f"Opción de limpieza no válida seleccionada: {opcion}")
