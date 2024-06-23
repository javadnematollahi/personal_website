from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def my_root():
    name = ""
    return render_template("index.html", name=name)