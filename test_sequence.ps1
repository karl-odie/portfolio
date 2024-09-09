# Run test sequence as it would occur in CI.
. docker compose -f docker-compose.local.yml build django
. docker compose -f docker-compose.docs.yml build docs
. docker compose -f docker-compose.docs.yml build node
# Prepare.
. docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
. docker compose -f docker-compose.local.yml run --rm django python manage.py spectacular --file portfolio/api/schema.yml
. docker compose -f docker-compose.local.yml run node npm run 'sync-api'
# Run tests.
. docker compose -f docker-compose.local.yml run django pytest
. docker compose -f docker-compose.local.yml run node npm test
. docker compose -f docker-compose.local.yml -f docker-compose.cypress.yml run cypress
. docker compose -f docker-compose.local.yml down
