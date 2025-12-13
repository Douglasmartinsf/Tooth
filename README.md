# Tooth
Tooth is not an Odontological Object Tagging Hub.

#To Install

git clone https://github.com/bootstrap666/Tooth.git

cd Tooth

git lfs install

git lfs pull

python -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt

python manage.py makemigrations imagemproc

python manage.py migrate

python -m gunicorn myproject.wsgi:application --bind 0.0.0.0:9000
