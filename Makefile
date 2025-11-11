mig:
	python manage.py makemigrations && python manage.py migrate

runserver:
	python manage.py runserver

runserver2:
	python manage.py runserver 8001

admin:
	python manage.py createsuperuser