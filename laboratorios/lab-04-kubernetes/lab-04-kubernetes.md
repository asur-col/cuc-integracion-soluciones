# Laboratorio 4 — Kubernetes: pods, deployments y services

**Curso:** Integración de Soluciones para Plataformas Cloud — Ingeniería de Sistemas
**Docente:** Ing. Rodolfo Cañas Cervantes — Universidad de la Costa (CUC) · 2026-2
**Unidad 2 · Actividad 2 · Ponderación: 10% de la nota final**
**Duración estimada:** 90 min · **Modalidad:** sesión de navegador en `labs.proyectoasur.org` (estación + registro + clúster de un nodo, sin instalación)
**Guía visual:** esta es la versión técnica en Markdown; la guía ilustrada con diagrama y botones de copiado es `index.html`

> Ejecución técnica, diseño del laboratorio y verificación: asistente de IA (OpenCode) bajo dirección académica de **Ing. Rodolfo Cañas Cervantes**.
> Los 16 bloques de comandos de esta guía fueron ejecutados **en orden y literales** el 2026-10-03 dentro de una sesión real del Lab 4 creada con `labctl`: bloques 1–15 terminaron con `exit=0` y el bloque 16 (`revisar`) respondió **5 de 5 criterios en verde** evaluado por el servidor de la plataforma. Ninguna salida está inventada.

## Introducción

**Este laboratorio cierra el arco de los Labs 1 y 3.** Ahí construiste una imagen y la publicaste en un registro; la pregunta que quedaba pendiente es: **¿quién decide cuántas copias corren, las reinicia si se caen y las actualiza sin cortar el servicio?** La respuesta es un **orquestador**, y aquí lo usas: cada estudiante tiene **su propio clúster Kubernetes de un nodo** con `kubectl` listo, sin instalar nada.

| | Laboratorio 1 y 3 (ya hechos) | Laboratorio 4 (este) |
|---|---|---|
| Quién corre tu app | Tú, con `docker run` a mano | **Un Deployment con 3 réplicas declaradas** |
| Si un contenedor se cae | Nadie lo repone | **El ReplicaSet lo repone solo** |
| Si cambia la versión | Detener y volver a arrancar | **Rollout con historial y rollback instantáneo** |
| Expuesto en un puerto | Mapeo manual de puertos | **Service con selector, endpoints y balanceo** |

Los ocho pasos de esta guía, en este orden, son exactamente lo que `revisar` comprueba desde el servidor:

1. Exploras tu clúster y entiendes qué es un nodo y qué es un pod.
2. Construyes `mi-app` y la subes a **tu** registro privado (`registry:5000`).
3. Despliegas un **Deployment** con 3 réplicas, sondas y límites de recursos.
4. Expones la app con un **Service** NodePort y ves el balanceo en la pestaña web.
5. Borras un pod y miras cómo el ReplicaSet lo repone.
6. Escalas de 3 a 5 y vuelves a 3 sin tocar pods a mano.
7. Despliegas la v2 y haces rollback a la v1.
8. Ejecutas `revisar` y terminas con **5 de 5 criterios en verde**.

> **La idea central del lab en una frase:** en Kubernetes no das órdenes de ejecución, declaras un estado deseado y el clúster trabaja para que la realidad lo alcance y se mantenga.

**Presupuesto de tiempo (90 minutos, no te desvíes):**

| Parte | Tiempo |
|---|---|
| 1 — Entra y explora tu clúster | 10 min |
| 2 — Construye mi-app y súbela a tu registro | 15 min |
| 3 — Deployment con 3 réplicas, sondas y límites | 15 min |
| 4 — Service y la app en la pestaña web | 10 min |
| 5 — Autorreparación (borra un pod) | 10 min |
| 6 — Escalado 5 y vuelta a 3 | 10 min |
| 7 — Rollout v1 → v2 y rollback | 15 min |
| 8 — Entregable (`revisar`) | 5 min |

***

## Paso 1 — Entra y explora tu clúster (~10 min)

**Objetivo:** entrar a tu sesión y distinguir **nodo** (la máquina) de **pod** (la unidad de despliegue).

### 1.1 Abre tu sesión

1. Entra en <https://labs.proyectoasur.org> con tus credenciales.
2. Busca el **Lab 4 — Kubernetes: pods, deployments y services** y pulsa **Iniciar lab**.
3. Cuando diga **Entrar**, ábrelo: verás tu terminal y una pestaña **Mi aplicación** (todavía vacía: la llenas en el paso 4).

### 1.2 Prepara tu espacio y mira el estado

Tu código de partida y tu clúster ya están en la estación; `mi-espacio` te deja en el directorio de trabajo y comprueba que el nodo está en marcha:

```bash
mi-espacio
kubectl get nodes
kubectl get pods -A
```

**Qué deberías ver:** el código copiado a `/workspace/app`, el nodo con estado `Ready` y, en el espacio de nombres `kube-system`, los pods `coredns` y `local-path-provisioner` en `Running`. En los primeros segundos del arranque el nodo puede aún estar en `NotReady`: espera 10 segundos y vuelve a ejecutar el bloque.

> **Un solo laboratorio a la vez.** Tu sesión se apaga sola si pasas demasiado tiempo sin trabajar y al terminar se borra todo: los pods, los manifiestos, tu imagen en el registro y el clúster completo. Lo único que queda es la evidencia que registra `revisar`.

### 1.3 Nodo y pod

Un **nodo** es la máquina donde corren tus workloads: tiene un `kubelet` que habla con el API server y un `containerd` que arranca los contenedores. Un **pod** es la unidad más pequeña que despliegas: uno o varios contenedores con la misma red y el mismo disco, con vida propia (se crea, se muere y no se "mueve": se recrea).

```bash
kubectl get nodes -o wide
kubectl describe node | grep -A14 'Capacity'
kubectl get pods -A -o wide
```

**Qué deberías ver:** la IP del nodo (por ejemplo `172.16.0.3`), la versión de Kubernetes y el runtime `containerd`, y en el `describe` los campos `Capacity` y `Allocatable` (CPU, memoria y límite de pods disponibles). Los pods de `kube-system` son del clúster: tú no los tocas.

***

## Paso 2 — Construye mi-app y súbela a tu registro (~15 min)

**Objetivo:** repetir el ciclo `build → push` de los Labs 1 y 3, pero contra **el registro de tu sesión** (`registry:5000`, privado: otro estudiante ve un catálogo vacío). De ahí lo va a leer **Kubernetes**, no `docker run`.

### 2.1 Lee el código de partida

```bash
cd /workspace/app
cat server.js
cat Dockerfile
```

Fíjate en dos cosas: el endpoint `/salud` (devuelve `{"estado":"ok", ...}` con el nombre del pod) es el que van a usar las sondas, y el `ARG VERSION` del Dockerfile es el que te va a permitir construir la v2 en el paso 7.

### 2.2 Construye

```bash
cd /workspace/app
docker build -t "$LAB_REGISTRO/mi-app:1.0.0" .
docker images | grep mi-app
```

`$LAB_REGISTRO` ya está definido en tu sesión y apunta a `registry:5000` (`echo $LAB_REGISTRO` para comprobarlo). La imagen base `node:22-alpine` ya está en caché, así que el build tarda unos segundos.

### 2.3 Publica y verifica

```bash
docker push "$LAB_REGISTRO/mi-app:1.0.0"
curl -s http://$LAB_REGISTRO/v2/mi-app/tags/list
```

**Qué deberías ver:** el push termina con el `digest` y el `curl` responde `{"name":"mi-app","tags":["1.0.0"]}`. Si está vacío o da error, **no pases al paso 3**: sin esa etiqueta en el registro, el clúster no puede bajar la imagen y el criterio de `revisar` se queda en rojo.

***

## Paso 3 — Deployment: 3 réplicas, sondas y límites (~15 min)

**Objetivo:** declarar la intención —"quiero 3 copias de esta imagen"— y dejar que el clúster la cumpla. Un **Deployment** es lo que declaras; detrás lleva un **ReplicaSet** que lleva la cuenta de pods.

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mi-app
spec:
  replicas: 3
  selector:
    matchLabels: { app: mi-app }
  template:
    metadata:
      labels: { app: mi-app }
    spec:
      containers:
        - name: mi-app
          image: registry:5000/mi-app:1.0.0
          ports: [{ containerPort: 3000 }]
          readinessProbe:
            httpGet: { path: /salud, port: 3000 }
            initialDelaySeconds: 2
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /salud, port: 3000 }
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests: { cpu: 50m, memory: 64Mi }
            limits: { cpu: 250m, memory: 128Mi }
EOF
kubectl rollout status deploy/mi-app --timeout=120s
```

La imagen es exactamente la que publicaste: `echo $LAB_REGISTRO` devuelve `registry:5000`. Las dos sondas apuntan a `/salud`: la **readiness** decide si el pod entra al Service (si no responde, no recibe tráfico) y la **liveness** decide si el contenedor se reinicia. Los `limits` son el techo que comparte cada pod.

### 3.1 Comprueba el estado

```bash
kubectl get deploy,rs,pods -o wide
kubectl get pods -l app=mi-app
```

**Qué deberías ver:** en `deploy` la columna `READY` en `3/3`, un ReplicaSet con sufijo tipo `97c55fb76` y tres pods con nombres distintos en estado `Running`. El `rollout status` del bloque anterior termina con `deployment "mi-app" successfully rolled out`.

***

## Paso 4 — Service: una dirección para tres pods (~10 min)

**Objetivo:** darle a los pods un nombre estable y un balanceo: con `selector: { app: mi-app }` el **Service** encuentra los pods con esa etiqueta y mantiene su lista de IPs en los **endpoints**. Los pods se crean y se borran con nombres aleatorios; nadie debe memorizarlos.

```bash
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Service
metadata: { name: mi-app }
spec:
  type: NodePort
  selector: { app: mi-app }
  ports: [{ port: 80, targetPort: 3000, nodePort: 30080 }]
EOF
sleep 3
kubectl get svc mi-app
kubectl get endpoints mi-app
```

**Qué deberías ver:** el Service con `PORT(S)` `80:30080/TCP` y los endpoints con **tres IPs** (una por pod). El mensaje *Warning: v1 Endpoints is deprecated* es normal: es un aviso de Kubernetes, no un error.

### 4.1 La app responde y balancea

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:30080/salud
for i in $(seq 1 8); do curl -s http://127.0.0.1:30080/ | grep -o 'Pod <strong>[^<]*'; done
```

**Qué deberías ver:** un `200` y, en las ocho peticiones, **varios nombres de pod distintos**: eso es el balanceo. Ahora abre la pestaña **Mi aplicación** de tu sesión: verás la misma página con el nombre del pod que te respondió — recarga y cambiará.

> **`Service` no es `NodePort` en producción.** Aquí usamos `NodePort` porque tu clúster es de un nodo y necesitas ver la app desde la pestaña web. En la nube normalmente pondrías `LoadBalancer` o entrarías por un ingress; el selector, los endpoints y el balanceo son exactamente los mismos.

***

## Paso 5 — Autorreparación: borra un pod (~10 min)

**Objetivo:** ver por qué existe el ReplicaSet. Tú vas a matar un pod a mano; él quería 3, ve 2 y crea uno nuevo. **No lo repares tú**: solo borra y observa.

```bash
kubectl get pods -l app=mi-app
P=$(kubectl get pods -l app=mi-app --no-headers | awk '$3=="Running"{print $1; exit}')
echo "voy a borrar $P"
kubectl delete pod "$P"
sleep 8
kubectl get pods -l app=mi-app
```

**Qué deberías ver:** el pod que borraste desaparece, aparece uno con **otro nombre** y vuelves a tener 3 pods `Running`. Mira quién lo hizo:

```bash
kubectl get events --field-selector involvedObject.kind=ReplicaSet --sort-by=.lastTimestamp | tail -5
```

Entre los eventos verás `SuccessfulCreate` con un mensaje como *"Created pod: mi-app-97c55fb76-xxxxx"*: ese es el ReplicaSet reponiendo la cuenta. Es el mismo mecanismo con el que Kubernetes aguanta la caída de un nodo.

***

## Paso 6 — Escalado: de 3 a 5 y vuelta a 3 (~10 min)

**Objetivo:** escalar cambiando un número en el Deployment, no arrancando contenedores a mano.

```bash
kubectl scale deploy/mi-app --replicas=5
sleep 10
kubectl get pods -l app=mi-app --no-headers | wc -l
kubectl scale deploy/mi-app --replicas=3
sleep 10
kubectl get deploy mi-app
kubectl get pods -l app=mi-app
```

**Qué deberías ver:** después del primer `scale` el conteo da `5`; después del segundo, el Deployment vuelve a `3/3` y dos pods desaparecen (el ReplicaSet los termina, no tú). Fíjate en que el `selector` del Service no se enteró de nada: los endpoints siguen apuntando a los pods vivos.

***

## Paso 7 — Rollout v1 → v2 y rollback (~15 min)

**Objetivo:** actualización continua sin caída. Construyes la v2 con otra etiqueta, la publicas y le dices al Deployment que use esa imagen: creará un ReplicaSet nuevo, irá poniendo sus pods en `READY` uno a uno y bajará el antiguo a 0.

### 7.1 Construye y publica la v2

```bash
cd /workspace/app
docker build --build-arg VERSION=2.0.0 -t "$LAB_REGISTRO/mi-app:2.0.0" .
docker push "$LAB_REGISTRO/mi-app:2.0.0"
curl -s http://$LAB_REGISTRO/v2/mi-app/tags/list
```

### 7.2 Cambia la imagen y mira el rollout

```bash
kubectl set image deploy/mi-app mi-app="$LAB_REGISTRO/mi-app:2.0.0"
kubectl rollout status deploy/mi-app --timeout=120s
kubectl rollout history deploy/mi-app
curl -s http://127.0.0.1:30080/ | grep -o 'Versión <strong>[^<]*'
```

**Qué deberías ver:** `deployment "mi-app" successfully rolled out`, un historial con más de una revisión y la app respondiendo **Versión 2.0.0** en la pestaña web. Cada cambio de imagen es una revisión nueva: `rollout history` es tu bitácora.

### 7.3 Vuelve atrás (rollback)

```bash
kubectl rollout undo deploy/mi-app
kubectl rollout status deploy/mi-app --timeout=120s
kubectl rollout history deploy/mi-app
curl -s http://127.0.0.1:30080/ | grep -o 'Versión <strong>[^<]*'
```

**Qué deberías ver:** la respuesta vuelve a **Versión 1.0.0** sin que tú tocaras nada más. El aviso *Warning: resource deployments/mi-app was previously managed with 'kubectl apply'* es inofensivo: te recuerda que la anotación de "último apply" no se actualiza con el rollback.

***

## Paso 8 — Entregable: `revisar` (~5 min)

El entregable es la **evidencia registrada por la plataforma**. Desde tu terminal:

```bash
revisar
```

Ese comando **no decide nada**: solo le pide al servidor que evalúe tu trabajo. La comprobación se hace **desde fuera de tu estación** — mirando tu registro, el estado real del clúster y las respuestas HTTP de tu Service —, así que lo que imprima tu terminal no cuenta. Deberías terminar con **5 de 5 criterios en verde**.

***

## Nota de industria — EKS, AKS y GKE

**EKS (AWS), AKS (Azure) y GKE (Google) son este mismo Kubernetes, gestionado.** Los objetos que acabas de escribir — `Deployment`, `ReplicaSet`, `Service`, sondas, `rollout` — son idénticos allá: usas el mismo `kubectl` y los mismos manifiestos YAML, sin cambiar una línea.

Lo que cambia es **quién administra qué**. Aquí tú eres el control plane de un nodo (k3s dentro de tu estación); en un servicio gestionado, el proveedor mantiene el API server, los nodos, las actualizaciones y la reparación del plano de control, y tú pagas por esa administración y te concentras en los manifiestos. Sobre eso se apoyan las diferencias reales: integración con la identidad y la red de la nube, nodos administrados en pools, balancesadores gestionados y cuotas por uso.

> **El ciclo no cambia.** Lo que hiciste en los Labs 1 y 3 y aquí (`build → push → run` con orquestador) es el mismo pipeline que ejecutan los equipos en producción: la imagen vive en un registro, y el entorno — local, AWS, Azure o Google — solo la descarga y la corre.

***

## Troubleshooting rápido

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `kubectl` dice *connection to the server 127.0.0.1:6443 was refused* | El nodo aún está arrancando (primeros segundos de la sesión) | Espera 10–15 s y vuelve a ejecutar `kubectl get nodes`. Si insiste, avisa al docente |
| Los pods están en `ErrImagePull` / `ImagePullBackOff` | Kubernetes no encontró la imagen en tu registro (no hiciste el push o pusheaste otra etiqueta) | `kubectl describe pod <pod>` y revisa el *Failed to pull image*; repite el paso 2 |
| Los pods se quedan en `ContainerCreating` | Están montando la red o esperando la imagen; si es un error, el `describe` lo dice | `kubectl describe pod <pod>`; espera 20 s y vuelve a mirar |
| `docker push` falla con *connection refused* hacia `registry:5000` | El registro de la sesión aún no está listo o no resuelve en la estación | Comprueba con `getent hosts registry` y `curl -s http://registry:5000/v2/_catalog`; espera 10 s, reintenta y si sigue, avisa al docente |
| Los endpoints del Service están vacíos | El `selector` no coincide con los `labels` del pod, o los pods no están `Ready` (sondas) | `kubectl get pods --show-labels` y `kubectl get endpoints mi-app` |
| La pestaña **Mi aplicación** está en blanco | Todavía no existe el Service en el puerto 30080, o no tiene endpoints | Termina el paso 4 y comprueba con `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:30080/` |
| *Warning: v1 Endpoints is deprecated* | Aviso de versión de Kubernetes, no es un error | Continúa; la lista de IPs que te interesa está ahí |
| *Warning: resource deployments/mi-app was previously managed with 'kubectl apply'* al hacer rollback | El `undo` no actualiza la anotación de "último apply" | Inofensivo; si vuelves a aplicar el manifiesto, se re-resuelve solo |
| `revisar` dice que no existe el Deployment o el Service | Te saltaste un paso o ejecutaste los bloques fuera de orden | Los bloques se ejecutan en orden: 2 (push) → 3 (deploy) → 4 (service) → 5, 6, 7 |

***

## Cómo se evalúa (10% de la nota final — Actividad 2 de U2)

La plataforma tiene **cinco criterios con el mismo peso** y cada uno se comprueba **desde el servidor**, contra el estado real de tu sesión: tu registro, la API del clúster y el HTTP de tu Service. Nada de lo que imprimas en la terminal cuenta.

| Criterio | Peso | Lo que se comprueba |
|---|---|---|
| Imagen de mi-app en el registro de la sesión | 20 % | La imagen está publicada en `registry:5000` de tu sesión (etiquetas visibles en `/v2/mi-app/tags/list`) |
| Deployment mi-app con 3 réplicas disponibles | 20 % | Deployment `mi-app` con ≥3 réplicas disponibles cuya imagen viene del registro de la sesión (su etiqueta existe ahí) y con `readinessProbe` y `livenessProbe` |
| Service con endpoints que responde HTTP 200 | 20 % | Service `mi-app` con endpoints hacia pods listos y respuesta HTTP 200 con el contenido de la app en su NodePort, pedida desde fuera de la estación |
| Autorreparación por ReplicaSet | 20 % | El ReplicaSet creó un pod que nadie le pidió borrar: alguien borró un pod y la cuenta de eventos del ReplicaSet (creados − borrados) supera a los pods que existen |
| Rollout v1 a v2 (o rollback) con historial | 20 % | Historial de rollout con ≥2 revisiones y, además, v2 desplegada o un rollback hecho (revisión actual ≥3) |

Cada paso de esta guía enciende su criterio: sin trabajar, **0 de 5**; con la imagen publicada, 1; con el Deployment, 2; con el Service, 3; al borrar un pod, 4; y con el rollout + rollback, **5 de 5**. Si alguno se queda en rojo, `revisar` te dice con qué comando arreglarlo.

***

## Referencias

- Kubernetes — Pods: <https://kubernetes.io/docs/concepts/workloads/pods/>
- Kubernetes — Deployments (rolling update y rollback): <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
- Kubernetes — ReplicaSet: <https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/>
- Kubernetes — Services y endpoints: <https://kubernetes.io/docs/concepts/services-networking/service/>
- Kubernetes — Liveness y readiness probes: <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/>
- Kubernetes — `kubectl`: <https://kubernetes.io/docs/reference/kubectl/>
- k3s — clúster ligero de un nodo: <https://docs.k3s.io/>
- AWS EKS: <https://docs.aws.amazon.com/eks/>
- Microsoft AKS: <https://learn.microsoft.com/azure/aks/>
- Google Kubernetes Engine: <https://cloud.google.com/kubernetes-engine/docs>

***

## Checklist antes de entregar

- [ ] `kubectl get nodes` dice `Ready` y viste los pods del sistema.
- [ ] Tu `$LAB_REGISTRO/mi-app:1.0.0` está publicada y `tags/list` la lista.
- [ ] El Deployment está en `3/3` con readiness y liveness declaradas.
- [ ] El Service tiene 3 endpoints y la app responde `200` en la pestaña web.
- [ ] Borraste un pod y el ReplicaSet lo volvió a crear.
- [ ] Escalaste a 5 y volviste a 3 sin tocar los pods a mano.
- [ ] El rollout a v2 y el rollback aparecen en `rollout history`.
- [ ] Ejecutaste `revisar` y los cinco criterios están en verde.
