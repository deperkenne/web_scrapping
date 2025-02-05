import psycopg2
cur = None
conn = None


def connection_to_db():
    global conn
    global cur
    try:
        conn = psycopg2.connect(host="192.168.178.194",
                                port="5432",
                                dbname="db",
                                user="root",
                                password="root")
        print("connection to database success")
        cur = conn.cursor()
    except Exception as e:
        print("error :", e.__str__())


def create_table_adidas_shoes(conn, cur):
    try:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS adidas_shoes (
                shoes_id SERIAL PRIMARY KEY,
                price VARCHAR(50),
                title VARCHAR(50),
                subtitle VARCHAR(50),
                number_of_color VARCHAR(50),
                date TIMESTAMP
             )
            """)
        conn.commit()
        print("success")
    except Exception as e:
        print(e)

if __name__ =="__main__":
    connection_to_db()