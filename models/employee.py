from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import Database

employees_bp = Blueprint('employees', __name__)

class Employee:
    def __init__(self,employeeid,firstname,lastname,email,dateofbirth,phonenumber,address,departmentid,roleid):
        self.employee_id = employeeid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.dateofbirth = dateofbirth
        self.phonenumber = phonenumber
        self.address = address
        self.departmentid = departmentid
        self.roleid = roleid

    @employees_bp.route('/saveemployee', methods=['POST'])
    @jwt_required()
    def add_employee():
        data = request.json
        employeeid = data.get('employeeid')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        dateofbirth = data.get('dateofbirth')
        phonenumber = data.get('phonenumber')
        address = data.get('address')
        departmentid = data.get('departmentid')
        roleid = data.get('roleid')

        if employeeid is None or not firstname or not lastname or not email or not dateofbirth or not phonenumber or not address or not departmentid or not roleid:
            return jsonify({'error': 'All fields (employeeid, firstname, lastname, email, dateofbirth, address department_id, roleid) are required'}), 400

        try:
            db = Database()
            query = "call sp_saveemployee(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            args = (employeeid, firstname, lastname, email, dateofbirth, phonenumber, address, departmentid, roleid)
            db.execute_query(query, args)

            print("Employee saved successfully")

            return jsonify({'message': 'Employee saved successfully'}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    @employees_bp.route('/getemployees', methods=['GET'])
    @jwt_required()
    def get_employees():
        try:
            db = Database()

            query = "sp_getemployee"

            employees_data = db.get_data(query, multi=True)

            field_names = [
                'employeeid',
                'firstname',
                'lastname',
                'email',
                'dateofbirth',
                'phonenumber',
                'address',
                'hiredate',
                'departmentid',
                'roleid',
                'deleted',
                'datedeleted'
            ]

            employees_list = []
            for employee_data in employees_data:
                employee_info = dict(zip(field_names, employee_data))
                employees_list.append(employee_info)

            return jsonify(employees_list), 200

        except Exception as e:
            print("Error fetching employees:", str(e))
            return jsonify({'error': 'An error occurred while fetching employees'}), 500

    @employees_bp.route('/deleteemployee/<int:employee_id>', methods=['POST'])
    @jwt_required()
    def delete_employee(employee_id):
        try:
            db = Database()
            query = "call sp_deleteemployee(%s)"
            args = (employee_id,)
            db.execute_query(query, args)

            print("Employee deleted successfully")

            return jsonify({'message': 'Employee deleted successfully'}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500
