# Checklist: Implementación del Módulo de Optimización de Servicios

Este checklist detalla los pasos para implementar y mejorar la funcionalidad de optimización de servicios, siguiendo un enfoque de TDD y las mejores prácticas.

## Fase 1: Preparación y Configuración

- [x] **1. Crear archivo de configuración para servicios:**
    - Crear `config/services_to_optimize.json` con una estructura que defina los servicios a optimizar, su descripción, el estado recomendado (`disabled`, `manual`), y un nivel de riesgo (`bajo`, `medio`, `alto`).
    - Incluir los servicios `DiagTrack` y `dmwappushservice` inicialmente, y algunos de los servicios adicionales discutidos.
- [x] **2. Actualizar `config_manager.py`:**
    - Añadir funcionalidad para cargar y parsear el nuevo archivo `services_to_optimize.json`.
    - Asegurar que el `config_manager` pueda manejar la estructura definida.
- [x] **3. Crear pruebas unitarias para `config_manager`:**
    - Verificar que el `config_manager` carga correctamente el archivo `services_to_optimize.json` y que los datos son accesibles.

## Fase 2: Refactorización y Lógica del Módulo

- [ ] **4. Refactorizar `system_optimizer.py` (o módulo de servicios):**
    - Modificar la función de optimización de servicios para que lea la lista de servicios y sus configuraciones desde `config_manager`.
    - Implementar la lógica para iterar sobre los servicios y aplicar los cambios.
- [ ] **5. Mejorar el manejo de errores y logging:**
    - Cuando un servicio no se encuentre, registrar un mensaje de advertencia claro y no intentar modificarlo.
    - Registrar el estado original del servicio antes de cualquier cambio.
    - Registrar el resultado de la operación (éxito/fallo y el cambio realizado).
- [ ] **6. Implementar la reversibilidad (opcional pero recomendado):**
    - Antes de modificar un servicio, guardar su estado original (tipo de inicio).
    - Añadir una función para restaurar los servicios a su estado original.
- [ ] **7. Crear pruebas unitarias para el módulo de optimización de servicios:**
    - Mockear las interacciones con el sistema operativo para simular el cambio de estado de los servicios.
    - Verificar que la lógica de lectura de configuración y aplicación de cambios funciona correctamente.
    - Probar el manejo de servicios no encontrados.

## Fase 3: Interfaz de Usuario y Experiencia

- [ ] **8. Actualizar `main.py`:**
    - Modificar la interacción con el usuario para el módulo de optimización de servicios.
    - Mostrar la descripción y el nivel de riesgo de cada servicio antes de pedir confirmación.
    - Ofrecer la opción de confirmar la optimización por servicio o una confirmación general.
    - Si se implementó, añadir la opción de restaurar los servicios.

## Fase 4: Documentación y Finalización

- [ ] **9. Actualizar `README.md` y `TASKS.md`:**
    - Reflejar el progreso y la finalización de esta tarea.
- [ ] **10. Commit de los cambios:**
    - Realizar un commit con un mensaje claro y en español.
- [ ] **11. Crear Pull Request (si aplica):**
    - Abrir una PR para fusionar la rama de funcionalidad a `main`.
