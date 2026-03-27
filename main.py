# fastapi run main.py
# uvicorn main:app --reload reload only in dev not prod

# pip install sqlalchemy psycopg2-binary  # For PostgreSQL
# # or
# pip install sqlalchemy pymysql          # For MySQL
# # or
# pip install sqlalchemy aiosqlite         # For SQLite (async)

# alembic init alembic
# python -m alembic init alembic
# alembic revision --autogenerate -m "Initial migration"
# python -m alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head
# alembic downgrade -1 // roll back

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "hello"}

from app.app import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
