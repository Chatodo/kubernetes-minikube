FROM python:latest

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Clone the frontend repository
RUN ghclone https://github.com/HR/Crypter/tree/dev/app

EXPOSE 8000

CMD ["flask", "run"]