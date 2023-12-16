from flask import Flask
from complaint import complaints_bp
from department import departments_bp
from employee import employees_bp
from leaverequest import leaverequests_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.register_blueprint(complaints_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(leaverequests_bp)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
