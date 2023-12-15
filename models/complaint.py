from flask import Blueprint, request, jsonify
from db import Database

complaints_bp = Blueprint('complaints', __name__)

class Complaint:
    def __init__(self, complaint_id, employee_id, complaint_type, description, status):
        self.complaint_id = complaint_id
        self.employee_id = employee_id
        self.complaint_type = complaint_type
        self.description = description
        self.status = status

@complaints_bp.route('/addcomplaints', methods=['POST'])
def add_complaint():
    data = request.json
    employeeid = data.get('employeeid')
    complainttype = data.get('complainttype')
    description = data.get('description')

    if not employeeid or not complainttype or not description:
        return jsonify({'error': 'All fields (employee_id, complaint_type, description) are required'}), 400

    try:
        db = Database()
        query = "sp_savecomplaint"
        args = (employeeid, complainttype, description)
        db.execute_query(query, args)

        print("Complaint added successfully")

        return jsonify({'message': 'Complaint added successfully'}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

@complaints_bp.route('/getcomplaints', methods=['GET'])
def get_complaints():
    try:
        db = Database()
        query = "sp_getcomplaints"
        complaints_data = db.get_data(query, multi=True)

        complaint_list = []
        for complaint in complaints_data:
            complaint_obj = Complaint(
                complaint[0], 
                complaint[1],
                complaint[2],
                complaint[3],
                complaint[4]
            )
            complaint_list.append(complaint_obj.__dict__)

        return jsonify(complaint_list)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

@complaints_bp.route('/deletecomplaints/<int:complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    query = "sp_deletecomplaint"
    args = (complaint_id,)
    db = Database()
    db.execute_query(query, args)

    print("Complaint deleted successfully from database")

    return jsonify({'message': 'Complaint deleted successfully'}), 200