import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route("/", methods=("POST", "GET"))
def index():
    if request.method == "POST":
        film = request.form["film"]
        resonse = film
        return redirect(url_for("index", result=film))
    else:
        result = request.args.get("result")
        return render_template("index.html", result=result)