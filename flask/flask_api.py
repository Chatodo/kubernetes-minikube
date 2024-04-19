from flask import Flask, jsonify
# import mysql.connector

app = Flask(__name__)

# Configuration de la base de données
# db_config = {
#     'host': 'mysql',
#     'user': 'ivan',
#     'password': 'ivan',
#     'database': 'produits'
# }

# @app.route('/api/produits')
# def products():
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, nom, prix FROM produits")
#     products = [{'id': row[0], 'nom': row[1], 'prix': row[2]} for row in cursor]
#     cursor.close()
#     conn.close()
#     return jsonify(products)

@app.route('/api')
def home():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)