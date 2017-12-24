from flask import Flask, render_template, flash, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
db = SQLAlchemy(app)

class Firma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    ausbilder = db.relationship("Ausbilder", backref="firma", lazy=True)

    def get_by_name():
        pass

    def firma_from_request(request):
        return Firma(
            name = request.form["firma"],
            )

class Ausbilder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    firma_id = db.Column(db.Integer, db.ForeignKey("firma.id"))
    schueler = db.relationship("Schueler", backref="ausbilder", lazy=True)

    def get_by_name():
        pass

    def ausbilder_from_request(request):
        firma = Firma.query.filter_by(name = request.form["firma"]).first()
        return Ausbilder(
            name = request.form["ausbilder"],
            firma_id = firma.id
            )

class Klasse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    lehrer = db.Column(db.String(80))
    schueler = db.relationship("Schueler", backref="klasse", lazy=True)

class Schueler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(80))
    nachname = db.Column(db.String(80))
    ausbilder_id = db.Column(db.Integer, db.ForeignKey("ausbilder.id"))
    klasse_id = db.Column(db.Integer, db.ForeignKey("klasse.id"))

    def schueler_from_request(request):
        ausbilder = Ausbilder.query.filter_by(name=request.form["ausbilder"]).first()
        return Schueler(
        vorname=request.form["vorname"],
        nachname=request.form["nachname"],
        ausbilder_id=ausbilder.id,
        klasse_id=request.form["klasse_id"],
        )

    def to_json(self):
        return {
    "id":self.id,
    "vorname":self.vorname,
    "nachname":self.nachname,
    "ausbilder_id":self.ausbilder_id,
    "klasse_id":self.klasse_id,
    }

    def __repr__(self):
        return "<Schüler %r %r>" % (self.vorname, self.nachname)


@app.route("/index")
@app.route("/")
def index():
    db.create_all()
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
    firma = Firma.firma_from_request(request)
    db.session.add(firma)
    ausbilder = Ausbilder.ausbilder_from_request(request)
    db.session.add(ausbilder)
    schueler = Schueler.schueler_from_request(request)
    db.session.add(schueler)
    db.session.commit()


def delete_schueler(id):
    schueler = Schueler.query.get_or_404(id)
    db.session.delete(schueler)
    db.session.commit()


if __name__ == '__main__':
    app.run()
