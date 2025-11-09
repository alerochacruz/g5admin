import os
import platform
import shutil
from datetime import datetime

# Obtener el nombre de usuario de forma multiplataforma usando os
try:
    usuario = os.getlogin()
except OSError:
    usuario = os.environ.get('USERNAME') or os.environ.get('USER')

# Obtener el directorio home del usuario
carpeta_home = os.path.expanduser("~")

# Diccionario de etiquetas para mapear hostname a departamento
etiquetas = {
    "vps2": "GERENCIA",
    "vps3": "VENTAS",
    "vps4": "ARTE"
}

def determinar_departamento():
    hostname_crudo = platform.node()
    for key, nombre_departamento in etiquetas.items():
        if key in hostname_crudo:
            return nombre_departamento
    return "GENERAL"  # fallback si no se encuentra coincidencia

# Determinar el departamento
departamento = determinar_departamento()

# Definir el nombre de la carpeta del departamento
carpeta_departamento = f"PROYECTOS_{departamento}"

# Definir el nombre de la carpeta de backups
carpeta_backups = "BACKUPS"

# Rutas completas
ruta_carpeta_departamento = os.path.join(carpeta_home, carpeta_departamento)
ruta_carpeta_backups = os.path.join(carpeta_home, carpeta_backups)

# Crear la carpeta de backups si no existe
os.makedirs(ruta_carpeta_backups, exist_ok=True)

# Nombre del archivo ZIP con timestamp
# Timestamp: AAAA-MM-DD_HH-MM-SS
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nombre_zip = f"{carpeta_departamento}_{timestamp}"

# Ruta completa del archivo ZIP (sin extensión, shutil lo agrega)
ruta_zip = os.path.join(ruta_carpeta_backups, nombre_zip)

# Comprimir la carpeta
shutil.make_archive(ruta_zip, 'zip', ruta_carpeta_departamento)

print(f"Backup creado exitosamente en: {ruta_zip}.zip")

