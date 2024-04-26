from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=200)
    father_name=models.CharField(max_length=200 ,null=True)
    gender=models.CharField(max_length=100 , null=True , blank=True)
    Date_of_birth=models.DateField(null=True, blank=True ,default="2023-01-01")
    age=models.CharField(max_length=20)
    city=models.CharField(max_length=200 , null=True)
    district=models.CharField(max_length=250 , null=True)
    state=models.CharField(max_length=200 , null=True)
    email=models.CharField(max_length=100 ,null=True)
    profession=models.CharField(max_length=200 , null=True)
    mobile=models.CharField(max_length=12 , null=True)
    alter_mobile=models.CharField(max_length=150 , null=True)
    address=models.TextField(null=True)
    remarks=models.TextField(null=True)
    image=models.ImageField(upload_to='images/' , default="" , null=True)
    time_duration=models.CharField(max_length=150 , default="" , null=True)
    account_no=models.CharField(max_length=20,default="")
    Document=models.FileField(upload_to='document/' ,null=True)
    pinCode=models.CharField(max_length=10 ,default='00000')
    is_active = models.BooleanField(default=True, help_text='Is the account active?')

    # gurranter 1 
    g1name=models.CharField(max_length=200 , default='')
    g1father_name=models.CharField(max_length=200 ,default='')
    g1DOB=models.DateField( blank=True , null=True,  default="2023-01-01")
    g1Age=models.CharField(max_length=12 , default='')
    g1Address=models.CharField(max_length=250 , default='')
    g1Relation=models.CharField(max_length=200 , default='')
    g1Adhar_no=models.CharField(max_length=12,default='')
    g1Image=models.ImageField(upload_to='images/' , default="")
    # g1Area=models.CharField(max_length=300,default='')
    g1City=models.CharField(max_length=200,default='')
    g1District=models.CharField(max_length=200,default='')
    g1State=models.CharField(max_length=100,default='')
    g1Mobile_NO=models.CharField(max_length=12,default='')
    g1Document=models.FileField(upload_to='document/', blank=True,null=True)

    # gurranter 2
    g2name=models.CharField(max_length=200,default='')
    g2father_name=models.CharField(max_length=200 ,default='')
    g2DOB=models.DateField(null=True, blank=True , default="2023-01-01")
    g2Age=models.CharField(max_length=12,default='')
    g2Address=models.CharField(max_length=250,default='')
    g2Relation=models.CharField(max_length=200,default='')
    g2Adhar_no=models.CharField(max_length=12,default='')
    g2Image=models.ImageField(upload_to='images/' , default='')
    # g2Area=models.CharField(max_length=300,default='')
    g2City=models.CharField(max_length=200,default='')
    g2District=models.CharField(max_length=200,default='')
    g2State=models.CharField(max_length=100,default='')
    g2Mobile_NO=models.CharField(max_length=12,default='')
    g2Document=models.FileField(upload_to='document/',  null=True)

    # # Nomneee
    nName=models.CharField(max_length=200,default='')
    nFather_name=models.CharField(max_length=200,default='')
    nMother_name=models.CharField(max_length=200,default='')
    nDOB=models.DateField(null=True, blank=True , default="2023-01-01")
    nAge=models.CharField(max_length=20,default='')
    nAdress=models.CharField(max_length=300,default='')
    nRelation=models.CharField(max_length=200 , default='')
    nAdhar_Number=models.CharField(max_length=15 , default='')
    nImage=models.ImageField(upload_to="images/" , default='')
    nArea=models.CharField(max_length=200 , default='')
    nCity=models.CharField(max_length=200 , default='')
    nDistrict=models.CharField(max_length=200 , default='')
    nState=models.CharField(max_length=100 , default='')
    nMobile_no=models.CharField(max_length=12 ,default='')
    nDocument=models.FileField(upload_to='document/' ,null=True)


    def __str__(self):
        return self.name
    

class Payment(models.Model):
    # account = models.ForeignKey(Register, on_delete=models.CASCADE , default='')
    account_no=models.CharField(max_length=100 , default="")
    name=models.CharField(max_length=200 , default='default_name')
    days=models.CharField(max_length=20 ,default='')
    principal_amount=models.CharField(max_length=200)
    intrest=models.CharField(max_length=10)
    total=models.CharField(max_length=200 , default='0')
    date=models.DateField(null=True , blank=True,default='2023-11-15')
    time_duration=models.CharField(max_length=150,default="")
    p_date=models.DateField(null=True , blank=True)
    remarks=models.CharField(max_length=500 , default='')

    @property
    def model_type(self):
        return 'Payment'

class Return(models.Model):
    # account = models.ForeignKey(Register, on_delete=models.CASCADE , default='')
    account_no=models.CharField(max_length=100 , default="")
    name=models.CharField(max_length=200,default="default_name")
    days=models.CharField(max_length=20,default='0')
    principal_amount=models.CharField(max_length=200,default="0")
    intrest=models.CharField(max_length=10)
    total=models.CharField(max_length=200,default='0')
    date=models.DateField(null=True , blank=True )
    time_duration=models.CharField(max_length=150 , default='')
    r_date=models.DateField(null=True , blank=True)
    intrestAmount=models.IntegerField(default=0)
    fine=models.CharField(max_length=200 ,default='0')
    remarks=models.CharField(max_length=500 , default='')

    @property
    def model_type(self):
        return 'Return'

class ActuallyIntrest(models.Model):
    # account = models.ForeignKey(Register, on_delete=models.CASCADE , default='')
    account_no=models.CharField(max_length=100 , default="")
    name=models.CharField(max_length=100,default="")
    totalUnpaid=models.IntegerField(default=0)
    totalReturn=models.IntegerField(default=0)
    adv=models.IntegerField(default=0)
    mInterest=models.IntegerField(default=0)
    PrevDues=models.IntegerField(default=0)
    Pint=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    father_name=models.CharField(max_length=100 , default='')
    adress=models.CharField(max_length=500 ,default='')
    a_date=models.DateField(null=True , blank=True)




