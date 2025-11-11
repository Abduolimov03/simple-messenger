mig:
	python manage.py makemigrations && python manage.py migrate

runserver:
	python manage.py runserver

admin:
	python manage.py createsuperuser