from app import create_app
from os import urandom

app = create_app()
app.secret_key = urandom(24)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug= True)
