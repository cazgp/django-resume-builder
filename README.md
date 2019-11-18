# django-resume-builder
This is the base project for the SteamaCo Django resume builder assessment.

## Setup (Docker)

Use docker-compose over plain docker.
This is because it sets up all the ports and volumes for us, not because we run multiple containers.

- `docker-compose run web python manage.py migrate`
- `docker-compose run web python manage.py createsuperuser`
- `docker-compose up`

## Setup (Manual UNIX)
- Install `python` (version 3), `pip`, and `virtualenv` for your platform.
- Clone this repository.
- Create a virtual environment in the repository's base directory. `env` has already been added to the `.gitignore`.
- Install the dependencies in `requirements.txt`.
- Run `python manage.py migrate`. This will create a local database, `db.sqlite3`.
- *Optional*: Create a superuser using `python manage.py createsuperuser`. This account may be used to access the Django admin site at `/admin/`.

## Local server
`docker-compose up` or `python manage.py runserver`

## Code style
This repository follows the [PEP8](https://www.python.org/dev/peps/pep-0008/) standard. `pycodestyle apps/` should produce no warnings.

## Testing
`docker-compose run web python manage.py test` or `./manage.py test`

## Architectural Decisions
The architectural decisions can be found in the `architecture.tex` document.
Compile with `pandoc -o architecture.pdf architecture.md`.

The graph can be retrieved with: `./manage.py graph_models resume auth -I Resume,ResumeItem,User -g -o model.png`
