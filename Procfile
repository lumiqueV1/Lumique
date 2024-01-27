release: python manage.py migrate
web: gunicorn Beautyswipe.wsgi:application
static: python manage.py collectstatic