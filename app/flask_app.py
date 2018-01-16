from flask import Flask, render_template, flash, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import json
import random

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
db = SQLAlchemy(app)

class Firma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    ausbilder = db.relationship("Ausbilder", backref="firma", lazy=True)

    def to_json(self):
        return {
    "id":self.id,
    "name":self.name,
    }
    
    def __str__(self):
        return self.name
    
class Ausbilder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    firma_id = db.Column(db.Integer, db.ForeignKey("firma.id"))
    schueler = db.relationship("Schueler", backref="ausbilder", lazy=True)

    def to_json(self):
        return {
    "id":self.id,
    "name":self.name,
    "firma_id":self.firma_id,
    }
    
    def __str__(self):
        return self.name

class Klasse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lehrer = db.Column(db.String(80))
    schueler = db.relationship("Schueler", backref="klasse", lazy=True)

    def to_json(self):
        return {
    "id":self.id,
    "name":self.name,
    "lehrer":self.lehrer,
    }
    
    def __str__(self):
        return self.name

class Schueler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(80), nullable=False)
    nachname = db.Column(db.String(80), nullable=False)
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


@app.route("/fuegeklassehinzu", methods=["POST"])
def klasse_hinzufuegen():
    if request.method == "POST":
        add_klasse(request.form["name"], request.form["lehrer"])
        flash("Klasse hinzugefügt")
    return redirect(url_for("index"))


@app.route("/schueler", methods=["GET"])
def schueler_anzeigen():
    data = Schueler.query.all()
    return render_template("schueler.html", data=data)


@app.route("/klassen", methods=["GET"])
def klassen_anzeigen():
	data = Klasse.query.all()
	return render_template("klassen.html", data=data)


@app.route("/api")
def api_anzeigen():
    return render_template("api.html")


@app.route("/api/schueler/", methods=["GET"])
def get_schueler_liste():
    if request.method=="GET":
        return json.dumps(get_schueler())


@app.route("/api/ausbilder/", methods=["GET"])
def get_ausbilder_liste():
    if request.method=="GET":
        return json.dumps(get_ausbilder())


@app.route("/api/firmen/", methods=["GET"])
def get_firmen_liste():
    if request.method=="GET":
        return json.dumps(get_firmen())


@app.route("/api/klassen/", methods=["GET"])
def get_klassen_liste():
    if request.method=="GET":
        return json.dumps(get_klassen())


def query_to_json(query):
    json_query = []
    for row in query:
        json_query.append(row.to_json())
    return json_query


def get_schueler():
    return query_to_json(Schueler.query.all())


def get_ausbilder():
    return query_to_json(Ausbilder.query.all())


def get_firmen():
    return query_to_json(Firma.query.all())


def get_klassen():
    return query_to_json(Klasse.query.all())

 
def add_to_db(request):
    add_firma(request.form["firma"])
    add_ausbilder(request.form["ausbilder"],request.form["firma"])
    k = random.randrange(1, len(Klasse.query.all()), 1)
    add_schueler(request.form["vorname"],request.form["nachname"],request.form["firma"],request.form["ausbilder"],k)
    db.session.commit()


def add_firma(name):
    if Firma.query.filter_by(name=name).first():
        return
    f=Firma(name=name)
    db.session.add(f)    
    db.session.commit()


def add_ausbilder(name, firma):
    f = Firma.query.filter_by(name=firma).first()
    if Ausbilder.query.filter_by(name=name,firma_id=f.id).first():
        return
    ausbilder=Ausbilder(name=name,firma_id=f.id)
    db.session.add(ausbilder)
    db.session.commit()


def add_schueler(vorname, nachname, firma, ausbilder, klasse):
    f=Firma.query.filter_by(name=firma).first()
    a=Ausbilder.query.filter_by(name=ausbilder,firma_id=f.id).first()
    s=Schueler(vorname=vorname,nachname=nachname,ausbilder_id=a.id,klasse_id=klasse)
    db.session.add(s)
    db.session.commit()


def delete_schueler(id):
    schueler = Schueler.query.get_or_404(id)
    db.session.delete(schueler)
    db.session.commit()


def add_klasse(name, lehrer):
    if Klasse.query.filter_by(name=name).first():
        return
    k = Klasse(name=name, lehrer=lehrer)
    db.session.add(k)
    db.session.commit()

if __name__ == '__main__':
    app.run()
