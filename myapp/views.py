from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Register , Payment , Return , ActuallyIntrest
from datetime import datetime ,date
from django.contrib import messages
from myapp.signals import two_digit_number_generated
import random
from django.shortcuts import render, get_object_or_404
from datetime import datetime , date , timedelta
import calendar
from calendar import month_name
from django.db.models import Q
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,Value,IntegerField
from django.db.models.functions import Coalesce


def nav(request):
    return render(request , 'start.html')

def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/dashboard')
        else:
            messages.error(request,"Invalid Credentials ! ")
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request,'form.html')

def generate_two_digit_number():
    return str(random.randint(10, 99))

def register_forms(request ,step=1):
    if request.method=='POST':
        cleaned_data = request.POST
        pic=request.FILES.get('pic')
        gpic=request.FILES.get('gpic')
        gdocument=request.FILES.get('gdocument')
        g2pic=request.FILES.get('g2pic')
        g2document=request.FILES.get('g2document')
        Npic=request.FILES.get('Npic')
        Ndocument=request.FILES.get('Ndocument')
        Document=request.FILES.get('Document')
        if step == 1:
            try:
                queryset = Register.objects.last()
                last = queryset.account_no
            except:
                last = 'RF001'

            l = last[2:]
            if int(l) < 10:
                acc = int(l) + 1
                account_no = 'RF00' + str(acc)
            elif 10 <= int(l) <= 99:
                acc = int(l) + 1
                account_no = 'RF0' + str(acc)
            else:
                acc = int(l) + 1
                account_no = 'RF' + str(acc)

            Register.objects.create(
                name=cleaned_data.get('rname'),
                father_name=cleaned_data.get('rfname'),
                gender=cleaned_data.get('gender'),
                # limit=cleaned_data.get('loan_limit'),
                # rate_of_interest=cleaned_data.get('roi'),
                # join_date=cleaned_data.get('rjoin'),
                Date_of_birth=cleaned_data.get('rdob'),
                age=cleaned_data.get('age'),
                # area=cleaned_data.get('area'),
                city=cleaned_data.get('city'),
                district=cleaned_data.get('district'),
                state=cleaned_data.get('state'),
                email=cleaned_data.get('remail'),
                profession=cleaned_data.get('profession'),
                mobile=cleaned_data.get('mobile'),
                alter_mobile=cleaned_data.get('alter_mobile'),
                address=cleaned_data.get('raddress'),
                remarks=cleaned_data.get('remarks'),
                image=pic,
                time_duration=cleaned_data.get('duration'),
                account_no=account_no,
                Document=Document,
                pinCode=cleaned_data.get('pincode')

                # Add other fields for Step 1
            )
        elif step == 2:
            registration_instance = Register.objects.latest('id')
            registration_instance.g1name = cleaned_data.get('gname')
            registration_instance.g1father_name = cleaned_data.get('gfname')
            registration_instance.g1DOB = cleaned_data.get('gdob')
            registration_instance.g1Age = cleaned_data.get('gage')
            registration_instance.g1Address = cleaned_data.get('gadres')
            registration_instance.g1Relation = cleaned_data.get('grelation')
            registration_instance.g1Adhar_no = cleaned_data.get('gadhar')
            registration_instance.g1Image = gpic
            registration_instance.g1Area = cleaned_data.get('garea')
            registration_instance.g1City = cleaned_data.get('gcity')
            registration_instance.g1District = cleaned_data.get('gdistrict')
            registration_instance.g1State = cleaned_data.get('gstate')
            registration_instance.g1Mobile_NO = cleaned_data.get('gmobile')
            registration_instance.g1Document = gdocument

            registration_instance.g2name = cleaned_data.get('g2name')
            registration_instance.g2father_name = cleaned_data.get('g2fname')
            registration_instance.g2DOB = cleaned_data.get('g2dob')
            registration_instance.g2Age = cleaned_data.get('g2age')
            registration_instance.g2Address = cleaned_data.get('g2adres')
            registration_instance.g2Relation = cleaned_data.get('g2relation')
            registration_instance.g2Adhar_no = cleaned_data.get('g2adhar')
            registration_instance.g2Image = g2pic
            registration_instance.g2Area = cleaned_data.get('g2area')
            registration_instance.g2City = cleaned_data.get('g2city')
            registration_instance.g2District = cleaned_data.get('g2district')
            registration_instance.g2State = cleaned_data.get('g2state')
            registration_instance.g2Mobile_NO = cleaned_data.get('g2mobile')
            registration_instance.g2Document = g2document

            # Add other fields for Step 2
            registration_instance.save()

        elif step == 3:
            registration_instance = Register.objects.latest('id')
            registration_instance.nName = cleaned_data.get('Nname')
            registration_instance.nFather_name = cleaned_data.get('Nfname')
            registration_instance.nMother_name = cleaned_data.get('Nmname')
            registration_instance.nDOB = cleaned_data.get('Ndob')
            registration_instance.nAge = cleaned_data.get('Nage')
            registration_instance.nAdress = cleaned_data.get('Nadresh')
            registration_instance.nRelation = cleaned_data.get('Nrelation')
            registration_instance.nAdhar_Number = cleaned_data.get('Nadhar')
            registration_instance.nImage = Npic
            registration_instance.nArea = cleaned_data.get('Narea')
            registration_instance.nCity = cleaned_data.get('Ncity')
            registration_instance.nDistrict = cleaned_data.get('Ndistrict')
            registration_instance.nState = cleaned_data.get('Nstate')
            registration_instance.nMobile_no = cleaned_data.get('Nmobile')
            registration_instance.nDocument = Ndocument
            # Add other fields for Step 4
            registration_instance.save()

        if step == 3:
            return redirect('/dashboard')

        return redirect('registration_view', step=step + 1)

    template_name = f'registerStep{step}.html'
    return render(request, template_name )

def rlist(request):
    res=Register.objects.all()
    param={'res':res}
    return render(request,'list.html',param)

def Dashboard(request):
    return render(request , 'index.html')

def EMI_Calculator(request):
    return render(request ,'emi.html')

def DayWise(request):
    res=Register.objects.filter(time_duration='Daywise')
    param={'res':res}
    return render(request , 'daywise.html' , param)

def toggle_active(request, item_id):
    record = get_object_or_404(Register, pk=item_id)
    status = request.GET.get('status', 'inactive')

    if status == 'active':
        record.is_active = True
    elif status == 'inactive':
        record.is_active = False

    record.save()
    return redirect('/monthly')

def Monthly(request):
    res=Register.objects.filter(time_duration='Monthly')
    param={'res':res}
    return render(request , 'monthly.html' , param)
    
def MonthlyList(request):
    res=Register.objects.filter(time_duration='Monthly')
    param={'res':res}
    return render(request ,'MonthlyList.html' , param)

def Weekly(request):
    res=Register.objects.filter(time_duration='Weekly')
    param={'res':res}
    return render(request, 'weekly.html' , param)

def fifteenDays(request):
    res=Register.objects.filter(time_duration='fifteen_days')
    param={'res':res}
    return render(request,'fif.html',param)

def paymentPage(request , Account_no):
    response=Register.objects.get(account_no=Account_no)
    
    ReturnData=Return.objects.filter(account_no=Account_no)
        
    if request.method=='POST':
        if response.time_duration=='Monthly':
            time_duration='Monthly'
            account_no=response.account_no
            name=response.name
            date=request.POST.get('date')
            input_date = datetime.strptime(date, '%Y-%m-%d')
            p_date=input_date
            today_date=datetime.now()
            days=today_date.day-input_date.day
            principal_amount=request.POST.get('principalA')
            remarks=request.POST.get('remark')
            intrest=request.POST.get('intrest')
            total=int(principal_amount)*(int(intrest)/100)/30*int(days)
            user=Payment(account_no=account_no,name=name,days=days , principal_amount=principal_amount ,intrest=intrest , total=total,date=date , time_duration=time_duration,p_date=p_date , remarks=remarks)
            user.save()
            return redirect(f"/view-page/{response.account_no}")
        
        elif response.time_duration=='Daywise':
            time_duration='Daywise'
            account_no=response.account_no
            name=response.name
            date=request.POST.get('date')
            input_date=datetime.strptime(date , '%Y-%m-%d')
            p_date=input_date
            today_date=datetime.now()
            days=today_date.day-input_date.day
            principal_amount=request.POST.get('principalA')
            remarks=request.POST.get('remark')
            intrest=request.POST.get('intrest')
            total=int(principal_amount)*(int(intrest)/100)/30*int(days)
            user=Payment(account_no=account_no,name=name,days=days,principal_amount=principal_amount , intrest=intrest,total=total,date=date , time_duration=time_duration , p_date=p_date , remarks=remarks)
            user.save()
            return redirect(f'/view-page/{response.account_no}') 
        
        elif response.time_duration=='Weekly':
            time_duration='Weekly'
            account_no=response.account_no
            name=response.name
            date=request.POST.get('date')
            input_date=datetime.strptime(date , '%Y-%m-%d')
            p_date=input_date
            today_date=datetime.now()
            days=today_date.day-input_date.day
            principal_amount=request.POST.get('principalA')
            remarks=request.POST.get('remark')
            intrest=request.POST.get('intrest')
            total=int(principal_amount)*(int(intrest)/100)/30*int(days)
            user=Payment(account_no=account_no,name=name,days=days,principal_amount=principal_amount , intrest=intrest,total=total,date=date , time_duration=time_duration , p_date=p_date , remarks=remarks)
            user.save()
            return redirect(f'/view-page/{response.account_no}') 
        
        elif response.time_duration=='fifteen_days':
            time_duration='fifteen_days'
            account_no=response.account_no
            name=response.name
            date=request.POST.get('date')
            input_date=datetime.strptime(date , '%Y-%m-%d')
            p_date=input_date
            today_date=datetime.now()
            days=today_date.day-input_date.day
            principal_amount=request.POST.get('principalA')
            remarks=request.POST.get('remark')
            intrest=request.POST.get('intrest')
            total=int(principal_amount)*(int(intrest)/100)/30*int(days)
            user=Payment(account_no=account_no,name=name,days=days,principal_amount=principal_amount , intrest=intrest,total=total,date=date , time_duration=time_duration , p_date=p_date , remarks=remarks)
            user.save()
            return redirect(f'/view-page/{response.account_no}')
            
    paymentData=Payment.objects.filter(account_no=Account_no)
    paymentDataLast=Payment.objects.filter(account_no=Account_no).last()
    amountt=0
    Pint=0
    fine=0
    for i in paymentData:
        amountt+=int(i.principal_amount)
        Pint+=float(i.total)
    
    for j in ReturnData:
        fine=j.fine
    pInt=round(Pint)
    
    params={'response':response ,'paymentData':paymentData ,'ReturnData':ReturnData , 'amountt':amountt ,"pInt":pInt ,'paymentDataLast':paymentDataLast ,'fine':fine}
            

    return render(request,'payment.html',params)

def returnPage(request ,Account_no):
    res=Register.objects.get(account_no=Account_no)
    returnData=Return.objects.filter(account_no=Account_no)
    if request.method=='POST':
        account_no=res.account_no
        name=res.name
        ir=Payment.objects.filter(name=name)
        inter=0
        if ir.exists():
            for i in ir:
                if int(i.intrest)>inter:
                    inter=int(i.intrest)
        date=request.POST.get('date')
        input_date=datetime.strptime(date,'%Y-%m-%d')
        r_date=input_date
        today_date=datetime.now()
        days=today_date.day-input_date.day
        principal_amount=request.POST.get('pamount')
        remarks=request.POST.get('remark')
        intrestAmount=request.POST.get('intrestAmount')
        fine=request.POST.get('rfine')
        if not principal_amount:
            principal_amount = 0
        tot=int(principal_amount)*(int(inter)/100)/30*int(days)
        total=round(tot)

        user=Return(account_no=account_no,name=name,days=days,principal_amount=principal_amount,intrest=inter,total=total , date=date,r_date=r_date , remarks=remarks ,intrestAmount=intrestAmount,fine=fine)
        user.save()
        return redirect(f'/view-page/{res.account_no}')

    paymentData=Payment.objects.filter(account_no=Account_no)
    amount=0
    NewFine=0
    Rint=0
    for i in returnData:
        amount+=int(i.principal_amount)
        Rint+=int(i.total)
        NewFine=i.fine
    
    returnDataLast=Return.objects.filter(account_no=Account_no).last()
        
    params={"res":res,"paymentData":paymentData ,'returnData':returnData , 'amount':amount , 'Rint':Rint ,'NewFine':NewFine , 'returnDataLast':returnDataLast}
        
    return render(request , 'return.html' , params)

def is_last_day_of_month(manual_date=None):
    if manual_date:
        today = manual_date
    else:
        today = datetime.now()

    last_day_of_month = calendar.monthrange(today.year, today.month)[1]

    return today.day == last_day_of_month


def viewPage(request , Account_no):
    current_date = datetime.now()
    # Extract the current month and year
    month = current_date.month
    year = current_date.year
    month_name = current_date.strftime('%B')
    res=Payment.objects.filter(Q(account_no=Account_no) & Q(p_date__month=month,p_date__year=year))
    
    for i in res:
        x=datetime.now().date()
        if i.date != x:
            days=(x.day-i.date.day)
            d=int(i.days)+days
            total=float(i.total)+int(i.principal_amount)*(float(i.intrest)/100)/30*int(days)
            i.days=d
            i.total=round(total)
            i.date=x
            i.save()
            
     # current return month 
    returnData=Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=month,r_date__year=year) & Q(principal_amount__gt="0"))
    
    for i in returnData:
        x=datetime.now().date()
        if i.date!=x:
            days=(x.day-i.date.day)
            d=int(i.days)+days
            total=float(i.total)+int(i.principal_amount)*(float(i.intrest)/100)/30*int(days)
            i.days=d
            i.total=round(total)
            i.date=x
            i.save()
            
    # current only intrest return month 
    returnInt=Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=month,r_date__year=year) & Q(principal_amount='0'))
            
    
    
    # for previous month 
    
    previous_month = current_date - relativedelta(months=1)
    pmonth=previous_month.month
    pyear=previous_month.year
    pMonth_name=previous_month.strftime('%B')
    pres=Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=pmonth , p_date__year=pyear))
    
    previous_last_day_of_month = calendar.monthrange(2023, pmonth)[1]
    previous_last_date_of_month = f"2023-{pmonth:02d}-{previous_last_day_of_month:02d}"
    prev_date_object = datetime.strptime(previous_last_date_of_month, "%Y-%m-%d")
    previous_last_date=prev_date_object.day
    
    for i in pres:
        # x=datetime.now().date()
        s=i.date.day
        i.days=str(previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        # i.date=x
        i.save()
        
    # for prev return month
    preturnData=Return.objects.filter(Q(account_no=Account_no)& Q(r_date__month=pmonth,r_date__year=pyear) & Q(principal_amount__gt='0'))
    
    for i in preturnData:
        # x=datetime.now().date()
        s=i.date.day
        i.days=str(previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        i.save()
        
    # prev  only intrest return month 
    preturnInt=Return.objects.filter(Q(account_no=Account_no )& Q(principal_amount='0') & Q(r_date__month=pmonth,r_date__year=pyear) )
        
        
    
    
    # second previous month 
    second_previous_month = current_date - relativedelta(months=2)
    p2month=second_previous_month.month
    p2year=second_previous_month.year
    p2Month_name=second_previous_month.strftime('%B')
    p2res=Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p2month , p_date__year=p2year))
    
    second_previous_last_day_of_month = calendar.monthrange(2023, p2month)[1]
    second_previous_last_date_of_month = f"2023-{p2month:02d}-{second_previous_last_day_of_month:02d}"
    date_object = datetime.strptime(second_previous_last_date_of_month, "%Y-%m-%d")
    second_previous_last_date=date_object.day
            
    for i in p2res:
        # x=datetime.now().date()
        s=i.date.day
        i.days=str(second_previous_last_date-s)
        print(i.days)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        # i.date=x
        i.save()
        
    # for second prev return month
    p2returnData=Return.objects.filter(Q(account_no=Account_no)& Q(r_date__month=p2month,r_date__year=p2year) & Q(principal_amount__gt='0'))
    
    for i in p2returnData:
        s=i.date.day
        i.days=str(second_previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        i.save()
    
    # secondprev only intrest  month 
    p2returnInt=Return.objects.filter(Q(account_no=Account_no )& Q(principal_amount='0') & Q(r_date__month=p2month,r_date__year=p2year) )
        
    
        

    
    # third  previous month 
    
    third_previous_month = current_date - relativedelta(months=3)
    p3month=third_previous_month.month
    p3year=third_previous_month.year
    p3Month_name=third_previous_month.strftime('%B')
    p3res=Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p3month , p_date__year=p3year))
    
    third_previous_last_day_of_month = calendar.monthrange(2023, p3month)[1]
    third_previous_last_date_of_month = f"2023-{p3month:02d}-{third_previous_last_day_of_month:02d}"
    third_previous_date_object = datetime.strptime(third_previous_last_date_of_month, "%Y-%m-%d")
    third_previous_last_date=third_previous_date_object.day
    
    for i in p3res:
        # x=datetime.now().date()
        s=i.date.day
        i.days=str(third_previous_last_date-s)
        print(i.days)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        # i.date=x
        i.save()
    
    # for third  prev return  month
    p3returnData=Return.objects.filter(Q(account_no=Account_no)& Q(r_date__month=p3month,r_date__year=p3year) & Q(principal_amount__gt='0'))
    
    for i in p3returnData:
        s=i.date.day
        i.days=str(third_previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        i.save()
    
    # third  prev only intrest month 
    p3returnInt=Return.objects.filter(Q(account_no=Account_no )& Q(principal_amount='0') & Q(r_date__month=p3month,r_date__year=p3year) )
    
    
    
    # fourth   previous month 
    
    fourth_previous_month = current_date - relativedelta(months=4)
    p4month=fourth_previous_month.month
    p4year=fourth_previous_month.year
    p4Month_name=fourth_previous_month.strftime('%B')
    p4res=Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p4month , p_date__year=p4year))
    
    fourth_previous_last_day_of_month = calendar.monthrange(2023, p4month)[1]
    fourth_previous_last_date_of_month = f"2023-{p4month:02d}-{fourth_previous_last_day_of_month:02d}"
    fourth_previous_date_object = datetime.strptime(fourth_previous_last_date_of_month, "%Y-%m-%d")
    fourth_previous_last_date=fourth_previous_date_object.day
    
    for i in p4res:
        # x=datetime.now().date()
        s=i.date.day
        i.days=str(fourth_previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        # i.date=x
        i.save()
    
    # for fourth  prev return month
    p4returnData=Return.objects.filter(Q(account_no=Account_no)& Q(r_date__month=p4month,r_date__year=p4year) & Q(principal_amount__gt='0'))
    
    for i in p4returnData:
        s=i.date.day
        i.days=str(fourth_previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        i.save()
    
    # fourth  prev only intrest return  month 
    p4returnInt=Return.objects.filter(Q(account_no=Account_no )& Q(principal_amount='0') & Q(r_date__month=p4month,r_date__year=p4year) )
    
    
    
    # fifth   previous month 
    
    fifth_previous_month = current_date - relativedelta(months=5)
    p5month=fifth_previous_month.month
    p5year=fifth_previous_month.year
    p5Month_name=fifth_previous_month.strftime('%B')
    p5res=Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p5month , p_date__year=p5year))
    
    fifth_previous_last_day_of_month = calendar.monthrange(2023, p5month)[1]
    fifth_previous_last_date_of_month = f"2023-{p5month:02d}-{fifth_previous_last_day_of_month:02d}"
    fifth_previous_date_object = datetime.strptime(fifth_previous_last_date_of_month, "%Y-%m-%d")
    fifth_previous_last_date=fifth_previous_date_object.day
    
    for i in p5res:
        # x=datetime.now().date()
        s=i.date.day
        i.days=str(fifth_previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        # i.date=x
        i.save()
        
    # for fifth  prev return  month
    p5returnData=Return.objects.filter(Q(account_no=Account_no)& Q(r_date__month=p5month,r_date__year=p5year) & Q(principal_amount__gt='0'))
    
    for i in p5returnData:
        s=i.date.day
        i.days=str(fifth_previous_last_date-s)
        total=float(i.principal_amount)*(int(i.intrest)/100)/30*int(i.days)
        i.total=round(total)
        i.save()
    
    # fifth  prev only intrest return  month 
    p5returnInt=Return.objects.filter(Q(account_no=Account_no )& Q(principal_amount='0') & Q(r_date__month=p5month,r_date__year=p5year) )
    
    # current month calculation
    
    Pint=0
    Rint=0
    unpaidPrincipal_amount=0
    returnPrincipal_amount=0
    unIntrest=0
    reIntrest=0
    Advance=0
    PrevDues=0
    PaidInt=0
    for i in res:
        Pint+=float(i.total)
        unpaidPrincipal_amount+=int(i.principal_amount)
        unIntrest+=float(i.total)
    for j in returnData:
        Rint+=int(j.total)
        returnPrincipal_amount+=int(j.principal_amount)
        reIntrest+=int(j.total)
    for i in returnInt:
        PaidInt+=int(i.intrestAmount)
    result=unpaidPrincipal_amount-returnPrincipal_amount
    Mint=Pint-Rint
    total=(Mint+PrevDues+Advance)-PaidInt
    
    account_No=Register.objects.get(account_no=Account_no)
    
    
    # previous month calculation 
    
    pAdvance=0
    pPrevDues=0
    pPaidInt=0
    pPint = Payment.objects.filter(Q(account_no=Account_no) & Q(p_date__month=pmonth, p_date__year=pyear)).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    pRint = Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=pmonth, r_date__year=pyear)  & Q(principal_amount__gt='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    pPaidInt= Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=pmonth, r_date__year=pyear)& Q(principal_amount='0')).aggregate(total_sum=Coalesce(Sum('intrestAmount', output_field=IntegerField()), Value(0)))['total_sum']
    
    pMint=pPint-pRint
    ptotal=(pMint+pPrevDues+pAdvance)-pPaidInt
    
    
    # sum of payment principal amount of this month 
    previous_total_principal_amount =Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=pmonth , p_date__year=pyear)).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    pUtotal =Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=pmonth , p_date__year=pyear)).aggregate(total_principal=Coalesce(Sum('total',output_field=IntegerField()),Value(0)))['total_principal']
    
    # sum of return principal amount of this month 
    previous_total_return_amount = Return.objects.filter(Q(account_no=Account_no)&Q(r_date__month=pmonth , r_date__year=pyear) & Q(principal_amount__gt='0')).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    pRtotal = Return.objects.filter(Q(account_no=Account_no)&Q(r_date__month=pmonth , r_date__year=pyear) & Q(principal_amount__gt='0')).aggregate(total_principal=Coalesce(Sum('total',output_field=IntegerField()),Value(0)))['total_principal']
    
    prev_result=previous_total_principal_amount-previous_total_return_amount
    
    
    # second previous month calculation
    
    p2Advance=0
    p2PrevDues=0
    p2PaidInt=0
    p2Pint = Payment.objects.filter(Q(account_no=Account_no) & Q(p_date__month=p2month, p_date__year=p2year)).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p2Rint = Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p2month, r_date__year=p2year)  & Q(principal_amount__gt='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p2PaidInt= Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p2month, r_date__year=p2year)& Q(principal_amount='0')).aggregate(total_sum=Coalesce(Sum('intrestAmount', output_field=IntegerField()), Value(0)))['total_sum']
    
    p2Mint=p2Pint-p2Rint
    p2total=(p2Mint+p2PrevDues+p2Advance)-p2PaidInt


        
    # sum of payment principal amount of this month 
    second_previous_total_principal_amount = Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p2month , p_date__year=p2year)).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    # sum of return principal amount of this month 
    second_previous_total_return_amount = Return.objects.filter(Q(account_no=Account_no)&Q(r_date__month=p2month , r_date__year=p2year) & Q(principal_amount__gt='0')).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    secondPrev_result=second_previous_total_principal_amount-second_previous_total_return_amount
        
    
    # third previous month calculation 
    
    p3Advance=0
    p3PrevDues=0
    p3PaidInt=0
    p3Pint = Payment.objects.filter(Q(account_no=Account_no) & Q(p_date__month=p3month, p_date__year=p3year)).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p3Rint = Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p3month, r_date__year=p3year)  & Q(principal_amount__gt='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p3PaidInt= Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p3month, r_date__year=p3year)& Q(principal_amount='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']
    
    p3Mint=p3Pint-p3Rint
    p3total=(p3Mint+p3PrevDues+p3Advance)-p3PaidInt


        
    # sum of payment principal amount of this month 
    third_previous_total_principal_amount = Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p3month , p_date__year=p3year)).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    # sum of return principal amount of this month 
    third_previous_total_return_amount =Return.objects.filter(Q(account_no=Account_no)&Q(r_date__month=p3month , r_date__year=p3year) & Q(principal_amount__gt='0')).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    third_prev_result=third_previous_total_principal_amount-third_previous_total_return_amount
        
    # fourth previous month calculation
    
    p4Advance=0
    p4PrevDues=0
    p4PaidInt=0
    p4Pint = Payment.objects.filter(Q(account_no=Account_no) & Q(p_date__month=p4month, p_date__year=p4year)).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p4Rint = Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p4month, r_date__year=p4year)  & Q(principal_amount__gt='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p4PaidInt= Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p4month, r_date__year=p4year)& Q(principal_amount='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']
    
    p4Mint=p4Pint-p4Rint
    p4total=(p4Mint+p4PrevDues+p4Advance)-p4PaidInt

        
    # sum of payment principal amount of this month 
    fourth_previous_total_principal_amount = Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p4month , p_date__year=p4year)).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    # sum of return principal amount of this month 
    fourth_previous_total_return_amount = Return.objects.filter(Q(account_no=Account_no)&Q(r_date__month=p4month , r_date__year=p4year) & Q(principal_amount__gt='0')).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    fourthprev_result=fourth_previous_total_principal_amount-fourth_previous_total_return_amount
        
    # fifth month calculation 
    
    p5Advance=0
    p5PrevDues=0
    p5PaidInt=0
    p5Pint = Payment.objects.filter(Q(account_no=Account_no) & Q(p_date__month=p5month, p_date__year=p5year)).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p5Rint = Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p5month, r_date__year=p5year)  & Q(principal_amount__gt='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']

    p5PaidInt= Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=p5month, r_date__year=p5year)& Q(principal_amount='0')).aggregate(total_sum=Coalesce(Sum('total', output_field=IntegerField()), Value(0)))['total_sum']
    
    p5Mint=p5Pint-p5Rint
    p5total=(p5Mint+p5PrevDues+p5Advance)-p5PaidInt

        
    # sum of payment principal amount of this month 
    fifth_previous_total_principal_amount = Payment.objects.filter(Q(account_no=Account_no)&Q(p_date__month=p5month , p_date__year=p5year)).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    # sum of return principal amount of this month 
    fifth_previous_total_return_amount =Return.objects.filter(Q(account_no=Account_no)&Q(r_date__month=p5month , r_date__year=p5year) & Q(principal_amount__gt='0')).aggregate(total_principal=Coalesce(Sum('principal_amount',output_field=IntegerField()),Value(0)))['total_principal']
    
    fifth_prev_result=fifth_previous_total_principal_amount-fifth_previous_total_return_amount
    
    fine=''
    for j in returnData:
        fine=j.fine
        
    # previous dues and Advance 
    
    if (p5Pint+p5PrevDues)>(p5Rint+p5PaidInt+p5Advance):
        p4PrevDues = max(0, (p5Pint+p5PrevDues) - (p5Rint+p5PaidInt+p5Advance))
    else:
        p4Advance=((p5Rint+p5PaidInt+p5Advance)-(p5Pint+p5PrevDues))
        
        
    if (p4Pint+p4PrevDues)>(p4Rint+p4PaidInt+p4Advance):
        p3PrevDues = max(0, (int(p4Pint)+int(p4PrevDues)) - (p4Rint+p4PaidInt+p4Advance))
    else:
        p3Advance=((p4Rint+p4PaidInt+p4Advance)-(p4Pint+p4PrevDues))
        
        
    if (p3Pint+p3PrevDues)>(p3Rint+p3PaidInt+p3Advance):
        p2PrevDues = max(0, (p3Pint+p3PrevDues) - (p3Rint+p3PaidInt+p3Advance))
    else:
        p2Advance=((p3Rint+p3PaidInt+p3Advance)-(p3Pint+p3PrevDues))
        
    
    if (p2Pint+p2PrevDues)>(p2Rint+p2PaidInt+p2Advance):
        pPrevDues = max(0, (p2Pint+p2PrevDues) - (p2Rint+p2PaidInt+p2Advance))
    else:
        pAdvance=((p2Rint+p2PaidInt+p2Advance)-(p2Pint+p2PrevDues))
        
        
    if (pPint+pPrevDues)>(pRint+pPaidInt+pAdvance):
        PrevDues = max(0, (pPint+pPrevDues) - (pRint+pPaidInt+pAdvance))
    else:
        p=pRint+pPaidInt+pAdvance
        s=pPint+pPrevDues
        Advance=p-s
        
    param={'res':res, 'returnData':returnData ,'Pint':Pint ,'Rint':Rint, 'Mint':Mint,'Advance':Advance ,'PrevDues':PrevDues ,'PaidInt':PaidInt,'total':total ,'returnInt':returnInt ,"unpaidPrincipal_amount":unpaidPrincipal_amount ,"returnPrincipal_amount":returnPrincipal_amount , "result":result , "month_name":month_name ,"year":year  ,'pMonth_name':pMonth_name ,'pres':pres ,'preturnData':preturnData ,'preturnInt':preturnInt , 'p2Month_name':p2Month_name , 'p2res':p2res ,'p2returnData':p2returnData ,'p2returnInt':p2returnInt,'p3Month_name':p3Month_name ,'p3res':p3res ,'p3returnData':p3returnData ,'p3returnInt':p3returnInt ,'p4Month_name':p4Month_name,"p5Month_name":p5Month_name,'p4res':p4res ,'p5res':p5res ,'p4returnData':p4returnData,'p5returnData':p5returnData ,'p4returnInt':p4returnInt ,'p5returnInt':p5returnInt ,'account_No':account_No,'fine':fine ,'p2Pint':p2Pint , 'p2Rint':p2Rint ,'p2Mint':p2Mint,'p2PaidInt':p2PaidInt ,'p2PrevDues':p2PrevDues ,'p2Advance':p2Advance ,'p2total':p2total ,'pPint':pPint,'pRint':pRint,'pMint':pMint,'pPaidInt':pPaidInt,'pPrevDues':pPrevDues,'pAdvance':pAdvance,'ptotal':ptotal ,'p3Pint':p3Pint,'p3Rint':p3Rint,'p3Mint':p3Mint,'p3PaidInt':p3PaidInt,'p3PrevDues':p3PrevDues,'p3Advance':p3Advance,'p3total':p3total ,'p4Pint':p4Pint,'p4Rint':p4Rint,'p4Mint':p4Mint,'p4PaidInt':p4PaidInt,'p4PrevDues':p4PrevDues,'p4Advance':p4Advance,'p4total':p4total ,'p5Pint':p5Pint,'p5Rint':p5Rint,'p5Mint':p5Mint,'p5PaidInt':p5PaidInt,'p5PrevDues':p5PrevDues,'p5Advance':p5Advance,'p5total':p5total ,'previous_total_principal_amount':previous_total_principal_amount,'second_previous_total_principal_amount':second_previous_total_principal_amount,'third_previous_total_principal_amount':third_previous_total_principal_amount,'fourth_previous_total_principal_amount':fourth_previous_total_principal_amount,'fifth_previous_total_principal_amount':fifth_previous_total_principal_amount ,'previous_total_return_amount':previous_total_return_amount,'second_previous_total_return_amount':second_previous_total_return_amount,'third_previous_total_return_amount':third_previous_total_return_amount,'fourth_previous_total_return_amount':fourth_previous_total_return_amount,'fifth_previous_total_return_amount':fifth_previous_total_return_amount,'fifth_prev_result':fifth_prev_result,'fourthprev_result':fourthprev_result,'third_prev_result':third_prev_result ,'secondPrev_result':secondPrev_result ,'prev_result':prev_result ,'unIntrest':unIntrest,'reIntrest':reIntrest ,'pUtotal':pUtotal ,'pRtotal':pRtotal}
    
    return render(request, 'view.html' ,param)

def guaranterPage(request):
    return render(request , 'guaranter.html')

def NomneePage(request):
    return render(request , 'nomnee.html')

def NomneeAndGuarranterPage(request,courseID):
    res=Register.objects.filter(id=courseID)
    return render(request , 'NomniAndGuranter.html',{'res':res})

def guarranterList1Page(request):
    res=Register.objects.all()
    return render(request , 'guarranterList1.html',{'res':res})

def guarranterList2Page(request):
    res=Register.objects.all()
    return render(request , 'guarranterList2.html' , {'res':res})

def guarranterView1Page(request , name):
    res=Register.objects.filter(g1name=name)
    return render(request ,'guarranterView1.html',{'res':res} )

def guarranterView2Page(request , name):
    res=Register.objects.filter(g2name=name)
    return render(request , 'guarranterView2.html' , {'res':res})
    
def ActionPage(request,Account_no):
    res=Register.objects.get(account_no=Account_no)
    returnData=Return.objects.filter(account_no=Account_no)
    file_type = 'unknown'
    t = res.g1Document.url if res.g1Document else ''
    if t.endswith('.pdf'):
        file_type='pdf'
    elif t.endswith('.jpg') or t.endswith('.jpeg') or t.endswith('.png'):
        file_type='image'
        
    if request.method=='POST':
        new_limit=request.POST.get('newLimit')
        res.limit=new_limit
        res.save()
        
    if request.method=='POST':
        newfine=request.POST.get('newFine')
        for i in returnData:
            i.fine=newfine
            i.save()
    NewFine=''
    for i in returnData:
        NewFine=i.fine
    return render(request ,'action.html' ,{'res':res , 'file_type':file_type , 'returnData':returnData , 'NewFine':NewFine})
    
def GurranterPage(request ,Account_no):
    res=Register.objects.get(account_no=Account_no)
    return render(request , 'gurranter.html' , {'res':res})

def NomneePage(request , Account_no):
    res=Register.objects.get(account_no=Account_no)
    return render(request , 'nomnee.html',{'res':res})
    
def RateWisePrincipalAmountPage(request):
    res = Payment.objects.all()
    interest = []
    amount = []

    for i in res:
        amount.append(i.principal_amount)
        interest.append(i.intrest)

    interest_result = []
    amount_result = {}

    for i in range(len(interest)):
        int_interest = int(interest[i])

        if int_interest not in amount_result:
            amount_result[int_interest] = int(amount[i])
        else:
            amount_result[int_interest] += int(amount[i])

    interest_result, amount_result = zip(*sorted(amount_result.items()))
    

    params = {'interest_result': interest_result, 'amount_result': amount_result ,'res':zip(interest_result,amount_result)}

    return render(request, 'RateWisePrincipal.html', params)
    
def CurrentDuesDashboard(request):
    return render(request , 'CurrentDash.html')
    
def MonthlyReportPage(request):
    return render(request , 'MonthlyReport.html')

def weeklyReportPage(request):
    return render(request , 'weeklyReport.html')

def reportDashboardPage(request):
    return render(request , 'reportDashboard.html')
    
def AllPaymentPage(request , Account_no):
    res=Payment.objects.filter(account_no=Account_no)
    return render(request , 'allPayment.html' , {'res':res})
 
@csrf_exempt  
def Update_fine(request , Account_no):
    res_return_data = Return.objects.filter(account_no=Account_no)

    if request.method == 'POST':
        new_fine = request.POST.get('newFine')

        for i in res_return_data:
            i.fine = new_fine
            i.save()

        return JsonResponse({'success': True, 'new_fine': new_fine})

    return JsonResponse({'success': False})
    
def MonthOptionPage(request):
    return render(request , 'MonthOption.html')

def WeekOptionPage(request):
    return render(request , 'WeekOption.html')

def DaywiseOptionPage(request):
    return render(request , 'DaywiseOption.html')

def FifteenDaysOption(request):
    return render(request,'FifteenDaysOption.html')
    
def formatDate(dateObject):
    if isinstance(dateObject, date):  # Check if it's a date object
        formatted_date = dateObject.strftime('%Y-%m-%d')
    else:
        try:
            date_object = datetime.strptime(str(dateObject), '%b. %d, %Y')
            formatted_date = date_object.strftime('%Y-%m-%d')
        except ValueError:
            formatted_date = None  # Handle invalid date string gracefully, if needed
    return formatted_date
    
def EditPage(request , Account_no):
    res=Register.objects.get(account_no=Account_no)
    formatted_date = formatDate(res.Date_of_birth)
    if request.method=='POST':
        name=request.POST.get('rname')
        father_name=request.POST.get('father_name')
        rdob=request.POST.get('rdob')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        profession=request.POST.get('profession')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        alter_mobile=request.POST.get('alter_mobile')
        pic=request.FILES.get('pic')
        if pic:
            img=pic
        else:
            img= res.image.url if res.image else None
        address=request.POST.get('address')
        city=request.POST.get('city')
        district=request.POST.get('district')
        state=request.POST.get('state')
        pin=request.POST.get('pin')
        remarks=request.POST.get('remarks')
        document=request.FILES.get('document')
        if document:
            doc=document
        else:
            doc= res.Document.url if res.Document else None
        pincode=request.POST.get('pin')

        res.name=name
        res.father_name=father_name
        res.gender=gender
        res.Date_of_birth=rdob
        res.age=age
        res.city=city
        res.district=district
        res.state=state
        res.email=email
        res.profession=profession
        res.mobile=mobile
        res.alter_mobile=alter_mobile
        res.address=address
        res.remarks=remarks
        res.image=img
        res.Document=doc
        res.pinCode=pincode
        res.save()
        
    return render(request,'Edit.html' ,{'res':res ,'formatted_date':formatted_date})

def reportPage(request):
    return render(request , 'report.html')  

def FilterViewPage(request , Account_no):
    if request.method == 'GET':
        start=request.GET['start']
        end=request.GET['end'] 
        monttt=get_month_names_between(start , end)
        
        months, years = get_month_names_and_years_between(start, end)

        # Print each month name and year individually
        total_month=len(monttt)
        count=1
        payments={}
        returns={}
        paid_intrest={}
        for month , year in zip(months , years):
            payment_var_name = f"payment{count}"
            return_var_name = f"return{count}"
            paidInt_var_name = f"paidint{count}"
            month_number=month_name_to_number(month)
            payment_var_value = Payment.objects.filter(Q(account_no=Account_no) & Q( p_date__month=month_number , p_date__year=year))
            return_var_value=Return.objects.filter(Q(account_no=Account_no)& Q(r_date__month=month_number,r_date__year=year) & Q(principal_amount__gt='0'))
            paidInt_var_value=Return.objects.filter(Q(account_no=Account_no) & Q(r_date__month=month_number,r_date__year=year) & Q(principal_amount='0') )
            payments[payment_var_name] = payment_var_value
            returns[return_var_name]=return_var_value
            paid_intrest[paidInt_var_name]=paidInt_var_value
            count+=1

        data={
            'months':monttt , 
            'payments':payments , 
            'returns':returns , 
            'account_no':Account_no,
            'PaidInt':paid_intrest
        }
    return render(request , 'filterView.html' , data) 

def month_name_to_number(month_name):
    # Create a datetime object with a dummy day and the given month name
    date_obj = datetime.strptime(month_name, "%B")
    
    # Extract the month number from the datetime object (1 for January, 2 for February, etc.)
    month_number = date_obj.month
    
    return month_number 

def get_month_names_between(start_date_str, end_date_str):
    # Parse start and end dates into datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m')
    end_date = datetime.strptime(end_date_str, '%Y-%m')

    # Initialize variables
    current_date = start_date
    month_names = []

    # Iterate over each month between start and end date
    while current_date <= end_date:
        # Get month name and year for the current date
        month_name = datetime.strftime(current_date, '%B')  # Full month name
        year = current_date.year
        
        # Append month name and year to the list
        month_names.append(f"{month_name} {year}")

        # Move to the next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)

    return month_names 

def get_month_names_and_years_between(start_date_str, end_date_str):
    # Parse start and end dates into datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m')
    end_date = datetime.strptime(end_date_str, '%Y-%m')

    # Initialize variables
    current_date = start_date
    month_names = []
    years = []

    # Iterate over each month between start and end date
    while current_date <= end_date:
        # Get month name and year for the current date
        month_name = datetime.strftime(current_date, '%B')  # Full month name
        year = current_date.year
        
        # Append month name and year to the lists
        month_names.append(month_name)
        years.append(year)

        # Move to the next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)

    return month_names, years