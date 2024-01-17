from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit
from db import Database

notifications_bp = Blueprint('notifications', __name__)
socketio = SocketIO()

class Notification:
    def __init__(self, notificationid, title, body, addedby, recipient, dateadded, deleted, datedeleted, read):
        self.notificationid = notificationid
        self.title = title
        self.body = body
        self.addedby = addedby
        self.recipient = recipient
        self.dateadded = dateadded
        self.deleted = deleted
        self.datedeleted = datedeleted
        self.read = read

    @notifications_bp.route('/savenotification', methods=['POST'])
    @jwt_required()
    def save_notification():
        data = request.json
        title = data.get('title')
        body = data.get('body')
        addedby = get_jwt_identity()
        recipient = data.get('recipient')

        if not title or not body or recipient is None:
            return jsonify({'error': 'All fields (title, body, recipient) are required'}), 400

        try:
            db = Database()
            query = "CALL sp_savenotification(%s, %s, %s, %s)"
            args = (title, body, addedby, recipient)
            notificationid = db.execute_query(query, args, fetch_one=True)[0]

            # Notify recipient in real-time
            socketio.emit('new_notification', {'message': 'You have a new notification'}, room=f'user_{recipient}')

            print("Notification saved successfully")

            return jsonify({'message': 'Notification saved successfully', 'notificationid': notificationid}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    @notifications_bp.route('/getnotifications', methods=['GET'])
    @jwt_required()
    def get_notifications():
        try:
            current_user_id = get_jwt_identity()
            page = request.args.get('page', 1, type=int)
            per_page = 10  # Adjust as needed

            db = Database()
            query = "CALL sp_getnotifications_paginated(%s, %s, %s)"
            args = (current_user_id, (page - 1) * per_page, per_page)
            notifications_data = db.get_data(query, args)

            field_names = [
                'notificationid',
                'title',
                'body',
                'addedby',
                'recipient',
                'dateadded',
                'deleted',
                'datedeleted',
                'read'
            ]

            notifications_list = []
            for notification_data in notifications_data:
                notification_info = Notification(*notification_data)
                notifications_list.append(notification_info.__dict__)

            return jsonify(notifications_list), 200

        except Exception as e:
            print("Error fetching notifications:", str(e))
            return jsonify({'error': 'An error occurred while fetching notifications'}), 500

    @notifications_bp.route('/deletenotification/<int:notificationid>', methods=['POST'])
    @jwt_required()
    def delete_notification(notificationid):
        try:
            db = Database()
            query = "CALL sp_deletenotification(%s)"
            args = (notificationid,)
            db.execute_query(query, args)

            print("Notification deleted successfully")

            return jsonify({'message': 'Notification deleted successfully'}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    # SocketIO event for marking a notification as read
    @socketio.on('mark_as_read')
    def mark_notification_as_read(notificationid):
        try:
            current_user_id = get_jwt_identity()
            db = Database()
            query = "CALL sp_mark_notification_as_read(%s, %s)"
            args = (current_user_id, notificationid)
            db.execute_query(query, args)

            print("Notification marked as read")

        except Exception as e:
            print("Error marking notification as read:", str(e))