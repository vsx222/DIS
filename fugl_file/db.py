import sqlite3
import os
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
    # Highscore table
    c.execute('''
        CREATE TABLE IF NOT EXISTS highscore (
            id INTEGER PRIMARY KEY,
            score INTEGER NOT NULL
        )
    ''')

    # Initialize with score = 0 if not set
    c.execute('INSERT OR IGNORE INTO highscore (id, score) VALUES (1, 0)')


    c.executemany('''
        INSERT OR IGNORE INTO celebrities (Name, Male, Alive, Musician, Actor, Sportsperson, American, Nobel_Prize_Winner, On_Instagram, Has_Children, Under_30, Over_50, Married, White, Black, Female, Model, Deceased, Divorced, Millionaire, Been_in_a_Movie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', celebrities)

    conn.commit()
    conn.close()