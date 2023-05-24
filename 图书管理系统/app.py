from flask import Flask
from flask_cors import CORS
from users import users
from admin import admin
from profile import profile


app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(admin)
app.register_blueprint(profile)
CORS(app, origins=['http://localhost:8080'])


if __name__ == '__main__':
    print(app.url_map)
    app.run()
