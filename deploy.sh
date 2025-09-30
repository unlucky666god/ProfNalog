#!/bin/bash

pip3 install -r requirements.txt

gunicorn app:app --timeout 60

echo "END"
