#!/bin/bash

git pull
python3 manage.py collectstatic
./restart.sh