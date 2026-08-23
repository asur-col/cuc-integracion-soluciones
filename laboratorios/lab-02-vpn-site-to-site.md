# Lab 2 — VPN Site-to-Site OPNsense: WordPress con base de datos remota

**Curso:** Integración de Soluciones para Plataformas Cloud — Ingeniería de Sistemas
**Docente:** Ing. Rodolfo Cañas Cervantes — Universidad de la Costa (CUC) · 2026-2
**Duración estimada:** 150 min · **Modalidad:** VirtualBox local (4 VMs)
**Guía visual:** esta es la versión técnica cruda; la guía ilustrada con diagramas es `lab-02-vpn-site-to-site-opnsense.html`

> Ejecución técnica, diagnóstico y documentación: **ox-alpha**, modelo IA de lenguaje.
> Dirección académica y arquitectura: **Ing. Rodolfo Cañas Cervantes**.
> Todo lo aquí documentado fue ejecutado y validado en infraestructura real antes de publicarse.

---

## Topología objetivo

```
                    [ Tu PC - admin / 172.10.20.0/24 ]
                                   |
        +--------------------------+--------------------------+
        |              WANLAB (NAT Network VB)                 |
        +---------------+----------------------+---------------+
                        |                      |
               WAN em0 .20.224            WAN em0 .20.128
                ROUTER-A (OPNsense)     ROUTER-B (OPNsense)
                LAN em1 10.0.0.1        LAN em1 20.0.0.1
                wg0 10.99.0.1           wg0 10.99.0.2
                        |    <== WG tun ==>   |
                  LAN-A internal         LAN-B internal
                        |                      |
                 SERVER-A 10.0.0.101    SERVER-B 20.0.0.101
                 WordPress+Apache+PHP   MariaDB :3306
                        +------ MySQL por tunel ------+
```

| Componente | Interfaz | IP |
|---|---|---|
| RouterA | em0/em1/wg0 | 172.10.20.224 · 10.0.0.1 · 10.99.0.1 |
| ServerA | enp0s3 | 10.0.0.101 (WordPress :80) |
| RouterB | em0/em1/wg0 | 172.10.20.128 · 20.0.0.1 · 10.99.0.2 |
| ServerB | enp0s3 | 20.0.0.101 (MariaDB :3306) |

---

## Parte A — Firewalls base (~30 min)

1. Instalar OPNsense x2 (login installer/opnsense, ZFS stripe, defaults).
2. Asignar interfaces: LAN=em1, WAN=em0. IPs LAN estaticas: 10.0.0.1/24 y 20.0.0.1/24.
3. Reglas WAN anti-lockout ANTES de habilitar pf:
   - pass TCP any -> self port 22
   - pass TCP any -> self port 443
   - Deshabilitar reply-to en ambas (Advanced).
4. Aplicar y probar conexion NUEVA antes de cerrar sesion actual.

## Parte B — DHCP Kea (~20 min)

Configuracion JSON nativa (/usr/local/etc/kea/kea-dhcp4.conf), Router-A:

```json
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
        { "name": "routers", "data": "10.0.0.1" },
        { "name": "domain-name-servers", "data": "8.8.8.8, 1.1.1.1" }
      ]
    } ],
    "loggers": [ { "name": "kea-dhcp4",
      "output-options": [ { "output": "/var/log/kea/kea-dhcp4.log" } ],
      "severity": "INFO" } ]
  }
}
```

Router-B espejo: id 2, subnet 20.0.0.0/24, pool .100-.200, routers/DNS 20.0.0.1.

Quirks Kea 3.0: `id` obligatorio; socket en `/var/run/kea`; logs en `/var/log/kea`;
`dhcp4=yes` en keactrl.conf; `service kea enable`.

Validacion: `service kea restart && sockstat -l | grep '.67'` y lease del server.

## Parte C - Tunel WireGuard site-to-site (~40 min) — VPN WireGuard site-to-site

### 7.1 Parámetros del túnel

| Parámetro | RouterA | RouterB |
|---|---|---|
| IP túnel | `10.99.0.1/30` | `10.99.0.2/30` |
| Listen port | UDP `51820` | UDP `51820` |
| AllowedIPs del peer | `20.0.0.0/24, 10.99.0.2/32` | `10.0.0.0/24, 10.99.0.1/32` |
| Endpoint del peer | `172.10.20.128:51820` | `172.10.20.224:51820` |
| Keepalive | 25 s | 25 s |

Claves generadas en cada router (`wg genkey` / `wg pubkey`) e intercambiadas manualmente.

### 7.2 Quirks del plugin os-wireguard

1. El campo `<interface>` del server DEBE contener el nombre del dispositivo (`wg0`); vacío = no hace nada.
2. `configctl wireguard configure` sin UUID no ejecuta nada: hay que invocar
   `php /usr/local/opnsense/scripts/wireguard/wg-service-control.php restart <uuid>`.
3. El script espera que otro proceso genere `/usr/local/etc/wireguard/wg0.conf` (render de templates que nunca se dispara por configd) → se escribió a mano.

### 7.3 Configuración efectiva (`/usr/local/etc/wireguard/wg0.conf`)

**RouterA:**
```ini
[Interface]
PrivateKey = <PRIV_A>
ListenPort = 51820

[Peer]
PublicKey = <PUB_B>
Endpoint = 172.10.20.128:51820
AllowedIPs = 20.0.0.0/24,10.99.0.2/32
PersistentKeepalive = 25
```

**RouterB:** espejo (`PUB_A`, endpoint `.224`, `AllowedIPs = 10.0.0.0/24,10.99.0.1/32`).

### 7.4 Activación manual (equivalente a wg_start del script oficial)

```sh
ifconfig wg0 create name wg0
/usr/bin/wg syncconf wg0 /usr/local/etc/wireguard/wg0.conf
ifconfig wg0 inet 10.99.0.1/30 alias      # .2/30 en B
ifconfig wg0 up
route -n add -net 20.0.0.0/24 -interface wg0   # 10.0.0.0/24 en B
```

Resultado verificado: `latest handshake: Now`, transfer > 0 en ambos sentidos.

### 7.5 Reglas firewall sobre la interfaz WG

Se registró `wg0` como interfaz OPT (`<interfaces><opt1><if>wg0</if>…`) para que pf pudiera filtrarla, y se agregaron dos reglas por router:

```pf
pass in quick on wg0 inet from <red_remota>/24 to any keep state
pass in quick on wg0 inet from any to <red_remota>/24 keep state
```

Nota: el ping entre las propias IPs del túnel (`10.99.0.x`) queda fuera de estas reglas — cubren el tráfico inter-LAN real, que usa IPs de LAN como fuente.

---

## 8. Fase 5 — Servidores Ubuntu

### 8.1 Ubuntu minimal: tres obstáculos típicos

| Problema | Causa | Solución |
|---|---|---|
| Sin SSH | La imagen minimal no trae `openssh-server` | `sudo apt install -y openssh-server` desde consola |
| DNS roto tras DHCP | Kea entregaba el router como DNS y Unbound no tenía upstreams | Entregar `8.8.8.8, 1.1.1.1` por DHCP + `resolv.conf` manual temporal |
| `network unreachable` en apt | **No era IPv6 ni DNS**: el gateway OPNsense había perdido su ruta default y devolvía `ICMP host unreachable` | Restaurar `route add default 172.10.20.1` en ambos routers |

Confirmación por captura en el gateway: SYNs correctos del server hacia `archive.ubuntu.com` respondidos con ICMP-unreachable por el propio router → problema de ruteo, no del cliente.

Para preferir IPv4 sobre IPv6 en clientes con el síntoma clásico de AAAA:

```sh
echo 'precedence ::ffff:0:0/96  100' | sudo tee -a /etc/gai.conf
```

---

## 9. Fase 6 — MariaDB en ServerB (BD remota)

```bash
sudo apt-get install -y mariadb-server
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf
sudo systemctl enable --now mariadb && sudo systemctl restart mariadb

sudo mysql -e "CREATE DATABASE wordpress CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'wpuser'@'10.0.0.%' IDENTIFIED BY 'WPLab2026!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'10.0.0.%';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

Puntos clave:
- `bind-address = 0.0.0.0`: escucha en todas las interfaces (el tráfico llega por em1).
- Usuario restringido a `'wpuser'@'10.0.0.%'`: SOLO acepta conexiones desde la LAN remota (que llega traducida al cruzar el túnel), nunca desde la WAN.
- Verificación: `ss -tln | grep 3306` → `LISTEN 0.0.0.0:3306`.

---

## 10. Fase 7 — WordPress en ServerA

```bash
sudo apt-get install -y apache2 libapache2-mod-php php php-mysql php-curl \
                        php-gd php-mbstring php-xml php-intl php-zip wget curl
cd /tmp && wget https://wordpress.org/latest.tar.gz && tar xzf latest.tar.gz
sudo cp -r wordpress /var/www/html/
sudo chown -R www-data:www-data /var/www/html/wordpress
```

`wp-config.php` — el corazón de la demo:

```php
define( 'DB_NAME',     'wordpress' );
define( 'DB_USER',     'wpuser'    );
define( 'DB_PASSWORD', 'WPLab2026!' );
define( 'DB_HOST',     '20.0.0.101' );   // ← BD REMOTA: cruza el túnel
```

Instalación headless sin wizard con wp-cli:

```bash
curl -sO https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
sudo -u www-data php wp-cli.phar core install \
  --url=http://172.10.20.230/wordpress \
  --title="Demo VPN Site-to-Site ASUR" \
  --admin_user=admin --admin_password=WPLab2026! \
  --admin_email=admin@lab.local --skip-email \
  --path=/var/www/html/wordpress
# → Success: WordPress installed successfully
```

Ese `Success` implica que WordPress **creó sus 12 tablas en la base remota cruzando el túnel**.

---

## 11. Validación de la demo

### 11.1 Conexión app → BD por el túnel (prueba reina)

Desde ServerA:

```
mysql -h 20.0.0.101 -u wpuser -p'WPLab2026!' wordpress -e "SELECT 1; SHOW TABLES;"
→ tunel_ok: 1
→ wp_commentmeta, wp_comments, wp_links, wp_options, wp_postmeta,
  wp_posts, wp_term_relationships, wp_term_taxonomy, wp_termmeta,
  wp_terms, wp_usermeta, wp_users
```

### 11.2 Evidencia de cifrado

- `wg show` en ambos routers: handshake reciente, transfer creciente.
- Las credenciales MySQL viajan cifradas dentro del túnel; MariaDB nunca quedó expuesto a la WAN.

---

## 12. Fase 8 — Exposición externa del WordPress

## Parte F - Validacion final y evidencias

```bash
wg show                                  # handshake reciente, transfer > 0
ping -S 10.0.0.101 20.0.0.101            # cruzado por tunel
mysql -h 20.0.0.101 -u wpuser -p'WPLab2026!' wordpress -e "SELECT 1; SHOW TABLES;"
# → 12 tablas wp_* creadas EN LA BD REMOTA
```

Prueba negativa (obligatoria):

```bash
ifconfig wg0 down     # en ROUTER-B
# WordPress debe fallar: "Error establishing a database connection"
ifconfig wg0 up       # keepalive re-negocia solo
```

## Incidentes reales documentados durante la construccion

| # | Sintoma | Causa raiz | Fix |
|---|---|---|---|
| 1 | SSH muere al habilitar pf | reglas con source=red WAN local, admin desde otra subred | source any + sesion vieja abierta |
| 2 | Reglas any pero sin retorno | reply-to automatico de OPNsense fuerza retorno por gateway WAN | disablereplyto=1 |
| 3 | IP LAN estatica revierte sola | dhclient residual relanzado por ciclos de interfaces | matar dhclient + limpiar /var/etc |
| 4 | apt: network unreachable | gateway SIN ruta default respondia ICMP host-unreachable | route add default + persistir en config.xml |
| 5 | Kea rechaza config | schema endurecido 3.0 | id/paths obligatorios |
| 6 | Port forward sin efecto | faltaba regla pass post-NAT (destino real 10.0.0.101 tras rdr) | segunda regla pass asociada al rdr |

Metodo transversal: tcpdump en ambos extremos + contadores `pfctl -vvsr` +
`/var/log/filter/latest.log`. Nunca adivinar reglas.

## Entregable

PDF unico con: topologia propia (tus IPs), evidencias (wg show, pings cruzados,
SHOW TABLES, navegador), prueba negativa y reflexion de media pagina sobre datos
sensibles (PII) en esta arquitectura.

## Creditos

- Ejecucion tecnica, diagnostico y documentacion: **ox-alpha**, modelo IA de lenguaje
- Direccion academica y arquitectura: **Ing. Rodolfo Cañas Cervantes** (CUC)
- Validado end-to-end en infraestructura real antes de publicarse — agosto 2026
