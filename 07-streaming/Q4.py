import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="postgres",
    database="postgres",
)

cursor = conn.cursor()

cursor.execute("""
    SELECT window_start, PULocationID, num_trips 
    FROM processed_events_aggregated 
    ORDER BY num_trips DESC 
    LIMIT 1;
""")

results = cursor.fetchall()

for row in results:
    print(f"window_start: {row[0]}, PULocationID: {row[1]}, num_trips: {row[2]}")

cursor.close()
conn.close()
