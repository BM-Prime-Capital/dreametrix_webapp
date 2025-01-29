set -o errexit
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py populate_classes
python manage.py populate_assignments
python manage.py populate_gradebooks