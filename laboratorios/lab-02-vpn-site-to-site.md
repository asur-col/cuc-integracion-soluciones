# Lab 2 — VPN Site-to-Site OPNsense: WordPress con base de datos remota

**Curso:** Integración de Soluciones para Plataformas Cloud — Ingeniería de Sistemas
**Docente:** Ing. Rodolfo Cañas Cervantes — Universidad de la Costa (CUC) · 2026-2
**Duración estimada:** 120 min · **Modalidad:** VirtualBox local (4 VMs)
**Tipo:** laboratorio práctico complementario — **sin nota**; se valida con el auto-check de la sección 10
**Guía visual:** esta es la versión técnica cruda; la guía ilustrada con diagramas es `lab-02-vpn-site-to-site-opnsense.html`

> Ejecución técnica, diagnóstico y documentación: **ox-alpha**, modelo IA de lenguaje.
> Dirección académica y arquitectura: **Ing. Rodolfo Cañas Cervantes**.
> Todo lo aquí documentado fue ejecutado y validado en infraestructura real antes de publicarse.
>
> **v2 — qué cambió:** los servers ya NO se instalan (se descargan listos desde OSBoxes con
> escritorio ligero), los firewalls se administran desde el navegador de los propios servers
> (nada de administrar desde "tu PC" dentro de la red WAN), y todos los bloques de comandos
> son copiar-pegar gracias al portapapeles bidireccional de VirtualBox.

---

## 0. Descargas previas — hazlas ANTES de clase

| Elemento | Detalle | Fuente |
|---|---|---|
| VirtualBox ≥ 7.0 | Hipervisor local — 4 VMs simultáneas | `virtualbox.org/wiki/Downloads` |
| OPNsense ISO (×1) | DVD amd64, variante **vga** — la misma ISO sirve para ambos firewalls | `opnsense.org/download` |
| Lubuntu 24.04 VDI (×1) | Imagen de disco lista con escritorio ligero LXQt — se clona para SERVER-B | `osboxes.org/lubuntu` |
| RAM del host | Recomendado 16 GB (mínimo 12 GB) | 2 GB por firewall + 2 GB por server |

Credenciales de la imagen OSBoxes: usuario `osboxes`, password `osboxes.org` (el mismo aplica para `sudo`).

> ⚠ Son ~3 GB de descarga entre la ISO y el VDI. No lo dejes para la hora de clase.

### VMs a crear

| VM | vCPU | RAM | Disco | Adaptador 1 | Adaptador 2 |
|---|---|---|---|---|---|
| ROUTER-A | 1 | 2 GB | 20 GB nuevo + ISO | NAT Network `WANLAB` | Internal `LAN-A` |
| ROUTER-B | 1 | 2 GB | 20 GB nuevo + ISO | NAT Network `WANLAB` | Internal `LAN-B` |
| SERVER-A | 2 | 2 GB | VDI OSBoxes | Internal `LAN-A` | — |
| SERVER-B | 2 | 2 GB | VDI OSBoxes (clon) | Internal `LAN-B` | — |

---

## 1. Topología objetivo

```
                ┌──────────────────────────────────────────┐
                │   WANLAB (NAT Network VirtualBox)        │
                │   172.10.20.0/24 — "internet" del lab     │
                └───────┬──────────────────────┬───────────┘
                        |                      |
               WAN em0 .20.224          WAN em0 .20.128
                ROUTER-A (OPNsense)     ROUTER-B (OPNsense)
                LAN em1 10.0.0.1        LAN em1 20.0.0.1
                wg0 10.99.0.1           wg0 10.99.0.2
                        |   ══ túnel WireGuard ══  |
                 Internal LAN-A            Internal LAN-B
                        |                      |
                SERVER-A 10.0.0.101    SERVER-B 20.0.0.101
                Lubuntu + WordPress    Lubuntu + MariaDB :3306
                        └── MySQL :3306 SOLO por el túnel ──┘
```

| Componente | Interfaz | IP |
|---|---|---|
| ROUTER-A | em0 / em1 / wg0 | 172.10.20.224 · 10.0.0.1 · 10.99.0.1 |
| SERVER-A | enp0s3 | 10.0.0.101 (WordPress :80) |
| ROUTER-B | em0 / em1 / wg0 | 172.10.20.128 · 20.0.0.1 · 10.99.0.2 |
| SERVER-B | enp0s3 | 20.0.0.101 (MariaDB :3306) |
| Túnel | wg0 | 10.99.0.0/30 |

> ⚠ Las IP WAN dependen de la NAT Network que crees. Este lab usa `172.10.20.x`;
> si usas otra subred, sustitúyela manteniendo la lógica intacta.

### Variables del lab — edítalas aquí una sola vez

| Variable | Valor del lab | Dónde se usa |
|---|---|---|
| Subred WANLAB | `172.10.20.0/24` | NAT Network en VirtualBox |
| LAN sitio A / B | `10.0.0.0/24` / `20.0.0.0/24` | LAN de cada firewall |
| Red del túnel | `10.99.0.0/30` | wg0 en ambos routers |
| Clave MySQL / admin WP | `WPLab2026!` | usuario `wpuser`, wp-config, wp-cli |

---

## 2. Redes en VirtualBox (5 min)

1. **Archivo → Herramientas → Administrador de red → NAT Networks → Crear**: nombre `WANLAB`, prefijo `172.10.20.0/24`, DHCP activado.
2. Las Internal Networks `LAN-A` y `LAN-B` no se crean aparte: se escriben directo en el adaptador de cada VM (Conectado a: **Red interna**, Nombre: `LAN-A` o `LAN-B`).

> ☠ CRÍTICO — el error más común del lab: conectar los dos servers a la MISMA internal
> network "por si acaso". Si LAN-A y LAN-B se tocan, la VPN pierde todo el sentido y las
> pruebas darán falsos positivos.

---

## 3. ROUTER-A y ROUTER-B — instalación y bootstrap por consola (~25 min)

Esto es lo ÚNICO que se digita directo en la consola de VirtualBox. Todo lo demás va por navegador o SSH con copiar-pegar.

### 3.1 Instalar OPNsense (×2)

1. Arranca desde la ISO → login `installer` / password `opnsense`.
2. Acepta defaults: teclado, **ZFS stripe** (o UFS, indistinto en lab), disco completo.
3. Al terminar: apaga, retira la ISO (Dispositivos → Unidades ópticas → Expulsar), arranca desde disco.
4. Credenciales de consola: `root` / `opnsense`.

### 3.2 Asignar interfaces y LAN (menú de consola)

```
Opción 1) Assign Interfaces
  LAN → em1   (Adapter 2, la internal network)
  WAN → em0   (Adapter 1, la NAT network)

Opción 2) Set interface(s) IP address → LAN
  ¿DHCP? NO
  IP:  10.0.0.1/24    (ROUTER-A)
       20.0.0.1/24    (ROUTER-B)
  IPv6: ninguno (Enter)
  ¿Habilitar DHCP server en LAN? SÍ   ← temporal; lo migramos a Kea en la fase 5
    Rango: 10.0.0.100 - 10.0.0.200    (ROUTER-A)
           20.0.0.100 - 20.0.0.200    (ROUTER-B)
```

La WAN queda por DHCP de la propia NAT Network (recibirá alguna `172.10.20.x`). Anótala — la necesitas para el `Endpoint` del túnel en la fase 6.

> ⚠ Si inviertes WAN/LAN, el lab entero se comporta raro. Verifica siempre con la opción 1 que LAN sea `em1`.
>
> 💡 Si tu versión de OPNsense ya no ofrece habilitar DHCP desde la consola, dale al server
> una IP temporal estática (10.0.0.10/24 gw 10.0.0.1) desde su applet de red y salta directo a la fase 5.

### 3.3 ¿Por qué ya no hay que abrir reglas WAN para administrar?

OPNsense trae en LAN una regla anti-lockout que permite TODO el tráfico desde la red LAN. Como los servers tienen navegador y viven dentro de cada LAN, la webGUI queda disponible de inmediato:

- ROUTER-A → `https://10.0.0.1` desde el navegador de SERVER-A
- ROUTER-B → `https://20.0.0.1` desde el navegador de SERVER-B

Acepta el certificado autofirmado. Login: `root` / `opnsense`.

> 💡 Las reglas WAN de administración (abrir 22/443 hacia la WAN) ya NO son necesarias en
> esta versión del lab — quedan como anexo D opcional. La lección de `reply-to` sigue viva:
> la necesitarás para la regla UDP 51820 del túnel (fase 6.4).

### 3.4 Habilitar SSH en cada firewall (para copiar-pegar por terminal)

Desde el navegador del server correspondiente:

1. **System → Settings → Administration → Secure Shell**: marca **Enable Secure Shell** y **Permit password login** → Save.
2. En el server abre una terminal (LXTerminal) y conéctate:

```bash
# desde SERVER-A:
ssh root@10.0.0.1        # acepta el fingerprint · password: opnsense

# desde SERVER-B:
ssh root@20.0.0.1
```

A partir de aquí, todo lo que hagas en los routers es copiar-pegar dentro de esa sesión SSH.

---

## 4. SERVER-A y SERVER-B desde OSBoxes (~10 min)

### 4.1 Crear las VMs sin instalar nada

1. Descarga y descomprime el VDI de **Lubuntu 24.04** desde `osboxes.org/lubuntu`.
2. VirtualBox → **Nueva**:
   - Nombre `SERVER-A`, Tipo Linux, Versión Ubuntu (64-bit)
   - 2048 MB RAM, 2 vCPU
   - Disco duro: **"Usar un archivo de disco duro virtual existente"** → selecciona el `.vdi` descargado
3. Clona: clic derecho sobre SERVER-A → **Clonar** → nombre `SERVER-B`, **Clonación completa**, política MAC: **Generar nuevas direcciones MAC en todas las interfaces**.
4. Red: SERVER-A → Adaptador 1 = Red interna `LAN-A` · SERVER-B → Adaptador 1 = Red interna `LAN-B`.

### 4.2 Primer arranque (en cada server)

1. Login: `osboxes` / `osboxes.org`.
2. Teclado latinoamericano (la imagen viene en inglés): menú → **Preferences → LXQt settings → Keyboard and Mouse → Keyboard → Add → Spanish (Latin American)** y súbelo al tope. Sin esto, la clave `WPLab2026!` saldrá mal digitada.
3. Portapapeles: menú de la ventana de la VM → **Dispositivos → Portapapeles compartido → Bidireccional** (las Guest Additions ya vienen instaladas en la imagen; si no funcionara, **Dispositivos → Insertar imagen de CD de las Guest Additions** y sigue el instalador).
4. Renombra cada equipo para no confundirlos:

```bash
# en SERVER-A:
sudo hostnamectl set-hostname server-a

# en SERVER-B:
sudo hostnamectl set-hostname server-b
```

5. Verifica que el DHCP del firewall les dio IP:

```bash
ip -br addr        # SERVER-A debe mostrar 10.0.0.1xx · SERVER-B 20.0.0.1xx
ip route           # default via 10.0.0.1   (o 20.0.0.1 en B)
ping -c2 10.0.0.1  # el firewall responde  (20.0.0.1 en B)
```

> 💡 Si un server no toma IP: revisa que su adaptador esté en la internal network correcta y
> que en la consola del firewall la opción 1 muestre `em1 UP`.

---

## 5. DHCP serio: migración de dhcpd a Kea (~15 min)

El DHCP que habilitaste en la consola (ISC dhcpd) es el clásico; OPNsense moderno usa **Kea**. Aquí lo migramos como se hace en producción.

### 5.1 Camino GUI (desde el navegador del server)

1. **Services → Kea DHCP → Dhcpv4 → Subnets → +**:
   - ROUTER-A: subnet `10.0.0.0/24`, pool `10.0.0.100 - 10.0.0.200`, option-data routers `10.0.0.1`, DNS `8.8.8.8, 1.1.1.1`
   - ROUTER-B: subnet `20.0.0.0/24`, pool `20.0.0.100 - 20.0.0.200`, option-data routers `20.0.0.1`, DNS `8.8.8.8, 1.1.1.1`
2. Habilita Kea (**Services → Kea DHCP → General → Enable**) y desactiva el clásico si aparece habilitado (**Services → ISC DHCPv4 → LAN → Enable: desmarcado**).

### 5.2 Camino JSON (lo que hicimos en producción) — copiar-pegar por SSH

ROUTER-A — archivo completo `/usr/local/etc/kea/kea-dhcp4.conf`:

```bash
cat > /usr/local/etc/kea/kea-dhcp4.conf <<'KEA'
{
  "Dhcp4": {
    "interfaces-config": { "interfaces": ["em1"] },
    "control-socket": { "socket-type": "unix",
                        "socket-name": "/var/run/kea/kea4-ctrl-socket" },
    "lease-database": { "type": "memfile",
                        "name": "/var/db/kea/kea-leases4.csv", "persist": true },
    "valid-lifetime": 7200, "renew-timer": 1800, "rebind-timer": 3600,
    "subnet4": [ {
      "id": 1,
      "subnet": "10.0.0.0/24",
      "pools": [ { "pool": "10.0.0.100 - 10.0.0.200" } ],
      "option-data": [
        { "name": "routers",             "data": "10.0.0.1" },
        { "name": "domain-name-servers", "data": "8.8.8.8, 1.1.1.1" }
      ]
    } ],
    "loggers": [ { "name": "kea-dhcp4",
      "output-options": [ { "output": "/var/log/kea/kea-dhcp4.log" } ],
      "severity": "INFO" } ]
  }
}
KEA
service kea restart
```

ROUTER-B — el archivo completo, sin "espejo": cópialo tal cual (cambia subnet, pools y routers):

```bash
cat > /usr/local/etc/kea/kea-dhcp4.conf <<'KEA'
{
  "Dhcp4": {
    "interfaces-config": { "interfaces": ["em1"] },
    "control-socket": { "socket-type": "unix",
                        "socket-name": "/var/run/kea/kea4-ctrl-socket" },
    "lease-database": { "type": "memfile",
                        "name": "/var/db/kea/kea-leases4.csv", "persist": true },
    "valid-lifetime": 7200, "renew-timer": 1800, "rebind-timer": 3600,
    "subnet4": [ {
      "id": 1,
      "subnet": "20.0.0.0/24",
      "pools": [ { "pool": "20.0.0.100 - 20.0.0.200" } ],
      "option-data": [
        { "name": "routers",             "data": "20.0.0.1" },
        { "name": "domain-name-servers", "data": "8.8.8.8, 1.1.1.1" }
      ]
    } ],
    "loggers": [ { "name": "kea-dhcp4",
      "output-options": [ { "output": "/var/log/kea/kea-dhcp4.log" } ],
      "severity": "INFO" } ]
  }
}
KEA
service kea restart
```

### 5.3 Validación

```bash
# en cada ROUTER (sesión SSH):
sockstat -l | grep '\.67'           # Kea escuchando DHCP ✓
tail -f /var/log/kea/kea-dhcp4.log  # verás los leases al renovar

# en cada SERVER (fuerza renovación de IP):
sudo nmcli networking off && sudo nmcli networking on
ip -br addr
```

Errores de schema Kea 3.0 que nos salieron en producción (si los ves, ya sabes la causa):

| Error | Causa |
|---|---|
| `missing parameter 'id'` | cada subnet necesita su `id` numérico (ya incluido arriba) |
| `invalid path: '/tmp'` | el control socket debe vivir en `/var/run/kea` |
| `invalid path in output` | los logs deben ir bajo `/var/log/kea` |

---

## 6. Túnel WireGuard site-to-site (~35 min)

### 6.1 Parámetros del túnel

| Parámetro | ROUTER-A | ROUTER-B |
|---|---|---|
| IP túnel | `10.99.0.1/30` | `10.99.0.2/30` |
| Listen port | UDP `51820` | UDP `51820` |
| AllowedIPs del peer | `20.0.0.0/24, 10.99.0.2/32` | `10.0.0.0/24, 10.99.0.1/32` |
| Endpoint del peer | `172.10.20.128:51820` | `172.10.20.224:51820` |
| Keepalive | 25 s | 25 s |

> La regla de oro de AllowedIPs: "qué redes viven AL OTRO LADO de este peer".

### 6.2 Generar las claves (SSH en cada router)

```bash
# en ROUTER-A:
wg genkey | tee /tmp/priv_a | wg pubkey > /tmp/pub_a
cat /tmp/pub_a     # ← cópiala al portapapeles: viaja a ROUTER-B

# en ROUTER-B:
wg genkey | tee /tmp/priv_b | wg pubkey > /tmp/pub_b
cat /tmp/pub_b     # ← cópiala al portapapeles: viaja a ROUTER-A
```

El portapapeles bidireccional pasa la clave de una VM a la otra (VM → host → VM).

> ☠ Nunca compartas la **PrivateKey** en chats, capturas o repositorios. Solo las PÚBLICAS cruzan equipos.

### 6.3 Configuración efectiva — archivo completo en cada router

ROUTER-A (la privada se inyecta sola; solo pega la pública de B donde dice `PEGA_AQUI_PUB_B`):

```bash
mkdir -p /usr/local/etc/wireguard
cat > /usr/local/etc/wireguard/wg0.conf <<WG
[Interface]
PrivateKey = $(cat /tmp/priv_a)
ListenPort = 51820

[Peer]
PublicKey = PEGA_AQUI_PUB_B
Endpoint = 172.10.20.128:51820
AllowedIPs = 20.0.0.0/24, 10.99.0.2/32
PersistentKeepalive = 25
WG
chmod 600 /usr/local/etc/wireguard/wg0.conf
```

ROUTER-B (completo, sin "espejo"):

```bash
mkdir -p /usr/local/etc/wireguard
cat > /usr/local/etc/wireguard/wg0.conf <<WG
[Interface]
PrivateKey = $(cat /tmp/priv_b)
ListenPort = 51820

[Peer]
PublicKey = PEGA_AQUI_PUB_A
Endpoint = 172.10.20.224:51820
AllowedIPs = 10.0.0.0/24, 10.99.0.1/32
PersistentKeepalive = 25
WG
chmod 600 /usr/local/etc/wireguard/wg0.conf
```

Verifica que el archivo quedó bien armado (la privada debe verse, la pública del peer debe ser la que copiaste):

```bash
cat /usr/local/etc/wireguard/wg0.conf
```

### 6.4 Activación y reglas de firewall

Activa la interfaz (en cada router por SSH):

```bash
# ROUTER-A:
ifconfig wg0 create name wg0
wg syncconf wg0 /usr/local/etc/wireguard/wg0.conf
ifconfig wg0 inet 10.99.0.1/30 alias
ifconfig wg0 up
route -n add -net 20.0.0.0/24 -interface wg0

# ROUTER-B:
ifconfig wg0 create name wg0
wg syncconf wg0 /usr/local/etc/wireguard/wg0.conf
ifconfig wg0 inet 10.99.0.2/30 alias
ifconfig wg0 up
route -n add -net 10.0.0.0/24 -interface wg0
```

Ahora las reglas, desde el navegador del server de cada sitio:

1. **Interfaces → Assignments → +** agrega `wg0` → habilítala con nombre `WGVPN` (sin configuración IP, ya la tiene) → Save.
2. **Firewall → Rules → WGVPN → +** (en cada router):
   - Regla 1: pass · IPv4 · any · Source = `red LAN remota` (A: `20.0.0.0/24` · B: `10.0.0.0/24`) · Destination = any
   - Regla 2: pass · IPv4 · any · Source = any · Destination = `red LAN remota`
3. **Firewall → Rules → WAN → +** (en cada router — sin esta regla NINGÚN paquete del túnel entra):
   - pass · IPv4 · UDP · Source = IP WAN del peer (A: `172.10.20.128` · B: `172.10.20.224`) · Destination = **This Firewall** · Puerto destino = `51820`
   - **Edita la regla → Display Advanced → desmarca "Reply-to"** → Save → Apply.

> ⚠ Lo del reply-to no es superstición: OPNsense agrega `reply-to (gateway WAN)` a las reglas
> de WAN y las respuestas salen forzadas por el gateway aunque hayan entrado por otro camino
> (ruteo asimétrico). En producción real nos costó dos lockouts — es el incidente #2 de la sección 9.

### 6.5 Validación del túnel

```bash
# en cualquiera de los dos routers:
wg show                       # latest handshake debe ser reciente (< 25 s con keepalive)

# desde ROUTER-A (ping con origen forzado, cruzando el túnel):
ping -S 10.0.0.1 20.0.0.101
```

> 💡 El ping SIN `-S` entre routers usa la IP del túnel (10.99.0.x) — si tus reglas solo
> cubren las redes LAN, ese ping fallará aunque el túnel esté perfecto. Prueba siempre con
> IPs reales de servidor.

---

## 7. SERVER-B — MariaDB remoto (~15 min)

Todo por copiar-pegar en la terminal de SERVER-B:

```bash
sudo apt update && sudo apt install -y mariadb-server

# escuchar en todas las interfaces (el tráfico llega por la LAN)
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' \
     /etc/mysql/mariadb.conf.d/50-server.cnf
sudo systemctl enable --now mariadb && sudo systemctl restart mariadb

# base de datos y usuario SOLO para la red remota
sudo mysql -e "CREATE DATABASE wordpress CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'wpuser'@'10.0.0.%' IDENTIFIED BY 'WPLab2026!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'10.0.0.%';"
sudo mysql -e "FLUSH PRIVILEGES;"

ss -tln | grep 3306      # → LISTEN 0.0.0.0:3306 ✓
```

> 💡 `'wpuser'@'10.0.0.%'` significa "este usuario solo existe si viene desde la red del
> sitio A". Aunque alguien abriera el 3306 hacia internet, no tendría usuario válido.
> Defensa en profundidad: firewall + bind + grants.

---

## 8. SERVER-A — WordPress apuntando a la BD remota (~20 min)

```bash
sudo apt update && sudo apt install -y apache2 libapache2-mod-php php php-mysql \
    php-curl php-gd php-mbstring php-xml php-intl php-zip wget curl
cd /tmp && wget https://wordpress.org/latest.tar.gz && tar xzf latest.tar.gz
sudo cp -r wordpress /var/www/html/
sudo chown -R www-data:www-data /var/www/html/wordpress

cd /var/www/html/wordpress
sudo cp wp-config-sample.php wp-config.php
sudo sed -i "s/database_name_here/wordpress/"   wp-config.php
sudo sed -i "s/username_here/wpuser/"           wp-config.php
sudo sed -i "s/password_here/WPLab2026!/"       wp-config.php
# LA LÍNEA DE LA DEMO — la BD está en la OTRA red:
sudo sed -i "s/'DB_HOST', 'localhost'/'DB_HOST', '20.0.0.101'/" wp-config.php
```

Instalación headless con wp-cli (sin wizard, sin salir de la terminal):

```bash
cd /tmp
curl -sO https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
sudo -u www-data php wp-cli.phar core install \
  --url=http://10.0.0.101/wordpress \
  --title="Demo VPN Site-to-Site" --admin_user=admin \
  --admin_password=WPLab2026! --admin_email=admin@lab.local \
  --skip-email --path=/var/www/html/wordpress

# → Success: WordPress installed successfully.
#   (ese Success implica que creó sus 12 tablas EN LA BD REMOTA, cruzando el túnel)
```

---

## 9. Validación final y evidencias (~15 min)

```bash
# en ambos routers:
wg show                                  # handshake reciente, transfer > 0

# ping cruzado entre servers (desde SERVER-A):
ping -c3 20.0.0.101

# la prueba reina — desde SERVER-A:
mysql -h 20.0.0.101 -u wpuser -p'WPLab2026!' wordpress -e "SELECT 1; SHOW TABLES;"
# → wp_commentmeta, wp_comments, wp_links, wp_options, wp_postmeta, wp_posts,
#   wp_term_relationships, wp_term_taxonomy, wp_termmeta, wp_terms, wp_usermeta, wp_users
```

(si no tienes el cliente: `sudo apt install -y mariadb-client`)

Abre en el navegador de SERVER-A: `http://10.0.0.101/wordpress/` → el sitio carga.

### Prueba negativa (obligatoria — demuestra que la dependencia es real)

```bash
# en ROUTER-B (SSH), baja el túnel:
ifconfig wg0 down
# en SERVER-A, refresca el sitio → "Error establishing a database connection" ✓
# sube el túnel:
ifconfig wg0 up        # el keepalive re-negocia solo
```

Si tu app sigue funcionando sin túnel, tu demo no demuestra nada — esta prueba negativa es la que convierte una captura bonita en evidencia.

### Evidencias para tu auto-check

- Captura de `wg show` en AMBOS routers con handshake reciente y transfer > 0
- Ping cruzado entre servers (10.0.0.101 ↔ 20.0.0.101)
- Salida de `SHOW TABLES;` desde SERVER-A contra la IP remota
- Captura del navegador de SERVER-A cargando `http://10.0.0.101/wordpress/`
- (Nivel pro) `tcpdump` en ROUTER-B demostrando que el 3306 llega por `wg0`, no por `em0`

---

## 10. Troubleshooting — los 6 incidentes que vivimos en producción

Estos NO son hipotéticos: ocurrieron construyendo esta misma demo. Si algo falla, busca tu síntoma aquí — el método importa más que la respuesta.

| # | Síntoma | Causa raíz | Diagnóstico | Fix |
|---|---|---|---|---|
| 1 | SSH muere al habilitar el firewall | Reglas con origen restringido a la red WAN local, administrando desde otra subred | ¿El SYN llega? (tcpdump) ¿Qué regla lo procesa? (`pfctl -vvsr`) | `source = any` o incluir tu subred admin · sesión vieja abierta como cuerda de seguridad |
| 2 | Reglas correctas pero sin retorno | OPNsense agrega `reply-to (gateway WAN)` a las reglas WAN → ruteo asimétrico | Contadores de la regla suben pero Packets=0 · `pfctl -sr` muestra el reply-to clavado | Editar la regla WAN → Advanced → **deshabilitar reply-to** |
| 3 | La IP estática del firewall "revierte sola" | Proceso dhclient residual relanzado por ciclos de interfaces | `ps aux \| grep dhclient` + leases de Kea mostrando el hostname del router | Matar dhclient, limpiar `/var/etc/dhclient.*.conf`, re-fijar IP y verificarla tras cada reload |
| 4 | apt dice "network unreachable" pero hay internet | NO era el cliente: el gateway había perdido su ruta default y respondía ICMP host-unreachable | tcpdump en la LAN del gateway: SYNs correctos respondidos con ICMP-unreachable POR EL ROUTER · `netstat -rn \| grep default` | `route add default <gw>` + persistir el gateway en config.xml |
| 5 | Kea rechaza la configuración completa | Kea 3.0 endureció validaciones: id obligatorio, paths restringidos | Log de kea-dhcp4 | `id` numérico por subnet · socket en `/var/run/kea` · logs en `/var/log/kea` |
| 6 | El port forward "no funciona" con pf bien | Tras el rdr, el paquete tiene destino POST-NAT y la regla pass solo cubría la VIP | `/var/log/filter/latest.log`: el paquete aparece YA TRADUCIDO siendo bloqueado | Segunda regla pass contra el destino post-NAT (asociada al rdr) |

> ☠ Lección transversal: cuando pf "ignora" paquetes, la respuesta casi siempre está en el
> filterlog o en los contadores por-regla — nunca en adivinar más reglas.
> Método general: captura en AMBOS extremos del enlace sospechoso. Lo que entra y no sale
> localiza el problema en un solo dispositivo.

---

## 11. Auto-check — ¿dominas esto? (libre, sin nota)

Este lab es complementario: nada se entrega ni se califica. Pero si puedes tachar esta lista completa, tienes un nivel de redes/firewalls que muchos ingenieros senior no tienen.

- [ ] Explicar SIN mirar la guía por qué las reglas WAN necesitan `disablereplyto`
- [ ] Túnel arriba: `wg show` con handshake reciente y transfer > 0 en ambos routers
- [ ] Ping cruzado entre LANs usando IPs de servidor (no las del túnel)
- [ ] WordPress instalado y creando tablas en la BD del OTRO sitio — `SHOW TABLES` desde SERVER-A
- [ ] Prueba negativa: bajar wg0 → WordPress falla → subir → funciona. Sabes explicar por qué eso demuestra la dependencia
- [ ] Sabes decir qué protocolo/puerto viaja cifrado dentro de qué otro (3306/TCP dentro de 51820/UDP)

> 💡 Reto adicional: agrega un tercer sitio (ROUTER-C, red 30.0.0.0/24) en hub-and-spoke, o
> sustituye WireGuard por IPsec IKEv2 y compara overhead con iperf3.

---

## Anexos

### Anexo A — wg0.conf de referencia (lab ya destruido)

```ini
[Interface]
PrivateKey = QKjSr7C9Se9CXXF3idg+06cTca/98KR3Mz9r+hZv5k4=
ListenPort = 51820

[Peer]
PublicKey = roLBQ8TSZ5PKPxtdFG0bnue+sqFIHQuR2Q25lxLJiCY=
Endpoint = 172.10.20.128:51820
AllowedIPs = 20.0.0.0/24,10.99.0.2/32
PersistentKeepalive = 25
```

> ⚠ Estas claves son de un lab ya destruido y están publicadas: NO las reuses. Genera las tuyas siempre (fase 6.2).

### Anexo B — SQL completo de la base de datos

```sql
CREATE DATABASE wordpress CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'wpuser'@'10.0.0.%' IDENTIFIED BY 'WPLab2026!';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'10.0.0.%';
FLUSH PRIVILEGES;
-- verificación desde SERVER-A (requiere mariadb-client):
-- mysql -h 20.0.0.101 -u wpuser -p'WPLab2026!' wordpress -e "SELECT 1; SHOW TABLES;"
```

### Anexo C — ¿Por qué no usamos el plugin os-wireguard?

Tres quirks reales que nos encontramos:

1. El campo `<interface>` del server DEBE contener el nombre del dispositivo (`wg0`); vacío = no hace nada.
2. `configctl wireguard configure` sin UUID no ejecuta nada: hay que invocar `php /usr/local/opnsense/scripts/wireguard/wg-service-control.php restart <uuid>`.
3. El script espera que otro proceso genere `/usr/local/etc/wireguard/wg0.conf` (render de templates que nunca se dispara por configd) → por eso lo escribimos a mano.

Además: la activación manual de la fase 6.4 NO sobrevive un reboot (es un lab). Si quieres persistencia, el camino soportado es el plugin con sus quirks, o `rc.conf`.

### Anexo D — (Opcional) Reglas WAN de administración

Si algún día quieres administrar los firewalls DESDE la WAN (no es necesario en este lab):

| # | Action | Protocol | Source | Destination | Puerto |
|---|---|---|---|---|---|
| 1 | pass | TCP | any (o tu subred admin) | This Firewall (self) | 22 SSH |
| 2 | pass | TCP | any (o tu subred admin) | This Firewall (self) | 443 HTTPS |

- Crea las reglas ANTES de habilitar el firewall, y prueba SIEMPRE una conexión nueva antes de cerrar la sesión actual (anti-lockout).
- Si administras desde otra subred distinta a la WAN: **Display Advanced → desactiva "Reply-to"** en cada regla.
- Truco pro: deja corriendo `sleep 180; pfctl -d` en otra sesión como watchdog; si confirmas acceso, lo cancelas.

### Anexo E — (Opcional) Ver el WordPress desde el navegador de tu PC

La NAT Network de VirtualBox no es alcanzable desde el host por defecto. Para exponer el sitio:

1. En ROUTER-A crea una VIP: **Interfaces → Virtual IPs → +** → IP `172.10.20.230/24` en WAN.
2. **Firewall → NAT → Port Forward → +**: interfaz WAN · TCP · destino `172.10.20.230` puerto 80 → redirect target `10.0.0.101` puerto 80 · **Filter rule association: Add associated filter rule** (esto evita el incidente #6: la regla queda contra el destino post-NAT).
3. En VirtualBox: **Administrador de red → NAT Networks → WANLAB → Reenvío de puertos → +**: host `127.0.0.1:8080` → guest `172.10.20.230:80`.
4. Navegador de tu PC: `http://127.0.0.1:8080/wordpress/`.

---

## Créditos

- Ejecución técnica, diagnóstico y documentación: **ox-alpha**, modelo IA de lenguaje
- Dirección académica y arquitectura: **Ing. Rodolfo Cañas Cervantes** (CUC)
- Validado end-to-end en infraestructura real antes de publicarse — agosto 2026
- v2: servers OSBoxes + administración desde los servers + bloques copiar-pegar — agosto 2026
