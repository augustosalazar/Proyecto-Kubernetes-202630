# Proyecto Kubernetes 202630 — Jobs parametrizados desde línea de comandos

Proyecto **grupal**: se trabaja en los grupos que se han venido usando durante el curso y
se entrega antes de la clase de la semana 12 (ver [Entrega](#entrega)).

Ya han trabajado con manifiestos `Job` de Kubernetes. En este proyecto el grupo usará esa
misma idea desde una herramienta de línea de comandos escrita en Python: en vez de editar
un YAML para cada ejecución, el usuario elige el lenguaje, la tarea y la complejidad, y el
programa crea el `Job` usando el cliente oficial de Kubernetes.

Kubernetes crea entonces un Pod y ejecuta el contenedor elegido con los argumentos
suministrados. El recorrido completo que el grupo debe entender —y saber defender— es:

```text
gestor_jobs.py -> Job de Kubernetes -> Pod -> contenedor con argumentos -> logs
```

No se incluye interfaz web, múltiples nodos, RBAC propio ni selección manual de nodos.
Esas capas quedan para la versión completa.

## Qué se entrega y qué construye el grupo

Se entrega como infraestructura, ya funcional:

- `imagenes/`: tres imágenes de ejemplo (Python, Java y C) con una tarea cada una.
- `catalogo/tareas.json`: catálogo modificable de lenguajes, imágenes y tareas admitidas.
- `k8s/00-namespace.yaml`: namespace dedicado para los Jobs.
- `scripts/preparar-imagenes.ps1`: construye las imágenes y las carga en Minikube.

Construye el grupo, sobre el esqueleto de `entrega/`:

- `entrega/gestor_jobs.py`, con cuatro capacidades:
  1. selección de lenguaje, tarea y complejidad;
  2. creación del `Job` mediante el cliente Python de Kubernetes;
  3. consulta del estado del `Job`;
  4. consulta de los logs del `Job`.

- Una cuarta tarea añadida al catálogo, en el lenguaje que el grupo prefiera. Implica
  ajustar el programa del contenedor que corresponda, reconstruir y cargar la imagen,
  añadir la entrada en `catalogo/tareas.json` y sus niveles de complejidad.

El esqueleto ya trae la estructura del programa y el andamiaje del cliente de Kubernetes
armado: los subcomandos, la carga del catálogo, el objeto `Job` con sus clases anidadas y
la búsqueda del Pod por etiqueta. Lo pendiente está marcado con `TODO` y con `...` en los
campos a completar, de modo que el trabajo sea entender el `Job` y no pelear con Python.

No está permitido resolver el proyecto invocando `kubectl` desde Python: el `Job` debe
crearse con el cliente `kubernetes`.

Como la entrega se defiende en grupo, todos los integrantes deben poder explicar el
código y el recorrido completo, sin importar quién escribió cada parte.

## Preparación

Ejecuten los siguientes comandos desde la carpeta raíz del proyecto:

```powershell
minikube start
kubectl apply -f .\k8s\00-namespace.yaml
.\scripts\preparar-imagenes.ps1
```

Instalen luego las dependencias de Python:

```powershell
pip install -r .\entrega\requirements.txt
```

Los nombres de imagen son deliberadamente locales (`kubernates-202630-*`). Se cargan en
Minikube; no se publica ninguna imagen durante el proyecto.

## Ejecución

Una vez implementado el gestor, prueben las tres tareas incluidas, variando la
complejidad:

```powershell
python .\entrega\gestor_jobs.py ejecutar --lenguaje python --tarea suma --complejidad baja
python .\entrega\gestor_jobs.py ejecutar --lenguaje java --tarea factorial --complejidad media
python .\entrega\gestor_jobs.py ejecutar --lenguaje c --tarea tabla --complejidad alta
```

Consulten después el estado y los logs con su propio programa:

```powershell
python .\entrega\gestor_jobs.py estado --job <nombre-del-job>
python .\entrega\gestor_jobs.py logs --job <nombre-del-job>
```

Pueden contrastar sus resultados con `kubectl get jobs,pods -n estudiantes-202630` y
`kubectl logs -n estudiantes-202630 job/<nombre-del-job>`.

## Entrega

El proyecto es grupal y se trabaja en los grupos que se han venido usando durante el
curso. La entrega vence **antes de la clase de la semana 12**.

1. Link al repositorio público entregado por la actividad del catálogo, antes de la clase
   de la semana 12.
2. En el README del repositorio se debe explicar la implementación.
3. En el README se debe agregar un link a un video de YouTube con el demo del proyecto.
4. El grupo completo debe estar disponible para defender la entrega.
