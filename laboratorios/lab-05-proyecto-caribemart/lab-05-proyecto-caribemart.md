# Laboratorio 5 — Proyecto práctico CaribeMart

**Ingeniería de Sistemas · Integración de Soluciones · Universidad de la Costa (CUC)**
Docente: Ing. Rodolfo Cañas Cervantes · 2026-2 · **Proyecto de Corte 2 — 20 % · Individual**

> Versión HTML con el diseño de los demás labs: `guia/index.html`.

## Escenario

CaribeMart deja de ser un monolito: pasa a **3 servicios contenerizados** (catálogo,
pedidos y frontend) desplegados en tu propio clúster Kubernetes, entregados por un
**pipeline**. La lógica de negocio ya está hecha (es trivial): se califica
**contenerización, orquestación y automatización**, no programación.

Los cinco entregables son exactamente lo que `revisar` comprueba:

1. **Imágenes publicadas** — 3 imágenes en tu registro con etiqueta **inmutable** (nunca `latest`).
2. **Despliegue en Kubernetes** — 3 Deployments con **≥2 réplicas**, sondas y límites.
3. **Servicios comunicados** — una petición al frontend recorre pedidos y catálogo.
4. **Autorreparación y rollout** — un pod borrado vuelve; una actualización no corta el servicio.
5. **Pipeline** — `ci.sh` (build → test → push → deploy) que se detiene si una prueba falla.

## Presupuesto (120 minutos)

| Parte | Tiempo |
|---|---|
| 1 — Reconoce CaribeMart y tu clúster | 10 min |
| 2 — Conteneriza los 3 servicios y publícalos | 20 min |
| 3 — Deployments, Services, sondas y límites | 30 min |
| 4 — Comunicación de punta a punta | 15 min |
| 5 — Autorreparación y rollout sin caída | 20 min |
| 6 — Pipeline `ci.sh` y Actions | 20 min |
| 7 — Entregable (`revisar`) | 5 min |

---

## Paso 1 — Reconoce CaribeMart y tu clúster

```sh
mi-espacio
kubectl get nodes
kubectl get pods -A
cd /workspace/proyecto && find . -maxdepth 2 -type f | sort
```

Qué deberías ver: `/workspace/proyecto`, el nodo `Ready` y los pods de `kube-system`
en `Running`. Los tres servicios ya están en el proyecto:

| Servicio | Endpoints | Necesita |
|---|---|---|
| catálogo | `/salud`, `/productos` | nada |
| pedidos | `/salud`, `/pedidos` (GET/POST) | `CATALOGO_URL` |
| frontend | `/salud`, `/api/estado`, `/api/pedidos` | `CATALOGO_URL`, `PEDIDOS_URL` |

> No hay manifiestos en `k8s/`: los escribes tú (paso 3).

## Paso 2 — Conteneriza los 3 servicios y publícalos

```sh
cd /workspace/proyecto
echo $LAB_REGISTRO                 # registry:5000
for s in catalogo pedidos frontend; do
  docker build -t "$LAB_REGISTRO/$s:1.0.0" "$s"
  docker push  "$LAB_REGISTRO/$s:1.0.0"
done
curl -s http://$LAB_REGISTRO/v2/_catalog
```

Debe ver los 3 repositorios publicados. Publica también una **v2** del frontend
(la necesitas en el paso 5):

```sh
docker build --build-arg VERSION=2.0.0 -t "$LAB_REGISTRO/frontend:2.0.0" frontend
docker push "$LAB_REGISTRO/frontend:2.0.0"
```

## Paso 3 — Deployments, Services, sondas y límites

Escribe los manifiestos en `/workspace/proyecto/k8s/`. Cada Deployment necesita:

- `spec.replicas` **≥2** y con las réplicas **disponibles**;
- la imagen desde tu registro: `registry:5000/<servicio>:1.0.0`;
- `readinessProbe` y `livenessProbe` hacia `/salud` (puerto 3000);
- `resources.requests` y `resources.limits`;
- en pedidos y frontend, `CATALOGO_URL`/`PEDIDOS_URL` con los **nombres de Service**.

Esqueleto (complétalo tú):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: catalogo }
spec:
  replicas: 2
  selector: { matchLabels: { app: catalogo } }
  template:
    metadata: { labels: { app: catalogo } }
    spec:
      containers:
        - name: catalogo
          image: registry:5000/catalogo:1.0.0
          ports: [{ containerPort: 3000 }]
          # readinessProbe, livenessProbe y resources: te toca
```

> **¿No recuerdas la sintaxis de las sondas o de los límites?** No necesitas Internet: la estación incluye la documentación de Kubernetes. Consúltala con `kubectl explain`, por ejemplo:
> ```sh
> kubectl explain deployment.spec.template.spec.containers.readinessProbe
> kubectl explain deployment.spec.template.spec.containers.livenessProbe
> kubectl explain deployment.spec.template.spec.containers.resources.limits
> ```
> Agrega `--recursive` para ver todos los campos. Las sondas apuntan a `/salud` en el puerto `3000`.

Aplica y espera el rollout:

```sh
kubectl apply -f /workspace/proyecto/k8s/
kubectl get deploy,rs,pods -o wide
kubectl rollout status deploy/catalogo --timeout=120s
```

El Service del **frontend** debe ser `NodePort` en el 30080; los otros pueden ser
`ClusterIP`:

```yaml
apiVersion: v1
kind: Service
metadata: { name: frontend }
spec:
  type: NodePort
  selector: { app: frontend }
  ports: [{ port: 80, targetPort: 3000, nodePort: 30080 }]
```

## Paso 4 — Comunicación de punta a punta

```sh
curl -s http://127.0.0.1:30080/api/estado
curl -s -X POST http://127.0.0.1:30080/api/pedidos \
  -H 'Content-Type: application/json' \
  -d '{"productoId":1,"cantidad":2,"referencia":"mi-prueba"}'
curl -s http://127.0.0.1:30080/api/estado
```

Debe ver `catalogo.ok=true` y `pedidos.ok=true`, la compra con el **nombre del producto**
y el contador de pedidos **+1**. El servidor lanza su propia compra (con una referencia
aleatoria), así que una página estática no engaña a `revisar`.

## Paso 5 — Autorreparación y rollout sin caída

Autorreparación (borra un pod y observa):

```sh
P=$(kubectl get pods -l app=frontend --no-headers | awk '$3=="Running"{print $1; exit}')
kubectl delete pod "$P"
sleep 8
kubectl get pods -l app=frontend
```

Rollout sin cortes (necesitas la v2 del paso 2 y ≥2 réplicas):

```sh
kubectl set image deploy/frontend frontend="$LAB_REGISTRO/frontend:2.0.0"
while kubectl rollout status deploy/frontend --timeout=1s 2>/dev/null; do
  curl -s -o /dev/null -w '%{http_code} ' http://127.0.0.1:30080/salud
done
```

Debe ver una fila de `200` sin cortes. El servidor repite estas dos pruebas él mismo (y
revierte la imagen al terminar).

## Paso 6 — Pipeline `ci.sh` y Actions

Contrato de `ci.sh`:

- anuncia `ETAPA build`, `ETAPA test`, `ETAPA push`, `ETAPA deploy`;
- ejecuta **todas** las pruebas de `pruebas/*.sh` y **aborta** si una falla;
- en *deploy* aplica `k8s/` y espera el rollout.

Escribe tu pipeline en `/workspace/proyecto/ci.sh`:

```sh
cd /workspace/proyecto
cat <<'EOF' > ci.sh
#!/bin/bash
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")" && pwd)"
REG="${LAB_REGISTRO:-registry:5000}"
export TAG="${TAG:-1.0.0}"
SERVICIOS="catalogo pedidos frontend"

echo "ETAPA build (tag $TAG)"
for s in $SERVICIOS; do
  echo "  - $s"
  docker build --build-arg "VERSION=$TAG" -t "$REG/$s:$TAG" "$RAIZ/$s"
done

echo "ETAPA test"
fallo=0
for t in "$RAIZ"/pruebas/*.sh; do
  [ -e "$t" ] || continue
  echo "  - $(basename "$t")"
  if ! sh "$t"; then
    echo "PRUEBA FALLIDA: $(basename "$t")"
    fallo=1
  fi
done
if [ "$fallo" -ne 0 ]; then
  echo "PIPELINE ABORTADO: hay pruebas en rojo; no se publica ni se despliega."
  exit 1
fi

echo "ETAPA push"
for s in $SERVICIOS; do
  docker push "$REG/$s:$TAG"
done

echo "ETAPA deploy"
if [ ! -d "$RAIZ/k8s" ]; then
  echo "FALTA el directorio k8s/ con tus manifiestos (Deployments y Services)."
  exit 1
fi
kubectl apply -f "$RAIZ/k8s/"
for s in $SERVICIOS; do
  kubectl rollout status "deploy/$s" --timeout=180s
done

echo "PIPELINE_OK"
EOF
chmod +x ci.sh
./ci.sh
```

Al final debe imprimir `PIPELINE_OK`. El workflow equivalente vive en
`.github/workflows/ci.yml` (el servidor comprueba que existe y es YAML válido).

## Paso 7 — Entregable

```sh
revisar
```

Pide al servidor que evalúe el proyecto desde fuera. Como el servidor ejecuta pruebas
activas (borra un pod, hace el rollout, corre y rompe el pipeline), **tarda más** que en
el Lab 4. Objetivo: **5 de 5 criterios automáticos en verde**; el docente completa la
defensa.

## Cómo se evalúa (rúbrica — suma 5,0)

| Criterio | Peso | Tipo | Lo que se comprueba |
|---|---|---|---|
| Imágenes publicadas | 0,8 | auto | 3 imágenes en `registry:5000` con etiqueta inmutable |
| Despliegue en Kubernetes | 0,8 | auto | 3 Deployments con ≥2 réplicas, sondas y límites |
| Servicios comunicados | 0,8 | auto | compra por el NodePort que pasa por pedidos y catálogo |
| Autorreparación y rollout | 0,8 | auto | pod repuesto y actualización sin cortes |
| Pipeline | 0,8 | auto | `ci.sh` se detiene ante una prueba rota; workflow válido |
| Defensa y evidencia | 1,0 | docente | defiendes tus decisiones en una conversación corta con el docente (ver abajo) |

Mientras el docente no complete su criterio, la nota aparece como **pendiente de rúbrica
docente** (la parte automática se muestra como parcial).

**La defensa (1,0), cómo funciona.** Es una conversación **individual de unos 5 minutos** con el docente, después de entregar. **La fecha y el horario los anuncia el docente** en clase o por Teams; no necesitas preparar nada aparte. Como evidencia sirve el resultado de `revisar` que queda registrado en tu ficha de la plataforma y tu propio conocimiento del trabajo: te hará preguntas sobre **tres decisiones tuyas** (por qué la etiqueta inmutable, para qué sirven la sonda de lectura y la de vida, qué hace la estrategia de actualización, o por qué tu `ci.sh` se detiene ante una prueba rota). Niveles: 1,0 defiende con soltura cada decisión; 0,6 explica con lagunas; 0,2 describe sin justificar; 0,0 no puede explicarlo. Tu estación se cierra al terminar y lo que escribiste dentro no se conserva: si quieres mostrar tus manifiestos o salidas, **toma capturas de pantalla o copia el texto mientras trabajas**.

## Checklist antes de entregar

- [ ] Las 3 imágenes están en `registry:5000` con etiqueta versionada (no `latest`).
- [ ] Los 3 Deployments están en `2/2` con sondas y `resources`.
- [ ] El Service del frontend es `NodePort 30080` y la pestaña **CaribeMart** responde.
- [ ] Una compra crea un pedido y el contador sube.
- [ ] Borraste un pod y volvió.
- [ ] Publicaste una v2 del frontend y el rollout no cortó el servicio.
- [ ] `./ci.sh` termina en `PIPELINE_OK` y se detiene si una prueba falla.
- [ ] Existe `.github/workflows/ci.yml` válido.
- [ ] Ejecutaste `revisar` con 5/5.
