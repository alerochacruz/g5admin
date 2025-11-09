#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

# Diccionario con información de los nodos destino
hosts = {
    "vps2": {
        "usuario": "vagrant",
        "ip": "192.168.0.251",
        "sistema_operativo": "debian12",
        "ejecutable": "python3",
        "hostname_full": "vps2.gerencia.local"
    },
    "vps3": {
        "usuario": "vagrant",
        "ip": "192.168.0.252",
        "sistema_operativo": "debian12",
        "ejecutable": "python3",
        "hostname_full": "vps3.ventas.local"
    },
    "vps4": {
        "usuario": "clementina",
        "ip": "192.168.0.253",
        "sistema_operativo": "windows10",
        "ejecutable": "py",
        "hostname_full": "vps4.arte.local"
    }
}

# Ruta remota del script de backups
ruta_remota_script = "REPOSITORIO/scripts/crear_backup.py"

# Ruta del archivo único de historial
ruta_historial = "/home/vagrant/LOGS/historial_backups.txt"

# Validar argumento
if len(sys.argv) != 2:
    print("Uso: python ejecutar_backups.py <etiqueta_host>")
    sys.exit(1)

etiqueta = sys.argv[1]

if etiqueta not in hosts:
    print(f"Etiqueta \"{etiqueta}\" no reconocida. Las opciones válidas son: {', '.join(hosts.keys())}")
    sys.exit(1)

# Obtener datos del host
host = hosts[etiqueta]
usuario = host["usuario"]
destino = host["ip"]
ejecutable = host["ejecutable"]

# Comando remoto
comando_remoto = f"{ejecutable} {ruta_remota_script}"

# Timestamp: AAAA-MM-DD HH:MM:SS
def obtener_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"\nConectando a \"{etiqueta}\" ({destino}) como \"{usuario}\" y ejecutando {ruta_remota_script}...")

try:
    # Ejecutar el script remoto por SSH
    resultado = subprocess.run(
        ["ssh", f"{usuario}@{destino}", comando_remoto],
        capture_output=True,
        text=True,
        check=True
    )

    # Añadir la salida al archivo de historial
    with open(ruta_historial, "a") as f:
        f.write(f"{obtener_timestamp()} Resultado en {host['hostname_full']} ({destino})\n")
        f.write(resultado.stdout + "\n")

    print(f"Backup ejecutado correctamente en {etiqueta} ({destino}).")
    print(f"Resultado añadido a {ruta_historial}")

except subprocess.CalledProcessError as e:
    print(f"Error al ejecutar el comando remoto en {etiqueta} ({destino}):")
    print(e.stderr)

