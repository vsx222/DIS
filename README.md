# Guess Who — Celebrity Web App (Documentation)
### Created by Caroline Busk (cxb190), Christoffer Fugl (kjq112), Trine Ibsen (jvs273) \& Max Marius Toft (vsx222)

A simple Flask-based web app where you guess a randomly selected celebrity based on name input. Built with Python, SQLite and HTML/CSS.

---
The sound is from: https://www.youtube.com/watch?v=x2NzoLMWAwQ&ab_channel=GamingSoundFX.
---

## E/R Diagram
<img width="884" alt="E:R diagram" src="https://github.com/user-attachments/assets/84a2704a-2709-42fd-ba90-2d6625dc19bb" />

This Entity-Relationship (E/R) diagram represents a system that stores and organizes information about celebrities, the movies they've appeared in, and their professional backgrounds.

At the heart of the diagram is the Celebrity entity, which includes personal details such as name, gender, age, nationality, marital status, whether they have children, eye color, and whether they are active on Instagram.

Celebrities are connected to Movies through the relationship "Has appeared in", which captures the films they’ve been part of. Each movie is identified by its title.

On the other side, celebrities are also connected to their Profession through the relationship "Famous for", which helps specify what they are known for professionally—such as acting, singing, or directing. Each profession has a name to describe it.

Overall, this diagram paints a clear picture of how a celebrity’s personal details, career highlights, and movie appearances are related, making it a useful model for managing information in entertainment databases or media platforms.

---

## How to compile the web-app from source (incl. scripts to initialize the database)

### OBS!!! Remember to turn on the sound!

After downloading the project, unzip it and navigate to the correct directory in  terminal:
	
	cd Code/

ON MAC/LINUX:
Run in terminal the following:

	python -m venv .venv
	source .venv/bin/activate
	pip install flask
	flask run --debug  
 	flask run --debugger (ON MAC)


ON WINDOWS
Run in terminal the following:

	python -m venv .venv
	Set-ExecutionPolicy Unrestricted -Scope Process
	.venv\Scripts\activate
	pip install flask
	flask run --debug  


---

## How to run and interact with your web-app?
When the web app is running:

* The app automatically selects a random celebrity as the target.

* You begin by asking questions and receiving answers to help narrow down the possible options.

* You can visually eliminate celebrities (by pressing the pictures) who no longer match the traits — just like in the classic “Guess Who?” game.

* When you are confident, enter a name in the “Guess Celebrity” input field. You’ll be told immediately whether your guess is correct or not.

* Every guess you make is stored and displayed on the page for easy tracking.

* Click “Restart Game” at any time to reset the game, clear guesses, and start fresh with a new mysterious celebrity. This will still keep your highscore so you can compare with your previous best result.
