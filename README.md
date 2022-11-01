## Installition for Dev
**pip install -r requirements.txt<br />
cd src/<br />**

add SECRET_KEY, EMAIL_HOST_PASSWORD to .env.example file<br />
rename .env.example to .env<br />

**python3 manage.py makemigrations account --settings=config.settings.development<br />
python3 manage.py makemigrations series --settings=config.settings.development<br />
python3 manage.py migrate --settings=config.settings.development<br />**<br />

## Run for Dev
**python3 manage.py runserver --settings=config.settings.development**<br /><br /><br />
## Run Periodic Tasks with RabbitMQ
### Installition RabbitMQ
**sudo apt-get install rabbitmq-server**<br />
**sudo systemctl start rabbitmq-server**<br />
### Run Celery
**celery -A config worker -l info**<br />
**celery -A config beat -l info**<br /><br />
## Run Periodic Tasks with Redis
### **add these two settings to base settings**<br />
**CELERY_BROKER_URL = "redis://localhost:6379"<br />
CELERY_RESULT_BACKEND = "redis://localhost:6379"**
### Installition Redis
**sudo apt install redis**<br />
**redis-server**<br />
### Run Celery
**celery -A config worker -l info**<br />
**celery -A config beat -l info**
