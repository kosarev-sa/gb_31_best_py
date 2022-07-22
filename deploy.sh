#!/bin/bash

python3 -m venv env
source env/bin/activate
cd BestJob/
pip3 install -r requirements.txt
python3 manage.py collectstatic
pip3 install gunicorn
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py fill_db
python3 manage.py fill_test_users
python3 manage.py fill_test_data
python3 manage.py rebuild_index
cd ..
chown -R django /home/django/
chmod -R 777 /home/django/gb_31_best_py/
cp gunicorn.service /etc/systemd/system/gunicorn.service
systemctl enable gunicorn
systemctl start gunicorn
cp Nginx /etc/nginx/sites-available/BestJob
ln -s /etc/nginx/sites-available/BestJob /etc/nginx/sites-enabled
systemctl restart nginx
