from flask import Blueprint, jsonify, request
from db import Database

notifications_bp = Blueprint('notifications', __name__)

class Notification:
    def __init__(self, notificationid, title, body, addedby, recipient):
        self.notificationid = notificationid
        self.title = title
        self.body = body
        self.addedby = addedby
        self.recipient = recipient

@notifications_bp.route('/savenotification', methods=['POST'])
def save_notification():
    data = request.json
    notificationid = data.get('notificationid')
    title = data.get('title')
    body = data.get('body')
    addedby = data.get('addedby')
    recipient = data.get('recipient')

    if notificationid is None or not title or not body or not addedby or recipient is None:
        return jsonify({'error': 'All fields (notificationid, title, body, addedby, recipient) are required'}), 400

    try:
        db = Database()
        query = "call sp_savenotification(%s, %s, %s, %s, %s)"
        args = (notificationid, title, body, addedby, recipient)
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
            'notificationid',
            'title',
            'body',
            'addedby',
            'recipient',
            'dateadded',
            'deleted',
            'datedeleted'
        ]

        notifications_list = []
        for notification_data in notifications_data:
            notification_info = dict(zip(field_names, notification_data))
            notifications_list.append(notification_info)

        return jsonify(notifications_list), 200

    except Exception as e:
        print("Error fetching notifications:", str(e))
        return jsonify({'error': 'An error occurred while fetching notifications'}), 500


@notifications_bp.route('/deletenotification/<int:notificationid>', methods=['POST'])
def delete_notification(notificationid):
    try:
        db = Database()
        query = "call sp_deletenotification(%s)"
        args = (notificationid,)
        db.execute_query(query, args)

        print("Notification deleted successfully")

        return jsonify({'message': 'Notification deleted successfully'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500