# forms.py
from django import forms
from .models import Register

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['name','father','gender','limit','rate_of_interest','join_date','Date_of_birth','age','area','city','district','state','email','profession','mobile','alter_mobile','address','remarks','image','time_duration','account_no','g1name','g1father_name','g1DOB','g1Age','g1Address','g1Relation','g1Adhar_no','g1Image','g1Area','g1City','g1District','g1State','g1Mobile_NO','g1Document','g2name','g2father_name','g2DOB','g2Age','g2Address','g2Relation','g2Adhar_no','g2Image','g2Area','g2City','g2District','g2State','g2Mobile_NO','g2Document','nName','nFather_name','nMother_name','nDOB','nAge','nAdress','nRelation','nAdhar_Number','nImage','nArea','nCity','nDistrict','nState','nMobile_no','nDocument']
        # Add other fields as needed
