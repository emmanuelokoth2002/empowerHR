from flask import Flask
from complaint import complaints_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.register_blueprint(complaints_bp)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
