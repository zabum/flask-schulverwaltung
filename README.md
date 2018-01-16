## Flask-Schulverwaltung

Flask-App zum Anmelden von Schülern (https://zabum.pythonanywhere.com)

## Vorraussetzungen

- Python3 (https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe)
- MySQL-Server (https://dev.mysql.com/downloads/mysql/)

### Datenbank erstellen

- ```mysql -u [Benutzername] -p [Passwort]```
- ```CREATE DATABASE schule;```

## Setup

1. ```git clone https://github.com/zabum/flask-schulverwaltung.git```

2. ```SQLALCHEMY_DATABASE_URI="mysql://[Benutzername]:[Passwort]@localhost/schule"```

3. ```pip install -r requirements.txt```

4. 
- cmd:```set FLASK_APP=app\flask_app.py```
- cmd:```set FLASK_DEBUG=1```

- powershell:```$env:FLASK_APP="app\flask_app.py"```
- powershell:```$env:FLASK_DEBUG=1```

5. ```flask run```
6. http://127.0.0.1:5000  im Browser öffnen
