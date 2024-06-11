from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__, template_folder='C:\\xampp\\htdocs\\FeNurse')
CORS(app)
app.config.from_object('Config.Config')
mysql = MySQL(app)

@app.route('/janji', methods=['GET', 'POST'])
def janji():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM management_janji")
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        patient_name = request.json['patient_name']
        nurse_name = request.json['nurse_name']
        appointment_date = request.json['appointment_date']
        patient_id = request.json['patient_id']  # New column
        nurse_id = request.json['nurse_id']  # New column
        cursor = mysql.connection.cursor()
        # Insert new appointment
        sql = "INSERT INTO management_janji (patient_name, nurse_name, appointment_date, patient_id, nurse_id) VALUES (%s, %s, %s, %s, %s)"
        val = (patient_name, nurse_name, appointment_date, patient_id, nurse_id)
        cursor.execute(sql, val)
        management_janji_id = cursor.lastrowid  # Get the last inserted id
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Janji added successfully', 'management_janji_id': management_janji_id})


@app.route('/detail_janji', methods=['GET'])
def detail_janji():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM management_janji WHERE id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)

@app.route('/delete_janji', methods=['DELETE'])
def delete_janji():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM management_janji WHERE id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Janji deleted successfully'})

@app.route('/get_nurse_name', methods=['GET'])
def get_nurse_name():
    if 'id' in request.args:
        nurse_id = request.args['id']
        cursor = mysql.connection.cursor()
        sql = "SELECT name FROM users WHERE id = %s AND role = 'nurse'"
        val = (nurse_id,)
        cursor.execute(sql, val)
        nurse_data = cursor.fetchone()
        cursor.close()
        if nurse_data:
            nurse_name = nurse_data[0]
            return jsonify({'nurse_name': nurse_name})
        else:
            return jsonify({'error': 'Nurse not found'}), 404
    else:
        return jsonify({'error': 'Nurse ID not provided'}), 400


@app.route('/update_janji', methods=['PUT'])
def update_janji():
    if 'id' in request.args:
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE management_janji SET patient_name = %s, nurse_name = %s, appointment_date = %s, patient_id = %s, disease_id = %s WHERE id = %s"
        val = (data['patient_name'], data['nurse_name'], data['appointment_date'], data['patient_id'], data['disease_id'], request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Janji updated successfully'})

@app.route('/get_patient_id', methods=['GET'])
def get_patient_id():
    if 'name' in request.args:
        patient_name = request.args['name']
        cursor = mysql.connection.cursor()
        sql = "SELECT id FROM users WHERE name = %s"
        val = (patient_name,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()
        if result:
            patient_id = result[0]
            return jsonify({'patient_id': patient_id})
        else:
            return jsonify({'error': 'Patient not found'}), 404
    else:
        return jsonify({'error': 'Name parameter is required'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=59, debug=True)
