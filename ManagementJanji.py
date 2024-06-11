from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'medis_konsultasi'
app.config['MYSQL_HOST'] = 'localhost'  

mysql = MySQL(app)

@app.route('/janji', methods=['GET', 'POST'])
def janji():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM management_janji")
        column_name = [i[0] for i in cursor.description]
        data = [dict(zip(column_name, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        patient_name = request.json['patient_name']
        nurse_name = request.json['nurse_name']
        appointment_date = request.json['appointment_date']
        created_at = request.json['created_at']
        cursor = mysql.connection.cursor()
        # Insert new appointment
        sql = "INSERT INTO management_janji (patient_name, nurse_name, appointment_date, created_at) VALUES (%s, %s, %s, %s)"
        val = (patient_name, nurse_name, appointment_date, created_at)
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
        column_name = [i[0] for i in cursor.description]
        data = [dict(zip(column_name, row)) for row in cursor.fetchall()]
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

@app.route('/update_janji', methods=['PUT'])
def update_janji():
    if 'id' in request.args:
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE management_janji SET patient_name = %s, nurse_name = %s, appointment_date = %s, created_at = %s WHERE id = %s"
        val = (data['patient_name'], data['nurse_name'], data['appointment_date'], data['created_at'], request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Janji updated successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
