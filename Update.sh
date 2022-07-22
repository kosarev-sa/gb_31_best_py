#!/bin/bash

git pull
systemctl stop gunicorn
systemctl stop nginx
systemctl start gunicorn
systemctl start nginx