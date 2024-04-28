from flask import Flask, jsonify, request, abort, session, redirect
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
		is_admin (bool): True si l'utilisateur est administrateur, False sinon.

	Méthodes:
		get_user(email): Récupère un utilisateur depuis la base de données.
	"""

	def __init__(self, id, email, password, is_admin=False):
		"""
		Initialise une nouvelle instance de la classe User.

		Args:
			id (int): L'ID de l'utilisateur.
			email (str): L'email/pseudo de l'utilisateur.
			password (str): Le mot de passe de l'utilisateur.
			is_admin (bool): True si l'utilisateur est administrateur, False sinon.
		"""
		self.id = id
		self.email = email
		self.password = password
		self.is_admin = is_admin

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
		return jsonify({'success': True, 'message': 'Connexion réussie.', 'is_admin': user.is_admin})
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

# Route pour changer le mot de passe / email
@app.route('/api/profil', methods=['POST'])
@login_required
def profil():
	data = request.get_json()
	if not data:
		abort(400)
	cur = mysql.connection.cursor()
	if 'email' in data:
		cur.execute("SELECT * FROM utilisateurs WHERE email = %s", (data['email'],))
		if cur.fetchone():
			cur.close()
			return jsonify({'success': False, 'message': 'Email déjà utilisé.'}), 400
		cur.execute("UPDATE utilisateurs SET email = %s WHERE id = %s", (data['email'], current_user.id))
	if 'password' in data:
		hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
		cur.execute("UPDATE utilisateurs SET password = %s WHERE id = %s", (hashed_password, current_user.id))
	mysql.connection.commit()
	cur.close()
	return jsonify({'success': True, 'message': 'Profil mis à jour.'})

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

### Route API ###
# Admin : Ajout de produit
@app.route('/api/produits', methods=['POST'])
@login_required
def add_produit():
	if current_user.is_admin:
		data = request.get_json()
		if not data:
			abort(400)
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)", (data['nom'], data['prix'], data['stock']))
		mysql.connection.commit()
		cur.close()
		return jsonify({'success': True, 'message': 'Produit ajouté.'})
	else:
		abort(403)

# Admin : Liste des utilisateurs
@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
	if current_user.is_admin:
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM utilisateurs")
		result = cur.fetchall()
		cur.close()
		return jsonify([{'id': row[0], 'email': row[1]} for row in result])
	else:
		abort(403)

#######################################################################################################
# Ajout de la vérification de l'existence des tables et de la création si nécessaire
def initialize_database():
	with app.app_context():
		cur = mysql.connection.cursor()
		cur.execute("SHOW TABLES LIKE 'utilisateurs'")
		result = cur.fetchone()
		if not result:
			cur.execute("""
				CREATE TABLE utilisateurs (
					id INT AUTO_INCREMENT PRIMARY KEY,
					email VARCHAR(255) NOT NULL,
					password VARCHAR(255) NOT NULL,
			   		is_admin BOOLEAN NOT NULL DEFAULT 0
					);
				""")
			admin_email = 'admin'
			admin_password = bcrypt.generate_password_hash('admin').decode('utf-8')
			cur.execute("INSERT INTO utilisateurs (email, password, is_admin) VALUES (%s, %s, 1)", (admin_email, admin_password))

		cur.execute("SHOW TABLES LIKE 'produits'")
		result = cur.fetchone()
		if not result:
			cur.execute("""
				CREATE TABLE produits (
					id INT AUTO_INCREMENT PRIMARY KEY,
					nom VARCHAR(255) NOT NULL,
					prix DECIMAL(10, 2) NOT NULL,
					stock INT NOT NULL DEFAULT 0
				);
			""")
		mysql.connection.commit()
		cur.close()

if __name__ == '__main__':
	initialize_database()
	app.run(host='0.0.0.0', port=5000, debug=True)