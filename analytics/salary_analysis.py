from sqlalchemy import text
from database.connection import engine

query ="""
SELECT
    position,
    salary_min,
    salary_max
FROM jobs
LIMIT 10;
"""
with engine.connect() as conn:
    result = conn.execute(text(query))

    print("\nSalary:\n")

    for row in result:
        print(row)