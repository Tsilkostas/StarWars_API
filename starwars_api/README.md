# Star Wars API Project

## Overview
This Django project provides a RESTful API to fetch, store, and search Star Wars characters, films, and starships. It integrates with the SWAPI, uses a SQL database (SQLite by default), and supports pagination, search, and filtering.

## Features
- Fetch and store Star Wars data from SWAPI
- Retrieve and search characters, films, and starships
- Pagination and filtering support
- Error handling for API/database issues
- Unit tests with 80%+ code coverage
- API documentation via Django REST Framework's browsable API

## Environment Setup
1. **Clone the repository**
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install manually:
   ```powershell
   pip install django djangorestframework django-filter coverage requests
   ```

## Database Setup
1. **Apply migrations:**
   ```powershell
   python manage.py migrate
   ```

## Running the Application
1. **Start the development server:**
   ```powershell
   python manage.py runserver
   ```
2. **Access the API:**
   - API root: http://127.0.0.1:8000/
   - Example endpoints:
     - `/api/characters/`
     - `/api/films/`
     - `/api/starships/`

## Fetching Data from SWAPI
- Use the custom `fetch` actions (POST requests) on each endpoint to populate the database from SWAPI.
- Example (using HTTPie or curl):
  ```bash
  http POST http://127.0.0.1:8000/api/characters/fetch/
  http POST http://127.0.0.1:8000/api/films/fetch/
  http POST http://127.0.0.1:8000/api/starships/fetch/
  ```
  # Note:
  - When adding or viewing character data, the url field should use the SWAPI format, e.g.
  ```bash
   https://swapi.info/api/people/1/
   ```

## Running Tests & Coverage
1. **Run unit tests:**
   ```powershell
   python manage.py test
   ```
2. **Check code coverage:**
   ```powershell
   coverage run manage.py test
   coverage report
   coverage html
   ```
   Open `htmlcov/index.html` in your browser for a detailed report.

3. **Test Coverage**:
   
   All tests pass.

Example coverage summary (from `coverage report -m`):
```
Name                             Stmts   Miss  Cover
----------------------------------------------------
api\__init__.py                      0      0   100%
api\admin.py                         7      0   100%
api\apps.py                          4      0   100%
api\migrations\0001_initial.py       5      0   100%
api\migrations\__init__.py           0      0   100%
api\models.py                       33      0   100%
api\serializers.py                  16      0   100%
api\swapi_client.py                 17      0   100%
api\tests.py                       229     62    72%
api\urls.py                          7      0   100%
api\views.py                        71      0   100%
manage.py                           11      2    82%
starwars_api\__init__.py             0      0   100%
starwars_api\settings.py            20      0   100%
starwars_api\urls.py                 6      0   100%
----------------------------------------------------
TOTAL                              426     64    85%
```
To generate this report, run:
   ```powershell
   coverage run manage.py test
   coverage report
   coverage report -m
   ```

## API Documentation
- Swagger/OpenAPI documentation is available at:
  - [Swagger UI](http://127.0.0.1:8000/api/schema/swagger-ui/)
  - [Redoc](http://127.0.0.1:8000/api/schema/redoc/)
- The browsable API is available at the root and each endpoint.
- API docs are powered by `drf-spectacular`.

## Django Admin

- Access the admin interface at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- Create a superuser with:
  ```powershell
  python manage.py createsuperuser

## Testing Notes

- All external SWAPI calls are mocked in unit tests for reliability.
- Code coverage is above 80% (see coverage instructions above).

## Notes
- Python 3.x required
- Default database is SQLite (configurable in `settings.py`)
- All dependencies should be installed in the virtual environment

## License
MIT
