FROM python:latest

RUN apt-get update && apt-get install -y \
	python3-dev \
	build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

CMD ["python", "flask_api.py"]
EXPOSE 5000
