from django.core.management.base import BaseCommand
from myapp.models import ActuallyIntrest ,Payment , Return ,Register
from django.db.models import Q
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models.functions import Coalesce
from django.db.models import Sum,Value,IntegerField


class Command(BaseCommand):
    help = 'Save data at the end of the month'

    def handle(self, *args, **options):
        print("Executing save_previous_data command...")
        # Your logic to save data goes here
        # data_to_save = ActuallyIntrest.objects.filter(your_filtering_criteria)
        # for item in data_to_save:
        #     # Your save logic here
        #     item.save()
        # current_date = datetime.now()
        current_date=datetime(2023,8,31)
        month = current_date.month
        year = current_date.year
        previous_month_date = current_date - relativedelta(months=1)
        previous_month = previous_month_date.month
        previous_year = previous_month_date.year
        
        Register_data=Register.objects.all()
        for data in Register_data:
            Payment_data=Payment.objects.filter(Q(account_no=data.account_no)&Q(p_date__month=previous_month , p_date__year=previous_year)).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
            Return_data=Return.objects.filter(Q(account_no=data.account_no)&Q(r_date__month=previous_month , r_date__year=previous_year) & Q(principal_amount__gt='0')).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
            mint=Payment_data - Return_data
            if mint:
                pint=Payment.objects.filter(Q(account_no=data.account_no) & Q(p_date__month=previous_month, p_date__year=previous_year))
                interest=0
                for i in pint:
                    if int(i.intrest)>interest:
                        interest=int(i.intrest)
                days=1
                total=int(mint)*(int(interest)/100)/30*int(days)
                data={
                    'account_no':data.account_no,
                    'name':data.name,
                    'principal_amount':mint,
                    'intrest':interest,
                    'date':current_date,
                    'p_date':current_date,
                    'time_duration':data.time_duration,
                    'days':days,
                    'total':round(total)
                }
                instance=Payment(**data)
                instance.save()
            self.stdout.write(self.style.SUCCESS('Data saved successfully at the previosy month  of the month'))