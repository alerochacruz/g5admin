#!/usr/bin/env python3
import subprocess

# Diccionario con información de las nodos destino
hosts = [
    {
        "etiqueta": "vps2",
        "usuario": "vagrant",
        "ip": "192.168.0.251",
        "sistema_operativo": "debian12",
        "ejecutable": "python3",
        "hostname_full": "vps2.gerencia.local"
    },
    {
        "etiqueta": "vps3",
        "usuario": "vagrant",
        "ip": "192.168.0.252",
        "sistema_operativo": "debian12",
        "ejecutable": "python3",
        "hostname_full": "vps3.ventas.local"
    },
    {
        "etiqueta": "vps4",
        "usuario": "clementina",
        "ip": "192.168.0.253",
        "sistema_operativo": "windows10",
        "ejecutable": "py",
        "hostname_full": "vps3.arte.local"
    }
]

# Ruta remota del script a ejecutar
ruta_remota_script = "REPOSITORIO/scripts/uso_de_recursos.py"

# Ruta del archivo único de historial
ruta_historial = "/home/vagrant/LOGS/historial_uso_de_recursos.txt"

for host in hosts:
    destino = host["ip"]
    usuario = host["usuario"]
    etiqueta_host = host["etiqueta"]
    ejecutable = host["ejecutable"]

    # Comando remoto
    comando_remoto = f"{ejecutable} {ruta_remota_script}"

    print(f"\nConectando a \"{etiqueta_host}\" ({destino}) como \"{usuario}\" y ejecutando {ruta_remota_script}...")

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
            f.write(resultado.stdout + "\n")

        print(f"Script ejecutado correctamente en {etiqueta_host} ({destino}).")
        print(f"Resultado añadido a {ruta_historial}")

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando remoto en {etiqueta_host} ({destino}):")
        print(e.stderr)

