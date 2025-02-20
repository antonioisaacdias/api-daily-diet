from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from datetime import datetime
from models.diet import Diet
from models.user import User

diet_bp = Blueprint('diet', __name__)


@diet_bp.route('/diet', methods=['POST'])
@login_required
def create_diet():
    data = request.json

    name = data.get('name')
    description = data.get('description')
    date_time_str = data.get('date_time')
    is_healthy = data.get('is_healthy')

    if name and description and date_time_str and is_healthy:

        try:
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Utilize YYYY-MM-DDTHH:MM:SS'}), 400

        diet = Diet(name=name, description=description, date_time=date_time_obj, is_healthy=is_healthy, user_id=current_user.id)
        db.session.add(diet)
        db.session.commit()
        return jsonify({'message': 'Dieta registrada com sucesso'}), 201

    return jsonify({'message': 'Dados incompletos'}), 400


@diet_bp.route('/diet', methods=['GET'])
@login_required
def list_diets():
    diets = Diet.query.filter_by(user_id=current_user.id).all()
    
    dictionary = []
    for diet in diets:
        dictionary.append(diet.to_dict())
    return jsonify({'dietas': dictionary, 'quantidade de registros': len(dictionary)}), 200


@diet_bp.route('/diet/<string:diet_id>', methods=['GET'])
@login_required
def fetch_diet(diet_id):
    diet = Diet.query.get(diet_id)
    
    if diet:    
        if diet.user_id != current_user.id and current_user.role != 'admin':
            return jsonify({'message': 'Consulta não autorizada.'}), 403
        
        return jsonify(diet.to_dict()), 200
    
    return jsonify({'message': 'Dieta não encontrada'}), 404


@diet_bp.route('/diet/<string:diet_id>', methods=['PATCH'])
@login_required
def update_diet(diet_id):

    diet = Diet.query.get(diet_id)
    data = request.json
    name = data.get('name')
    description = data.get('description')
    date_time_str = data.get('date_time')
    is_healthy = data.get('is_healthy')

    if diet:    
        if diet.user_id != current_user.id and current_user.role != 'admin':
            return jsonify({'message': 'Consulta não autorizada.'}), 403
        
        if 'date_time' in data:
            try:
                date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                return jsonify({'message': 'Formato de data inválido. Utilize YYYY-MM-DDTHH:MM:SS'}), 400
        
        if name:
            diet.name = name
        if description:
            diet.description = description
        if is_healthy is not None:
            diet.is_healthy = is_healthy
        diet.date_time = date_time_obj
        db.session.commit()
        return jsonify({'message': 'Dieta atualizada com sucesso'}), 200
    
    return jsonify({'message': 'Dieta não encontrada'}), 404

@diet_bp.route('/diet/<string:diet_id>', methods=['DELETE'])
@login_required
def delete_diet(diet_id):
    diet = Diet.query.get(diet_id)

    if diet:
        if diet.user_id != current_user.id and current_user.role != 'admin':
            return jsonify({'message': 'Deleção não autorizada.'}), 403
        
        db.session.delete(diet)
        db.session.commit()
        return jsonify({'message': 'Dieta excluída com sucesso'}), 200

    return jsonify({'message': 'Dieta não encontrada'}), 404