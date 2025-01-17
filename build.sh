set -o errexit
pip install -r requirements.txt
python manage.py migrate Authentication --fake
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput