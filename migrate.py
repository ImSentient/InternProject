import sys
import subprocess

subprocess.check_call("python manage.py makemigrations", shell=True)
subprocess.check_call("python manage.py migrate --noinput", shell=True)
subprocess.check_call("python manage.py runserver 0.0.0.0:8000", shell=True)
