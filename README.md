#  Botanica

A Django project combining two connected apps:
- **The Journal** — a narrative blog for botanical essays and field notes
- **The Grimoire** — a structured living archive of plant knowledge

---

## Deploying on Railway

This project is configured for Railway with:
- `runtime.txt` to pin Python version
- `requirements.txt` for dependencies
- `railway.toml` build/release/start commands
- `Procfile` for the web process

Required environment variables:
- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- `DJANGO_ALLOWED_HOSTS` (optional; defaults to `*`)
- `DJANGO_DEBUG` (optional; defaults to `False` in Railway)

The app also supports local development fallback to `db.sqlite3` when `DATABASE_URL` is not defined.
