from django.urls import path
from .views import SignupView,InsertLoanView,getData,InsertIntoUserAcc,getPrsonalData,PersonalDataSerializer,getLoanDeatilsAll,UpdateLoanView,getCustomerDashboardData,getResidenceDetails,getWorkDetails,getDocumentsDetails,DocumentInsertView,getArchivekDetails,getAllLoandata,SearchSales,SalesAction

urlpatterns=[
	path('signup',SignupView.as_view()),
	path('loan_insert',InsertLoanView.as_view()),
	path('insert_user_details',InsertIntoUserAcc.as_view()),
	path('update_user_details',UpdateLoanView.as_view()),
	path('get_loan_details',getLoanDeatilsAll.as_view()),
	path('get',getData.as_view()),
	path('getpersonal',getPrsonalData.as_view()),
	path('getdashboarddata',getCustomerDashboardData.as_view()),
	path('get_residence_details',getResidenceDetails.as_view()),
	path('get_work_details',getWorkDetails.as_view()),
	path('get_documents_details',getDocumentsDetails.as_view()),
	path('insert_documents_details',DocumentInsertView.as_view()),
	path('archive_details',getArchivekDetails.as_view()),
	path('quick_view',getAllLoandata.as_view()),
	path('search',SearchSales.as_view()),
	path('sales_action',SalesAction.as_view())	
]