# On récupère les variables d'environnement définies dans le .yml
import os
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
SECRET_KEY = '3e862c790ef3c04ba2e38e51a70ddd433051faaaa69d84ef4f8d47d95269f323' # Généré avec secrets.token_hex()