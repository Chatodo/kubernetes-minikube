FROM nginx:latest

RUN apt-get update && apt-get upgrade -y 

# Copier les fichiers statiques dans le dossier de serveur Nginx
COPY frontend /usr/share/nginx/html

EXPOSE 80

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]