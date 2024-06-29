import random

from flask import Flask,render_template,request

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def main():
    rps = ["가위", "바위", "보"]

    if request.method == "POST":
        guest = request.form.get("guest") #게스트
        bot = random.choice(rps) #봇


    return render_template("main.html", data={"g" :guest, "b":bot})
