from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Simuation d'une base de données
produits = [
    {'id': 1, 'nom': 'Livre', 'prix': 39.99},
    {'id': 2, 'nom': 'Ordinateur', 'prix': 999.99},
]

# Fonction pour récupérer un produit par son id
def get_produit(id):
    for produit in produits:
        if produit['id'] == id:
            return produit
    abort(404)

# Routes de l'API
@app.route('/api/produits', methods=['GET'])
def get_produits():
    return jsonify(produits)

@app.route('/api/produits/<int:id>', methods=['GET'])
def get_produit_route(id):
    produit = get_produit(id)
    return jsonify(produit)

@app.route('/api/produits', methods=['POST'])
def create_produit():
    if not request.json or not 'nom' in request.json:
        abort(400)
    produit = {
        'id': produits[-1]['id'] + 1,
        'nom': request.json['nom'],
        'prix': request.json.get('prix', 0.0)
    }
    produits.append(produit)
    return jsonify(produit), 201

@app.route('/api/produits/<int:id>', methods=['PUT'])
def update_produit(id):
    produit = get_produit(id)
    if not request.json:
        abort(400)
    if 'nom' in request.json:
        produit['nom'] = request.json['nom']
    if 'prix' in request.json:
        produit['prix'] = request.json['prix']
    return jsonify(produit)

@app.route('/api/produits/<int:id>', methods=['DELETE'])
def delete_produit(id):
    produit = get_produit(id)
    produits.remove(produit)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)