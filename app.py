from flask import Flask, request, jsonify
from database import db
from models.diet import Diet
from models.user import User
from config import Config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import bcrypt

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
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

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    
    return jsonify({'message': 'Credenciais inválidas'}), 400

@app.route('/user/<string:user_id>', methods=['PATCH'])
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

@app.route('/user/<string:user_id>', methods=['DELETE'])
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

@


if __name__ == '__main__':
    app.run(debug=True)

