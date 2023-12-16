from flask import Blueprint, request, jsonify
from db import Database

complaints_bp = Blueprint('complaints', __name__)

class Complaint:
    def __init__(self, complaintid, employeeid, type, description, status):
        self.complaintid = complaintid
        self.employeeid = employeeid
        self.type = type
        self.description = description
        self.status = status

@complaints_bp.route('/savecomplaint', methods=['POST'])
def add_complaint():
    data = request.json
    complaintid=data.get('complaintid')
    employeeid = data.get('employeeid')
    type = data.get('type')
    description = data.get('description')
    status = data.get('status')
    
    if complaintid is None or not employeeid or not type or not description or not status:
        return jsonify({'error': 'All fields (complaintid, employeeid, type, description, status) are required'}), 400


    try:
        db = Database()
        query = "call sp_savecomplaint(%s, %s, %s, %s, %s)"
        args = (complaintid, employeeid, type, description, status)
        db.execute_query(query, args)


        print("Complaint saved successfully")

        return jsonify({'message': 'Complaint saved successfully'}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

@complaints_bp.route('/getcomplaints', methods=['GET'])
def get_complaints():
    try:
        db = Database()

        query = "sp_getcomplaints"

        complaints_data = db.get_data(query, multi=True)

        field_names = [
            'complaint_id',
            'employee_id',
            'department',
            'issue',
            'status',
            'created_at',
            'deleted',
            'deleted_at'
        ]

        complaints_list = []
        for complaint_data in complaints_data:
            complaint_info = dict(zip(field_names, complaint_data))
            complaints_list.append(complaint_info)

        return jsonify(complaints_list), 200

    except Exception as e:
        print("Error fetching complaints:", str(e))
        return jsonify({'error': 'An error occurred while fetching complaints'}), 500


@complaints_bp.route('/deletecomplaint/<int:complaintid>', methods=['POST'])
def delete_complaint(complaintid):
    try:
        db = Database()
        query = "call sp_deletecomplaint(%s)"
        args = (complaintid,)
        db.execute_query(query, args)

        print("Complaint deleted successfully")

        return jsonify({'message': 'Complaint deleted successfully'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500


