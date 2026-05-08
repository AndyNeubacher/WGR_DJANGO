# WGR — Getting Started

Greenfield Django backend for the water-gauge reading webapp described in [CLAUDE.md](CLAUDE.md). This howto covers what was scaffolded for **Task 1 (Backend)** and how to bring it up on a fresh machine.

## What was created

Django 5.2 project with three apps:

- [core/](core/) — shared domain models (Customer, Site, SiteGroup, Gauge, Reading, Photo) and role profiles (TechnicianProfile, ManagerProfile, AdminProfile). Also wires every model into the Django admin.
- [technician/](technician/) — placeholder views + URLs for the mobile technician UI (Task 2).
- [manager/](manager/) — placeholder views + URLs for the desktop manager UI (Task 3).

> **Naming note.** CLAUDE.md asked for an `admin` app. That name collides with `django.contrib.admin`, so the shared/admin-side code lives in `core` and the admin role itself is modelled as `core.AdminProfile`. The Django admin site at `/admin/` already provides the CRUD surface CLAUDE.md asks for.

### Data model

All in [core/models.py](core/models.py):

| Model | Purpose |
| --- | --- |
| `Customer` | Utility customer (name, address, contact, member-since). |
| `SiteGroup` | Group of sites — a customer's sites can be grouped freely. |
| `Site` | A physical location belonging to a customer; optional group; lat/lon. |
| `Gauge` | Mechanical water meter with unique `serial_number`, JSON `additional_data`, lives on a `Site`. |
| `Photo` | Image of a gauge (Pillow `ImageField`) plus uploader and timestamp. |
| `Reading` | OCR + verified serial / consumed-volume pair, optional 1:1 link to a `Photo`, manager note. |
| `TechnicianProfile` | 1:1 with `auth.User`. Has `assigned_sites` and `assigned_gauges` M2M for Task 4. |
| `ManagerProfile` | 1:1 with `auth.User`. Department + phone. |
| `AdminProfile` | 1:1 with `auth.User`. Internal notes. |

Users (and passwords) are stored in Django's built-in `auth.User`, so passwords are hashed with PBKDF2 by default — that satisfies the "credentials encrypted in DB" requirement in Task 4 and avoids a custom user model now (which is hard to introduce later).

### Project settings highlights

[wgr/settings.py](wgr/settings.py):

- `LANGUAGE_CODE = "de-at"`, `TIME_ZONE = "Europe/Vienna"` (UI is German-only).
- `MEDIA_URL` / `MEDIA_ROOT` configured for uploaded photos (`media/gauges/<YYYY>/<MM>/`).
- `LOGIN_URL = "login"`, `LOGIN_REDIRECT_URL = "/"`, `LOGOUT_REDIRECT_URL = "login"`.

## Prerequisites

- Python 3.12 (project was scaffolded against 3.12.10).
- Git (optional, for version control).
- Windows / macOS / Linux. Commands below are PowerShell; bash equivalents are noted.

## First-time setup

From the project root (`c:\workspace\WGR_DJANGO`):

```powershell
# 1. create + activate the virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# bash: source .venv/bin/activate

# 2. install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. apply migrations (already generated, in core/migrations/0001_initial.py)
python manage.py migrate

# 4. create the first superuser (becomes your initial admin)
python manage.py createsuperuser
```

## Running the dev server

```powershell
python manage.py runserver
```

Then open:

- http://127.0.0.1:8000/admin/ — Django admin (CRUD for Customer / Site / Gauge / Reading / Photo / role profiles)
- http://127.0.0.1:8000/login/ — login page (Django auth)
- http://127.0.0.1:8000/technician/ — technician dashboard placeholder (login required)
- http://127.0.0.1:8000/manager/ — manager dashboard placeholder (login required)

The root `/` redirects to `/admin/` for now.

## Common commands

```powershell
python manage.py check                   # static project sanity check
python manage.py makemigrations          # after editing models
python manage.py migrate                 # apply pending migrations
python manage.py shell                   # interactive ORM shell
python manage.py collectstatic           # only relevant for production
python manage.py createsuperuser         # add another admin user
```

## Creating users for the three roles

Until the manager UI for user management exists (Task 4), add accounts via Django admin:

1. Log in to `/admin/` as the superuser.
2. **Authentication and Authorization → Users → Add user** — set username + password.
3. **Core → Techniker / Manager / Administratoren → Add** — link the user to the appropriate profile model. Assigning sites/gauges to a technician is done from `TechnicianProfile`.

## VS Code

A [.vscode/settings.json](.vscode/settings.json) is committed that points the Python extension at `.venv\Scripts\python.exe`. If you see "Cannot find module django.\*" diagnostics, run **Python: Select Interpreter** and pick the one inside `.venv` — your IDE is using a system Python that does not have Django installed.

## Layout

```
WGR_DJANGO/
  manage.py
  requirements.txt
  howto.md                <-- this file
  CLAUDE.md
  wgr/                    <-- project package (settings, root urls, wsgi/asgi)
    settings.py
    urls.py
  core/                   <-- domain models + admin registrations
    models.py
    admin.py
    migrations/0001_initial.py
  technician/             <-- mobile UI app (Task 2)
    views.py
    urls.py
  manager/                <-- desktop UI app (Task 3)
    views.py
    urls.py
  media/                  <-- uploaded gauge photos (gitignored, created on first upload)
  .venv/                  <-- virtual env (gitignored)
  db.sqlite3              <-- dev database (gitignored)
```

## What's next

- **Task 2** — implement the technician camera/upload flow + OCR in [technician/](technician/).
- **Task 3** — implement the manager review/annotation UI in [manager/](manager/).
- **Task 4** — wire the manager UI to provision users and assign technicians to sites/gauges (the M2M fields on `TechnicianProfile` are already in place).
- **Task 5** — CSV import/export of customers + gauges and a search/filter UI.
