[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot

@('python', 'java', 'c') | ForEach-Object {
    $lenguaje = $_
    $tag = "kubernates-202630-$lenguaje`:1.0"
    docker build -t $tag (Join-Path $raiz "imagenes/$lenguaje")
    if ($LASTEXITCODE -ne 0) { throw "No se pudo construir $tag" }
    minikube image load $tag
    if ($LASTEXITCODE -ne 0) { throw "No se pudo cargar $tag en Minikube" }
}
