# Fuente Box Debian 12:
# https://portal.cloud.hashicorp.com/vagrant/discover/debian/bookworm64

Vagrant.configure("2") do |config|
  # Nodo "Sistemas" (vps1) | 2 cores | 2 GB RAM
  config.vm.define "vps1_sistemas" do |node|
    node.vm.box = "debian/bookworm64"
    node.vm.box_version = "12.20250126.1"
    node.vm.hostname = "vps1.sistemas.local"
    # Ajustar el nombre del adaptador de red ("bridge") y la IP según
    # la configuración local del sistema afitrión.
    node.vm.network "public_network", bridge: "wlo1", ip: "192.168.0.250"
    
    # Carpeta compartida
    node.vm.synced_folder "./shared/", "/home/vagrant/REPOSITORIO"

    node.vm.provider "virtualbox" do |vb|
      vb.name = "prog--vps1_sistemas"
      vb.memory = 2048
      vb.cpus = 2
    end

    # Operaciones con privilegio (como "root")
    node.vm.provision "shell", inline: <<-SHELL
      echo "vps1.sistemas.local" > /etc/hostname
      hostnamectl set-hostname vps1.sistemas.local
      
      # Install packages
      apt update
      apt install python3.11-venv --yes
      apt install python3-psutil --yes
      # Discouraged by Debian (use venv pip instead)
      apt install python3-pip --yes
    SHELL

    # Operaciones sin privilegio (como usuario "vagrant")
    node.vm.provision "shell", privileged: false, inline: <<-SHELL
      mkdir -p /home/vagrant/PROYECTOS_SISTEMAS
      mkdir -p /home/vagrant/BACKUPS
      mkdir -p /home/vagrant/LOGS

      mkdir -p /home/vagrant/.ssh
      chown vagrant:vagrant /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh
    SHELL

    # Provisión de la llave privada
    node.vm.provision "file", source: "./ssh_keypair/vm1_to_others", destination: "/home/vagrant/.ssh/id_ed25519"

    # Establecer permisos de la llave privada
    node.vm.provision "shell", inline: <<-SHELL
      chown vagrant:vagrant /home/vagrant/.ssh/id_ed25519
      chmod 600 /home/vagrant/.ssh/id_ed25519
    SHELL
  end

  # Nodo "Gerencia" (vps2) | 1 Core | 1 GB RAM
  config.vm.define "vps2_gerencia" do |node|
    node.vm.box = "debian/bookworm64"
    node.vm.box_version = "12.20250126.1"
    node.vm.hostname = "vps2.gerencia.local"
    # Ajustar el nombre del adaptador de red ("bridge") y la IP según
    # la configuración local del sistema afitrión.
    node.vm.network "public_network", bridge: "wlo1", ip: "192.168.0.251"
    
    # Carpeta compartida
    node.vm.synced_folder "./shared/", "/home/vagrant/REPOSITORIO"

    node.vm.provider "virtualbox" do |vb|
      vb.name = "prog--vps2_gerencia"
      vb.memory = 1024
      vb.cpus = 1
    end

    # Operaciones con privilegio (como "root")
    node.vm.provision "shell", inline: <<-SHELL
      echo "vps2.gerencia.local" > /etc/hostname
      hostnamectl set-hostname vps2.gerencia.local

      # Install packages
      apt update
      apt install python3.11-venv --yes
      apt install python3-psutil --yes
      # Discouraged by Debian (use venv pip instead)
      apt install python3-pip --yes
    SHELL

    # Operaciones sin privilegio (como usuario "vagrant")
    node.vm.provision "shell", privileged: false, inline: <<-SHELL
      mkdir -p /home/vagrant/PROYECTOS_GERENCIA
      mkdir -p /home/vagrant/BACKUPS
      mkdir -p /home/vagrant/LOGS

      cat /home/vagrant/REPOSITORIO/keys/vm1_to_others.pub >> /home/vagrant/.ssh/authorized_keys
      chown -R vagrant:vagrant /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh
      chmod 600 /home/vagrant/.ssh/authorized_keys
    SHELL
  end

  # Nodo "Ventas" (vps3) | 2 cores | 2 GB RAM
  config.vm.define "vps3_ventas" do |node|
    node.vm.box = "debian/bookworm64"
    node.vm.box_version = "12.20250126.1"
    node.vm.hostname = "vps3.ventas.local"
    # Ajustar el nombre del adaptador de red ("bridge") y la IP según
    # la configuración local del sistema afitrión.
    node.vm.network "public_network", bridge: "wlo1", ip: "192.168.0.252"

    # Carpeta compartida
    node.vm.synced_folder "./shared/", "/home/vagrant/REPOSITORIO"

    node.vm.provider "virtualbox" do |vb|
      vb.name = "prog--vps3_ventas"
      vb.memory = 2048
      vb.cpus = 2
    end

    # Operaciones con privilegio (como "root")
    node.vm.provision "shell", inline: <<-SHELL
      echo "vps3.ventas.local" > /etc/hostname
      hostnamectl set-hostname vps3.ventas.local

      # Install packages
      apt update
      apt install python3.11-venv --yes
      apt install python3-psutil --yes
      # Discouraged by Debian (use venv pip instead)
      apt install python3-pip --yes
    SHELL

    # Operaciones sin privilegio (como usuario "vagrant")
    node.vm.provision "shell", privileged: false, inline: <<-SHELL
      mkdir -p /home/vagrant/PROYECTOS_VENTAS
      mkdir -p /home/vagrant/BACKUPS
      mkdir -p /home/vagrant/LOGS

      cat /home/vagrant/REPOSITORIO/keys/vm1_to_others.pub >> /home/vagrant/.ssh/authorized_keys
      chown -R vagrant:vagrant /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh
      chmod 600 /home/vagrant/.ssh/authorized_keys
    SHELL
  end
end

# PENDIENTES
# Intentar incorporar nodo con Windows 10
# https://portal.cloud.hashicorp.com/vagrant/discover/gusztavvargadr/windows-10

