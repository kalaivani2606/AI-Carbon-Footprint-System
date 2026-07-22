import sqlite3

DATABASE = "carbon.db"

def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT UNIQUE,

        password TEXT

    )
    """)

    # Carbon History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        transport REAL,

        electricity REAL,

        water REAL,

        plastic REAL,

        waste REAL,

        fuel REAL,

        carbon REAL,

        category TEXT

    )
    """)

    conn.commit()
    conn.close()


# ---------------- USER ----------------

def register_user(name,email,password):

    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()

    cursor.execute(

    "INSERT INTO users(name,email,password) VALUES(?,?,?)",

    (name,email,password)

    )

    conn.commit()

    conn.close()


def login_user(email,password):

    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()

    cursor.execute(

    "SELECT * FROM users WHERE email=? AND password=?",

    (email,password)

    )

    user=cursor.fetchone()

    conn.close()

    return user


# ---------------- HISTORY ----------------

def save_history(transport,electricity,water,plastic,waste,fuel,carbon,category):

    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()

    cursor.execute("""

    INSERT INTO history(

    transport,

    electricity,

    water,

    plastic,

    waste,

    fuel,

    carbon,

    category

    )

    VALUES(?,?,?,?,?,?,?,?)

    """,(transport,electricity,water,plastic,waste,fuel,carbon,category))

    conn.commit()

    conn.close()


def get_history():

    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")

    data=cursor.fetchall()

    conn.close()

    return data