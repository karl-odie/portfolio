if (test-path("package-lock.json")){
    ri package-lock.json
}
if (test-path("node_modules")){
    ri -Recurse node_modules
}
. docker compose -f docker-compose.local.yml up