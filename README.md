# Blog CRUD RESTful API
This is a very simple blog CRUD api powered by FastAPI that relies on JWT and refresh tokens for authentication

## Features
- Extensible
- JWT Authentication
- Refresh tokens
- SQLModel for database queries
- settings.env file for setting jwt settings

# Setup
```bash
git clone https://github.com/XCarCedo/blog-api.git
cd blog-api

pip install uv
# Skip if uv is already installed

uv sync
uv run fastapi dev
```

# Docs
Auto generated docs are available at localhost:8000/docs for Swagger UI and localhost:8000/redoc for Redoc UI