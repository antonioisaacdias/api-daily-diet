from flask import Flask
from database import db
from models.user import User
from routes.auth import auth_bp
from routes.user import user_bp
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



if __name__ == '__main__':
    app.run(debug=True)

