# configurar_entorno_vagrant.py
import os
import shutil
import subprocess
from pathlib import Path
import platform

def configurar_entorno():
    print("Configurando directorios locales para Vagrant...")

    # 1. Crear la estructura de directorios compartidos
    ruta_llaves_compartidas = Path("shared/keys")
    ruta_llaves_compartidas.mkdir(parents=True, exist_ok=True)

    # 2. Generar un par de llaves si no existe
    ruta_llave_privada = Path("ssh_keypair/vm1_to_others")
    carpeta_llaves = ruta_llave_privada.parent
    carpeta_llaves.mkdir(parents=True, exist_ok=True)

    if not ruta_llave_privada.exists():
        print("Generando nuevo par de llaves SSH...")
        try:
            subprocess.run([
                "ssh-keygen",
                "-t", "ed25519",
                "-f", str(ruta_llave_privada),
                "-q",
                "-N", ""
            ], check=True)
        except FileNotFoundError:
            print("Error: no se encontró 'ssh-keygen'. Asegúrate de tener OpenSSH instalado y en tu PATH.")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error al generar la llave SSH: {e}")
            return

    # 3. Copiar la llave pública al directorio compartido para aprovisionamiento
    ruta_llave_publica = ruta_llave_privada.with_suffix(".pub")
    destino_llave_publica = ruta_llaves_compartidas / ruta_llave_publica.name
    shutil.copy2(ruta_llave_publica, destino_llave_publica)

    print("Configuración local completa. Ahora podés ejecutar 'vagrant up'.")

configurar_entorno()

