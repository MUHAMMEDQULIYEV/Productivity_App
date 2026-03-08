# Productivity & Language Learning Platform

A self-hosted, fully local productivity platform with integrated language learning features. Built with FastAPI, Vanilla JS, PostgreSQL, and Docker.

---

## Features

- **Task Manager** — Create, prioritise, and track tasks with deadlines, categories, and status tracking
- **Notes** — Rich note-taking with tags and full-text search
- **Flashcards** — Spaced-repetition flashcard decks using the SM-2 algorithm
- **Language Learning** — Extract vocabulary from YouTube transcripts, file uploads, or pasted text; track words learned
- **Analytics Dashboard** — Visualise productivity trends and language learning progress with Chart.js
- **Email Notifications** — Configurable SMTP notifications for task reminders, daily summaries, and weekly reports
- **Dark Mode** — Persisted dark/light theme toggle

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Browser (port 3000)                  │
│  Vanilla JS SPA  ←→  Nginx (proxy /api/* → backend)     │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP
          ┌──────────────▼──────────────┐
          │   FastAPI Backend (port 5000) │
          │  ┌─────────────────────────┐ │
          │  │ Routers: tasks, notes,  │ │
          │  │ flashcards, language,   │ │
          │  │ analytics, notifications│ │
          │  └────────────┬────────────┘ │
          │               │              │
          │  ┌────────────▼────────────┐ │
          │  │  Services: SM-2, NLP,   │ │
          │  │  YouTube, Email, Sched  │ │
          │  └────────────┬────────────┘ │
          └───────────────┼──────────────┘
                ┌─────────┴──────────┐
                │                    │
        ┌───────▼───────┐   ┌────────▼───────┐
        │  PostgreSQL    │   │     Redis       │
        │  (port 5432)   │   │  (port 6379)    │
        └───────────────┘   └────────────────┘
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- (Optional) [ngrok](https://ngrok.com/) for public tunnelling

---

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/Productivity_App.git
   cd Productivity_App
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and fill in your SMTP credentials (optional for full email support)
   ```

3. **Build and start services**
   ```bash
   make build
   make up
   ```

4. **Run database migrations**
   ```bash
   make migrate
   ```

5. **Open the app**
   Visit [http://localhost:3000](http://localhost:3000) in your browser.

---

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make up` | Start all services in detached mode |
| `make down` | Stop and remove containers |
| `make build` | Build (or rebuild) Docker images |
| `make logs` | Tail logs from all services |
| `make migrate` | Run Alembic database migrations |
| `make shell-backend` | Open a shell in the backend container |
| `make shell-db` | Open a psql session in the database container |

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks` | List tasks (filters: status, category, priority) |
| GET | `/api/tasks/upcoming` | Tasks due in next 24h |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| POST | `/api/notes` | Create note |
| GET | `/api/notes` | List notes |
| GET | `/api/notes/search?q=` | Search notes |
| POST | `/api/decks` | Create flashcard deck |
| GET | `/api/decks` | List decks |
| POST | `/api/cards` | Add card to deck |
| GET | `/api/cards/review/{deck_id}` | Get due cards |
| PUT | `/api/cards/{id}/review` | Submit review (SM-2) |
| POST | `/api/language/extract-youtube` | Extract vocab from YouTube |
| POST | `/api/language/extract-upload` | Extract vocab from .srt/.txt |
| POST | `/api/language/extract-text` | Extract vocab from text |
| GET | `/api/analytics/dashboard` | Dashboard summary |
| GET | `/api/analytics/productivity` | Productivity trends |
| GET | `/api/analytics/recommendations` | Study recommendations |
| POST | `/api/notifications/settings` | Save SMTP settings |
| POST | `/api/notifications/test-email` | Send test email |

Full interactive API docs available at [http://localhost:5000/docs](http://localhost:5000/docs) (FastAPI Swagger UI).

---

## Development

Hot-reload is enabled by default via `docker-compose.override.yml`:

- **Backend** — Uvicorn reloads on Python file changes (volume-mounted `./backend`)
- **Frontend** — Nginx serves from volume-mounted `./frontend/public` so JS/HTML/CSS changes are reflected immediately on refresh

> **Note:** This project uses Docker Compose v2 (`docker compose` plugin). All `make` commands use the `docker compose` syntax. If you have an older Docker installation that only provides the standalone `docker-compose` (v1), please upgrade to a recent version of Docker Desktop or Docker Engine.

---

## ngrok Tunnelling (optional)

To expose the app publicly for testing:

```bash
ngrok http 3000
```

Copy the HTTPS URL from ngrok and add it to `ALLOWED_ORIGINS` in your `.env` file, then restart the backend:

```bash
make down && make up
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@db:5432/productivity` | Async PostgreSQL DSN (use `db` for Docker, `localhost` for host) |
| `REDIS_URL` | `redis://redis:6379/0` | Redis URL (use `redis` for Docker, `localhost` for host) |
| `SECRET_KEY` | `change-me-in-production` | JWT signing key |
| `SMTP_HOST` | `smtp.gmail.com` | SMTP server host |
| `SMTP_PORT` | `587` | SMTP server port |
| `SMTP_USER` | *(empty)* | SMTP login |
| `SMTP_PASSWORD` | *(empty)* | SMTP password / app password |
| `SMTP_FROM` | *(empty)* | From address in emails |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | CORS allowed origins |

---

## License

MIT
