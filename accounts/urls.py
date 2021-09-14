from django.urls import path
from .views import SignupView,InsertLoanView,getData,InsertIntoUserAcc,getPrsonalData,PersonalDataSerializer,getLoanDeatilsAll,UpdateLoanView,getCustomerDashboardData,getResidenceDetails,getWorkDetails,getDocumentsDetails,DocumentInsertView,getArchivekDetails,getAllLoandata,SearchSales,SalesAction,InsertAdditional,CoAppData,DeleteLoanRow,CoAppRequest,DocumentInsertViewCoApp,getDocumentsDetailsCoapp
from .views import RequestPass,setNewPass,PasswordTokenCheck,VerifyPhone,GetEquifax,GenEsign

urlpatterns=[
	path('signup',SignupView.as_view()),
	#path('password_reset/<uidb64>/<token>/',PasswordTokenCheck.as_view(),name='password_reset_confirm'),
	path('check_validity',PasswordTokenCheck.as_view()),
	path('request_reset_email',RequestPass.as_view(),name='request_reset_email'),
	path('password_reset',setNewPass.as_view(),name='password_reset'),
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
	path('sales_action',SalesAction.as_view()),
	path('insert_additional',InsertAdditional.as_view()),
	path('get_coapp',CoAppData.as_view()),
	path('delete_loan',DeleteLoanRow.as_view()),
	path('register_coapp',CoAppRequest.as_view()),
	path('insert_coapp_docs',DocumentInsertViewCoApp.as_view()),
	path('get_coapp_docs',getDocumentsDetailsCoapp.as_view()),
	path('phone_verify',VerifyPhone.as_view()),
	path('efx',GetEquifax.as_view()),
	path('esign',GenEsign.as_view())
]