FROM python:3.10

WORKDIR /server

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod +x ./docker/app.sh

CMD ["./docker/app.sh"]


