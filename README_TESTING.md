# Pruebas y ejecución (OptiTech System Optimizer)

Este archivo describe los pasos recomendados para preparar el entorno en Windows, ejecutar la suite de tests y probar la aplicación interactivamente de manera segura.

Requisitos
- Windows (target), pero el código contiene mocks para permitir pruebas en otras plataformas.
- Python 3.10+ (se probó con Python 3.14 en este entorno).
- Virtualenv (recomendado).

1) Crear y activar entorno virtual (PowerShell)
```powershell
# Desde la raíz del repositorio
python -m venv .venv
# Si PowerShell bloquea la ejecución de scripts temporalmente:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3) Ejecutar tests (unittest)
```powershell
python -m unittest discover -v
```

4) Ejecutar la aplicación en modo no-elevado (útil durante desarrollo)
```powershell
python -m src.main --no-elevate
```
Esto muestra el menú sin intentar re-ejecutar con UAC. Útil para prueba de opciones y modos informe.

5) Ejecutar la aplicación en modo normal (intento de elevación UAC)
```powershell
python -m src.main
```
Al ejecutarlo sin `--no-elevate`, la aplicación intentará re-ejecutarse con privilegios elevados. Windows mostrará el diálogo UAC; si aceptas, la sesión no-elevada saldrá y la aplicación continuará en la sesión elevada.

6) Logs e informes
- Logs: `%LOCALAPPDATA%\OptiTechOptimizer\logs\app.log`
- Informes: `%LOCALAPPDATA%\OptiTechOptimizer\reports\Informe_Analisis_Sistema_*.txt`

7) Recomendaciones de seguridad
- Funciones como limpieza de WinSxS o eliminación de copias de sombra ejecutan comandos nativos (DISM, vssadmin). No las ejecuten en sistemas productivos sin respaldos y sin comprender su impacto.
- Prefiere "modo informe" antes de ejecutar limpiezas destructivas.

8) Desarrollo y CI
- Añadir una opción CLI `--no-elevate` (ya incluida) mejora las pruebas en CI y desarrollo.
- Para integración continua en GitHub Actions, usar `windows-latest` runner y ejecutar `python -m unittest discover -v`.

9) Solución de problemas
- Si `Activate.ps1` falla por política de ejecución, ejecutar el comando `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force`.
- Si la elevación abre una ventana que se cierra de golpe, asegúrate de que el proyecto se ejecute con `python -m src.main` (la invocación por módulo evita abrir otra ventana en algunos entornos). Este proyecto ya intenta usar `-m src.main` durante elevación.

Contacto
- Para cambios o pruebas avanzadas, crea un branch y un PR; puedo ayudar a añadir GH Actions o tests adicionales.
