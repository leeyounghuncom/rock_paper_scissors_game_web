import random

from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rpsgw.db')

db = SQLAlchemy(app)

#디비 부분 테이블
class GameHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_choice = db.Column(db.String, nullable=False)
    computer_choice = db.Column(db.String, nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'ok'

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET","POST"])
def main():

    rps = ["가위", "바위", "보"]
    msg = None
    gh = None
    w=0
    l=0
    d=0

    if request.method == "POST":
        #POST 방식으로 저장 할 경우 form.get
        guest = request.form.get("guest") #게스트
        bot = random.choice(rps) #봇

        if not guest:
            title_receive = "Guest No Data"

        #가위바위보 기존 코드 복붙
        #0: 비김 #1:패 #2:승
        if guest == bot:
            r = "비겼습니다"
        elif ((guest == "가위" and bot == "바위") or (guest == "바위" and bot == "보") or (guest == "보" and bot == "가위")):
            r = "졌습니다"
        else:
            r = "이겼습니다"

        gh = GameHistory(user_choice=guest, computer_choice=bot, result=r)
        db.session.add(gh)
        db.session.commit()

        msg = f"사용자 : {guest} 컴퓨터 : {bot} {r}"

        q = GameHistory.query.all();
        w = GameHistory.query.filter_by(result="이겼습니다").count()
        l = GameHistory.query.filter_by(result="졌습니다").count()
        d = GameHistory.query.filter_by(result="비겼습니다").count()

        # return redirect(url_for('main.index'))

    return render_template("main.html", data={"msg":msg,"gh":q,"w":w,"l":l,"d":d})
