. docker compose -f .\docker-compose.local.yml run --rm django python manage.py spectacular --file portfolio/api/schema.yml
. docker compose -f .\docker-compose.local.yml run --rm node npm run sync-api
