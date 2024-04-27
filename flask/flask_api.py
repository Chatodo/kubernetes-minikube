from flask import Flask, jsonify, request, abort, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__, instance_relative_config=True)

# Flask MySQL
mysql = MySQL(app)

# flask_bcrypy : Gestion du hash des mots de passe
bcrypt = Bcrypt(app)

# Flask Login
# Chargement de la configuration de flask_login (fichier : instance/config.py)
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)

# Flask Session avec CacheLib
# Chargement de la configuration de flask_session (fichier : instance/config_sessions.py)
app.config.from_pyfile('config_sessions.py')
Session(app)

# Classe User pour gérer les utilisateurs
#######################################################################################################
class User(UserMixin):
	"""
	Représente un utilisateur.

	Attributs:
		id (int): L'id de l'utilisateur.
		email (str): email/pseudo de l'utilisateur.
		password (str): Mot de passe de l'utilisateur.

	Méthodes:
		get_user(email): Récupère un utilisateur depuis la base de données.
	"""

	def __init__(self, id, email, password):
		"""
		Initialise une nouvelle instance de la classe User.

		Args:
			id (int): L'ID de l'utilisateur.
			email (str): L'email/pseudo de l'utilisateur.
			password (str): Le mot de passe de l'utilisateur.
		"""
		self.id = id
		self.email = email
		self.password = password

	@classmethod
	def get_user(cls, id=None, email=None):
		"""
		Récupère un utilisateur, soit par son ID, soit par son email.
		
		Args:
			id (int): L'ID de l'utilisateur.
			email (bool): True si on veut récupérer l'utilisateur par son email, False par défaut.

		Returns:
			User: Un objet User si l'utilisateur existe, None sinon.
		"""
		cur = mysql.connection.cursor()
		if email:
			cur.execute("SELECT * FROM utilisateurs WHERE email = %s", [email])
		elif id:
			cur.execute("SELECT * FROM utilisateurs WHERE id = %s", [id])
		result = cur.fetchone()
		cur.close()
		return cls(*result) if result else None

# Loader de l'utilisateur pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
	return User.get_user(id=user_id)

#### Route API ####
# Connexion
@app.route('/api/login', methods=['POST'])
def login():
	data = request.get_json()
	if not data:
		abort(400)
	user = User.get_user(email=data.get('email'))
	if user and bcrypt.check_password_hash(user.password, data.get('password')):
		login_user(user, remember=True)
		session.permanent = True
		return jsonify({'success': True, 'message': 'Connexion réussie.'})
	return jsonify({'success': False, 'message': 'Mauvais identifiants.'}), 401

# Route pour s'inscrire
@app.route('/api/register', methods=['POST'])
def register():
	data = request.get_json()
	if not data:
		abort(400)
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM utilisateurs WHERE email = %s", (data['email'],))
	if cur.fetchone():
		cur.close()
		return jsonify({'success': False, 'message': 'Email déjà utilisé.'}), 400
	hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
	cur.execute("INSERT INTO utilisateurs (email, password) VALUES (%s, %s)", (data['email'], hashed_password))
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
	return jsonify({'success': current_user.is_authenticated})

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
		stock (int): La quantité du produit.

	Méthodes:
		get_all_produits(): Récupère tous les produits depuis la base de données.
	"""

	def __init__(self, id, nom, prix, stock):
		"""
		Initialise une nouvelle instance de la classe Produit.

		Args:
			id (int): L'ID du produit.
			nom (str): Le nom du produit.
			prix (float): Le prix du produit.
			stock (int): La quantité du produit.
		"""
		self.id = id
		self.nom = nom
		self.prix = prix
		self.stock = stock

	@staticmethod
	def get_all_produits():
		"""
		Récupère tous les produits depuis la base de données.
		self.stock > 0 pour ne récupérer que les produits en stock.

		Returns:
			list: Une liste de tous les produits qui a stock > 0.
		"""
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM produits WHERE stock > 0")
		result = cur.fetchall()
		cur.close()
		return [Produit(*row) for row in result]

#### Route API ####
# Route pour récupérer tous les produits
@app.route('/api/produits', methods=['GET'])
@login_required
def get_produits():
	produits = Produit.get_all_produits()
	return jsonify([{'id': p.id, 'nom': p.nom, 'prix': p.prix} for p in produits])

#######################################################################################################

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)