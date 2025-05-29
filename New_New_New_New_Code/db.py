import os
import sqlite3

def db_connection():
    return sqlite3.connect("guess.db")

def init_db():
    # Optional: Delete database file to rebuild cleanly each time during development
    if os.path.exists("guess.db"):
        os.remove("guess.db")

    conn = db_connection()
    c = conn.cursor()

    # Create guesses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS guesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guess_text TEXT NOT NULL
        )
    ''')

    # Create celebrities table
    c.execute('''
        CREATE TABLE IF NOT EXISTS celebrities (
            Name TEXT PRIMARY KEY,
            Gender TEXT,
            Nationality TEXT,
            Age INTEGER,
            Eye_Color TEXT,
            Married TEXT,
            Has_Children TEXT,
            on_Instagram TEXT
        )
    ''')

    # Create highscore table
    c.execute('''
        CREATE TABLE IF NOT EXISTS highscore (
            id INTEGER PRIMARY KEY,
            score INTEGER NOT NULL
        )
    ''')
    c.execute('INSERT OR IGNORE INTO highscore (id, score) VALUES (1, 0)')

    # Create professions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS professions (
            Profession_Name TEXT PRIMARY KEY
        )
    ''')

    # Create join table: celebrity_professions
    c.execute('''
        CREATE TABLE IF NOT EXISTS celebrity_professions (
            Celebrity_Name TEXT,
            Profession_Name TEXT,
            PRIMARY KEY (Celebrity_Name, Profession_Name),
            FOREIGN KEY (Celebrity_Name) REFERENCES celebrities(Name),
            FOREIGN KEY (Profession_Name) REFERENCES professions(Profession_Name)
        )
    ''')

    # Insert professions
    professions = [
        ('Actor',),
        ('Musician',),
        ('Dancer',),
        ('Football player',),
        ('Professional cyclist',),
        ('President',),
        ('TV host',),
        ('Entrepreneur',),
        ('Reality TV-star',)
    ]
    c.executemany('INSERT OR IGNORE INTO professions (Profession_Name) VALUES (?)', professions)
    
    # Insert movies
    movies = [
    "Harry Potter",
    "Once Upon a Time in Hollywood",
    "Don't Look Up",
    "The Great Gatsby",
    "Deadpool",
    "Barbie",
    "Top Gun",
    "Spider-Man",
    "Mean Girls",
    "Monte Carlo"
    ]
    # Create movies table
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            title TEXT PRIMARY KEY
        )
    ''')

    # Insert celebrities
    celebrities = [
        ('Michael Jackson', 'Male', 'American', 50, 'Brown', 'Yes', 'No', 'No'),
        ('Lindsay Lohan', 'Female', 'American', 38, 'Green', 'No', 'No', 'Yes'),
        ('Selena Gomez', 'Female', 'American', 32, 'Brown', 'No', 'No', 'Yes'),
        ('Jonas Vingegaard', 'Male', 'Danish', 28, 'Blue', 'Yes', 'Yes', 'Yes'),
        ('Emma Watson', 'Female', 'British', 35, 'Brown', 'No', 'No', 'Yes'),
        ('Barack Obama', 'Male', 'American', 63, 'Brown', 'Yes', 'Yes', 'Yes'),
        ('Beyoncé', 'Female', 'American', 43, 'Brown', 'Yes', 'Yes', 'Yes'),
        ('Cristiano Ronaldo', 'Male', 'Portuguse', 40, 'Brown', 'Yes', 'Yes', 'Yes'),
        ('Taylor Swift', 'Female', 'American', 35, 'Blue', 'No', 'No', 'Yes'),
        ('Leonardo DiCaprio', 'Male', 'American', 50, 'Blue', 'No', 'No', 'Yes'),
        ('Oprah Winfrey', 'Female', 'American', 71, 'Brown', 'Yes', 'Yes', 'Yes'),
        ('Billie Eilish', 'Female', 'American', 23, 'Blue', 'No', 'No', 'Yes'),
        ('Elon Musk', 'Male', 'South Africa', 53, 'Green', 'No', 'Yes', 'Yes'),
        ('Kim Kardashian', 'Female', 'American', 44, 'Brown', 'No', 'Yes', 'Yes'),
        ('Ryan ReyNolds', 'Male', 'Canadian', 48, 'Brown', 'Yes', 'Yes', 'Yes'),
        ('Margot Robbie', 'Female', 'Australia', 35, 'Blue', 'No', 'No', 'Yes'),
        ('Rasmus Højlund', 'Male', 'Danish', 22, 'Blue', 'No', 'No', 'Yes'),
        ('Meryl Streep', 'Female', 'American', 75, 'Blue', 'Yes', 'Yes', 'Yes'),
        ('Ed Sheeran', 'Male', 'British', 34, 'Blue', 'No', 'No', 'Yes'),
        ('Rihanna', 'Female', 'Barbados', 37, 'Green', 'No', 'Yes', 'Yes'),
        ('Zendaya', 'Female', 'American', 28, 'Brown', 'No', 'No', 'Yes'),
        ('David Beckham', 'Male', 'British', 50, 'Brown', 'Yes', 'Yes', 'Yes'),
        ('Tom Holland', 'Male', 'British', 29, 'Brown', 'No', 'No', 'Yes'),
        ('Tom Cruise', 'Male', 'American', 62, 'Green', 'No', 'Yes', 'Yes')
    ]
    c.executemany('''
        INSERT OR IGNORE INTO celebrities (Name, Gender, Nationality, Age, Eye_Color, Married, Has_Children, on_Instagram)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', celebrities)

    # Insert celebrity-profession mappings
    celebrity_professions = [
        ('Michael Jackson', 'Musician'),
        ('Michael Jackson', 'Dancer'),
        ('Lindsay Lohan', 'Actor'),
        ('Lindsay Lohan', 'Musician'),
        ('Selena Gomez', 'Actor'),
        ('Selena Gomez', 'Musician'),
        ('Jonas Vingegaard', 'Professional cyclist'),
        ('Emma Watson', 'Actor'),
        ('Barack Obama', 'President'),
        ('Beyoncé', 'Musician'),
        ('Beyoncé', 'Dancer'),
        ('Cristiano Ronaldo', 'Football player'),
        ('Taylor Swift', 'Musician'),
        ('Leonardo DiCaprio', 'Actor'),
        ('Oprah Winfrey', 'TV host'),
        ('Billie Eilish', 'Musician'),
        ('Elon Musk', 'Entrepreneur'),
        ('Kim Kardashian', 'Reality TV-star'),
        ('Ryan ReyNolds', 'Actor'),
        ('Margot Robbie', 'Actor'),
        ('Rasmus Højlund', 'Football player'),
        ('Meryl Streep', 'Actor'),
        ('Ed Sheeran', 'Musician'),
        ('Rihanna', 'Musician'),
        ('Rihanna', 'Entrepreneur'),
        ('Zendaya', 'Musician'),
        ('Zendaya', 'Dancer'),
        ('Zendaya', 'Actor'),
        ('David Beckham', 'Football player'),
        ('Tom Holland', 'Actor'),
        ('Tom Cruise', 'Actor')
    ]
    c.executemany('''
        INSERT OR IGNORE INTO celebrity_professions (Celebrity_Name, Profession_Name)
        VALUES (?, ?)
    ''', celebrity_professions)


    # Insert celebrity-movie mappings
    c.execute('''
        CREATE TABLE IF NOT EXISTS celebrity_movies (
        celebrity_name TEXT,
        movie_title TEXT,
        PRIMARY KEY (celebrity_name, movie_title),
        FOREIGN KEY (celebrity_name) REFERENCES celebrities(Name),
        FOREIGN KEY (movie_title) REFERENCES movies(title)    
    
        )
    ''')
    celebrity_movies = [
    ('Emma Watson', 'Harry Potter'),
    ('Leonardo DiCaprio', 'Once Upon a Time in Hollywood'),
    ('Leonardo DiCaprio', "Don't Look Up"),
    ('Leonardo DiCaprio', 'The Great Gatsby'),
    ('Ryan ReyNolds', 'Deadpool'),
    ('Margot Robbie', 'Once Upon a Time in Hollywood'),
    ('Margot Robbie', 'Barbie'),
    ('Meryl Streep', "Don't Look Up"),
    ('Zendaya', 'Spider-Man'),
    ('Tom Holland', 'Spider-Man'),
    ('Tom Cruise', 'Top Gun'),
    ('Lindsay Lohan', 'Mean Girls'),
    ('Selena Gomez', 'Monte Carlo'),
]

    # Insert using executemany just like professions
    c.executemany('''
        INSERT OR IGNORE INTO celebrity_movies (celebrity_name, movie_title)
        VALUES (?, ?)
    ''', celebrity_movies)


    conn.commit()
    conn.close()
