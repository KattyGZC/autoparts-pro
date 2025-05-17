# Configuration and usage

## Prerequisites

- Python 3.11
- Docker
- Docker Compose

## Installation

1. Clone the repository
2. Located at the root of the project
3. Run `docker compose up --build`
4. Wait for the containers to start
5. The application will be available at `http://localhost:5173`
6. The API will be available at `http://localhost:8000`
7. The database will be available at `http://localhost:5432`
8. The database name is `autoparts`

## Migrations

1. Run `alembic upgrade head`

## Usage

### API

