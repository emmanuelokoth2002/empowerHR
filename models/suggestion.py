from flask import Blueprint, request, jsonify
from db import Database

suggestions_bp = Blueprint('suggestions', __name__)

@suggestions_bp.route('/savesuggestion', methods=['POST'])
def add_suggestion():
    data = request.json
    suggestion_id = data.get('suggestion_id')
    employee_id = data.get('employee_id')
    suggestion_text = data.get('suggestion_text')

    if suggestion_id is None or not employee_id or not suggestion_text:
        return jsonify({'error': 'All fields (suggestion_id, employee_id, suggestion_text) are required'}), 400

    try:
        db = Database()
        query = "call sp_savesuggestion(%s, %s, %s)"
        args = (suggestion_id, employee_id, suggestion_text)
        db.execute_query(query, args)

        print("Suggestion saved successfully")

        return jsonify({'message': 'Suggestion saved successfully'}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

@suggestions_bp.route('/getsuggestions', methods=['GET'])
def get_suggestions():
    try:
        db = Database()
        query = "sp_getsuggestions"

        suggestions_data = db.get_data(query, multi=True)

        field_names = [
            'suggestion_id',
            'employee_id',
            'suggestion_text'
        ]

        suggestions_list = []
        for suggestion_data in suggestions_data:
            suggestion_info = dict(zip(field_names, suggestion_data))
            suggestions_list.append(suggestion_info)

        return jsonify(suggestions_list), 200

    except Exception as e:
        print("Error fetching suggestions:", str(e))
        return jsonify({'error': 'An error occurred while fetching suggestions'}), 500

@suggestions_bp.route('/deletesuggestion/<int:suggestion_id>', methods=['DELETE'])
def delete_suggestion(suggestion_id):
    try:
        db = Database()
        query = "call sp_deletesuggestion(%s)"
        args = (suggestion_id,)
        db.execute_query(query, args)

        print("Suggestion deleted successfully")

        return jsonify({'message': 'Suggestion deleted successfully'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500
