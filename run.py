from app import create_app
from app.services.db import DBManager
from os import urandom, environ

app = create_app()
app.secret_key = urandom(24)

if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    DBManager().check_coherence()
    app.run(host='0.0.0.0', port=port , debug= True)
