# init_db.py
import sqlite3

DB_FILE = "demo.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "USER" (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Login TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        Name TEXT NOT NULL
    )
    """)

    try:
        cursor.execute("""
        INSERT INTO "USER" (Login, Password, Name)
        VALUES (?, ?, ?)
        """, ("john_doe", "securepassword123", "John Doe"))
        conn.commit()
        print("Utilisateur 'john_doe' inséré.")
    except sqlite3.IntegrityError:
        print("Utilisateur déjà existant.")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "TASK" (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        description TEXT NOT NULL,
        statut TEXT NOT NULL,
        priorite TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES USER(id)
    )
    """)

    # Récupération de l'id de john_doe
    cursor.execute("SELECT id FROM USER WHERE Login = ?", ("john_doe",))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
        try:
            cursor.execute("""
            INSERT INTO "TASK" (description, statut, priorite, user_id)
            VALUES (?, ?, ?, ?)
            """, ("descriptiondoe", "statutdoe", "prioritedoe", user_id))
            conn.commit()
            print("Tâche insérée.")
        except sqlite3.IntegrityError:
            print("Tâche déjà existante.")
    else:
        print("Utilisateur john_doe introuvable pour la tâche.")

    conn.close()

if __name__ == "__main__":
    init_db()
