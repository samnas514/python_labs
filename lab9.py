from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request



app = Flask(__name__)

app.config['SQLALCHEMY-DATABASE-URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

class GamesDone(db.Model):
    game = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)


@app.route("/input", methods=("POST","GET"))
def input():
    if request.method == "POST":
        try:
            g = GamesDone(game,year)
            db.session.add(g)

            db.session.commit()
        except:
            db.session.rollback()
            print("Что-то пошло не так(((")
    return render_template("input.html", title="Пройденные игры")

if __name__ ==  "__main__":
    app.run(debug=True)

