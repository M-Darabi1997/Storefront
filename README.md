# Storefront API

A Django REST Framework backend for an online store. It includes products and collections, product images and reviews, shopping carts, customers, orders, and JWT based user accounts. The project also includes Celery tasks, Redis caching, an admin site, and development tools for tests and load testing.

## Stack

- Django and Django REST Framework
- Djoser and Simple JWT for account and token endpoints
- MySQL in the included Docker Compose stack, with Redis for Celery and caching
- Celery worker and beat, Flower, and smtp4dev for local email inspection
- pytest and Locust for testing

## Run with Docker Compose

Create a `.env` file in the repository root. The development settings use INI sections, not ordinary shell environment variable syntax:

```ini
[general]
SECRET_KEY=replace-with-a-long-random-secret

[database]
DB_ENGINE=django.db.backends.mysql
DB_NAME=storefront3
DB_USER=root
DB_PASSWORD=MyPassword
DB_HOST=mysql
DB_PORT=3306
```

These database values match the MySQL service in `docker-compose.yml`. Change the sample password in both places for any environment beyond local development. The settings default to PostgreSQL when `DB_ENGINE` is omitted, so keep that line when using the included Compose stack.

```bash
docker compose up --build
```

The web container waits for MySQL, applies migrations, and starts Django at `http://localhost:8000/`. The API lives under `/store/`; Django admin is at `/admin/`. Optional services include smtp4dev at `http://localhost:5000/` and Flower at `http://localhost:5555/`.

To create an admin account or load the sample product and collection data:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_db
```

The `seed_db` command executes `store/management/commands/seed.sql`; use it on a disposable development database.

**Python version note:** `Pipfile` requests Python 3.11 while `Dockerfile` uses Python 3.9. If the image build fails on the Python version check, align those two files before using Compose.

## API routes

| Route | Purpose |
| --- | --- |
| `/store/products/` | Browse, search, filter, and order products |
| `/store/collections/` | Browse collections |
| `/store/products/{id}/reviews/` | Product reviews |
| `/store/products/{id}/images/` | Product images |
| `/store/carts/` | Create a cart |
| `/store/carts/{id}/items/` | Manage items in a cart |
| `/store/customers/me/` | Read or update the signed-in customer's profile |
| `/store/orders/` | Create and list orders |
| `POST /auth/users/` | Register a user |
| `POST /auth/jwt/create/` | Obtain JWT access and refresh tokens |

Product and collection writes require admin access; order endpoints require authentication. Send an access token as `Authorization: JWT <access_token>`. Product listing supports the filters defined in `store/filters.py`, text search on title and description, ordering by price or update time, and pagination.

## Development and tests

The project uses `storefront.settings.dev` by default. Its `.env` file is ignored by Git. To run tests inside the Compose environment:

```bash
docker compose run --rm tests pytest
```

The Compose `tests` service normally starts `ptw` in watch mode; the command above runs pytest once. A Locust scenario for browsing products is in `locustfiles/browse_products.py`.
