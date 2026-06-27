from sqlalchemy import text
from database.connection import engine

query ="""
SELECT
    company,
    COUNT(*) AS jobs
FROM jobs
GROUP By company
ORDER BY jobs DESC
LIMIT 10;
"""
with engine.connect() as conn:
    result = conn.execute(text(query))

    print("\nTop Companies:\n")

    for row in result:
        print(row)