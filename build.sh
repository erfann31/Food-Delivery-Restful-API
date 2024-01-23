
# exit on error
set -o errexit
pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

#python manage.py makemigrations
python manage.py migrate
#python manage.py runserver

python manage.py create_default_superuser
