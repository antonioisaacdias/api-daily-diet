from flask import Flask
from database import db
from models.diet import Diet
from models.user import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)



if __name__ == '__main__':
    app.run(debug=True)
