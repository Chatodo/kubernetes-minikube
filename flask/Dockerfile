FROM python:slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
	python3-dev \
	build-essential \
	default-libmysqlclient-dev \ 
	libxslt-dev \
	pkg-config

# Créer un dossier pour les sessions et un utilisateur appuser
RUN mkdir /sessions && \
adduser --disabled-password --gecos '' appuser && \
chown appuser:appuser /sessions

WORKDIR /app

COPY requirements.txt .

USER appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"

RUN pip install -r requirements.txt
COPY . .

CMD ["python", "flask_api.py"]
EXPOSE 5000