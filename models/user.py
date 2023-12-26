from flask import Blueprint, request, jsonify
from db import Database

users_bp = Blueprint('users', __name__)

class user:
    def __init__(self,userid,employeeid,username,password,email):
        self.userid = userid
        self.employeeid = employeeid
        self.username = username
        self.password = password
        self.email = email

@users_bp.route('/saveuser', methods=['POST'])
def add_user():
    data = request.json
    userid = data.get('userid')
    employeeid = data.get('employeeid')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if userid is None or not username or not password or not email or not employeeid:
        return jsonify({'error': 'All fields (userid, employeeid, username, password, email) are required'}), 400

    try:
        db = Database()
        query = "call sp_saveuser(%s, %s, %s, %s, %s)"
        args = (userid, employeeid, username, password, email)
        db.execute_query(query, args)

        print("User saved successfully")

        return jsonify({'message': 'User saved successfully'}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

@users_bp.route('/getusers', methods=['GET'])
def get_users():
    try:
        db = Database()
        query = "sp_getusers"

        users_data = db.get_data(query, multi=True)

        field_names = [
            'userid',
            'employeeid',
            'username',
            'password',
            'email'
        ]

        users_list = []
        for user_data in users_data:
            user_info = dict(zip(field_names, user_data))
            users_list.append(user_info)

        return jsonify(users_list), 200

    except Exception as e:
        print("Error fetching users:", str(e))
        return jsonify({'error': 'An error occurred while fetching users'}), 500

@users_bp.route('/getuser/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        db = Database()
        query = "call sp_getuser(%s)"
        args = (user_id,)
        user_data = db.get_data(query, args)

        if user_data:
            field_names = ['user_id', 'username', 'email']
            user_info = dict(zip(field_names, user_data[0]))
            return jsonify(user_info), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print("Error fetching user:", str(e))
        return jsonify({'error': 'An error occurred while fetching user'}), 500

@users_bp.route('/deleteuser/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        db = Database()
        query = "call sp_deleteuser(%s)"
        args = (user_id,)
        db.execute_query(query, args)

        print("User deleted successfully")

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500
