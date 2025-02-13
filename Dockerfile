# Utiliser une image officielle de Python comme base
FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port utilisé par Django
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["gunicorn", "SchoolManagementSystem.wsgi:application", "--bind", "0.0.0.0:8000"]