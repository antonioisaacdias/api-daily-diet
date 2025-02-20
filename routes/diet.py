from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from datetime import datetime
from models.diet import Diet
from models.user import User

diet_bp = Blueprint('diet', __name__)

@login_required
@diet_bp.route('/diet', methods=['POST'])
def create_diet():
    data = request.json

    name = data.get('name')
    description = data.get('description')
    date_time = datetime.fromisoformat(data.get('date_time').replace("Z", "+00:00"))
    is_healthy = data.get('is_healthy')

    if name and description and date_time and is_healthy:
        diet = Diet(name=name, description=description, date_time=date_time, is_healthy=is_healthy, user_id=current_user.id)
        db.session.add(diet)
        db.session.commit()
        return jsonify({'message': 'Dieta registrada com sucesso'}), 201

    return jsonify({'message': 'Dados incompletos'}), 400

@login_required
@diet_bp.route('/diet', methods=['GET'])
def list_diets():
    diets = Diet.query.filter_by(user_id=current_user.id).all()
    
    dictionary = []
    for diet in diets:
        dictionary.append(diet.to_dict())
    return jsonify({'dietas': dictionary, 'quantidade de registros': len(dictionary)})