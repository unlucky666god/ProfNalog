pip3 install -r requirements.txt

gunicorn main:app --timeout 60

echo "END"
