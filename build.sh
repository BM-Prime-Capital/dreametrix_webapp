set -o errexit
pip install -r requirements.txt
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py populate_gradebooks