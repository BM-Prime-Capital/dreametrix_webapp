set -o errexit
pip install -r requirements.txt
python manage.py migrate Authentication zero
python manage.py makemigrations Authentication
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput