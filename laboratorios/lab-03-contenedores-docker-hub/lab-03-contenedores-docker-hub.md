# Laboratorio 3 — Contenedores, segundo nivel: versionado, registro y portabilidad real (semana 8)

**Curso:** Integración de Soluciones para Plataformas Cloud — Ingeniería de Sistemas
**Docente:** Ing. Rodolfo Cañas Cervantes — Universidad de la Costa (CUC) · 2026-2
**Unidad 2 · Actividad 1 · Ponderación: 10% de la nota final**
**Duración estimada:** 90 min · **Modalidad:** sesión de navegador en `labs.proyectoasur.org` (estación con Docker real y registro con login, sin instalación)
**Guía visual:** esta es la versión técnica en Markdown; la guía ilustrada con diagrama y botones de copiado es `index.html`

> Ejecución técnica, diseño del laboratorio y verificación: asistente de IA (OpenCode) bajo dirección académica de **Ing. Rodolfo Cañas Cervantes**.
> Los 14 bloques de comandos ejecutables de esta guía (más el bloque ilustrativo de la *Nota de industria*, que lleva marcadores `<…>` y no se ejecuta) fueron corridos **en orden y literales** el 2026-10-03 dentro de una sesión real del Lab 3 creada por la plataforma (login → **Iniciar lab**): sin trabajo la evaluación respondió **0 de 5**, cada paso encendió su criterio y el bloque final (`revisar`) respondió **5 de 5 criterios en verde**. Ninguna salida está inventada.

## Introducción

**Este laboratorio es la continuación directa del Laboratorio 1** (Sandbox de contenedores, semana 3): ahí construiste una imagen, la publicaste en un registro privado y la corriste con verificación de salud. Aquí vas un nivel más allá — no se repite lo mismo, se completa lo que quedó fuera:

| | Laboratorio 1 (ya hecho) | Laboratorio 3 (este) |
|---|---|---|
| Registro | Privado, del curso, ya configurado para ti | **Con cuenta y clave: haces `docker login` tú** |
| Versionado | Una sola versión de la imagen | **Dos versiones (`v1` y `v2`) coexistiendo con digests distintos** |
| Portabilidad | Corre en tu estación | **Prueba real: la imagen baja del registro a un entorno limpio** |
| Multi-servicio | No aplica | **Reto: la app y un servicio de datos hablando por la red de Docker** |

Vas a trabajar en tu **sesión de `labs.proyectoasur.org`**: una estación real de Docker en el navegador, sin instalar nada en tu equipo. Publicas en **el registro de tu propia sesión** (`hub:5000`), que tiene **cuenta, clave y namespace propios tuyos**: `hub:5000/<tu-usuario>/mi-app`.

> **En la industria esto es Docker Hub / ECR / ACR / Artifact Registry: los comandos son los mismos.** Cambia el nombre del servidor y quién lo administra; `docker login`, `docker push`, `docker pull` y los digests son idénticos. Aquí no dependes de una cuenta pública ni de la cuota anónima de internet: el registro vive en tu sesión y se borra contigo.

> **La idea central del lab en una frase:** la imagen es inmutable y vive en el registro; cualquier máquina que la descargue obtiene exactamente la misma aplicación.

El recorrido completo, en este orden, es exactamente lo que `revisar` comprueba al final:

1. Entras a tu sesión y te autenticas en tu registro (`docker login` con tu cuenta de la sesión).
2. Correspond tu primer contenedor y un servidor web publicando el puerto 8080.
3. Lees el código de partida, construyes `mi-app` desde su `Dockerfile` y la corres.
4. Publicas `v1` y luego `v2` con etiquetas inmutables en `hub:5000/<tu-usuario>/mi-app`.
5. Compruebas la portabilidad: borras la copia local y la vuelves a bajar del registro.
6. Levantas el reto multi-contenedor con `docker compose`.
7. Ejecutas `revisar` y terminas con **5 de 5 criterios en verde**.

**Presupuesto de tiempo (90 min, no te desvíes):**

| Parte | Tiempo |
|---|---|
| 0 — Entra y conoce tu registro | 10 min |
| Pasos 1–2 — Primer contenedor, puertos y aislamiento | 15 min |
| Pasos 3–5 — Tu app: Dockerfile, build y run | 25 min |
| Pasos 6–7 — Registro: push y versionado | 20 min |
| Paso 8 — Prueba de portabilidad | 10 min |
| Paso 9 — Reto multi-contenedor | 5 min |
| Paso 10 — Entregable (`revisar`) | 5 min |

***

## Paso 0 — Entra y conoce tu registro (~10 min)

**Objetivo:** abrir tu sesión y descubrir **tu** cuenta en el registro de la clase.

### 0.1 Abre tu sesión

1. Entra en <https://labs.proyectoasur.org> con tus credenciales.
2. Busca el **Lab 3 — Contenedores y Docker Hub** y pulsa **Iniciar lab**.
3. Cuando diga **Entrar**, ábrelo: verás tu terminal y una pestaña **Mi aplicación** (todavía vacía: la llenas en el paso 5).

### 0.2 Tu espacio de trabajo

Tu estación trae Docker de verdad y el código de partida; el comando `mi-espacio` te lo copia y te deja la lista de archivos a la vista.

```bash
docker version
mi-espacio
```

**Qué debes ver:** la versión del servidor de Docker (no es un simulador) y, en `/workspace/app`, cinco archivos: `Dockerfile`, `package.json`, `server.js`, `datos.js` y `docker-compose.yml`.

### 0.3 Tu cuenta en el registro de tu sesión

La plataforma generó **para tu sesión** un registro con autenticación y unas credenciales que viven solo en tu estación, en el fichero `/etc/labs-hub-credenciales`. Cárgalas en tu terminal y acéstate con `docker login`:

```bash
. /etc/labs-hub-credenciales
echo "registro: $REGISTRO   usuario: $USUARIO   repositorio: $REGISTRO/$USUARIO/mi-app"
printf '%s' "$CLAVE" | docker login "$REGISTRO" -u "$USUARIO" --password-stdin
```

**Qué debes ver:** la ruta de tu repositorio y, al final, `Login Succeeded`.

> **Tu clave no se imprime ni se pega.** Solo se carga en las variables de tu terminal y entra al registro por `stdin` (`--password-stdin`), así que no aparece en capturas, en la evidencia ni en el historial. Si la escribes a mano y te equivocas, el registro la **rechaza**: no hay cuenta que "se salve" con una clave mala. `mi-espacio` te recuerda dónde vive.

> **Un solo laboratorio a la vez.** Tu sesión se cierra sola a los 180 min (2 × tu tiempo estimado de 90) y al terminar se borra todo: tus imágenes, tus contenedores y tu registro. Lo único que queda es la evidencia que registra `revisar`.

***

## Paso 1 — Tu primer contenedor (imagen vs. contenedor)

**Objetivo:** ver la diferencia entre una **imagen** (el paquete inmutable) y un **contenedor** (la instancia en ejecución).

```bash
docker run --rm hello-world
docker ps -a
```

**Qué debes ver:**

1. `docker run hello-world` descarga la imagen (si no la tienes) y ejecuta un contenedor que imprime `Hello from Docker!` y los cuatro pasos: cliente → daemon → creación → salida.
2. `docker run --rm` borra el contenedor al salir, así que `docker ps -a` queda vacío: no hay nada ocupando disco.

**Dato clave:** `docker ps` solo muestra los contenedores **activos**; `docker ps -a` los muestra todos (también los detenidos).

***

## Paso 2 — Un servidor web en un contenedor (puertos y modo detached)

**Objetivo:** correr un proceso que **no termina** (un servidor web) y publicar su puerto hacia afuera.

```bash
docker run -d --name web -p 8080:80 nginx:1.27-alpine
docker ps --filter name=web
curl -s http://127.0.0.1:8080 | head -5
```

- `-d`: en segundo plano (detached) — la terminal queda libre.
- `-p 8080:80`: publica el **puerto 80** del contenedor en el **puerto 8080** de tu estación.
- `--name web`: le pone nombre para referenciarlo después.

**Qué debes ver:** el contenedor `web` con STATUS `Up` y el mapeo `0.0.0.0:8080->80/tcp`, y en el `curl` la cabecera `<!DOCTYPE html>` de la página de bienvenida de nginx. En el navegador, la pestaña **Mi aplicación** de tu sesión muestra exactamente eso: lo que haya en el 8080 de tu estación.

### 2.1 Ejecutar algo dentro del contenedor (aislamiento)

**Objetivo:** comprobar que el contenedor tiene **su propio sistema de archivos**, distinto al de tu estación.

```bash
docker exec web cat /etc/os-release
docker exec web nginx -v
```

**Qué debes ver:** el `ID=alpine` (o la base de nginx) y `nginx version: nginx/1.27.x`. Con `docker exec -it web sh` entrarías a un shell **dentro** del contenedor y saldrías con `exit`; aquí lo usamos en modo no interactivo para que puedas pegar el bloque completo.

**Dato clave:** el contenedor corre su propia distribución aunque la estación sea otra — aislamiento a nivel de proceso y de sistema de archivos.

***

## Paso 3 — Tu propia app: el código de partida

**Objetivo:** leer los archivos que vas a construir.

```bash
cd /workspace/app
ls -la
cat Dockerfile
```

**Qué debes ver:** el `Dockerfile` con dos secciones: `FROM node:22-alpine` (la imagen base) y las instrucciones `COPY`, `RUN npm install`, `ARG VERSION` y `CMD`. Fíjate en dos cosas:

- `ARG VERSION=2.0.0` + `ENV VERSION=${VERSION}`: la versión **entra por build-arg**, así que puedes construir la v1 y la v2 sin editar el Dockerfile.
- `HEALTHCHECK ... /salud`: el mismo sondeo que en el Lab 1.

Los otros cuatro archivos son la app (`server.js`), el servicio de datos del reto (`datos.js`), sus dependencias (`package.json`) y el `docker-compose.yml` del paso 9.

***

## Paso 4 — Construir la imagen (capas y tags)

**Objetivo:** convertir el código en una imagen identificable por tag.

```bash
cd /workspace/app
docker build --build-arg VERSION=1.0.0 -t mi-app:1.0.0 .
docker images --filter reference=mi-app
```

> **El punto final** (` . `) del build es obligatorio: indica que el contexto de construcción es la carpeta actual.

**Qué debes ver:**

1. El build termina con `naming to docker.io/library/mi-app:1.0.0 done`.
2. `docker images` lista `mi-app` con tag `1.0.0`.

**Dato clave:** una imagen es una **pila de capas inmutables**. Si más adelante cambias solo `server.js`, el `npm install` se sirve del caché y el build es inmediato: por eso construir sobre una imagen base conocida es barato.

***

## Paso 5 — Ejecutar tu imagen (ciclo build → run)

**Objetivo:** reemplazar el nginx genérico por **tu** app en el puerto 8080.

```bash
cd /workspace/app
docker rm -f web
docker run -d --name mi-app -p 8080:3000 mi-app:1.0.0
sleep 5
curl -s http://127.0.0.1:8080/salud
```

**Qué debes ver:** el `curl` responde `{"estado":"ok","version":"1.0.0",...}` y la pestaña **Mi aplicación** muestra ahora **tu** app («Mi aplicación contenedorizada» con **Versión 1.0.0**), no la página genérica de nginx.

***

## Paso 6 — El registro: publica tu imagen (push)

**Objetivo:** subir tu imagen a **tu** namespace del registro de la sesión, con la etiqueta inmutable `v1`.

```bash
cd /workspace/app
. /etc/labs-hub-credenciales
docker tag mi-app:1.0.0 $REGISTRO/$USUARIO/mi-app:v1
docker push $REGISTRO/$USUARIO/mi-app:v1
curl -s -u "$USUARIO:$CLAVE" http://$REGISTRO/v2/$USUARIO/mi-app/tags/list
```

- `docker tag` crea un **alias** con la ruta completa: `hub:5000/<tu-usuario>/mi-app:v1`. Sin ese alias, `push` no sabe a qué namespace subir.
- `docker push` sube las capas que falten y termina con `v1: digest: sha256:...`: la **prueba criptográfica** de que tu imagen quedó almacenada.
- El `curl` consulta la API del registro (con tu usuario y clave por la misma sesión) y debe responder `{"name":"<tu-usuario>/mi-app","tags":["v1"]}`.

**Comprueba tu namespace:** solo tú publicas en `hub:5000/<tu-usuario>/mi-app`; el registro es de tu sesión, así que lo de los demás no está ahí.

***

## Paso 7 — La versión 2: etiquetas inmutables

**Objetivo:** publicar una segunda versión **sin tocar la primera**.

El cambio de versión entra por build-arg: mismo Dockerfile, otro contenido de imagen.

```bash
cd /workspace/app
. /etc/labs-hub-credenciales
docker build --build-arg VERSION=2.0.0 -t mi-app:2.0.0 .
docker tag mi-app:2.0.0 $REGISTRO/$USUARIO/mi-app:v2
docker push $REGISTRO/$USUARIO/mi-app:v2
docker inspect -f '{{.Id}}' mi-app:1.0.0 mi-app:2.0.0
curl -s -u "$USUARIO:$CLAVE" http://$REGISTRO/v2/$USUARIO/mi-app/tags/list
```

**Qué debes ver:**

1. `docker inspect` imprime **dos IDs distintos**: cada versión es un artefacto con su propio digest.
2. El `curl` ya lista **dos tags**: `v1` y `v2`. Ambas coexisten — una etiqueta nunca se sobrescribe.

**Dato clave:** por eso en producción nadie despliega `latest`: `latest` se mueve, las etiquetas de versión (`v1`, `v2`) no. Cambiar el código y volver a publicar con la **misma** etiqueta es exactamente lo que no hay que hacer.

***

## Paso 8 — Prueba de portabilidad: "funciona en cualquier lado"

**Objetivo:** demostrar que tu app corre en un entorno que **no tiene nada tuyo**.

```bash
cd /workspace/app
. /etc/labs-hub-credenciales
docker rmi mi-app:2.0.0 $REGISTRO/$USUARIO/mi-app:v2
docker pull $REGISTRO/$USUARIO/mi-app:v2
docker run -d --rm --name portabilidad -p 18080:3000 $REGISTRO/$USUARIO/mi-app:v2
sleep 5
curl -s http://127.0.0.1:18080/salud
docker rm -f portabilidad
```

Borraste **ambas etiquetas locales** (la imagen desapareció de tu estación), la volviste a descargar desde el registro y arrancó en un contenedor nuevo que nunca la construyó. Esa es la conclusión del lab: la imagen es un artefacto portable — el mismo digest corre en cualquier host con Docker, sin recompilar nada. Es la misma propiedad que hace que un pipeline despliegue la misma aplicación en distintas nubes.

***

## Paso 9 — Reto (bonus +0.5): multi-contenedor

**Objetivo:** dos contenedores que se comunican por nombre en una red propia: la app y su servicio de datos.

```bash
cd /workspace/app
docker rm -f mi-app
docker compose up -d --build
sleep 10
docker compose ps
curl -s http://127.0.0.1:8080/datos
```

**Qué debes ver:** `docker compose ps` muestra los dos servicios (`app` y `datos`) corriendo, y el `curl` responde `{"origen":"servicio-de-datos","visitas":N,...}`: el contador **no** lo lleva la app, lo lleva el **otro** contenedor (`datos.js`), al que la app llama por el nombre `datos` dentro de la red de compose.

Vuelve a llamar a `/datos` varias veces y mira los logs de ambos:

```bash
curl -s http://127.0.0.1:8080/datos
docker compose logs --tail 20
```

> Este levantamiento deja tu app en el puerto 8080, que es lo que ve la pestaña **Mi aplicación**.

***

## Paso 10 — Entregable (un solo comando)

El entregable es la **evidencia registrada por la plataforma**. Ejecuta el validador:

```bash
revisar
```

`revisar` **no decide si aprobaste**: solo le pide al servidor que evalúe tu trabajo. La comprobación se hace **desde fuera de tu estación** — mirando tu namespace en el registro, el HTTP de tu app y el compose en marcha —, así que lo que imprima tu terminal no cuenta. Deberías terminar con **5 de 5 criterios en verde**:

| Criterio | Qué comprueba el servidor |
|---|---|
| Etiqueta v1 publicada | Existe `v1` (o `1.0.0`) en `hub:5000/<tu-usuario>/mi-app` |
| Etiqueta v2 con digest distinto | Existe `v2` y su digest no es el de `v1` (etiquetas inmutables) |
| El contenedor responde HTTP | La app responde 200 con su contenido en el puerto 8080 de tu estación |
| Prueba de portabilidad | La imagen publicada se descarga del registro y corre en un contenedor limpio |
| Reto multi-contenedor | El compose está en marcha y `/datos` responde desde el servicio de datos |

***

## Nota de industria — Docker Hub, ECR, ACR y Artifact Registry

**El registro de tu sesión es un Docker Hub propio de la clase**: el mismo software de registro, con autenticación y namespace por estudiante. En la industria usas el servicio gestionado de tu proveedor — **Docker Hub**, **ECR** (AWS), **ACR** (Azure) o **Artifact Registry** (Google) — y los comandos son **exactamente los mismos**:

```bash
docker login <servicio-del-registro>
docker tag mi-app:1.0.0 <servicio-del-registro>/<cuenta>/mi-app:v1
docker push <servicio-del-registro>/<cuenta>/mi-app:v1
docker pull <servicio-del-registro>/<cuenta>/mi-app:v1
```

Lo único que cambia es **quién administra el registro** y cómo se paga (cuota anónima, cuenta corporativa o factura por uso). Aquí no dependes de internet ni de la cuota pública: el registro vive en tu sesión y el `revisar` lo evalúa desde el servidor, contra ese mismo registro.

***

## Criterios de evaluación (10% de la nota final)

La plataforma tiene **cinco criterios con el mismo peso** y cada uno se comprueba **desde el servidor**, contra el estado real de tu sesión: la API de tu registro, el HTTP de tu estación y el compose en marcha.

| Criterio | Peso | Lo que se comprueba |
|---|---|---|
| Etiqueta v1 publicada | 20% | La imagen está en tu namespace del registro con etiqueta `v1` |
| Etiqueta v2 con digest distinto | 20% | Publicación con etiquetas inmutables, verificada por digest |
| Contenedor responde HTTP | 20% | La app corre, responde 200 y es visible en la vista web de la sesión |
| Prueba de portabilidad | 20% | La imagen publicada se descarga del registro y corre en un entorno limpio |
| Reto multi-contenedor | 20% | Compose en marcha con app + servicio de datos comunicados |

Cada paso enciende su criterio: sin trabajar, **0 de 5**; con la app corriendo, 1; con `v1` publicada, 2; con `v2` publicada, **4** — se encienden las etiquetas inmutables y, de una vez, la portabilidad, porque es una propiedad del artefacto publicado—; y con el compose en marcha, **5 de 5**. Si alguno se queda en rojo, `revisar` te dice con qué comando arreglarlo.

**Ponderación en la nota de la asignatura: Actividad 1 de U2, 10%.**

***

## Plan B — si tu sesión no arranca

Si **Iniciar lab** no despliega nada en ~2 minutos o la terminal no aparece, pasa a la cola (la plataforma te dice tu posición) o recarga la página (`F5`) y vuelve a entrar. Tu sesión es **tuya y efímera**: si se cierra sola por inactividad, inicia otra y continúa desde el paso en que ibas — tu imagen publicada vive mientras viva **esa** sesión, y el registro se crea con ella.

***

## Troubleshooting rápido

| Síntoma | Causa probable | Solución |
|---|---|---|
| `docker push` falla con *unauthorized* o *denied* | No hiciste login, o te equivocaste al escribir la clave | `. /etc/labs-hub-credenciales` y repite el `docker login` del paso 0.3. Una clave incorrecta siempre se rechaza |
| `curl` a la API del registro responde `401` | La petición va sin credenciales | Usa `-u "$USUARIO:$CLAVE"` con las variables ya cargadas |
| `push` falla con *connection refused* hacia `hub:5000` | El registro de la sesión aún no está listo | Espera 10 s, comprueba `getent hosts hub` y reintenta |
| `push` falla con *http: server gave HTTP response to HTTPS client* | El registro no está en `insecure-registries` | No debería pasar: el `daemon.json` de la estación ya trae `hub:5000`; avisa al docente |
| `port is already allocated` al hacer `run` | Ya tienes algo en el 8080 | `docker rm -f web mi-app` y vuelve a intentar |
| `v1` y `v2` tienen el mismo digest | Publicaste dos etiquetas sin cambiar nada | Construye con otro `--build-arg VERSION=...` y vuelve a publicar |
| `docker: invalid reference format` en el build | Falta el punto final o el tag tiene espacios | `docker build --build-arg VERSION=1.0.0 -t mi-app:1.0.0 .` |
| `/datos` responde `memoria-local` | El servicio `datos` no está corriendo | `docker compose ps` y `docker compose logs` |
| El compose no levanta: puerto ocupado | Tu app del paso 5 sigue en el 8080 | El paso 9 ya la quita con `docker rm -f mi-app`; repítelo |
| La pestaña **Mi aplicación** está en blanco | No hay nada escuchando en el 8080 | Repite el paso 5 o el paso 9 |
| `revisar` no ve mis etiquetas | Publicaste en otro namespace o sin login | `echo $REGISTRO/$USUARIO/mi-app` y compara con el paso 6 |

***

## Referencias

- Docker Registry — API v2 (la misma que consulta `revisar` desde el servidor): <https://docs.docker.com/registry/spec/api/>
- Docker — `docker login` y credenciales por `stdin`: <https://docs.docker.com/reference/cli/docker/login/>
- Docker — etiquetas y digests de imagen: <https://docs.docker.com/get-started/docker-concepts/building-images/tagging-images/>
- Docker — capas y caché de builds: <https://docs.docker.com/build/cache/>
- Docker — registros sin TLS en red local: <https://docs.docker.com/registry/insecure/>
- Docker Compose — referencia: <https://docs.docker.com/compose/>

***

## Checklist antes de entregar

- Entraste con **Iniciar lab** y cargaste tus credenciales con `. /etc/labs-hub-credenciales` (la clave nunca se imprimió).
- Hiciste `docker login` contra `hub:5000` y terminó en `Login Succeeded`.
- `mi-app:1.0.0` corre en tu estación y la pestaña web muestra **Versión 1.0.0**.
- `$REGISTRO/$USUARIO/mi-app:v1` y `:v2` están publicadas y sus digests son distintos.
- Borraste la copia local, la bajaste de nuevo del registro y respondió `/salud` (portabilidad).
- El reto multi-contenedor está en marcha y `/datos` responde `servicio-de-datos`.
- Ejecutaste `revisar` y los cinco criterios están en verde.
