Param(
    [string]$command = ""
)

$DOCKER_COMPOSE = "docker compose -f .\.docker\docker-compose.yml"

function Copy-Env {
    if (!(Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Host "Archivo .env creado."
    }
}

function Create-Symlink {
    $target = ".env"
    $link = ".docker\.env"

    if (!(Test-Path $link)) {
        New-Item -ItemType SymbolicLink -Path $link -Target "..\.env" | Out-Null
        Write-Host "Symlink creado en .docker\.env"
    }
}

function Print-Urls {
    Write-Host "## Acceso a la Aplicación:   http://localhost:8081/"
    Write-Host "## Acceso a PhpMyAdmin:      http://localhost:8082/"
}

function Up      { iex "$DOCKER_COMPOSE up -d" }
function Down    { iex "$DOCKER_COMPOSE down" }
function Restart { iex "$DOCKER_COMPOSE restart" }
function Ps      { iex "$DOCKER_COMPOSE ps" }
function Logs    { iex "$DOCKER_COMPOSE logs" }
function Build   { iex "$DOCKER_COMPOSE build" }
function StopC   { iex "$DOCKER_COMPOSE stop" }
function Shell   { iex "$DOCKER_COMPOSE exec --user jonathanA server_docker bash" }
function InitChatbot { iex "$DOCKER_COMPOSE exec --user jonathanA server_docker python init_chatbot.py" }

function Clean-Docker {
    docker rmi -f $(docker images -q) 2>$null
    docker volume rm $(docker volume ls -q) 2>$null
    docker network prune -f
}

switch ($command) {

    "init-app" {
        Copy-Env
        Create-Symlink
        Up
        Print-Urls
    }

    "copy-env"       { Copy-Env }
    "create-symlink" { Create-Symlink }
    "print-urls"     { Print-Urls }

    "up"       { Up }
    "down"     { Down }
    "restart"  { Restart }
    "ps"       { Ps }
    "logs"     { Logs }
    "build"    { Build }
    "stop"     { StopC }
    "shell"    { Shell }
    "init-chatbot" { InitChatbot }

    "clean-docker" { Clean-Docker }

    default {
        Write-Host "Comandos disponibles:"
        Write-Host "  init-app"
        Write-Host "  up, down, restart, ps, logs, build, stop"
        Write-Host "  shell, init-chatbot"
        Write-Host "  copy-env, create-symlink, print-urls"
        Write-Host "  clean-docker"
    }
}
