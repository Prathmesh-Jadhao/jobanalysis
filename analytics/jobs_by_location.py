from sqlalchemy import text
from database.connection import engine

query ="""
SELECT
    location,
    COUNT(*)
FROM jobs
GROUP BY location
ORDER BY COUNT(*) DESC;
"""
with engine.connect() as conn:
    result = conn.execute(text(query))

    print("\nJob Location:\n")

    for row in result:
        print(row)