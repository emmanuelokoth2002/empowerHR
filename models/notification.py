from flask import Blueprint, jsonify, request
from db import Database

notifications_bp = Blueprint('notifications', __name__)

class Notification:
    def __init__(self, notificationid, employeeid, notificationtype, message, is_read):
        self.notificationid = notificationid
        self.employeeid = employeeid
        self.notificationtype = notificationtype
        self.message = message
        self.is_read = is_read

@notifications_bp.route('/savenotification', methods=['POST'])
def save_notification():
    data = request.json
    notificationid = data.get('notificationid')
    employeeid = data.get('employeeid')
    notificationtype = data.get('notificationtype')
    message = data.get('message')
    is_read = data.get('is_read')

    if notificationid is None or not employeeid or not notificationtype or not message or is_read is None:
        return jsonify({'error': 'All fields (notificationid, employeeid, notificationtype, message, is_read) are required'}), 400

    try:
        db = Database()
        query = "call sp_savenotification(%s, %s, %s, %s, %s)"
        args = (notificationid, employeeid, notificationtype, message, is_read)
        db.execute_query(query, args)

        print("Notification saved successfully")

        return jsonify({'message': 'Notification saved successfully'}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

@notifications_bp.route('/getnotifications', methods=['GET'])
def get_notifications():
    try:
        db = Database()
        query = "sp_getnotifications"

        notifications_data = db.get_data(query, multi=True)

        field_names = [
            'notification_id',
            'user_id',
            'message',
            'created_at',
            'is_read'
        ]

        notifications_list = []
        for notification_data in notifications_data:
            notification_info = dict(zip(field_names, notification_data))
            notifications_list.append(notification_info)

        return jsonify(notifications_list), 200

    except Exception as e:
        print("Error fetching notifications:", str(e))
        return jsonify({'error': 'An error occurred while fetching notifications'}), 500


@notifications_bp.route('/deletenotification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    try:
        db = Database()
        query = "call sp_deletenotification(%s)"
        args = (notification_id,)
        db.execute_query(query, args)

        print("Notification deleted successfully")

        return jsonify({'message': 'Notification deleted successfully'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500