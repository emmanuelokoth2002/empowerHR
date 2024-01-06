from flask import Flask
from flask_jwt_extended import JWTManager
from complaint import complaints_bp
from department import departments_bp
from employee import employees_bp
from leaverequest import leaverequests_bp
from role import roles_bp
from suggestion import suggestions_bp
from notification import notifications_bp
from user import users_bp

app = Flask(__name__)

# Configure Flask app to use Flask-JWT-Extended
app.config['SECRET_KEY'] = 'emmanuel'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']  # Adjust as needed
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Set your desired expiration time in seconds

jwt = JWTManager(app)

app.register_blueprint(complaints_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(leaverequests_bp)
app.register_blueprint(roles_bp)
app.register_blueprint(suggestions_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)