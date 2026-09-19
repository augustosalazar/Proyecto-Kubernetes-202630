"""Gestor de Jobs de Kubernetes para la practica 202630.

ESQUELETO: el andamiaje del cliente de Kubernetes ya esta puesto. Lo que falta
esta marcado con TODO y con `...` en los campos que debes completar. El foco de
la practica es Kubernetes, no Python: no tienes que inventar la estructura del
codigo, sino entender que significa cada campo del Job.

No se permite invocar `kubectl` desde este programa; el Job se crea con el
cliente oficial de Python (`pip install -r requirements.txt`).

Uso previsto una vez implementado:

    python gestor_jobs.py ejecutar --lenguaje python --tarea suma --complejidad baja
    python gestor_jobs.py estado --job <nombre-del-job>
    python gestor_jobs.py logs   --job <nombre-del-job>
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

from kubernetes import client, config

NAMESPACE = "estudiantes-202630"
RAIZ = Path(__file__).resolve().parent.parent
CATALOGO = RAIZ / "catalogo" / "tareas.json"

# Argumentos que recibe el contenedor segun la complejidad elegida.
# Al agregar una cuarta tarea al catalogo, agrega aqui sus tres niveles.
COMPLEJIDADES = {
    "suma": {
        "baja": ["4", "7"],
        "media": ["1234", "5678"],
        "alta": ["987654321", "123456789"],
    },
    "factorial": {
        "baja": ["5"],
        "media": ["12"],
        "alta": ["20"],
    },
    "tabla": {
        "baja": ["8"],
        "media": ["37"],
        "alta": ["1250"],
    },
}


def cargar_catalogo():
    """Devuelve el contenido de catalogo/tareas.json como diccionario."""
    with CATALOGO.open(encoding="utf-8") as archivo:
        return json.load(archivo)


# ---------------------------------------------------------------------------
# 1. Seleccion de lenguaje, tarea y complejidad
# ---------------------------------------------------------------------------

def seleccionar(catalogo, lenguaje, tarea, complejidad):
    """Valida la seleccion del usuario y devuelve (imagen, argumentos).

    `argumentos` es la lista que recibira el contenedor. Su primer elemento es
    el nombre de la tarea, por ejemplo ["suma", "4", "7"].
    """
    definicion = catalogo.get(lenguaje)
    if definicion is None:
        raise SystemExit(f"Lenguaje no disponible: {lenguaje}")

    # TODO: comprobar que `tarea` esta en definicion["tasks"]; si no, abortar
    # con un mensaje claro igual que arriba.

    niveles = COMPLEJIDADES.get(tarea, {})
    # TODO: comprobar que `complejidad` es una de las claves de `niveles`.

    imagen = ...  # TODO: la imagen que declara `definicion` en el catalogo.
    argumentos = ...  # TODO: [tarea] seguido de los argumentos del nivel elegido.

    return imagen, argumentos


def nombre_job(lenguaje, tarea, complejidad):
    """Construye un nombre de Job valido para Kubernetes.

    Reglas de Kubernetes: solo minusculas, digitos y guiones, maximo 63
    caracteres. El sufijo de tiempo permite repetir la misma tarea sin chocar
    con un Job anterior que siga en el namespace.
    """
    base = f"{lenguaje}-{tarea}-{complejidad}-{int(time.time())}".lower()
    return re.sub(r"[^a-z0-9-]", "-", base)[:63].strip("-")


# ---------------------------------------------------------------------------
# 2. Creacion del Job con el cliente Python de Kubernetes
# ---------------------------------------------------------------------------

def cliente_batch():
    """Carga la configuracion de kubeconfig y devuelve un BatchV1Api."""
    config.load_kube_config()
    return client.BatchV1Api()


def crear_job(nombre, imagen, argumentos):
    """Crea el Job en el namespace `NAMESPACE` y devuelve su nombre.

    El objeto que se arma abajo es el equivalente exacto de este YAML:

        apiVersion: batch/v1
        kind: Job
        metadata:
          name: <nombre>
          namespace: estudiantes-202630
        spec:
          backoffLimit: 0
          template:
            spec:
              restartPolicy: Never
              containers:
                - name: tarea
                  image: <imagen>
                  imagePullPolicy: Never
                  args: [<argumentos>]

    Completa los `...` comparando cada linea con ese YAML. Ojo: en el cliente
    de Python los campos van en snake_case (`image_pull_policy`,
    `restart_policy`, `backoff_limit`) y en el YAML en camelCase.
    """
    contenedor = client.V1Container(
        name="tarea",
        image=imagen,
        image_pull_policy=...,  # TODO
        args=...,               # TODO: los argumentos del contenedor.
    )

    plantilla = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(
            restart_policy=...,  # TODO
            containers=[contenedor],
        ),
    )

    especificacion = client.V1JobSpec(
        backoff_limit=...,  # TODO
        template=plantilla,
    )

    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=nombre, namespace=NAMESPACE),
        spec=especificacion,
    )

    # TODO: enviar el objeto al cluster con
    #   cliente_batch().create_namespaced_job(namespace=NAMESPACE, body=job)
    # y devolver `nombre`.
    raise NotImplementedError("crear_job")


# ---------------------------------------------------------------------------
# 3. Consulta de estado
# ---------------------------------------------------------------------------

def consultar_estado(nombre):
    """Devuelve una descripcion legible del estado del Job indicado."""
    job = cliente_batch().read_namespaced_job_status(name=nombre, namespace=NAMESPACE)

    # Estos contadores valen None mientras Kubernetes no los ha fijado.
    activos = job.status.active or 0
    correctos = job.status.succeeded or 0
    fallidos = job.status.failed or 0

    # TODO: devolver un texto que distinga los tres casos:
    #   - `activos` > 0    -> el Job sigue en ejecucion;
    #   - `correctos` > 0  -> el Job termino correctamente;
    #   - `fallidos` > 0   -> el Job fallo.
    raise NotImplementedError("consultar_estado")


# ---------------------------------------------------------------------------
# 4. Consulta de logs
# ---------------------------------------------------------------------------

def consultar_logs(nombre):
    """Devuelve la salida del contenedor ejecutado por el Job.

    Los logs pertenecen al Pod, no al Job. Kubernetes etiqueta cada Pod que
    crea un Job con `job-name=<nombre del Job>`, y por ahi se le encuentra.
    """
    config.load_kube_config()
    core = client.CoreV1Api()

    pods = core.list_namespaced_pod(
        namespace=NAMESPACE,
        label_selector=f"job-name={nombre}",
    )
    if not pods.items:
        raise SystemExit(f"El Job {nombre} todavia no tiene Pods.")

    pod = pods.items[0].metadata.name

    # TODO: devolver la salida del Pod con
    #   core.read_namespaced_pod_log(name=pod, namespace=NAMESPACE)
    raise NotImplementedError("consultar_logs")


# ---------------------------------------------------------------------------
# Linea de comandos
# ---------------------------------------------------------------------------

def construir_parser():
    parser = argparse.ArgumentParser(description="Gestor de Jobs de la practica 202630")
    subcomandos = parser.add_subparsers(dest="accion", required=True)

    ejecutar = subcomandos.add_parser("ejecutar", help="crea un Job nuevo")
    ejecutar.add_argument("--lenguaje", required=True)
    ejecutar.add_argument("--tarea", required=True)
    ejecutar.add_argument("--complejidad", required=True, choices=["baja", "media", "alta"])

    estado = subcomandos.add_parser("estado", help="consulta el estado de un Job")
    estado.add_argument("--job", required=True)

    logs = subcomandos.add_parser("logs", help="consulta los logs de un Job")
    logs.add_argument("--job", required=True)

    return parser


def main(argv=None):
    args = construir_parser().parse_args(argv)

    if args.accion == "ejecutar":
        catalogo = cargar_catalogo()
        imagen, argumentos = seleccionar(catalogo, args.lenguaje, args.tarea, args.complejidad)
        nombre = nombre_job(args.lenguaje, args.tarea, args.complejidad)
        crear_job(nombre, imagen, argumentos)
        print(f"Job creado: {nombre}")
        return 0

    if args.accion == "estado":
        print(consultar_estado(args.job))
        return 0

    if args.accion == "logs":
        print(consultar_logs(args.job))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
