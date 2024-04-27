# Normalement, on DOIT caché ses informations de connexion (par ex, en ajoutant ce fichier .gitignore)
# mais pour les besoins de l'exercice, on les laisse en clair.

MYSQL_HOST = 'mysql'
MYSQL_USER = 'flask'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'dbflask'
SECRET_KEY = '3e862c790ef3c04ba2e38e51a70ddd433051faaaa69d84ef4f8d47d95269f323' # Généré avec secrets.token_hex()