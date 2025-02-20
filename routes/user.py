from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models.user import User
import bcrypt

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['POST'])
def create_user():

    data = request.json
    username = data.get('username')
    password = data.get('password')
    already_exists = User.query.filter_by(username=username).first()

    if already_exists:
        return jsonify({'message': 'Esse nome de usuário já está em utilização'}), 400

    if username and password:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    
    return jsonify({'message': 'Credenciais inválidas'}), 400

@user_bp.route('/user/<string:user_id>', methods=['PATCH'])
@login_required
def update_user(user_id):
    
    data = request.json
    password = data.get('password')
    user = User.query.get(user_id)

    if not password:
        return jsonify({'message': 'Senha não pode ser vazia'}), 400

    if user is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    if current_user.id != user.id and current_user.role != 'admin':
        return jsonify({'message': 'Operação não autorizada'}), 403

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed_password
    db.session.commit()

    return jsonify({'message': f'Usuário {user_id} atualizado com sucesso'}), 200

@user_bp.route('/user/<string:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    if user_id != current_user.id and current_user.role == 'admin':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user_id} deletado com sucesso"})
    
    return jsonify({'message': 'Operação não autorizada'}), 403