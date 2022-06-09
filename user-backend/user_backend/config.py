import os

DEVELOPMENT = False

if not DEVELOPMENT:
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']
    database = os.environ['POSTGRES_DB']
    port = os.environ['POSTGRES_PORT']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

    DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
else:
    JWT_SECRET_KEY = "jwtsecretkey"
    # DATABASE_CONNECTION_URI = "postgresql://postgres:password@localhost:5432/userbackend"
    DATABASE_CONNECTION_URI = "sqlite:///test.db"

