from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.nav),
    path('login/',views.loginuser),
    path('home/',views.home),
    # path('register/',views.register_forms,name='register_forms'),
    path('register/<int:step>/',views.register_forms, name="registration_view"),
    path('list/',views.rlist  ,name="list"),
    path('dashboard/',views.Dashboard),
    path('calculate/',views.EMI_Calculator),
    path('day-wise/' , views.DayWise ),
    path('fifteen-days/' , views.fifteenDays),
    path('monthly/',views.Monthly),
    path('weekly/',views.Weekly),
    path('payment-page/<str:Account_no>/',views.paymentPage , name='payment-page'),
    path('return-page/<str:Account_no>/',views.returnPage,name='return-page'),
    path('view-page/<str:Account_no>/' , views.viewPage , name='view-page'),
    path('guarranter-page/', views.guaranterPage),
    path('nomnee-page/',views.NomneePage),
    path('nomiAndGuranter/<courseID>',views.NomneeAndGuarranterPage,name='nomiAndGuranter'),
    path('guaranter-page1/',views.guarranterList1Page),
    path('guaranter-page2/',views.guarranterList2Page),
    path('guarranter-view1/<str:name>/',views.guarranterView1Page , name='guarranter-view1'),
    path('guarranter-view2/<str:name>/',views.guarranterView2Page , name='guarranter-view2'),
    path('action/<str:Account_no>/',views.ActionPage ,name="action"),
    # path('image/<courseID>',views.ImagePage , name='image'),
    path('guarranter/<str:Account_no>/',views.GurranterPage ,name='guarranter'),
    path('nomnee/<str:Account_no>/' , views.NomneePage , name='nomnee'),
    path('rateWise/', views.RateWisePrincipalAmountPage),
    path('CurrentDuesDashboard/' , views.CurrentDuesDashboard),
    path('monthlyreport/',views.MonthlyReportPage),
    path('rdash/',views.reportDashboardPage),
    path('weeklyReport/',views.weeklyReportPage),
    path('allPayment/<str:Account_no>/',views.AllPaymentPage , name='allPayment'),
    path('update_fine/<str:Account_no>/', views.Update_fine, name='update_fine'),
    path('Monthlyoption/',views.MonthOptionPage ,name="option"),
    path('WeeklyOption/',views.WeekOptionPage),
    path('DaywiseOption/',views.DaywiseOptionPage),
    path('FifteenOption/',views.FifteenDaysOption ),
    path('edit/<str:Account_no>/',views.EditPage),
    path('monthlyList/',views.MonthlyList),
    path('toggle-active/<int:item_id>/', views.toggle_active, name='toggle_active'),
    path('filter-view/<str:Account_no>/',views.FilterViewPage , name='filter-view'),
    path('report-page/',views.reportPage),
    # path('fetch_data/', views.fetch_data, name='fetch_data'),

]