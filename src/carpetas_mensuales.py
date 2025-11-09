import os
import platform

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

# Definir el nombre de la carpeta del departamento
departamento = f"PROYECTOS_{determinar_departamento()}"

# Lista de carpetas mensuales
carpetas_mensuales = [
    "001_ENERO",
    "002_FEBRERO",
    "003_MARZO",
    "004_ABRIL",
    "005_MAYO",
    "006_JUNIO",
    "007_JULIO",
    "008_AGOSTO",
    "009_SEPTIEMBRE",
    "010_OCTUBRE",
    "011_NOVIEMBRE",
    "012_DICIEMBRE",
]

# Crear carpetas mensuales dentro del ciclo/año
for nombre_de_carpeta in carpetas_mensuales:
    ruta_completa = os.path.join(carpeta_home, departamento, nombre_de_carpeta)
    try:
        os.makedirs(ruta_completa, exist_ok=True)
        print(f"Carpeta creada exitosamente: {ruta_completa}")
    except Exception as e:
        print(f"Error creando carpeta {ruta_completa}: {e}")

