import psycopg2

conn = psycopg2.connect (
    host = 'localhost',
    port = '5432',
    database = 'postgres',
    user = 'postgres',
    password = 'postgres'
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE currencies (
	id SERIAL PRIMARY KEY,
	currency_name VARCHAR(50) NOT NULL,
	rate NUMERIC(10, 4) NOT NULL
    )
""")

conn.commit()
print("Таблица создана")

cursor.close()
conn.close()
