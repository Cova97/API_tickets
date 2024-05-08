import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)   # create an app instance

def connect():
    conn = psycopg2.connect(
        dbname='tickets',
        user='acova',
        password='1234',
        host='localhost',
        port='5432'
    )
    
    return conn

# Create all routes for auditorios
@app.route('/auditorios', methods=['POST']) # POST method to create a new auditorio
def create_adutorio():
    auditorio_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    # Comprobamos si el auditorio ya existe
    try:
        cur.execute(
            "SELECT * FROM Auditorios WHERE AuditorioID = %s",
            (auditorio_data['AuditorioID'],)
        )
        if cur.fetchone() is not None:
            return {'message': 'Auditorio already exists'}, 400
    except Exception as e:
        return {'message': 'Error while trying to create auditorio'}, 500
    # Creamos el auditorio
    cur.execute(
        "INSERT INTO Auditorios (AuditorioID, Nombre, Ubicacion, CapacidadTotal) VALUES (%s, %s, %s, %s)",
        (auditorio_data['AuditorioID'], auditorio_data['Nombre'], auditorio_data['Ubicacion'], auditorio_data['CapacidadTotal'])
    )
    conn.commit()
    return {'message': 'Auditorio created successfully'}, 200

@app.route('/auditorios', methods=['GET']) # GET method to read all auditorios
def read_auditorios():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM auditorios')
        rows = cur.fetchall()
        return {'auditorios': rows}, 200
    except Exception as e:
        return {'message': 'Error while trying to read auditorios'}, 500

@app.route('/auditorios', methods=['PUT']) # PUT method to update an auditorio
def update_auditorio():
    auditorio_data = request.get_json()
    conn = connect()
    cur = conn.cursor()

    try:
        # Check if the auditorio exists
        cur.execute(
            "SELECT * FROM Auditorios WHERE AuditorioID = %s",
            (auditorio_data['AuditorioID'],)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Auditorio does not exist'}), 404

        # Update the auditorio
        cur.execute(
            "UPDATE Auditorios SET Nombre = %s, Ubicacion = %s, CapacidadTotal = %s WHERE AuditorioID = %s",
            (auditorio_data['Nombre'], auditorio_data['Ubicacion'], auditorio_data['CapacidadTotal'], auditorio_data['AuditorioID'])
        )
        conn.commit()
        return jsonify({'message': 'Auditorio updated successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to update auditorio', 'error': str(e)}), 500

@app.route('/auditorios/<int:auditorio_id>', methods=['DELETE']) # DELETE method to delete an auditorio
def delete_auditorio(auditorio_id):
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the auditorio exists
        cur.execute(
            "SELECT * FROM Auditorios WHERE AuditorioID = %s",
            (auditorio_id,)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Auditorio does not exist'}), 404

        # Proceed with deletion if the auditorio exists
        cur.execute(
            "DELETE FROM Auditorios WHERE AuditorioID = %s",
            (auditorio_id,)
        )
        conn.commit()
        return jsonify({'message': 'Auditorio deleted successfully'}), 200

    except Exception as e:
        conn.rollback()  # Ensure to rollback on error
        return jsonify({'message': 'Error while trying to delete auditorio', 'error': str(e)}), 500


# Create all routes for boletos
@app.route('/boletos', methods=['POST']) # POST method to create a new boleto
def create_boletos():
    boletos_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the boleto already exists
        cur.execute(
            "SELECT * FROM Boletos WHERE BoletoID = %s",
            (boletos_data['BoletoID'],)
        )
        if cur.fetchone() is not None:
            return {'message': 'Boleto already exists'}, 400
    except Exception as e:
        return {'message': 'Error while trying to create boleto'}, 500

    # Create the boleto
    cur.execute(
        "INSERT INTO Boletos (BoletoID, ZonaID, Precio) VALUES (%s, %s, %s)",
        (boletos_data['BoletoID'], boletos_data['ZonaID'], boletos_data['Precio'])
    )
    conn.commit()
    return {'message': 'Boleto created successfully'}, 200

@app.route('/boletos', methods=['GET']) # GET method to read all boletos
def read_boletos():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM boletos')
        rows = cur.fetchall()
        return {'boletos': rows}, 200
    except Exception as e:
        return {'message': 'Error while trying to read boletos'}, 500

@app.route('/boletos', methods=['PUT']) # PUT method to update a boleto
def update_boletos():
    boletos_data = request.get_json()
    conn = connect()
    cur = conn.cursor()

    try:
        # Check if the boleto exists
        cur.execute(
            "SELECT * FROM Boletos WHERE BoletoID = %s",
            (boletos_data['BoletoID'],)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Boleto does not exist'}), 404

        # Update the boleto
        cur.execute(
            "UPDATE Boletos SET ZonaID = %s, Precio = %s, Disponibles = %s WHERE BoletoID = %s",
            (boletos_data['ZonaID'], boletos_data['Precio'], boletos_data['Disponibles'], boletos_data['BoletoID'])
        )
        conn.commit()
        return jsonify({'message': 'Boleto updated successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to update boleto', 'error': str(e)}), 500

@app.route('/boletos/<int:boleto_id>', methods=['DELETE']) # DELETE method to delete a boleto
def delete_boletos(boleto_id):
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the boleto exists
        cur.execute(
            "SELECT * FROM Boletos WHERE BoletoID = %s",
            (boleto_id,)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Boleto does not exist'}), 404

        # Proceed with deletion if the boleto exists
        cur.execute(
            "DELETE FROM Boletos WHERE BoletoID = %s",
            (boleto_id,)
        )
        conn.commit()
        return jsonify({'message': 'Boleto deleted successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to delete boleto', 'error': str(e)}), 500

# Create all routes for conciertos
@app.route('/conciertos', methods=['POST']) # POST method to create a new concierto
def create_conciertos():
    conciertos_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the concierto already exists
        cur.execute(
            "SELECT * FROM Conciertos WHERE ConciertoID = %s",
            (conciertos_data['ConciertoID'],)
        )
        if cur.fetchone() is not None:
            return {'message': 'Concierto already exists'}, 400
        
         # Execute the INSERT statement to create a new concierto
        cur.execute(
            "INSERT INTO Conciertos (ConciertoID, NombreEvento, FechaEvento, AuditorioID) VALUES (%s, %s, %s, %s)",
            (conciertos_data['ConciertoID'], conciertos_data['NombreEvento'], conciertos_data['FechaEvento'], conciertos_data['AuditorioID'])
        )
        conn.commit()
        return jsonify({'message': 'Concierto created successfully'}), 201
    except Exception as e:
        return {'message': 'Error while trying to create concierto'}, 500

@app.route('/conciertos', methods=['GET']) # GET method to read all conciertos
def read_conciertos():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM conciertos')
        rows = cur.fetchall()
        return {'conciertos': rows}, 200
    except Exception as e:
        return {'message': 'Error while trying to read conciertos'}, 500

@app.route('/conciertos', methods=['PUT']) # PUT method to update a concierto
def update_conciertos():
    conciertos_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the concierto exists
        cur.execute(
            "SELECT * FROM Conciertos WHERE ConciertoID = %s",
            (conciertos_data['ConciertoID'],)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Concierto does not exist'}), 404

        # Update the concierto
        cur.execute(
            "UPDATE Conciertos SET NombreEvento = %s, FechaEvento = %s, AuditorioID = %s WHERE ConciertoID = %s",
            (conciertos_data['NombreEvento'], conciertos_data['FechaEvento'], conciertos_data['AuditorioID'], conciertos_data['ConciertoID'])
        )
        conn.commit()
        return jsonify({'message': 'Concierto updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to update concierto', 'error': str(e)}), 500

@app.route('/conciertos/<int:concierto_id>', methods=['DELETE']) # DELETE method to delete a concierto
def delete_conciertos(concierto_id):
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the concierto exists
        cur.execute(
            "SELECT * FROM Conciertos WHERE ConciertoID = %s",
            (concierto_id,)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Concierto does not exist'}), 404

        # Proceed with deletion if the concierto exists
        cur.execute(
            "DELETE FROM Conciertos WHERE ConciertoID = %s",
            (concierto_id,)
        )
        conn.commit()
        return jsonify({'message': 'Concierto deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to delete concierto', 'error': str(e)}), 500

# Create all routes for vendedores
@app.route('/vendedores', methods=['POST']) # POST method to create a new vendedor
def create_vendedores():
    vendedores_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the vendedor already exists
        cur.execute(
            "SELECT * FROM Vendedores WHERE VendedorID = %s",
            (vendedores_data['VendedorID'],)
        )
        if cur.fetchone() is not None:
            return {'message': 'Vendedor already exists'}, 400
        cur.execute(
            "INSERT INTO Vendedores (VendedorID, NombreVendedor, SitioWeb) VALUES (%s, %s, %s)",
            (vendedores_data['VendedorID'], vendedores_data['NombreVendedor'], vendedores_data['SitioWeb'])
        )
        conn.commit()
        return {'message': 'Vendedor created successfully'}, 200

    except Exception as e:
        return {'message': 'Error while trying to create vendedor'}, 500

@app.route('/vendedores', methods=['GET']) # GET method to read all vendedores
def read_vendedores():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM vendedores')
        rows = cur.fetchall()
        return {'vendedores': rows}, 200
    except Exception as e:
        return {'message': 'Error while trying to read vendedores'}, 500

@app.route('/vendedores', methods=['PUT']) # PUT method to update a vendedor
def update_vendedores():
    vendedores_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the vendedor exists
        cur.execute(
            "SELECT * FROM Vendedores WHERE VendedorID = %s",
            (vendedores_data['VendedorID'],)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Vendedor does not exist'}), 404

        # Update the vendedor
        cur.execute(
            "UPDATE Vendedores SET NombreVendedor = %s, SitioWeb = %s WHERE VendedorID = %s",
            (vendedores_data['NombreVendedor'], vendedores_data['SitioWeb'], vendedores_data['VendedorID'])
        )
        conn.commit()
        return jsonify({'message': 'Vendedor updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to update vendedor', 'error': str(e)}), 500

@app.route('/vendedores/<int:vendedor_id>', methods=['DELETE']) # DELETE method to delete a vendedor
def delete_vendedores(vendedor_id):
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the vendedor exists
        cur.execute(
            "SELECT * FROM Vendedores WHERE VendedorID = %s",
            (vendedor_id,)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Vendedor does not exist'}), 404

        # Proceed with deletion if the vendedor exists
        cur.execute(
            "DELETE FROM Vendedores WHERE VendedorID = %s",
            (vendedor_id,)
        )
        conn.commit()
        return jsonify({'message': 'Vendedor deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to delete vendedor', 'error': str(e)}), 500

# Create all routes for zonas
@app.route('/zonas', methods=['POST']) # POST method to create a new zona
def create_zonas():
    zonas_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the zona already exists
        cur.execute(
            "SELECT * FROM Zonas WHERE ZonaID = %s",
            (zonas_data['ZonaID'],)
        )
        if cur.fetchone() is not None:
            return {'message': 'Zona already exists'}, 400
        cur.execute(
            "INSERT INTO Zonas (ZonaID, NombreZona, Capacidad, AuditorioID) VALUES (%s, %s, %s, %s)",
            (zonas_data['ZonaID'], zonas_data['NombreZona'], zonas_data['Capacidad'], zonas_data['AuditorioID'])
        )
        conn.commit()
        return jsonify({'message': 'Zona created successfully'}), 201
    except Exception as e:
        return {'message': 'Error while trying to create zona: ' + str(e)}, 500

    
@app.route('/zonas', methods=['GET']) # GET method to read all zonas
def read_zonas():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM zonas')
        rows = cur.fetchall()
        return {'zonas': rows}, 200
    except Exception as e:
        return {'message': 'Error while trying to read zonas'}, 500

@app.route('/zonas', methods=['PUT']) # PUT method to update a zona
def update_zonas():
    zonas_data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the zona exists
        cur.execute(
            "SELECT * FROM Zonas WHERE ZonaID = %s",
            (zonas_data['ZonaID'],)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Zona does not exist'}), 404

        # Update the zona
        cur.execute(
            "UPDATE Zonas SET NombreZona = %s, Capacidad = %s, AuditorioID = %s WHERE ZonaID = %s",
            (zonas_data['NombreZona'], zonas_data['Capacidad'], zonas_data['AuditorioID'], zonas_data['ZonaID'])
        )
        conn.commit()
        return jsonify({'message': 'Zona updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to update zona', 'error': str(e)}), 500

@app.route('/zonas/<int:zona_id>', methods=['DELETE']) # DELETE method to delete a zona
def delete_zonas(zona_id):
    conn = connect()
    cur = conn.cursor()
    try:
        # Check if the zona exists
        cur.execute(
            "SELECT * FROM Zonas WHERE ZonaID = %s",
            (zona_id,)
        )
        if cur.fetchone() is None:
            return jsonify({'message': 'Zona does not exist'}), 404

        # Proceed with deletion if the zona exists
        cur.execute(
            "DELETE FROM Zonas WHERE ZonaID = %s",
            (zona_id,)
        )
        conn.commit()
        return jsonify({'message': 'Zona deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error while trying to delete zona', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)   # run the flask app in debug mode