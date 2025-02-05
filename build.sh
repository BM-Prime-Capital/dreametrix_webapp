set -o errexit
pip install -r requirements.txt
python manage.py makemigrations --fake
python manage.py migrate
python manage.py collectstatic --noinput
