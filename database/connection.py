from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres:postgres123@localhost:5432/job_market_db"
)

engine = create_engine(DATABASE_URL)