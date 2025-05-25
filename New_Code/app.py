from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'


db.init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = db.db_connection()
    c = conn.cursor()
    # Get current highscore
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

            # Update highscore if current guess_count is greater
            if session["guess_count"] < highscore:
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
    )


@app.route("/reset")
def reset():
    conn = db.db_connection()
    conn.execute("DELETE FROM guesses")
    conn.commit()
    conn.close()
    session.clear()  # Clears the stored target celebrity and guess count
    return redirect("/")  # Redirects back to the main page
