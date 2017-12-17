## flask-schulverwaltung

Flask-App zum Anmelden von Schülern (https://zabum.pythonanywhere.com)

## Vorraussetzungen

- Python3 (https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe)
- MySQL-Server (https://dev.mysql.com/downloads/mysql/)

### Datenbank erstellen

- MySQL-Server installieren
- Terminal in ```C:\Program Files\MySQL\MySQL Server 5.7\bin``` öffnen
- Folgenden Befehl eingeben ```mysql - u [Benutzername] -p```, falls bei der Installation ein Passwort eigegeben wurde 
- Datenbank erstellen ```CREATE DATABASE [Datenbankname];``` die Tabellen werden später automatisch angelegt

## Setup

- Repository runterladen oder klonen ```git clone https://github.com/zabum/flask-schulverwaltung.git```
- Terminal in ```flask-schulverwaltung``` öffnen und Pakete installieren ```pip install -r requirements.txt```

- Terminal sagen welche Datei ausgeführt werden soll:
- cmd:```set FLASK_APP=app\flask_app.py```
- powershell:```$env:FLASK_APP="app\flask_app.py"```

- App starten ```flask run```
- http://127.0.0.1:5000  im Browser öffnen
