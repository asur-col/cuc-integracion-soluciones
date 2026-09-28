# Laboratorio 1 — Sandbox de Contenedores: build → push → run en infraestructura propia

**Curso:** Integración de Soluciones para Plataformas Cloud — Ingeniería de Sistemas
**Docente:** Ing. Rodolfo Cañas Cervantes — Universidad de la Costa (CUC)
**Unidad 1 · Actividad 2 · Ponderación: 5% de la nota final**
**Duración estimada: 90 minutos** (parte práctica de la sesión, después del bloque teórico)

## Introducción

En la parte teórica vimos cómo las plataformas cloud se interconectan (VCN/VPC, peering, VPN). Ahora vas a ejecutar el flujo que hace posible desplegar una aplicación en cualquier nube: **construir una imagen de contenedor, subirla a un registro privado y correrla como servicio verificado**.

Vas a trabajar sobre un entorno Docker **real y aislado**, aprovisionado en servidores propios (ASUR) para esta clase: cada estudiante tiene su propio daemon Docker en modo *rootless* — sin acceso al sistema anfitrión y sin poder afectar a tus compañeros. Es el mismo patrón que usa un pipeline CI/CD de producción: `build → push → run → verify`.

No necesitas instalar nada en tu equipo: todo sucede en tu terminal web.

**Presupuesto de tiempo (90 min totales, no te desvíes de esto):**

| Parte | Tiempo |
|---|---|
| A — Entrar a tu entorno y verificar | 10 min |
| B — Construir la imagen (`build`) | 20 min |
| C — Subir al registro privado (`push`) | 15 min |
| D — Correr y verificar salud (`run` + `curl`) | 15 min |
| E — Entregable (evidencias) | 15 min |
| Margen para imprevistos | 15 min |

Si te atrasas en una parte, sigue adelante y documenta hasta donde llegaste — es mejor un entregable parcial completo que quedarte atascado en un solo paso.

***

## Requisitos previos (verifícalos antes de empezar)

1. Un navegador web (Chrome/Firefox/Edge actualizado).
2. Las credenciales que entregó el docente:
   - **URL única de entrada**: `https://labs.proyectoasur.org/` — es la misma para todo el curso, no hay una URL distinta por estudiante.
   - **Usuario de terminal**: cada estudiante tiene un usuario **asignado y fijo** entre `ios-est01` y `ios-est20` — el tuyo está en la tabla de abajo. Ese usuario es tu identidad en la evidencia del entregable.
   - **Clave de terminal**: `cuc2026lab` (la misma para las 20 cuentas).
   - **Usuario del registro Docker**: `ios-lab` — **ojo, NO es tu usuario de terminal** (`ios-estNN`), es un usuario distinto y único, igual para todos.
   - **Clave del registro Docker**: `cuc2026lab` — la misma clave que usaste para entrar a la terminal.

> Este lab corre íntegramente en infraestructura del curso. Nada se instala ni se configura en tu computador.

### Tabla de asignación — tu usuario del lab

Busca tu nombre y usa **exclusivamente** ese usuario durante todo el lab (orden alfabético por apellidos, según la lista oficial de clase del grupo PRESENCIAL-24801):

| Estudiante | Usuario asignado |
|---|---|
| ARRIETA RICARDO KEVIN ALFONSO | `ios-est01` |
| BARBOSA FERNANDEZ ARNOOLD | `ios-est02` |
| CARO MOLINA JUAN SEBASTIAN | `ios-est03` |
| DE LA HOZ GONZALEZ DAVID ANDRES | `ios-est04` |
| DOUGLAS ROMERO LUIS DAVID | `ios-est05` |
| ECHEVERRIA VERGARA ALEJANDRO | `ios-est06` |
| GOMEZ PINEDA ISABELLA MARIA | `ios-est07` |
| GUEVARA CARABALLO MARLENE DEL PILAR | `ios-est08` |
| JIMENEZ TERAN MELANY LORAINE | `ios-est09` |
| LIZARAZO DUARTE JUAN DAVID | `ios-est10` |
| LOPEZ ARIZA GIAN LUCAS | `ios-est11` |
| MONTERROZA CONTRERAS ALAN MANUEL | `ios-est12` |
| NARVAEZ VARELA ISAAC DANIEL | `ios-est13` |
| NIÑO CABRERA JUAN MANUEL | `ios-est14` |
| PARRA JESSURUM ISABELLA MAIGRET | `ios-est15` |
| PEDRAZA GRANADOS BRANDON DANIEL | `ios-est16` |
| PEREZ HADECHINI JUAN FRANCISCO | `ios-est17` |
| PEÑA DE LA TORRE JUAN DAVID | `ios-est18` |
| SUAREZ DIAZ SARAY PAOLA | `ios-est19` |
| SUAREZ NAVARRO ANDRES FELIPE | `ios-est20` |

***

## Parte A — Entrar a tu entorno (~10 min)

### A.1 — Abrir tu terminal web

1. Abre en el navegador `https://labs.proyectoasur.org/`.
2. En la página de login, escribe tu usuario asignado (ej. `ios-est07`, mira la tabla anterior) y la clave `cuc2026lab`. Nadie más usará tu usuario — si el login te rechaza, revisa que hayas escrito bien tu número.
3. Debe aparecer un banner como este:

```
============================================================
 Lab: Sandbox de Contenedores — Integración de Soluciones
 Usuario: ios-est07   |   Tu puerto: 8007   |   Registro: 200.30.0.3:5000
------------------------------------------------------------
 Flujo del lab (guía completa entregada en clase):
   cd ~/hello-multicloud
   docker build -t "$IMAGE" .
   docker login 200.30.0.3:5000          <- usuario y clave del registro
   docker push "$IMAGE"
   docker run -d --name hello -p 8007:3000 "$IMAGE"
   curl localhost:8007/health            <- ESTA ES TU EVIDENCIA
============================================================
```

> **Apunta tu puerto** (aparece en el banner): cada estudiante publica su app en un puerto distinto para no chocar con los demás.

### A.2 — Verificar tu entorno

Ejecuta y observa la salida:

```bash
whoami
docker version
ls ~/hello-multicloud
```

Resultado esperado:

- `whoami` → tu usuario (`ios-estNN` asignado).
- `docker version` → **Client** y **Server** con versión; si Server da error, avisa al docente.
- El proyecto starter con dos archivos: `server.js` y `Dockerfile`.

### A.3 — Entender qué vas a desplegar

Revisa el código de la app:

```bash
cat ~/hello-multicloud/server.js
```

Es un servidor HTTP mínimo con un endpoint de salud:

- `GET /health` → JSON `{"status":"ok","app":"hello-multicloud",...}` — **este endpoint es tu evidencia final**.
- Cualquier otra ruta → página HTML de bienvenida.

Y el Dockerfile:

```bash
cat ~/hello-multicloud/Dockerfile
```

Observa las 4 instrucciones: imagen base oficial (`node:22-alpine`), directorio de trabajo, copia del código y comando de arranque. Con eso basta para producción en este caso.

***

## Parte B — Construir la imagen (~20 min)

### B.1 — Build

```bash
cd ~/hello-multicloud
docker build -t "$IMAGE" .
```

La variable `$IMAGE` ya está preconfigurada en tu sesión apuntando a tu propio repositorio dentro del registro del curso (algo como `200.30.0.3:5000/hello-multicloud-ios-estNN:v1`). Puedes verla con `echo $IMAGE`.

**Qué está pasando (léelo una vez, sirve para el quiz de U1):** Docker descarga la capa base `node:22-alpine`, copia tu código y congela todo en una imagen inmutable identificada por un *digest* `sha256:...`. La segunda vez que corras `build` será casi instantánea: solo se reconstruyen las capas que cambiaron (*caché de capas*).

### B.2 — Verificar la imagen construida

```bash
docker images
```

Debe listar `hello-multicloud-ios-estNN` con tag `v1` y tamaño ~55 MB.

***

## Parte C — Push al registro privado (~15 min)

En producción nadie despliega desde el laptop: la imagen se publica en un registro y desde ahí se corre en cualquier nube. Aquí usamos un registro privado montado para el curso, con autenticación obligatoria.

### C.1 — Autenticarte

```bash
docker login 200.30.0.3:5000
```

Usuario: `ios-lab` (**no** tu usuario de terminal `ios-estNN`). Clave: `cuc2026lab` (la misma de tu terminal). La salida correcta termina en `Login Succeeded`.

> Si te equivocas de usuario/clave tres veces, espera 30 segundos e inténtalo de nuevo.

### C.2 — Publicar tu imagen

```bash
docker push "$IMAGE"
```

Salida esperada (captura esto para el entregable):

```
The push refers to repository [200.30.0.3:5000/hello-multicloud-ios-estNN]
v1: digest: sha256:92907e84d135... size: 856
```

El **digest** es la prueba criptográfica de que TU imagen quedó almacenada en el registro.

### C.3 — Comprobar que vive en el registro (opcional pero recomendable)

```bash
docker rmi "$IMAGE"
docker pull "$IMAGE"
```

Si puedes borrar tu copia local y re-descargarla desde el registro, la publicación fue perfecta.

***

## Parte D — Correr el contenedor y verificar salud (~15 min)

### D.1 — Run

```bash
docker run -d --name hello -p ${LAB_PORT}:3000 "$IMAGE"
docker ps
```

- `-d`: en segundo plano (daemonizado).
- `--name hello`: nombre fijo para referenciarlo.
- `-p ${LAB_PORT}:3000`: publica el puerto interno 3000 del contenedor en **tu** puerto asignado.

`docker ps` debe mostrar tu contenedor con status `Up ...` y el mapeo de puertos.

### D.2 — Verificación de salud (LA EVIDENCIA)

```bash
curl localhost:${LAB_PORT}/health
```

Salida esperada:

```json
{"status":"ok","app":"hello-multicloud","hostname":"abd43b2b9b2c","time":"2026-08-22T12:19:04Z"}
```

**Captura de pantalla de este comando con su salida completa** — es el requisito central del entregable: demuestra que un contenedor construido por ti, publicado en un registro y redeployado, está corriendo y respondiendo con un chequeo de salud automatizable (exactamente lo que haría un load balancer o un orquestador antes de enviar tráfico real).

Prueba también la raíz:

```bash
curl localhost:${LAB_PORT}/
```

***

## Parte E — Entregable (~15 min)

Un solo documento (PDF) con estas 4 evidencias, en este orden:

1. **Push al registro**: captura de la salida de `docker push` donde se vea el `digest: sha256:...`.
2. **Contenedor activo**: captura de `docker ps` mostrando `hello` con `Up` y el mapeo `${LAB_PORT}:3000`.
3. **Chequeo de salud**: captura de `curl localhost:${LAB_PORT}/health` con el JSON completo.
4. **Explicación de 3-5 líneas**: ¿por qué el flujo `build → push → run` es la base de un despliegue multicloud? (Pista: la imagen es inmutable y portable — el mismo digest puede correrse en AWS, Azure, GCP o en un servidor propio; lo único que cambia es dónde está el registro y el runtime.)

### Relación con la rúbrica (5% de la nota final)

| Criterio | Peso |
|---|---|
| Imagen construida correctamente (build sin errores) | 20% |
| Push exitoso al registro con digest visible | 25% |
| Contenedor corriendo con puerto correcto | 25% |
| Evidencia de health check + explicación del flujo | 30% |

***

## Troubleshooting rápido

| Síntoma | Causa probable | Solución |
|---|---|---|
| `port is already allocated` al hacer `run` | Usaste el puerto de otro estudiante | Usa TU `$LAB_PORT` del banner (variable ya configurada) |
| `denied: requested access to the resource is denied` en `push` | No estás autenticado o sesión expiró | Repite `docker login 200.30.0.3:5000` |
| `401 Unauthorized` al hacer `login` | Usaste tu usuario de terminal (`ios-estNN`) en vez del usuario del registro | El registro se autentica con usuario **`ios-lab`**, no con tu `ios-estNN`. Clave: `cuc2026lab` |
| `network unreachable` o timeout al hacer login/push | Escribiste mal la dirección del registro | El registro es `200.30.0.3:5000`, ni `localhost` ni otra IP |
| `docker version` no muestra sección Server | Tu daemon tardó en arrancar o se cayó | Avisa al docente (se reinicia con un comando) |
| Terminal web pide credenciales de nuevo | Sesión expirada | Vuelve a entrar a https://labs.proyectoasur.org/ con tu usuario y la clave `cuc2026lab` |
| Al abrir `https://labs.proyectoasur.org/` te manda directo a la terminal de otro compañero | Ese usuario quedó logueado en esta compu (es compartida) | Verás un panel "Sesión activa" — haz clic en **"Cerrar sesión y entrar con otro usuario"** y entra con el tuyo |

## Checklist de advertencias (revisar durante el lab)

- La clave es compartida, pero tu **usuario asignado** (tabla de arriba) es tu identidad para la evidencia — entra siempre con él, nunca con el de otro compañero.
- Todo corre remoto en los servidores del curso: no intentes instalar Docker en tu PC durante el lab.
- Usa siempre `$IMAGE` y `${LAB_PORT}` de tu sesión en vez de tipear valores a mano — evitas el 90% de los errores.
- Al terminar la clase el entorno se conserva unos días por si el docente pide evidencia adicional; después se limpia con el procedimiento de teardown.
- **Cierra tu sesión al terminar** (botón "Cerrar sesión y entrar con otro usuario" en `https://labs.proyectoasur.org/`) si compartes la computadora con un compañero — si no, el siguiente entra directo a tu terminal.
