#! /bin/sh
source /home/cajitasdeamor-services/cajitas-services/bin/activate
uwsgi --socket 0.0.0.0:5000 --protocol=http -w src/wsgi:src/app
