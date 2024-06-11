from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# MySQL configurations

app = Flask(__name__, template_folder='C:\\xampp\\htdocs\\FeNurse')
CORS(app)
app.config.from_object('Config.Config')
mysql = MySQL(app)

@app.route('/diseases', methods=['GET', 'POST'])
def diseases():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM diseases")
        column_name = [i[0] for i in cursor.description]
        data = [dict(zip(column_name, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        name = request.json['name']
        description = request.json['description']
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO diseases (name, description) VALUES (%s, %s)"
        val = (name, description)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Disease added successfully'})

@app.route('/detail_disease/<int:id>', methods=['GET'])
def detail_disease(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM diseases WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    column_names = [i[0] for i in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    return jsonify(data)

@app.route('/delete_disease', methods=['DELETE'])
def delete_disease():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM diseases WHERE id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Disease deleted successfully'})

@app.route('/update_disease/<int:disease_id>', methods=['PUT'])
def update_disease(disease_id):
    try:
        data = request.get_json()  # Get JSON data from request body
        name = data.get('name')  # Retrieve 'name' from JSON data
        description = data.get('description')  # Retrieve 'description' from JSON data
        
        # Check if both 'name' and 'description' are provided
        if name is None or description is None:
            return jsonify({'error': 'Both name and description are required'}), 400
        
        # Update disease in the database
        cursor = mysql.connection.cursor()
        sql = "UPDATE diseases SET name = %s, description = %s WHERE id = %s"
        val = (name, description, disease_id)  # Use the disease_id from the URL
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Disease updated successfully'}), 200
    
    except Exception as e:
        # Handle exceptions and provide appropriate error response
        return jsonify({'error': str(e)}), 500

# @app.route('/update_disease', methods=['PUT'])
# def update_disease():
#     if 'id' in request.args:
#         data = request.get_json()
#         cursor = mysql.connection.cursor()
#         sql = "UPDATE diseases SET name = %s, description = %s WHERE id = %s"
#         val = (data['name'], data['description'], request.args['id'])
#         cursor.execute(sql, val)
#         mysql.connection.commit()
#         cursor.close()
#         return jsonify({'message': 'Disease updated successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58, debug=True)