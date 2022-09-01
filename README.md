## Demo Project Link
https://ayxan.pythonanywhere.com

## Installition for Dev
**pip install -r requirements.txt<br />
cd src/<br />**

add SECRET_KEY to .env.example file<br />
rename .env.example to .env<br />

**python3 manage.py makemigrations account --settings=config.settings.development<br />
python3 manage.py makemigrations series --settings=config.settings.development<br />
python3 manage.py migrate --settings=config.settings.development<br />**

## Run for Dev
**python3 manage.py runserver --settings=config.settings.development**
