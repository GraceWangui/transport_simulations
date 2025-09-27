````markdown
# Transport Simulations

A minimal Django web application for managing **transport research simulations** and their **runs**.  
Built to practice **research software engineering best practices**: reproducibility, authorship, and clean deployment (Django + Docker + Pipelines).

---

## Features

- User authentication (register, login, logout)
- Manage **Simulations** (title, description, mode, baseline flag, author)
- Manage **Runs** linked to simulations (label, git commit, CO₂ emissions, author)
- Authors are automatically set based on the logged-in user
- Clean UI with gradient/brand navbar and card-based layout
- Tables with clear headers and action buttons (View, Edit, Delete)
- Responsive navigation with Home, Profile, Settings
- Background  image for visual branding

---

## Tech Stack

- **Backend:** Django 5.x, Python 3.13
- **Frontend:** Django HTML templates, custom CSS
- **Database:** SQLite (default) – easily swappable with PostgreSQL
- **Auth:** Django’s built-in authentication
- **Deployment-ready:** Git, Docker, Pipelines

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/transport_simulations.git
cd transport_simulations
````

### 2. Create and activate virtual environment

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin panel)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

1. Register a new account or log in.
2. Create a new **Simulation**.
3. Add **Runs** under each simulation with:

   * `label`
   * `git_commit`
   * `CO₂ emissions`
4. Each record will display the **author** automatically.
5. Manage your profile and settings via the navbar.

---

## Development Notes

* Models use `author = ForeignKey(User)` to track provenance for both Simulations and Runs.
* Create/update views set `instance.author = request.user`.
* Static assets served via `/static/`; e.g. background image lives in `static/img/`.
* Table headers styled for contrast:

