from django.core.management.base import BaseCommand
from myapp.models import ActuallyIntrest ,Payment , Return ,Register
from django.db.models import Q
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Save data at the end of the month'

    def handle(self, *args, **options):
        print("Executing save_monthly_amount command...")
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
            Pint=0
            Rint=0
            PaidInt=0
            name=data.name
            res=Payment.objects.filter(Q(account_no=data.account_no)&Q(p_date__month=month , p_date__year=year))
            returnData=Return.objects.filter(Q(account_no=data.account_no)& Q(r_date__month=month,r_date__year=year) & Q(principal_amount__gt='0'))
            returnInt=Return.objects.filter(account_no=data.account_no ,principal_amount='0')
            try:
                prev_act=ActuallyIntrest.objects.get(Q(account_no=data.account_no)&Q(a_date__month=previous_month , a_date__year=previous_year))
                if prev_act:
                    if (prev_act.totalUnpaid+prev_act.PrevDues)>(prev_act.totalReturn+prev_act.Pint+prev_act.adv):
                        PrevDues=(prev_act.totalUnpaid+prev_act.PrevDues)-(prev_act.totalReturn+prev_act.Pint+prev_act.adv)
                    else:
                        Advance=(prev_act.totalReturn+prev_act.Pint+prev_act.adv)-(prev_act.totalUnpaid+prev_act.PrevDues)
            except:
                Advance=0
                PrevDues=0
            for i in res:
                Pint+=float(i.total)
            for j in returnData:
                Rint+=j.total
            for i in returnInt:
                PaidInt+=i.intrestAmount

            Mint=Pint-Rint
            total=(Mint+PrevDues+Advance)-PaidInt
            data={
                'account_no':data.account_no,
                'name':name,
                'totalUnpaid':Pint,
                'totalReturn':Rint,
                'adv':Advance,
                'mInterest':Mint,
                'PrevDues':PrevDues,
                'Pint':PaidInt,
                'total':total,
                'father_name':data.father_name,
                'adress':data.address,
                'a_date':current_date,
            }
            instance=ActuallyIntrest(**data)
            instance.save()
        self.stdout.write(self.style.SUCCESS('Data saved successfully at the end of the month'))