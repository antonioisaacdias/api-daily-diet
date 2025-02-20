from database import db
from uuid import uuid4

class Diet(db.Model):
    __tablename__ = 'diets'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    is_healthy = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='diets')

