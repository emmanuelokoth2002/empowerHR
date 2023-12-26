from flask import Blueprint, request, jsonify
from db import Database

suggestions_bp = Blueprint('suggestions', __name__)

class suggestion:
    def __init__(self,suggestionid,employeeid,description,status):
        self.suggestionid = suggestionid
        self.employeeid = employeeid
        self.description = description
        self.status = status

@suggestions_bp.route('/savesuggestion', methods=['POST'])
def add_suggestion():
    data = request.json
    suggestionid = data.get('suggestionid')
    employeeid = data.get('employeeid')
    description = data.get('description')
    status = data.get('status')

    if suggestionid is None or not employeeid or not description or not status:
        return jsonify({'error': 'All fields (suggestionid, employeeid, description, status) are required'}), 400

    try:
        db = Database()
        query = "call sp_savesuggestion(%s, %s, %s, %s)"
        args = (suggestionid, employeeid, description, status)
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
            'suggestionid',
            'employeeid',
            'description',
            'status'
        ]

        suggestions_list = []
        for suggestion_data in suggestions_data:
            suggestion_info = dict(zip(field_names, suggestion_data))
            suggestions_list.append(suggestion_info)

        return jsonify(suggestions_list), 200

    except Exception as e:
        print("Error fetching suggestions:", str(e))
        return jsonify({'error': 'An error occurred while fetching suggestions'}), 500

@suggestions_bp.route('/deletesuggestion/<int:suggestion_id>', methods=['POST'])
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
