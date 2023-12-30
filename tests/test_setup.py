from flask import Flask
from  ..models.complaint import complaints_bp
from ..models.department import departments_bp
from ..models.employee import employees_bp
from ..models.leaverequest import leaverequests_bp

test_app = Flask(__name__)
test_app.config['TESTING'] = True  # Set testing mode
test_app.register_blueprint(complaints_bp)
test_app.register_blueprint(departments_bp)
test_app.register_blueprint(employees_bp)
test_app.register_blueprint(leaverequests_bp)

# Function to create a test client for the testing environment
def create_test_client():
    return test_app.test_client()
