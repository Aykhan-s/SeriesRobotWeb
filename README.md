# ATTENTION: DEPRECATED!
This project has been deprecated because the `imdb-api.com` service it used to retrieve series data has been discontinued.
<br /> <br />
## This website uses imdb api to send users new episode notifications of their recorded series via e-mail.

## Installition for Dev (Debian based OS)
```sh
pip install -r requirements.txt
cd src/
```

add SECRET_KEY, EMAIL_HOST_PASSWORD to .env.example file<br />
rename .env.example to .env<br />
```sh
python3 manage.py makemigrations account --settings=config.settings.development
python3 manage.py makemigrations series --settings=config.settings.development
python3 manage.py migrate --settings=config.settings.development
```

## Run for Dev
```sh
python3 manage.py runserver --settings=config.settings.development
```
## Run Periodic Tasks with RabbitMQ
### Installition RabbitMQ
```sh
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
```
### Run Celery
```sh
celery -A config worker -l info
celery -A config beat -l info
```
## Run Periodic Tasks with Redis
### **add these two settings to base settings**<br />
```sh
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
```
### Installition Redis
```sh
sudo apt install redis
redis-server
```
### Run Celery
```
celery -A config worker -l info
celery -A config beat -l info
```
