import sqlite3
import json
import pandas as pd


conn = sqlite3.connect("05/crime_data.db")
cursor = conn.cursor()


# 1. 10 последних зарегестрированных преступлений с типом Burglary, отсортированных по месяцу, в порядке убывания
first_query = """
SELECT crime_id, month, reported_by, location
FROM lincolnshire_police
WHERE crime_type = "Burglary"
ORDER BY month DESC
LIMIT 10;
"""

result = pd.read_sql_query(first_query, conn)
result.to_json(
    "05/query_answers/burglary.json", orient="records", force_ascii=False, indent=4
)
print("1 Done")


# 2. Количество преступлений по каждому типу из каждой таблицы
second_query = """
SELECT crime_type, COUNT(*) AS crime_count
FROM (
    SELECT crime_type FROM north_wales_police
    UNION ALL
    SELECT crime_type FROM north_yorkshire_police
    UNION ALL
    SELECT crime_type FROM lincolnshire_police 
) AS combined
GROUP BY crime_type
ORDER BY crime_count DESC;
"""

result = pd.read_sql_query(second_query, conn)
result.to_json(
    "05/query_answers/all_crimes_count.json",
    orient="records",
    force_ascii=False,
    indent=4,
)
print("2 done")


# 3. Min, Max, Avg широты для преступлений с типом Anti-social behaviour
third_query = """
SELECT 
    MIN(latitude) AS min_latitude,
    MAX(latitude) AS max_latitude,
    AVG(latitude) AS avg_latitude
FROM north_wales_police
WHERE crime_type = 'Anti-social behaviour';
"""

result = pd.read_sql_query(third_query, conn)
result.to_json(
    "05/query_answers/min_max_avg.json",
    orient="records",
    force_ascii=False,
    indent=4,
)
print("3 done")


# 4. Группировка по lsoa_code
fourth_query = """
SELECT lsoa_code, COUNT(*) AS crime_count
FROM north_yorkshire_police
GROUP BY lsoa_code
ORDER BY crime_count DESC;
"""

result = pd.read_sql_query(fourth_query, conn)
result.to_json(
    "05/query_answers/lsoa_code.json",
    orient="records",
    force_ascii=False,
    indent=4,
)
print("4 done")


# 5. Обновление данных, где last_outcome_category пустой
queries = [
    """
    UPDATE north_wales_police
    SET last_outcome_category = 'Unknown'
    WHERE last_outcome_category IS NULL OR last_outcome_category = '';
    """,
    """
    UPDATE north_yorkshire_police
    SET last_outcome_category = 'Unknown'
    WHERE last_outcome_category IS NULL OR last_outcome_category = '';
    """,
    """
    UPDATE lincolnshire_police 
    SET last_outcome_category = 'Unknown'
    WHERE last_outcome_category IS NULL OR last_outcome_category = '';
    """,
]

for query in queries:
    cursor.execute(query)
conn.commit()


# 6. Подсчет предступлений, имещие last_outcome_category = "Under investigation"
sixth_query = """
SELECT 
    'North Wales' AS region, COUNT(*) AS count
FROM north_wales_police
WHERE last_outcome_category = "Under investigation"
UNION ALL
SELECT 
    'North Yorkshire' AS region, COUNT(*) AS count
FROM north_yorkshire_police
WHERE last_outcome_category = "Under investigation"
UNION ALL
SELECT 
    'Lincolnshire' AS region, COUNT(*) AS count
FROM lincolnshire_police 
WHERE last_outcome_category = "Under investigation";
"""

result = pd.read_sql_query(sixth_query, conn)
result.to_json(
    "05/query_answers/under_investig.json",
    orient="records",
    force_ascii=False,
    indent=4,
)
print("5 done")
conn.close()
