from flask import Flask, render_template, request, redirect, session, jsonify
import db
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
db.init_db()

# List of supported question options (value, label)
QUESTION_OPTIONS = [
    ("Male", "Is the person a male?"),
    ("Female", "Is the person a female?"),
    ("Musician", "Is the person a musician?"),
    ("Actor", "Is the person an actor?"),
    ("Dancer", "Is the person a dancer?"),
    ("Football player", "Is the person a football player?"),
    ("Professional cyclist", "Is the person a professional cyclist?"),
    ("President", "Is the person a president?"),
    ("TV host", "Is the person a TV host?"),
    ("Entrepreneur", "Is the person an entrepreneur?"),
    ("Reality TV-star", "Is the person a reality TV-star?"),
    ("On_Instagram", "Is the person on Instagram?"),
    ("Has_Children", "Does the person have children?"),
    ("Under_30", "Is the person under 30 years old?"),
    ("Over_50", "Is the person over 50 years old?"),
    ("Married", "Is the person married?"),

    # ✅ Movie-related questions
    ("movie:Harry Potter", "Has the person appeared in Harry Potter?"),
    ("movie:Once Upon a Time in Hollywood", "Has the person appeared in Once Upon a Time in Hollywood?"),
    ("movie:Don't Look Up", "Has the person appeared in Don't Look Up?"),
    ("movie:The Great Gatsby", "Has the person appeared in The Great Gatsby?"),
    ("movie:Deadpool", "Has the person appeared in Deadpool?"),
    ("movie:Barbie", "Has the person appeared in Barbie?"),
    ("movie:Top Gun", "Has the person appeared in Top Gun?"),
    ("movie:Spider-Man", "Has the person appeared in Spider-Man?"),
    ("movie:Mean Girls", "Has the person appeared in Mean Girls?"),
    ("movie:Monte Carlo", "Has the person appeared in Monte Carlo?")
]

@app.route("/", methods=["GET", "POST"])
def index():
    conn = db.db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    highscore = c.execute("SELECT score FROM highscore WHERE id = 1").fetchone()["score"]

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
            if session["guess_count"] < highscore or highscore == 0:
                highscore = session["guess_count"]
                c.execute("UPDATE highscore SET score = ? WHERE id = 1", (highscore,))
                conn.commit()
        else:
            session["winner"] = False

    guesses = c.execute("SELECT guess_text FROM guesses").fetchall()
    headers = [desc[0] for desc in c.execute("SELECT * FROM celebrities").description]
    data = c.execute("SELECT * FROM celebrities").fetchall()
    conn.close()

    return render_template(
        "name.html",
        guesses=guesses,
        headers=headers,
        data=data,
        guess_count=session.get("guess_count", 0),
        winner=session.get("winner", None),
        highscore=highscore,
        question_options=QUESTION_OPTIONS
    )

@app.route("/reset")
def reset():
    conn = db.db_connection()
    conn.execute("DELETE FROM guesses")
    conn.commit()
    conn.close()
    session.clear()
    return redirect("/")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    conn = db.db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    data = request.get_json()
    attribute_key = data.get("attribute")
    celeb_name = session.get("target_celebrity")

    if not celeb_name:
        return jsonify({"error": "No target celebrity in session"}), 400

    celeb = c.execute("SELECT * FROM celebrities WHERE Name = ?", (celeb_name,)).fetchone()
    if not celeb:
        return jsonify({"error": "Celebrity not found"}), 404

    # ✅ Increment question count for all questions
    session["guess_count"] = session.get("guess_count", 0) + 1
    guess_count = session["guess_count"]

    # === Logic-based answers ===
    if attribute_key == "Male":
        return jsonify({"answer": "Yes" if celeb["Gender"] == "Male" else "No", "guess_count": guess_count})
    elif attribute_key == "Female":
        return jsonify({"answer": "Yes" if celeb["Gender"] == "Female" else "No", "guess_count": guess_count})
    elif attribute_key == "Married":
        return jsonify({"answer": "Yes" if celeb["Married"] == "Yes" else "No", "guess_count": guess_count})
    elif attribute_key == "Has_Children":
        return jsonify({"answer": "Yes" if celeb["Has_Children"] == "Yes" else "No", "guess_count": guess_count})
    elif attribute_key == "On_Instagram":
        return jsonify({"answer": "Yes" if celeb["on_Instagram"] == "Yes" else "No", "guess_count": guess_count})
    elif attribute_key == "Under_30":
        return jsonify({"answer": "Yes" if celeb["Age"] < 30 else "No", "guess_count": guess_count})
    elif attribute_key == "Over_50":
        return jsonify({"answer": "Yes" if celeb["Age"] > 50 else "No", "guess_count": guess_count})

    # Profession questions
    elif attribute_key in [
        "Actor", "Musician", "Dancer", "Football player", "Professional cyclist",
        "President", "TV host", "Entrepreneur", "Reality TV-star"
    ]:
        result = c.execute('''
            SELECT 1 FROM celebrity_professions
            WHERE Celebrity_Name = ? AND Profession_Name = ?
        ''', (celeb_name, attribute_key)).fetchone()
        return jsonify({"answer": "Yes" if result else "No", "guess_count": guess_count})

    # Movie questions (fixed)
    elif attribute_key.startswith("movie:"):
        movie_title = attribute_key.replace("movie:", "")
        result = c.execute('''
            SELECT 1
            FROM celebrity_movies
            WHERE celebrity_name = ? AND movie_title = ?
        ''', (celeb_name, movie_title)).fetchone()
        return jsonify({"answer": "Yes" if result else "No", "guess_count": guess_count})

    # Unknown
    else:
        return jsonify({"error": f"Unknown attribute: {attribute_key}"})
