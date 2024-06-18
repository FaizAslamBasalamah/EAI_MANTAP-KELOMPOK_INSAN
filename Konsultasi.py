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
        SELECT 
            konsultasi.id, 
            konsultasi.patient_name, 
            konsultasi.patient_age, 
            diseases.name AS disease, 
            nurses.name AS nurse,  
            konsultasi.management_janji_id, 
            konsultasi.resep_hasil_konsultasi
        FROM konsultasi
        LEFT JOIN diseases ON konsultasi.disease_id = diseases.id
        LEFT JOIN users AS nurses ON konsultasi.nurse_id = nurses.id
        LEFT JOIN users AS patients ON konsultasi.patient_id = patients.id
        """
        cursor.execute(query)
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.json
        nurse_id = data.get('nurse_id')
        patient_id = data.get('patient_id')
        patient_age = data.get('patient_age')
        disease_id = data.get('disease_id')
        management_janji_id = data.get('management_janji_id')
        resep_hasil_konsultasi = data.get('resep_hasil_konsultasi')

        cursor = mysql.connection.cursor()
        # Insert new consultation
        sql = """
        INSERT INTO konsultasi (patient_name, patient_age, disease_id, nurse_id, patient_id, management_janji_id, resep_hasil_konsultasi)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (data.get('patient_name'), patient_age, disease_id, nurse_id, patient_id, management_janji_id, resep_hasil_konsultasi)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Consultation added successfully'})
    
@app.route('/detail_konsultasi/<int:id>', methods=['GET'])
def detail_user(id):
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM konsultasi WHERE id = %s"
        cursor.execute(query, (id,))
        column_names = [i[0] for i in cursor.description]
        data = cursor.fetchone()
        cursor.close()
        if data:
            return jsonify(dict(zip(column_names, data)))
        else:
            return jsonify({'message': ' not found'}), 404
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
    patient_id = %s,
    management_janji_id = %s,  # New column
    resep_hasil_konsultasi = %s  # New column
    WHERE id = %s
    """
    val = (
        patient_name,
        data.get('patient_age'),
        data.get('disease_id'),
        data.get('nurse_id'),
        data.get('patient_id'),
        data.get('management_janji_id'),  # New column
        data.get('resep_hasil_konsultasi'),  # New column
        id
    )
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Consultation updated successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55, debug=True)
