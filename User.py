from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__, template_folder='C:\\xampp\\htdocs\\FeNurse')
CORS(app)
app.config.from_object('Config.Config')
mysql = MySQL(app)

@app.route('/users', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        column_name = [i[0] for i in cursor.description]
        data = [dict(zip(column_name, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        name = request.json['name']
        username = request.json['username']
        password = request.json['password']
        role = request.json.get('role', 'patient')  # Default role is 'patient'
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO users (name, username, password, role) VALUES (%s, %s, %s, %s)"
        val = (name, username, password, role)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User added successfully'})

@app.route('/detail_user/<int:id>', methods=['GET'])
def detail_user(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM users WHERE id = %s"
    cursor.execute(sql, (id,))
    column_name = [i[0] for i in cursor.description]
    data = cursor.fetchone()
    cursor.close()
    if data:
        return jsonify(dict(zip(column_name, data)))
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/getConsultationsPatientName', methods=['GET', 'POST'])
def consultations():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        sql = """
            SELECT c.id, c.patient_age, c.disease_id, c.nurse_id, c.patient_id, u.name as patient_name
            FROM konsultasi c
            JOIN users u ON c.patient_id = u.id
        """
        cursor.execute(sql)
        column_name = [i[0] for i in cursor.description]
        data = [dict(zip(column_name, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.json
        patient_name = data['patient_name']
        patient_id = data['patient_id']
        patient_age = data['patient_age']
        disease_id = data['disease_id']
        nurse_id = data['nurse_id']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO konsultasi (patient_name, patient_age, disease_id, nurse_id, patient_id) VALUES (%s, %s, %s, %s, %s)"
        val = (patient_name, patient_age, disease_id, nurse_id, patient_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Consultation added successfully'})

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM users WHERE id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User deleted successfully'})

@app.route('/update_user', methods=['PUT'])
def update_user():
    if 'id' in request.args:
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE users SET name = %s, username = %s, password = %s, role = %s WHERE id = %s"
        val = (data['name'], data['username'], data['password'], data['role'], request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User updated successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)
