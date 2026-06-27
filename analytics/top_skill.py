from sqlalchemy import text
from database.connection import engine

query = """
SELECT
    s.skill_name,
    COUNT(*) AS demand
FROM job_skills js
JOIN skills s
    ON js.skill_id = s.id
GROUP BY s.skill_name
ORDER BY demand DESC
LIMIT 10;
"""

with engine.connect() as conn:
    result = conn.execute(text(query))

    print("\nTop Skills:\n")

    for row in result:
        print(row)