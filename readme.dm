
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
python app.py

dann sieht ihr alles unter 0.0.0.0:5000


# Migrate every time i add some new properties
flask db init
flask db migrate -m "da schreibe ich meine nachrichten"
flask db upgrade