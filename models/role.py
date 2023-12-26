from flask import Blueprint, request, jsonify
from db import Database

roles_bp = Blueprint('roles', __name__)

class role:
    def __init__(self,roleid,rolename):
        self.roleid = roleid
        self.rolename = rolename

@roles_bp.route('/saverole', methods=['POST'])
def add_role():
    data = request.json
    roleid = data.get('roleid')
    rolename = data.get('rolename')

    if roleid is None or not rolename:
        return jsonify({'error': 'All fields (role_id, role_name) are required'}), 400

    try:
        db = Database()
        query = "call sp_saverole(%s, %s)"
        args = (roleid, rolename)
        db.execute_query(query, args)

        print("Role saved successfully")

        return jsonify({'message': 'Role saved successfully'}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

@roles_bp.route('/getroles', methods=['GET'])
def get_roles():
    try:
        db = Database()
        query = "sp_getroles"

        roles_data = db.get_data(query, multi=True)

        field_names = [
            'roleid',
            'rolename'
        ]

        roles_list = []
        for role_data in roles_data:
            role_info = dict(zip(field_names, role_data))
            roles_list.append(role_info)

        return jsonify(roles_list), 200

    except Exception as e:
        print("Error fetching roles:", str(e))
        return jsonify({'error': 'An error occurred while fetching roles'}), 500

@roles_bp.route('/deleterole/<int:role_id>', methods=['POST'])
def delete_role(role_id):
    try:
        db = Database()
        query = "call sp_deleterole(%s)"
        args = (role_id,)
        db.execute_query(query, args)

        print("Role deleted successfully")

        return jsonify({'message': 'Role deleted successfully'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500
