import pymysql

# -------------------- DB Connection --------------------
def connect_db():
    return pymysql.connect(
        host="mysql-200444-0.cloudclusters.net",
        port=10027,
        user="admin",
        password="user001@",
        database="real_estate",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # Return results as dictionaries
    )

# -------------------- Load All Clients --------------------
def load_clients():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM clients")
            return cursor.fetchall()
    finally:
        conn.close()

# -------------------- Insert New Client --------------------
def insert_client(client):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO clients (id, name, father_name, plot_no, block, location,
                    total_price, paid_amount, last_payment_date, pin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                client["id"], client["name"], client["father_name"], client["plot_no"],
                client["block"], client["location"], client["total_price"], client["paid_amount"],
                client["last_payment_date"], client["pin"]
            ))
            conn.commit()
    finally:
        conn.close()

# -------------------- Update Existing Client --------------------
def update_client_db(client):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            query = """
                UPDATE clients SET name=%s, father_name=%s, plot_no=%s, block=%s, location=%s,
                    total_price=%s, paid_amount=%s, last_payment_date=%s, pin=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                client["name"], client["father_name"], client["plot_no"],
                client["block"], client["location"], client["total_price"], client["paid_amount"],
                client["last_payment_date"], client["pin"], client["id"]
            ))
            conn.commit()
    finally:
        conn.close()

# -------------------- Delete Client --------------------
def delete_client_db(client_id, pin):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM clients WHERE id=%s AND pin=%s", (client_id, pin))
            conn.commit()
    finally:
        conn.close()

# -------------------- Get Client By ID --------------------
def get_client_by_id(client_id):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM clients WHERE id=%s", (client_id,))
            return cursor.fetchone()
    finally:
        conn.close()
