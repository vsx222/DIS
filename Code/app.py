from flask import Flask, render_template, request, redirect # We import render_template so we can render Jinja2 code, and request so we can handle POSTs
# We import sqlite, likely we don't need to install any new library because this is a default Python library
import sqlite3

# This creates the connection to the database
def db_connection():
    # When we run this code we will this file being created. The file will persist between executations of the server.
    # Keep in mind that you may need to delete this file every time you change the schema of your database.
    conn = sqlite3.connect('guess.db')
    conn.row_factory = sqlite3.Row
    return conn

# This initializes our database with a schema, and some initial data
def init_db():
    conn = db_connection()
    # We create a table that has two fields: the id of the todo, and a todo_text that is unique
    conn.execute('''CREATE TABLE IF NOT EXISTS guesses (id INTEGER PRIMARY KEY AUTOINCREMENT, guess_text TEXT NOT NULL UNIQUE)''')

    # This cursor a database bureaucracy: it is a control structure that enables traversal over the records in a database.
    c = conn.cursor()
    guesses = ['DIS assignment 1', 'Groceries', 'DIS assignment 2', 'DIS project']
    for guess in guesses:
        # (todo, ) is a Python quirk: we need to provide tuples to the insert query, and that is how we can define a tuple with a single element (an 1-nary tuple).
        # The OR IGNORE is a trick so when we run the database again we don't get errors from duplicated entries (as we have the UNIQUE constraint).
        c.execute('INSERT OR IGNORE INTO guesses (guess_text) VALUES (?)', (guess,))

    conn.commit()
    conn.close()

# We initialize the database
init_db()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return redirect('/guess')

# We have a new route to /todo
@app.route('/guess', methods=['GET', 'POST'])
def list_guess():
    conn = db_connection()
    # This route has two functions: GET and POST.
    # If there is a POST, we do the insert in the database
    if request.method == 'POST':
        new_guess = request.form['new_guess']
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO guesses (guess_text) VALUES (?)', (new_guess,))
        conn.commit()

    # But we always get all entries from the database
    db_guesses = conn.execute('SELECT guess_text FROM guesses').fetchall()
    conn.close()
    guesses = []
    # The entries come in dictionary data structure, we need to convert it to a list
    for db_guess in db_guesses:
        guesses.append(db_guess['guess_text'])

    # We render the todo template with guesses we fetched from the database
    return render_template('guess.html', guesses=guesses)
