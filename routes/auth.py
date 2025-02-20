from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from models.user import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            return jsonify({'message': 'Logado com sucesso'}), 200

    return jsonify({'message': 'Cedenciais inválidas'}), 400

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'})