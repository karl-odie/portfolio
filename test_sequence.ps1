# Run test sequence as it would occur in CI.
. docker compose -f docker-compose.local.yml build django
. docker compose -f docker-compose.docs.yml build docs
. docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
. docker compose -f docker-compose.local.yml run django pytest
. docker compose -f docker-compose.local.yml down
