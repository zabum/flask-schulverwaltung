## Flask-Schulverwaltung

Flask-App zum Anmelden von Schülern (https://zabum.pythonanywhere.com)

## Vorraussetzungen

- Python3 (https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe)
- MySQL-Server (https://dev.mysql.com/downloads/mysql/)

### Datenbank erstellen

- MySQL-Server installieren, Benutzername und Passwort aufschreiben (brauchen wir später)
- Terminal in ```C:\Program Files\MySQL\MySQL Server 5.7\bin``` öffnen
- Folgenden Befehl (ohne Klammern) eingeben ```mysql -u [Benutzername] -p [Passwort]```
- Datenbank erstellen ```CREATE DATABASE schule;``` die Tabellen werden später automatisch angelegt

## Setup

1. Repository runterladen oder klonen ```git clone https://github.com/zabum/flask-schulverwaltung.git```

2. "config.cfg" aus dem "app"-Verzeichnis mit einem Texteditor öffnen, die Datenbank-Infos (ohne Klammern) eingeben und speichern
```SQLALCHEMY_DATABASE_URI="mysql://[Benutzername]:[Passwort]@localhost/schule"```

3. Terminal in ```flask-schulverwaltung``` öffnen und Pakete installieren ```pip install -r requirements.txt```

Falls es Fehler geben sollte, Pakete über folgende Befehle nachinstallieren
```pip install [Paketname]```
oder
```easy_install [Paketname]``` 

4. Terminal sagen welche Datei ausgeführt werden soll:
- cmd:```set FLASK_APP=app\flask_app.py```
- powershell:```$env:FLASK_APP="app\flask_app.py"```

4b. Debugmodus aktivieren:
- cmd:```set FLASK_DEBUG=1```

5. App starten ```flask run```
6. http://127.0.0.1:5000  im Browser öffnen
