# yourapp/signals.py
from django.db.models.signals import Signal
from django.dispatch import receiver
import random

two_digit_number_generated = Signal()

@receiver(two_digit_number_generated)
def generate_two_digit_number(sender, instance, **kwargs):
    print('signal emitted')
    if not instance.two_digit_number:
        # Generate a two-digit number and assign it to the instance
        instance.two_digit_number = generate_two_digit_number()

def generate_two_digit_number():
    print('generate two digit number ')
    # Your logic to generate a two-digit number (e.g., using random module)
    # This is just a simple example; you may need to customize it based on your requirements
    return random.randint(10, 99)
