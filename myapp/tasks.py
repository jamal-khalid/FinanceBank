from celery import shared_task
from celery.decorators import periodic_task
from datetime import timedelta
from django.db import transaction
from .models import ActuallyIntrest
import logging

logger = logging.getLogger(__name__)

@shared_task
@periodic_task(run_every=timedelta(minutes=2))
def save_data_at_end_of_month():
    try:
        with transaction.atomic():
            # Your code to save data to the database
            account_no = 'RF100'
            name = 'jhatu'
            totalUnpaid = 9876
            totalReturn = 876
            adv = 8765
            mInterest = 87654
            PrevDues = 876
            Pint = 567
            total = 765

            logger.info("Task started...")
            # ...
            count = 1
            while count < 4:
                # Your code to save ActuallyIntrest instances
                data = {
                    'account_no': account_no,
                    'name': name,
                    'totalUnpaid': totalUnpaid,
                    'totalReturn': totalReturn,
                    'adv': adv,
                    'mInterest': mInterest,
                    'PrevDues': PrevDues,
                    'Pint': Pint,
                    'total': total
                }
                instance = ActuallyIntrest(**data)
                instance.save()

                logger.info("Data saved successfully.")
                # ...
                count += 1
    except Exception as e:
        # Log any exceptions
        logger.error(f"Error saving data: {e}")
        print(f"Error saving data: {e}")
        # Rollback changes if an exception occurs
        transaction.set_rollback(True)
