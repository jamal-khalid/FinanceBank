import os
import sys
import schedule
import time
from django.core.management import call_command
from django.core.management import get_commands
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'B.settings')
# print("Available Commands:", get_commands())

# print("Python Executable:", sys.executable)
# print("PYTHONPATH:", sys.path)
# print("Current Directory:", os.getcwd())
# Explicitly set the DJANGO_SETTINGS_MODULE


def save_monthly_data():
    os.system('python manage.py save_monthly_data')

def save_previous_data():
    os.system('python manage.py save_previous_data')
# Schedule the task to run at regular intervals
schedule.every(1).minutes.do(save_monthly_data)
schedule.every(2).minutes.do(save_previous_data)

while True:
    schedule.run_pending()
    time.sleep(1)
