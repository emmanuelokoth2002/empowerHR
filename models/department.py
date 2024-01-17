from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import Database

departments_bp = Blueprint('departments', __name__)

class Department:
    def __init__(self, departmentid, departmentname):
        self.departmentid = departmentid
        self.departmentname = departmentname

    @departments_bp.route('/savedepartment', methods=['POST'])
    @jwt_required()
    def add_department():
        data = request.json
        departmentid = data.get('departmentid')
        departmentname = data.get('departmentname')

        if departmentid is None or not departmentname:
            return jsonify({'error': 'All fields (departmentid, departmentname) are required'}), 400

        try:
            db = Database()
            query = "call sp_savedepartment(%s, %s)"
            args = (departmentid, departmentname)
            db.execute_query(query, args)

            print("Department saved successfully")

            return jsonify({'message': 'Department saved successfully'}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    @departments_bp.route('/getdepartments', methods=['GET'])
    @jwt_required()
    def get_departments():
        try:
            db = Database()

            query = "sp_getdepartments"

            departments_data = db.get_data(query, multi=True)

            field_names = [
                'departmentid',
                'departmentname'
            ]

            departments_list = []
            for department_data in departments_data:
                department_info = dict(zip(field_names, department_data))
                departments_list.append(department_info)

            return jsonify(departments_list), 200

        except Exception as e:
            print("Error fetching departments:", str(e))
            return jsonify({'error': 'An error occurred while fetching departments'}), 500

    @departments_bp.route('/deletedepartment/<int:departmentid>', methods=['POST'])
    @jwt_required()
    def delete_department(departmentid):
        try:
            db = Database()
            query = "call sp_deletedepartment(%s)"
            args = (departmentid,)
            db.execute_query(query, args)

            print("Department deleted successfully")

            return jsonify({'message': 'Department deleted successfully'}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500
