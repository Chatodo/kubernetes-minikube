FROM python:latest

RUN apt-get update && apt-get install -y \
	python3-dev \
	build-essential \
	default-libmysqlclient-dev \ 
	pkg-config

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

CMD ["python", "flask_api.py"]
EXPOSE 5000
