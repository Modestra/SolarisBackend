#!/bin/bash/
sudo docker exec -it backend /bin/bash
sudo python manage.py migrate
sudo export DJANGO_SUPERUSER_USERNAME=Modestra
sudo export DJANGO_SUPERUSER_PASSWORD=Terrarik22
sudo export DJANGO_SUPERUSER_EMAIL="testuser@example.com"
sudo python manage.py createsuperuser --noinput