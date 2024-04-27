from flask import Flask, jsonify, request, abort, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__, instance_relative_config=True)

# Configuration de l'application (fichier : flask/instance/config.py)
app.config.from_pyfile('config.py')

# Flask MySQL
mysql = MySQL(app)

# Flask Login
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Flask Session avec CacheLib
app.config.from_pyfile('config_sessions.py')
Session(app)

# Classe User pour gérer les utilisateurs
#######################################################################################################
class User(UserMixin):
	"""
	Représente un utilisateur.

	Attributs:
		id (int): L'ID de l'utilisateur.
		email (str): Email de l'utilisateur.
		password (str): Mot de passe de l'utilisateur.

	Méthodes:
		get_user(email): Récupère un utilisateur depuis la base de données.
	"""

	def __init__(self, id, email, password):
		"""
		Initialise une nouvelle instance de la classe User.

		Args:
			id (int): L'ID de l'utilisateur.
			email (str): Le nom d'utilisateur de l'utilisateur.
			password (str): Le mot de passe de l'utilisateur.
		"""
		self.id = id
		self.email = email
		self.password = password

	@staticmethod
	def get_user(email):
		"""
		Récupère un utilisateur (email) depuis la base de données.

		Args:
			email (str): Email de l'utilisateur.

		Returns:
			User: L'utilisateur correspondant à l'email.
		"""
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
		result = cur.fetchone()
		cur.close()
		if result:
			return User(*result)
		return None

@login_manager.user_loader
def load_user(user_id):
	"""
	Cette fonction est utilisée pour charger un utilisateur depuis la base de données.

	Args:
		user_id (int): L'ID de l'utilisateur.

	Returns:
		User: L'utilisateur correspondant à l'ID.
	"""
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM utilisateurs WHERE id = %s", (user_id,))
	result = cur.fetchone()
	cur.close()
	if result:
		return User(*result)
	return None

# Route pour connexion
@app.route('/api/login', methods=['POST'])
def login():
	email = request.json.get('email')
	password = request.json.get('password')
	if not email or not password:
		abort(400)
	user = User.get_user(email)
	if user and bcrypt.check_password_hash(user.password, password):
		login_user(user, remember=True)
		app.session_interface.regenerate(session)
		session.permanent = True
		return jsonify({'success': True, 'message': 'Connexion réussie.'})
	return  jsonify({'error': True, 'message': 'Mauvais identifiants.'}), 401

# Route pour s'inscrire
@app.route('/api/register', methods=['POST'])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	if not email or not password:
		abort(400)
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
	if cur.fetchone():
		cur.close()
		return  jsonify({'error': True, 'message': 'Email déjà utilisé.'}), 400
	cur.execute("INSERT INTO utilisateurs (email, password) VALUES (%s, %s)", (email, bcrypt.generate_password_hash(password).decode('utf-8')))
	mysql.connection.commit()
	cur.close()
	return jsonify({'success': True, 'message': 'Inscription réussie.'})

# Route pour déconnexion
@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
	logout_user()
	return jsonify({'message': 'Vous êtes déconnecté.'})

# Route pour vérifier si l'utilisateur est connecté
@app.route('/api/status', methods=['GET'])
def status():
    if current_user.is_authenticated:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

#######################################################################################################

# Classe Produit pour gérer les produits
#######################################################################################################
class Produit:
	"""
	Représente un produit.

	Attributs:
		id (int): L'ID du produit.
		nom (str): Le nom du produit.
		prix (float): Le prix du produit.

	Méthodes:
		get_all_produits(): Récupère tous les produits depuis la base de données.
	"""

	def __init__(self, id, nom, prix):
		"""
		Initialise une nouvelle instance de la classe Produit.

		Args:
			id (int): L'ID du produit.
			nom (str): Le nom du produit.
			prix (float): Le prix du produit.
		"""
		self.id = id
		self.nom = nom
		self.prix = prix

	@staticmethod
	def get_all_produits():
		"""
		Récupère tous les produits depuis la base de données.

		Returns:
			list: Une liste de tous les produits.
		"""
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM produits")
		result = cur.fetchall()
		cur.close()
		return [Produit(*row) for row in result]

# Route pour récupérer tous les produits via une requête GET
@app.route('/api/produits', methods=['GET'])
@login_required
def get_produits():
	try:
		produits = Produit.get_all_produits()
		return jsonify([{'id': p.id, 'nom': p.nom, 'prix': p.prix} for p in produits])
	except Exception as e:
		app.logger.error(f"Erreur lors de la récupération des produits: {e}")
		return jsonify([]), 500
#######################################################################################################

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)