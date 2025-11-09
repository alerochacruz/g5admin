# Automatizaciones distribuidas con Python

—GRUPO 5

Este repositorio contiene una colección de scripts desarrollados para automatizar tareas administrativas en una infraestructura distribuida, utilizando Python y sus módulos estándar: `subprocess`, `os` y `shutil`.

## Infraestructura simulada

Las automatizaciones están diseñadas para ejecutarse desde un nodo central (`vps1.sistemas.local`) hacia tres nodos remotos:

| Hostname              | IP             | Usuario     | Sistema Operativo  | Sector     |
|-----------------------|----------------|-------------|--------------------|------------|
| vps1.sistemas.local   | 192.168.0.250  | vagrant     | Debian 12          | Sistemas   |
| vps2.gerencia.local   | 192.168.0.251  | vagrant     | Debian 12          | Gerencia   |
| vps3.ventas.local     | 192.168.0.252  | vagrant     | Debian 12          | Ventas     |
| vps4.arte.local       | 192.168.0.253  | clementina  | Windows 10         | Arte       |

## Automatizaciones disponibles

### Automatización N.º 1: Uso de recursos del sistema

- **Script principal:** `obtener_uso_de_recursos.py`
- **Script remoto:** `uso_de_recursos.py`
- **Funcionalidad:** Ejecuta remotamente un script que recolecta métricas de CPU, RAM y disco en cada nodo. Los resultados se almacenan en `LOGS/historial_uso_de_recursos.txt`.

### Automatización N.º 2: Creación de carpetas mensuales

- **Script principal:** `iniciar_carpetas_mensuales.py`
- **Script remoto:** `carpetas_mensuales.py`
- **Funcionalidad:** Crea una estructura de carpetas mensuales dentro de una carpeta de proyectos departamentales en el home del usuario remoto. Los resultados se registran en `LOGS/historial_carpetas_mensuales.txt`.

### Automatización N.º 3: Generación de backups comprimidos

- **Script principal:** `iniciar_backups.py`
- **Script remoto:** `crear_backup.py`
- **Funcionalidad:** Comprime la carpeta de proyectos del departamento en un archivo ZIP con timestamp. El archivo se guarda en una carpeta `BACKUPS` en el home del usuario. El historial se guarda en `LOGS/historial_backups.txt`.

## Requisitos

- Python 3.x instalado en todos los nodos.
- Conectividad SSH entre `vps1` y los nodos remotos.
- Llaves SSH configuradas para acceso sin contraseña.
- Módulos parte de la biblioteca estándar de Python: `subprocess`, `os`, `shutil`, `platform`, `datetime`.
- Módulo externo de Python: `psutil`.

> Nota: El módulo `psutil`, necesario para la Automatización N.º 1, es instalado automáticamente por Vagrant en los nodos Debian durante el aprovisionamiento. Para instalar `psutil` en el nodo Windows:
> ```powershell
> py -m pip install psutil
> ```

## Ejecución

Desde el nodo central (`vps1`), ejecutar:

```text
./obtener_uso_de_recursos.py
./iniciar_carpetas_mensuales.py <etiqueta_host>
./iniciar_backups.py <etiqueta_host>
```

Donde `<etiqueta_host>` puede ser: `vps2`, `vps3` o `vps4`.

## Infraestructura con Vagrant

Este proyecto utiliza [Vagrant](https://www.vagrantup.com/) junto con [VirtualBox](https://www.virtualbox.org/) para simular una infraestructura distribuida compuesta por múltiples máquinas virtuales. Cada nodo representa un sector organizacional distinto y está configurada con Debian 12.

### Box utilizada

- **Nombre:** `debian/bookworm64`
- **Versión:** `12.20250126.1`
- **Fuente:** [HashiCorp Cloud Portal](https://portal.cloud.hashicorp.com/vagrant/discover/debian/bookworm64)

### Máquinas virtuales definidas

| VM                | Hostname              | IP             | RAM   | CPU | Usuario     | Sector     |
|-------------------|-----------------------|----------------|-------|-----|-------------|------------|
| vps1_sistemas     | vps1.sistemas.local   | 192.168.0.250  | 2 GB  | 2   | vagrant     | Sistemas   |
| vps2_gerencia     | vps2.gerencia.local   | 192.168.0.251  | 1 GB  | 1   | vagrant     | Gerencia   |
| vps3_ventas       | vps3.ventas.local     | 192.168.0.252  | 2 GB  | 2   | vagrant     | Ventas     |

> Nota: El nodo `vps4.arte.local` con Windows 10, por el momento, no se gestiona vía Vagrant en este repositorio.

### Provisión automática

Cada VM se configura automáticamente con:

- Hostname personalizado
- Carpeta compartida `REPOSITORIO` sincronizada con el sistema anfitrión
- Carpetas internas: `PROYECTOS_<DEPARTAMENTO>`, `BACKUPS`, `LOGS`
- Claves SSH para conexión sin contraseña desde `vps1`
- Instalación de paquetes necesarios:
  - `python3.11-venv`
  - `python3-psutil`
  - `python3-pip` (incluido por completitud; en proceso de investigación)

### Uso

Para generar las llaves SSH y estructura de carpetas compartidas, ejecute el siguiente script:

```bash
python3 configurar_entorno_vagrant.py
```

Para levantar la infraestructura:

```bash
vagrant up
```

Para destruirla:

```bash
vagrant destroy
```

Para acceder a una VM:

```bash
vagrant ssh vps1_sistemas
```

> Asegúrese de tener instalado [Vagrant](https://www.vagrantup.com/downloads) y [VirtualBox](https://www.virtualbox.org/wiki/Downloads) antes de iniciar.

#### Confianza SSH (`known_hosts`)

Para asegurar que la máquina virtual principal (`vps1_sistemas`, IP `192.168.0.250`) pueda conectarse a las otras máquinas virtuales (`vps2_gerencia`, `vps3_ventas`, `vps4_arte`) a través de SSH sin recibir advertencias de seguridad sobre llaves de host desconocidas, deben añadirse las llaves públicas de los *hosts* de destino al archivo `known_hosts` de la máquina de origen.

Ejecute los siguientes comandos **dentro de la máquina virtual `vps1_sistemas`**, después de usar `vagrant ssh vps1_sistemas`:

```bash
ssh-keyscan -H 192.168.0.251 >> ~/.ssh/known_hosts
ssh-keyscan -H 192.168.0.252 >> ~/.ssh/known_hosts
ssh-keyscan -H 192.168.0.253 >> ~/.ssh/known_hosts
```

Resultado: Esto permite que `vps1_sistemas` se conecte automáticamente —sin requerir interacción del usuario— a las otras VMs usando la llave SSH aprovisionada, facilitando tareas de automatización o administración remota.

Importante: El uso de `ssh-keyscan` de esta manera es apropiado y conveniente para entornos de desarrollo/laboratorio. Sin embargo, en entornos de producción reales, se recomienda verificar la huella digital (fingerprint) del *host* de destino manualmente la primera vez que se conecta.

## Licencia

Este proyecto es para uso académico y educativo. Puede adaptarse libremente para fines de aprendizaje propios.

