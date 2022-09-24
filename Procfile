web: gunicorn -b "0.0.0.0:$PORT" -w 3 retail_project.wsgi
release: python manage.py migrate