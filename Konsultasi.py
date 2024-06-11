from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__, template_folder='C:\\xampp\\htdocs\\FeNurse')
CORS(app)
app.config.from_object('Config.Config')
mysql = MySQL(app)

@app.route('/konsultasi', methods=['GET', 'POST'])
def konsultasi():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = """
        SELECT konsultasi.id, konsultasi.patient_name, konsultasi.patient_age, diseases.name AS disease, nurses.name AS nurse, patients.name AS patient
        FROM konsultasi
        JOIN diseases ON konsultasi.disease_id = diseases.id
        JOIN users AS nurses ON konsultasi.nurse_id = nurses.id
        JOIN users AS patients ON konsultasi.patient_id = patients.id
        """
        cursor.execute(query)
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        patient_id = request.json.get('patient_id')
        cursor = mysql.connection.cursor()
        
        # Fetch the patient name from the users table
        cursor.execute("SELECT name FROM users WHERE id = %s", (patient_id,))
        patient_name = cursor.fetchone()[0]
        
        patient_age = request.json.get('patient_age')
        disease_id = request.json.get('disease_id')
        nurse_id = request.json.get('nurse_id')

        sql = """
        INSERT INTO konsultasi (patient_name, patient_age, disease_id, nurse_id, patient_id) 
        VALUES (%s, %s, %s, %s, %s)
        """
        val = (patient_name, patient_age, disease_id, nurse_id, patient_id)
        cursor.execute(sql, val)
        new_id = cursor.lastrowid
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Consultation added successfully', 'id': new_id})

@app.route('/detail_konsultasi/<int:id>', methods=['GET'])
def detail_konsultasi(id):
    try:
        cursor = mysql.connection.cursor()
        sql = """
        SELECT konsultasi.id, konsultasi.patient_name, konsultasi.patient_age, 
               diseases.name AS disease, diseases.description AS disease_description, 
               nurses.name AS nurse, patients.name AS patient
        FROM konsultasi
        JOIN diseases ON konsultasi.disease_id = diseases.id
        JOIN users AS nurses ON konsultasi.nurse_id = nurses.id
        JOIN users AS patients ON konsultasi.patient_id = patients.id
        WHERE konsultasi.id = %s
        """
        val = (id,)
        cursor.execute(sql, val)
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_konsultasi', methods=['DELETE'])
def delete_konsultasi():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM konsultasi WHERE id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Consultation deleted successfully'})

@app.route('/update_konsultasi/<int:id>', methods=['PUT'])
def update_konsultasi(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    
    # Fetch the patient name from the users table
    cursor.execute("SELECT name FROM users WHERE id = %s", (data.get('patient_id'),))
    patient_name = cursor.fetchone()[0]
    
    sql = """
    UPDATE konsultasi SET 
    patient_name = %s, 
    patient_age = %s, 
    disease_id = %s, 
    nurse_id = %s, 
    patient_id = %s
    WHERE id = %s
    """
    val = (
        patient_name,
        data.get('patient_age'),
        data.get('disease_id'),
        data.get('nurse_id'),
        data.get('patient_id'),
        id
    )
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Consultation updated successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55, debug=True)
