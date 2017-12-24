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

class Ausbilder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    firma_id = db.Column(db.Integer, db.ForeignKey("firma.id"))
    schueler = db.relationship("Schueler", backref="ausbilder", lazy=True)

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
        add_to_db(request)
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


def add_to_db(request):
    add_firma(request.form["firma"])
    add_ausbilder(request.form["ausbilder"],request.form["firma"])
    add_schueler(request.form["vorname"],request.form["nachname"],request.form["firma"],request.form["ausbilder"],1)
    db.session.commit()


def add_firma(name):
    if Firma.query.filter_by(name=name).first():
        return
    firma=Firma(name=name)
    db.session.add(firma)    
    db.session.commit()


def add_ausbilder(name, firma):
    firma = Firma.query.filter_by(name=firma).first()
    if Ausbilder.query.filter_by(name=name,firma_id=firma.id).first():
        return
    ausbilder=Ausbilder(name=name,firma_id=firma.id)
    db.session.add(ausbilder)
    db.session.commit()


def add_schueler(vorname, nachname, firma, ausbilder, klasse):
    f=Firma.query.filter_by(name=firma).first()
    a=Ausbilder.query.filter_by(name=ausbilder,firma_id=f.id).first()
    schueler=Schueler(vorname=vorname,nachname=nachname,ausbilder_id=a.id,klasse_id=klasse)
    db.session.add(schueler)
    db.session.commit()


def delete_schueler(id):
    schueler = Schueler.query.get_or_404(id)
    db.session.delete(schueler)
    db.session.commit()


if __name__ == '__main__':
    app.run()
