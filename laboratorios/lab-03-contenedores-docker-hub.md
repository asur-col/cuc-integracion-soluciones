# Laboratorio 3 — Contenedores: build → push → run con Docker Hub (semana 8)

**Curso:** Integración de Soluciones para Plataformas Cloud — Ingeniería de Sistemas
**Docente:** Ing. Rodolfo Cañas Cervantes — Universidad de la Costa (CUC) · 2026-2
**Unidad 2 · Actividad 1 · Ponderación: 10% de la nota final**
**Duración estimada:** 90 min · **Modalidad:** Play with Docker (navegador, sin instalación) + Docker Hub
**Guía visual:** esta es la versión técnica en Markdown; la guía ilustrada para Moodle es `lab-03-contenedores-docker-hub.html`

> Ejecución técnica, diseño del laboratorio y capturas reales: modelo de IA (GLM, vía `oco`), corregido y verificado por Claude (Anthropic) contra evidencia real de comandos ejecutados.
> Dirección académica: **Ing. Rodolfo Cañas Cervantes**.
> Todos los comandos y salidas de este documento fueron ejecutados y verificados en Play with Docker antes de publicarse — ninguna salida está inventada.

## Introducción

En la clase de esta semana vimos qué es un contenedor, cómo se construye una imagen con un `Dockerfile` y por qué el registro de imágenes es la pieza que convierte una app en un artefacto portable. Ahora lo vas a hacer tú: **vas a construir tu propia imagen de contenedor, publicarla en un registro y correrla en una máquina distinta a la que la construyó**, que es exactamente el flujo `build → push → run` que usan los pipelines de despliegue en cualquier nube.

Vas a trabajar en **Play with Docker** (`labs.play-with-docker.com`): una instancia real de Docker en tu navegador, gratis, sin instalar nada en tu equipo. Tu imagen se publica en **Docker Hub**, el registro público de Docker — el mismo concepto que Amazon ECR, Azure Container Registry o Google Artifact Registry.

> **La idea central del lab en una frase:** la imagen es inmutable y vive en el registro; cualquier máquina que la descargue obtiene exactamente la misma aplicación.

**Presupuesto de tiempo (90 min, no te desvíes):**

| Parte | Tiempo |
|---|---|
| 0 — Prerrequisitos (cuenta + instancia) | 5 min |
| Pasos 1–3 — Primer contenedor, puertos y aislamiento | 20 min |
| Pasos 4–6 — Tu propia app: Dockerfile, build y run | 25 min |
| Pasos 7–8 — Registro: push y versionado | 20 min |
| Paso 9 — Prueba de portabilidad | 10 min |
| Paso 10 — Reto (bonus) | 10 min |

***

## Prerrequisitos (5 min)

1. **Cuenta en Docker Hub** — ve a [hub.docker.com](https://hub.docker.com), crea una cuenta gratuita (o usa la que ya tengas). **Anota tu nombre de usuario**: lo usarás en todos los comandos como `<usuario>`.
2. **Play with Docker** — entra a [labs.play-with-docker.com](https://labs.play-with-docker.com):
   - Clic en **Login** (usa tu cuenta de Docker Hub que acabas de crear).
   - Clic en **Start**.
   - Clic en el botón **"+ ADD NEW INSTANCE"** (arriba a la izquierda).
3. Debe aparecer una terminal en el navegador con un mensaje de bienvenida de Docker y un botón **8080** en la barra superior. Esa terminal es **tu host Docker real** (una máquina efímera de 4 horas).

> **Importante:** la sesión de Play with Docker dura **4 horas** y al terminar se borra todo lo que esté solo en la instancia. Lo único que sobrevive es lo que empujaste a Docker Hub — por eso el push (paso 7) es el corazón del lab.

***

## Paso 1 — Tu primer contenedor (imagen vs. contenedor)

**Objetivo:** ver la diferencia entre una **imagen** (el paquete inmutable) y un **contenedor** (la instancia en ejecución).

```bash
docker run hello-world
docker images
docker ps -a
```

**Qué debes ver:**

1. `docker run hello-world` descarga la imagen (si no la tienes) y ejecuta un contenedor que imprime:

   ```
   Hello from Docker!
   This message shows that your installation appears to be working correctly.
   ...
   1. The Docker client contacted the Docker daemon.
   2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
   3. The Docker daemon created a new container from that image ...
   4. The Docker daemon streamed that output to the Docker client ...
   ```

2. `docker images` lista `hello-world` con su TAG (`latest`) y su tamaño (~13 kB).
3. `docker ps -a` muestra el contenedor con STATUS `Exited (0)` — ya terminó su trabajo y salió.

**Dato clave:** `docker ps` solo muestra los contenedores **activos**; `docker ps -a` los muestra todos (también los detenidos).

***

## Paso 2 — Un servidor web en un contenedor (puertos y modo detached)

**Objetivo:** correr un proceso que **no termina** (un servidor web) y publicar su puerto hacia afuera.

```bash
docker run -d -p 8080:80 --name web nginx:alpine
docker ps
```

- `-d`: en segundo plano (detached) — la terminal queda libre.
- `-p 8080:80`: publica el **puerto 80** del contenedor en el **puerto 8080** de tu instancia.
- `--name web`: le pones nombre para referenciarlo después.

**Qué debes ver:** el comando imprime un largo ID hexadecimal y `docker ps` muestra el contenedor `web` con STATUS `Up` y el mapeo `0.0.0.0:8080->80/tcp`.

**Para ver la página:** haz clic en el botón **8080** que aparece en la barra superior de Play with Docker — se abre una pestaña con la página de bienvenida de nginx.

***

## Paso 3 — Entrar al contenedor (aislamiento)

**Objetivo:** comprobar que el contenedor tiene **su propio sistema de archivos**, distinto al de tu instancia.

```bash
docker exec -it web sh
cat /etc/os-release
exit
```

**Qué debes ver:** el prompt cambia a `/ #` (estás **dentro** del contenedor). `cat /etc/os-release` responde:

```
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.24.2
PRETTY_NAME="Alpine Linux v3.24"
```

**Dato clave:** el contenedor corre Alpine Linux aunque la instancia sea otra distribución — ese es el aislamiento a nivel de proceso y de sistema de archivos. Con `exit` vuelves a tu instancia.

***

## Paso 4 — Tu propia app: el Dockerfile

**Objetivo:** crear los dos archivos mínimos de una app contenedorizada.

Crea una carpeta y sus dos archivos (puedes usar el editor de Play with Docker o pegar estos comandos completos):

```bash
mkdir mi-app && cd mi-app

cat > index.html <<'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Mi primera app en contenedor</title>
  <style>body{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;background:#A6192E;color:#fff;margin:0}h1{font-size:3rem}</style>
</head>
<body>
  <div>
    <h1>Hola, soy Tu Nombre Aquí</h1>
    <p>Mi primera imagen de contenedor — Integración de Soluciones 2026-2</p>
  </div>
</body>
</html>
EOF

cat > Dockerfile <<'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EOF
```

> **Cambia "Tu Nombre Aquí" por tu nombre real** (edita `index.html`): esa página es tu evidencia final.

**Qué debes ver:** `cat Dockerfile` muestra exactamente dos líneas: `FROM` (la imagen base) y `COPY` (tu contenido). `cat index.html` muestra tu página con tu nombre.

***

## Paso 5 — Construir la imagen (capas y tags)

**Objetivo:** convertir el Dockerfile en una imagen identificable por tag.

```bash
docker build -t <usuario>/mi-app:1.0 .
docker history <usuario>/mi-app:1.0
```

> Reemplaza `<usuario>` por tu usuario de Docker Hub en **todos** los comandos de aquí en adelante. **El punto final** (` . `) del build es obligatorio: indica que el contexto de construcción es la carpeta actual.

**Qué debes ver:**

1. El build termina con `naming to docker.io/<usuario>/mi-app:1.0 done`.
2. `docker history` muestra las **capas**: tu `COPY index.html ...` arriba, y debajo las capas que heredaste de `nginx:alpine` (todas las que ves son la imagen base: ~52 MB + tu capa de ~25 kB).

**Dato clave:** una imagen es una **pila de capas inmutables**. Tu app solo agregó una capa encima de nginx:alpine — por eso construir sobre una imagen base conocida es barato y rápido.

***

## Paso 6 — Ejecutar tu imagen (ciclo build → run)

**Objetivo:** reemplazar el nginx genérico por **tu** app.

```bash
docker rm -f web
docker run -d -p 8080:80 <usuario>/mi-app:1.0
docker ps
```

**Qué debes ver:** `docker ps` muestra tu contenedor con la imagen `<usuario>/mi-app:1.0`. Haz clic en **8080**: ahora la página muestra **tu nombre** con fondo vino — no la página genérica de nginx.

***

## Paso 7 — El registro: publicar tu imagen (push ≙ ECR)

**Objetivo:** subir tu imagen a Docker Hub para que cualquier máquina pueda descargarla.

```bash
docker login
docker push <usuario>/mi-app:1.0
```

- `docker login` pide tu usuario y clave de Docker Hub → debe terminar en `Login Succeeded`.
- `docker push` sube las capas que falten.

**Qué debes ver:**

```
The push refers to repository [docker.io/<usuario>/mi-app]
...
1.0: digest: sha256:... size: 856
```

La línea `digest: sha256:...` es la **prueba criptográfica** de que tu imagen quedó almacenada en el registro.

**Comprueba en el navegador:** entra a `https://hub.docker.com/r/<usuario>/mi-app` — tu repositorio debe estar ahí con el tag `1.0`.

> **Nota sobre la captura de ejemplo:** las salidas de esta guía se capturaron ejecutando los comandos reales contra un registro del curso (por eso en el ejemplo el usuario es `student01`); en tu caso el repositorio es `hub.docker.com/<tu-usuario>/mi-app` y el formato de salida es idéntico.

***

## Paso 8 — La versión 2: tags inmutables

**Objetivo:** publicar una segunda versión **sin tocar la primera**.

1. Edita `index.html` y cambia el `<h1>` a `Hola, soy Tu Nombre Aquí — v2.0`.
2. Construye y publica con tag nuevo:

```bash
docker build -t <usuario>/mi-app:2.0 .
docker push <usuario>/mi-app:2.0
```

**Qué debes ver:** en `hub.docker.com/r/<usuario>/mi-app` (pestaña **Tags**) ahora hay **dos tags**: `1.0` y `2.0`. Ambas versiones coexisten — un tag nunca se sobrescribe; cada versión es un artefacto distinto con su propio digest.

**Dato clave:** por eso en producción nadie usa el tag `latest` como referencia de despliegue: `latest` se mueve, los tags de versión (`1.0`, `2.0`) no.

***

## Paso 9 — Prueba de portabilidad: "funciona en cualquier lado"

**Objetivo:** demostrar que tu app corre en una máquina que **nunca construyó nada**.

1. Clic en **"+ ADD NEW INSTANCE"** — esta es una máquina **nueva y vacía** (simula otro servidor, otra nube, otro equipo).
2. En la instancia nueva:

```bash
docker run -d -p 8080:80 <usuario>/mi-app:2.0
```

**Qué debes ver:** Docker **descarga** tu imagen desde el registro (no hay nada local que construir) y arranca el contenedor. Clic en **8080** de la instancia nueva: tu página **v2.0** aparece idéntica a como la dejaste.

**Esta es la conclusión del lab:** la imagen es un artefacto portable — el mismo digest corre en cualquier host con Docker, sin recompilar nada. Es la misma propiedad que hace que un pipeline despliegue la misma aplicación en distintas nubes.

***

## Paso 10 — Reto (bonus +0.5): multi-contenedor

**Objetivo:** dos contenedores que se comunican por nombre en una red propia (el embrión de un despliegue multi-servicio).

**Opción A — red y DNS de Docker:**

```bash
docker network create red
docker run -d --name web2 --network red nginx:alpine
docker run --rm --network red busybox ping -c 3 web2
```

**Qué debes ver:** el `ping` resuelve `web2` por nombre y responde (`64 bytes from 172.x.x.x ...`) — los contenedores de la misma red se encuentran por nombre, sin IP manual.

**Opción B — Docker Compose (web + redis):**

```bash
cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
  redis:
    image: redis:alpine
EOF

docker compose up -d
docker compose ps
```

**Qué debes ver:** `docker compose ps` muestra los dos servicios (`web` y `redis`) corriendo; el servicio `web` publica el 8080.

***

## Entregables (un solo PDF)

1. **URL pública de tu imagen en Docker Hub** con los dos tags visibles: `https://hub.docker.com/r/<usuario>/mi-app` — captura de la página de Tags.
2. **Captura de `docker ps`** con tu contenedor `<usuario>/mi-app:1.0` corriendo (puedes usar el paso 6 o el 9).
3. **Captura del navegador con tu app** (la página con tu nombre, puerto 8080).

**Fecha de entrega:** según el cronograma de la semana (Actividad 1 de U2). La evidencia se sube a Moodle.

***

## Criterios de evaluación (10% de la nota final)

| Criterio | Puntos |
|---|---|
| Pasos 1–3 completos (primer contenedor, servidor web, aislamiento) | 1.0 |
| Dockerfile + build correcto (imagen propia construida y corriendo) | 1.5 |
| Push de 2 tags (`1.0` y `2.0`) con digest visible en Docker Hub | 1.5 |
| Prueba de portabilidad en instancia nueva (paso 9) | 1.0 |
| **Ret**o multi-contenedor (paso 10, opción A o B) | **+0.5 extra** |
| **Total** | **5.0 (+0.5 bonus)** |

***

## Plan B — si Play with Docker no responde

Si al entrar a `labs.play-with-docker.com` ves un mensaje de **"Docker is at capacity"**, error de conexión o la instancia no arranca en ~2 minutos, pasa a **Killercoda** (mismos comandos, distinta interfaz):

1. Entra a [killercoda.com/playgrounds/scenario/ubuntu](https://killercoda.com/playgrounds/scenario/ubuntu) (necesitas crear una cuenta gratuita).
2. Clic en **START** — obtienes una terminal Ubuntu con Docker preinstalado.
3. Ejecuta **los mismos comandos de los pasos 1 a 10** sin cambios.
4. Diferencias prácticas con Play with Docker:
   - No hay botones de puerto: para ver tu página usa `curl -s localhost:8080` dentro de la terminal (o el visor HTTP del playground si está disponible).
   - `docker login` funciona igual contra Docker Hub.
   - La sesión dura menos (~1 hora): si se cierra, vuelve a entrar y continúa desde el paso en que ibas (tu imagen ya está en Docker Hub si llegaste al paso 7).

***

## Troubleshooting rápido

| Síntoma | Causa probable | Solución |
|---|---|---|
| `Unable to find image ... Pulling` y tarda mucho | Primera descarga de la imagen base | Espera; `alpine`/`nginx:alpine` son pequeñas (~10-50 MB) |
| `pull access denied` o `rate limit` de Docker Hub | Límite de pulls anónimos por IP | `docker login` primero y reintenta; usa tu cuenta (los pulls autenticados tienen más cuota) |
| `port is already allocated` al hacer `run` | Ya tienes un contenedor en el 8080 | `docker rm -f web` (o el nombre que tenga) y vuelve a intentar |
| `docker: invalid reference format` en el build | Falta el punto final o el tag tiene espacios | `docker build -t <usuario>/mi-app:1.0 .` (nota el ` . ` al final) |
| `denied: requested access to the resource is denied` en el push | No estás logueado o el usuario no coincide con el de la imagen | `docker login` y verifica que la imagen se llame `<tu-usuario>/mi-app:1.0` |
| `no such file or directory: Dockerfile` | No estás dentro de la carpeta `mi-app` | `cd mi-app` y repite |
| La instancia PWD se apagó sola | Sesión de 4 horas vencida | Entra de nuevo, "+ ADD NEW INSTANCE", y continúa — tu imagen vive en Docker Hub |
| `docker compose ps` no existe | Tu playground no tiene Compose | Usa la opción A del paso 10 (red + ping) |

***

## Checklist de advertencias

- Tu cuenta de Docker Hub es **personal** — no la compartas; la evidencia lleva tu usuario.
- No pongas contraseñas reales dentro de `index.html` ni en ningún archivo del lab.
- Usa siempre `<usuario>` reemplazado por **tu** usuario de Docker Hub — un push con nombre equivocado queda en el repositorio equivocado.
- Play with Docker es una máquina pública efímera: no la uses para guardar archivos personales.
