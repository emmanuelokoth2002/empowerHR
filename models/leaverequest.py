from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import Database

leaverequests_bp = Blueprint('leaverequests', __name__)

class LeaveRequest:
    def __init__(self, leaverequestid, employeeid, leavetype, startdate, enddate, reason, status):
        self.leaverequestid = leaverequestid
        self.employeeid = employeeid
        self.leavetype = leavetype
        self.startdate = startdate
        self.enddate = enddate
        self.reason = reason
        self.status = status

    @leaverequests_bp.route('/saveleaverequest', methods=['POST'])
    @jwt_required()
    def save_leave_request():
        data = request.json
        leaverequestid = data.get('leaverequestid')
        employeeid = data.get('employeeid')
        leavetype = data.get('leavetype')
        startdate = data.get('startdate')
        enddate = data.get('enddate')
        reason = data.get('reason')
        status = data.get('status')

        if leaverequestid is None or not employeeid or not leavetype or not startdate or not enddate or not reason:
            return jsonify({'error': 'All fields (leaveid, employeeid, leavetype, startdate, enddate, reason) are required'}), 400

        try:
            db = Database()
            query = "call sp_saveleaverequest(%s, %s, %s, %s, %s, %s, %s)"
            args = (leaverequestid, employeeid, leavetype, startdate, enddate, reason, status)
            db.execute_query(query, args)

            print("Leave request saved successfully")

            return jsonify({'message': 'Leave request saved successfully'}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    @leaverequests_bp.route('/getleaverequests', methods=['GET'])
    @jwt_required()
    def get_leave_requests():
        try:
            db = Database()
            query = "sp_getleaverequests"

            leaverequests_data = db.get_data(query, multi=True)

            field_names = [
                'leaverequestid',
                'employeeid',
                'leavetype',
                'startdate',
                'enddate',
                'reason',
                'status'
            ]

            leaverequests_list = []
            for leaverequest_data in leaverequests_data:
                leaverequest_info = dict(zip(field_names, leaverequest_data))
                leaverequests_list.append(leaverequest_info)

            return jsonify(leaverequests_list), 200

        except Exception as e:
            print("Error fetching leave requests:", str(e))
            return jsonify({'error': 'An error occurred while fetching leave requests'}), 500
        
    @leaverequests_bp.route('/deleteleaverequest/<int:leaverequestid>', methods=['POST'])
    @jwt_required()
    def delete_leave_request(leaverequestid):
        try:
            db = Database()
            query = "call sp_deleteleaverequest(%s)"
            args = (leaverequestid,)
            db.execute_query(query, args)

            print("Leave request deleted successfully")

            return jsonify({'message': 'Leave request deleted successfully'}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500
