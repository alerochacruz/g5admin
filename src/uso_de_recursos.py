import psutil
import platform
from datetime import datetime

etiquetas = {
    "vps2": "vps2.gerencia.local",
    "vps3": "vps3.ventas.local",
    "vps4": "vps4.arte.local"
}

def determinar_hostname_full():
    hostname_crudo = platform.node()
    for key, hostname_full in etiquetas.items():
        if key in hostname_crudo:
            return hostname_full
    return hostname_crudo  # fallback a hostname crudo si no hay match

def determinar_sistema_operativo():
    if platform.system() == "Windows":
        return "Windows 10"
    else:
        return "Debian 12"

def bytes_to_mb(bytes_val):
    return round(bytes_val / (1024 ** 2), 2)

def bytes_to_gb(bytes_val):
    return round(bytes_val / (1024 ** 3), 2)

# CPU
cpu_usado = psutil.cpu_percent(interval=1)
cpu_cores = psutil.cpu_count(logical=False)

# Memoria RAM
ram = psutil.virtual_memory()
ram_usada_mb = bytes_to_mb(ram.used)
ram_total_gb = bytes_to_gb(ram.total)
ram_percent = ram.percent

# Disco
disco = psutil.disk_usage('/')
disco_usado_gb = bytes_to_gb(disco.used)
disco_total_gb = bytes_to_gb(disco.total)
disco_porcentaje = disco.percent

# Timestamp: AAAA-MM-DD HH:MM:SS
def obtener_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Salida
print(f"Hostname: {determinar_hostname_full()}")
print(f"Sistema Operativo: {determinar_sistema_operativo()}")
print(f"Timestamp: {obtener_timestamp()}")
print(f"CPU: {cpu_usado} %")
print(f"vCores: {cpu_cores}")
print(f"Memoria RAM: {ram_usada_mb} MB / {ram_total_gb} GB ({ram_percent}%)")
print(f"Disco: {disco_usado_gb} GB / {disco_total_gb} GB ({disco_porcentaje}%)")

