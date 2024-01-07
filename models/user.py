from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from db import Database
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

class user:
    def __init__(self, userid, roleid, username, passwordhash, email):
        self.userid = userid
        self.roleid = roleid
        self.username = username
        self.password_hash = generate_password_hash(passwordhash)
        self.email = email

    def authenticate(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def from_dict(cls, user_data):
        return cls(
            userid=user_data.get('userid'),
            roleid=user_data.get('roleid'),
            username=user_data.get('username'),
            passwordhash=user_data.get('passwordhash'),
            email=user_data.get('email')
        )
        
    @users_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('passwordhash')

        if not username or not password:
            return jsonify({'error': 'Both username and password are required'}), 400

        try:
            db = Database()
            query = "sp_getuserbyusername"
            args = (username,)
            user_data = db.get_data(query, args)
            print(user_data)

            if user_data:
                user_info = dict(zip(['userid', 'roleid', 'username', 'passwordhash', 'email'], user_data[0]))
                user_obj = user.from_dict(user_info)

                if user_obj.authenticate(password):
                    response_data = {
                    'message': 'Login successful',
                    'roleid': user_obj.roleid,
                    'access_token': create_access_token(identity=user_obj.username)
                    }
                    return jsonify(response_data), 200
                else:
                    return jsonify({'error': 'Invalid username or password'}), 401
            else:
                return jsonify({'error': 'User not found'}), 404

        except Exception as e:
            print("Error during login:", str(e))
            return jsonify({'error': 'An error occurred during login'}), 500
    
    @users_bp.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp


    @users_bp.route('/saveuser', methods=['POST'])
    def add_user():
        data = request.json
        userid = data.get('userid')
        roleid = data.get('roleid')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if userid is None or not username or not password or not email or not roleid:
            return jsonify({'error': 'All fields (userid, employeeid, username, password, email) are required'}), 400

        try:
            db = Database()
            query = "call sp_saveuser(%s, %s, %s, %s, %s)"
            args = (userid, roleid, username, password, email)
            db.execute_query(query, args)

            print("User saved successfully")

            return jsonify({'message': 'User saved successfully'}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    @users_bp.route('/getusers', methods=['GET'])
    @jwt_required()
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
    @jwt_required()
    def delete_user(user_id):
        current_user = get_jwt_identity()
        if 'admin' not in current_user['roles']:
             return jsonify({'error': 'Unauthorized'}), 401
        
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