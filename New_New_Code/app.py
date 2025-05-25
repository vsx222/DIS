from flask import Flask, render_template, request, redirect, session, jsonify
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
    )


@app.route("/reset")
def reset():
    conn = db.db_connection()
    conn.execute("DELETE FROM guesses")
    conn.commit()
    conn.close()
    session.clear()  # Clears the stored target celebrity and guess count
    return redirect("/")  # Redirects back to the main page


@app.route("/get_answer", methods=["POST"])
def get_answer():
    from flask import jsonify
    import json
    conn = db.db_connection()
    conn.row_factory = db.sqlite3.Row
    c = conn.cursor()

    data = request.get_json()
    attribute_key = data.get("attribute")

    # Map dropdown values to actual database column names
    attribute_map = {
        "Male": "Male",
        "Alive": "Alive",
        "Musician": "Musician",
        "Actor": "Actor",
        "Sportsperson": "Sportsperson",
        "American": "American",
        "Nobel_Prize_Winner": "Nobel_Prize_Winner",
        "On_Instagram": "On_Instagram",
        "Has_Children": "Has_Children",
        "Under_30": "Under_30",
        "Over_50": "Over_50",
        "Married": "Married",
        "White": "White",
        "Black": "Black",
        "Female": "Female",
        "Model": "Model",
        "Deceased": "Deceased",
        "Divorced": "Divorced",
        "Millionaire": "Millionaire",
        "Been_in_a_Movie": "Been_in_a_Movie"
    }

    column_name = attribute_map.get(attribute_key)
    if not column_name:
        return jsonify({"error": "Invalid attribute selected"}), 400

    celeb_name = session.get("target_celebrity")
    if not celeb_name:
        return jsonify({"error": "No target celebrity in session"}), 400

    celeb = c.execute("SELECT * FROM celebrities WHERE Name = ?", (celeb_name,)).fetchone()
    conn.close()

    if not celeb or column_name not in celeb.keys():
        return jsonify({"error": "Invalid column or celebrity not found"}), 404

    # ✅ Increment guess/question count
    session["guess_count"] = session.get("guess_count", 0) + 1

    answer = celeb[column_name]
    return jsonify({"answer": str(answer)})


