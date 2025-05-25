from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def db_connection():
    conn = sqlite3.connect('guess.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Optional: Delete database file to rebuild cleanly each time during development
    if os.path.exists("guess.db"):
        os.remove("guess.db")

    conn = db_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS guesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guess_text TEXT NOT NULL
        )
    ''')

    # Celebrities table with only a few traits for now (you can expand this)
    c.execute('''
        CREATE TABLE IF NOT EXISTS celebrities (
            Name TEXT PRIMARY KEY,
            Male TEXT,
            Alive TEXT,
            Musician TEXT,
            Actor TEXT,
            Sportsperson TEXT,
            American TEXT,
            Nobel_Prize_Winner TEXT,
            On_Instagram TEXT,
            Has_Children TEXT,
            Under_30 TEXT,
            Over_50 TEXT,
            Married TEXT,
            White TEXT,
            Black TEXT,
            Female TEXT,
            Model TEXT,
            Deceased TEXT,
            Divorced TEXT,
            Millionaire TEXT,
            Been_in_a_Movie TEXT
        )
    ''')


    # Sample data (expand as needed)
    celebrities = [
        ('Michael Jackson', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes'),
    ('Lindsay Lohan', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Selena Gomez', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Jonas Vingegaard', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'),
    ('Emma Watson', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Barack Obama', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no'),
    ('Beyoncé', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'yes', 'yes'),
    ('Cristiano Ronaldo', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'),
    ('Taylor Swift', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Leonardo DiCaprio', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes'),
    ('Oprah Winfrey', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Billie Eilish', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Elon Musk', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'),
    ('Kim Kardashian', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes'),
    ('Ryan Reynolds', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes'),
    ('Margot Robbie', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes'),
    ('Rasmus Højlund', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'),
    ('Meryl Streep', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Ed Sheeran', 'yes', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'),
    ('Rihanna', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'yes'),
    ('Zendaya', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes'),
    ('David Beckham', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'),
    ('Tom Holland', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes'),
    ('Tom Cruise', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes')
    ]

    c.executemany('''
        INSERT OR IGNORE INTO celebrities (Name, Male, Alive, Musician, Actor, Sportsperson, American, Nobel_Prize_Winner, On_Instagram, Has_Children, Under_30, Over_50, Married, White, Black, Female, Model, Deceased, Divorced, Millionaire, Been_in_a_Movie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', celebrities)

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = db_connection()
    c = conn.cursor()

    if "target_celebrity" not in session:
        celeb = c.execute("SELECT Name FROM celebrities ORDER BY RANDOM() LIMIT 1").fetchone()
        session["target_celebrity"] = celeb["Name"]
        session["guess_count"] = 0

    if request.method == "POST":
        guess = request.form["new_guess"]
        c.execute("INSERT INTO guesses (guess_text) VALUES (?)", (guess,))
        session["guess_count"] += 1
        conn.commit()

        if guess.lower().strip() == session["target_celebrity"].lower():
            session["winner"] = True
        else:
            session["winner"] = False

    guesses = c.execute("SELECT guess_text FROM guesses").fetchall()
    headers = [desc[0] for desc in c.execute("SELECT * FROM celebrities").description]
    data = c.execute("SELECT * FROM celebrities").fetchall()
    conn.close()

    return render_template(
        "name.html",  # Updated to match your renamed template
        guesses=guesses,
        headers=headers,
        data=data,
        guess_count=session.get("guess_count", 0),
        winner=session.get("winner", None),
    )

@app.route("/reset")
def reset():
    conn = db_connection()
    conn.execute("DELETE FROM guesses")
    conn.commit()
    conn.close()
    session.clear()  # Clears the stored target celebrity and guess count
    return redirect("/")  # Redirects back to the main page



