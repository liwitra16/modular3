from flask import Flask
from controllers.routes import main as main_blueprint

app = Flask(__name__)
app.secret_key = 'khanza22'  # Ganti dengan secret key yang lebih aman

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
