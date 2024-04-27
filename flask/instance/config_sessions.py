# Normalement, on DOIT caché ses informations de connexion (par ex, en ajoutant ce fichier .gitignore)
# mais pour les besoins de l'exercice, on les laisse en clair.

from cachelib import FileSystemCache

SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="/sessions")