from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask import render_template

app = Flask(__name__)

# Config for JWT (use a strong secret key)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to your own secret key
jwt = JWTManager(app)

# Dummy user data
users = {"test@example.com": {"password": "password123", "id": 1}}
@app.route('/zohoverify/verifyforzoho.html')
def email():
    return render_template("verifyforzoho.html")
@app.route('/')
def index():
    return render_template("index.html")
# Route to authenticate user and generate JWT token
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    
    # Check if the user exists and the password is correct
    user = users.get(email)
    if user and user["password"] == password:
        # Create a JWT token with user identity
        access_token = create_access_token(identity={"id": user["id"], "email": email})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401

# Protected route that requires JWT authentication
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
