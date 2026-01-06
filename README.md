# 🚀 Portal BT

- [Getting Started](#️-getting-started)
- [Docker Management](#docker-container-management)
- [Schema Naming](#guidelines-for-schema-naming)
- [Migrations](#migrations)

## 🛠️ Getting Started

Follow these steps to get the project up and running in your local environment using Docker.

### 📦 Clone the repository

```bash
git clone https://github.com/AndriwRC/portal-bt.git
cd portal-bt
```

### ⚙️ Set environment variables

Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

Then, edit the `.env` file and set your environment variables accordingly.

### 🐳 Build the Docker image

To build the image with Docker Compose:

```bash
docker compose up --build -d
```

### Run Database Migrations

To run database migrations we are using [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) package:

```bash
docker compose exec api alembic upgrade head
```

### Run Database Seeder

This will insert some data that is required to manage the api properly (e.g., admin roles and permissions):

```bash
docker compose exec api python -m app.cli seed
```

# Docker Container management

### ▶️ Run the container

After building, you can run the container with:

```bash
docker compose up -d
```

### 🛑 Stop the container

To stop the running containers:

```bash
docker compose down
```

### Open an interactive shell inside the container

Use this when you want to run multiple commands (e.g. migrations, seeders):

```bash
docker compose exec api bash
```
To exit just run `exit`.

### Run a single command inside the container

Use this when you want to execute one command without opening a shell:

```bash
docker compose exec api <command_to_run>
```

# Guidelines for Schema Naming

Use these suffixes consistently:

### **Suffixes**

| Suffix         | Meaning                |
| -------------- | ---------------------- |
| `Base`         | Shared fields          |
| `Create`       | Required input payload |
| `Update`       | Partial input payload  |
| `Read`         | Response model         |
| `ReadMin`      | Lightweight response   |
| `ReadDetailed` | Heavy response         |
| `ReadWithX`    | Nested relationships   |

# Migrations

### Create a migration

To create a migration use `alembic revision -m "<migration name>"`:

```bash
alembic revision -m "init db"
```

This creates a new file inside `app/database/migrations/versions/` folder. Then place your DB changes in this file.

### Autogenerate a migration

If `--autogenerate` flag is used, alembic will detect some changes and place them in the file created:

```bash
alembic revision --autogenerate -m "init db"
```

Alembic can't detect all the changes performed to the database, so is important to check and fix the file created before running the migration.

### Run a migration

To run a specific migration you can use the revision id that you can find inside the file created:

```bash
alembic upgrade <revision_id>
```

### Run the latest migration

To apply all the migrations and bring the database to the latest version:

```bash
alembic upgrade head
```

This run all pending migrations in order.

### Reverting Migrations

To revert the last migration:

```bash
alembic downgrade -1
```

Also you can downgrade to a specific version using the `revision_id` and revert all the migrations using `base`.
