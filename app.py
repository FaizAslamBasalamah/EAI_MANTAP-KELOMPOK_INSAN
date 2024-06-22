from flask import Flask, jsonify, request, redirect, url_for, session, render_template, make_response
from datetime import datetime
import requests
import time
from datetime import timedelta
import jwt
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'
app.config.from_object('Config.Config')
mysql = MySQL(app)

JWT_SECRET = 'your_jwt_secret'
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_IN = 15  # 30 seconds for demo
REFRESH_TOKEN_EXPIRES_IN = 3600  # 1 hour

tokens = {}  # In-memory store for tokens

def generate_token(user_id, role, name, expires_in, token_type='access'):
    payload = {
        'user_id': user_id,
        'role': role,
        'name': name,
        'exp': time.time() + expires_in,
        'type': token_type
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def generate_access_token(user_id, role, name):
    return generate_token(user_id, role, name, ACCESS_TOKEN_EXPIRES_IN, 'access')

def generate_refresh_token(user_id, role, name):
    return generate_token(user_id, role, name, REFRESH_TOKEN_EXPIRES_IN, 'refresh')

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def refresh_access_token(user_id):
    refresh_token = tokens[user_id]['refresh_token']
    decoded = decode_token(refresh_token)
    if decoded and decoded['type'] == 'refresh':
        role = decoded['role']
        name = decoded['name']
        access_token = generate_access_token(user_id, role, name)
        tokens[user_id]['access_token'] = access_token
        tokens[user_id]['expires_at'] = time.time() + ACCESS_TOKEN_EXPIRES_IN
        return access_token
    else:
        raise Exception("Invalid or expired refresh token")

def get_valid_access_token(user_id):
    if user_id in tokens:
        if time.time() >= tokens[user_id]['expires_at']:
            return refresh_access_token(user_id)
        return tokens[user_id]['access_token']
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_password_str = hashed_password.decode('utf-8')  # Convert bytes to string
        print("Hashed password:", hashed_password_str)  # Log the hashed password

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role, name) VALUES (%s, %s, %s, %s)", 
                           (username, hashed_password_str, role, name))  # Store as string
            mysql.connection.commit()
        except Exception as e:
            return str(e), 400
        finally:
            cursor.close()

        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])
            user = cursor.fetchone()
            if user:
                stored_password = user[3].encode('utf-8')
                print(f"Stored password (hashed): {stored_password}")  # Log the stored hashed password
                print(f"Entered password: {password}")  # Log the entered password
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    session['user_id'] = user[0]  # Set user_id in session
                    session['role'] = user[4]  # Assuming the role is stored at index 4
                    name = user[1]  # Assuming the name is stored at index 1
                    access_token = generate_access_token(user[0], user[4], name)
                    refresh_token = generate_refresh_token(user[0], user[4], name)
                    # Store the refresh token in the database
                    cursor.execute("UPDATE users SET refresh_token = %s WHERE id = %s", (refresh_token, user[0]))
                    mysql.connection.commit()
                    tokens[user[0]] = {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'role': user[4],
                        'name': name,
                        'expires_at': time.time() + ACCESS_TOKEN_EXPIRES_IN
                    }
                    print(tokens[user[0]])

                    if 'patient' in user[4]:
                        response = make_response(redirect(url_for('patient_home')))
                        response.set_cookie('access_token', access_token, httponly=False, samesite='Lax')
                        response.set_cookie('refresh_token', refresh_token, httponly=False, samesite='Lax')
                        return response
                    elif 'nurse' in user[4]:
                        return redirect(url_for('nurse_home'))
                    else:
                        return 'Invalid role', 403
                else:
                    print("Password verification failed")  # Log when password verification fails
                    return "Invalid username or password", 401
            else:
                print("User not found")  # Log when user is not found
                return "Invalid username or password", 401
        except Exception as e:
            return str(e), 400
        finally:
            cursor.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id in tokens:
        tokens.pop(user_id)
    session.pop('user_id', None)
    return redirect(url_for('login'))

def get_username(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", [user_id])
        user = cursor.fetchone()
        cursor.close()
        if user:
            return user[0]  # Return username if user exists
        else:
            return None
    except (TypeError, KeyError):
        return None

@app.route('/medis')
def nurse_home():
    user_id = session.get('user_id')
    print("User ID from session:", user_id)  # Add this line to check the user_id
    username = get_username(user_id)  # Moved this line here
    print("Username:", username)  # Added this line to check the username
    if not user_id:
        return redirect(url_for('login'))

    access_token = get_valid_access_token(user_id)
    if not access_token:
        print("Access token:", access_token)
        return "Access Denied. Please log in again.", 403

    role = tokens[user_id]['role']

    return render_template('index.html', access_token=access_token, role=role, username=username)

@app.route('/patient')
def patient_home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    access_token = get_valid_access_token(user_id)
    role = tokens[user_id]['role']
    username = get_username(user_id)

    return render_template('patient.html', access_token=access_token, role=role, username=username)

@app.route('/')
def landing_page():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=70, debug=True)
