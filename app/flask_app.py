from flask import Flask, render_template, flash, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import configparser
import json


app = Flask(__name__)
app.secret_key = "ij298hw9iofgj3ugdf"
config = configparser.ConfigParser()
config.read("my.ini")
info = config["STUFF"]
app.config["SQLALCHEMY_ECHO"]=False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://{}:{}@{}/{}".format(
    info["user"],
    info["password"],
    info["host"],
    info["database"],
)
db = SQLAlchemy(app)


class Schueler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(80))
    nachname = db.Column(db.String(80))
    beruf = db.Column(db.String(80))
    firma = db.Column(db.String(80))
    ausbilder = db.Column(db.String(80))

    def schueler_from_request(request):
        return Schueler(
        vorname=request.form["vorname"],
        nachname=request.form["nachname"],
        beruf=request.form["beruf"],
        firma=request.form["firma"],
        ausbilder=request.form["ausbilder"],
        )

    def to_json(self):
        return {
    "id":self.id,
    "vorname":self.vorname,
    "nachname":self.nachname,
    "beruf":self.beruf,
    "firma":self.firma,
    "ausbilder":self.ausbilder,
    }

    def __repr__(self):
        return "<Schüler %r %r>" % (self.vorname, self.nachname)


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/anmelden", methods=["POST"])
def anmelden():
    if request.method == "POST":
        add_schueler(request)
        flash("Schüler angemeldet")
    return redirect(url_for("index"))


@app.route("/löschen", methods=["POST"])
def loeschen():
    if request.method == "POST":
        delete_schueler(request.form["id"])
        flash("Schüler gelöscht")
    return redirect(url_for("index"))


@app.route("/schueler", methods=["GET"])
def schueler_anzeigen():
    data = Schueler.query.all()
    return render_template("liste.html", data=data)


@app.route("/api")
def api_anzeigen():
    return render_template("api.html")


@app.route("/api/schueler/", methods=["GET"])
def get_schueler_liste():
    if request.method == "GET":
        schueler = get_all_schueler()
        return json.dumps(schueler)


@app.route("/api/schueler/<id>", methods=["GET", "DELETE"])
def get_schueler_by_id(id):
    if request.method == "GET":
        return get_schueler(id)
    if request.method == "DELETE":
        return delete_schueler(id)


def get_all_schueler():
    schueler = []
    for row in Schueler.query.all():
        schueler.append(row.to_json())
    return schueler


def get_schueler(id):
    schueler = Schueler.query.get_or_404(id)
    return json.dumps(schueler.to_json())


def add_schueler(request):
    schueler = Schueler.schueler_from_request(request)
    db.session.add(schueler)
    db.session.commit()


def delete_schueler(id):
    schueler = Schueler.query.get_or_404(id)
    db.session.delete(schueler)
    db.session.commit()

if __name__ == '__main__':
    app.run()
