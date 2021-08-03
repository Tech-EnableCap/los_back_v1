from django.contrib.auth import get_user_model
from django.db.models import Q
import datetime
from rest_framework import status
User=get_user_model()
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import UserAccount,LoanForms,Archive
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer,UserAccountSerializer,LoanFormsSerializer,CheckPrevSerializer,PersonalDataSerializer,ApplicantDashboardSerialer,ResidenceSerializer,UserUpdatetSerializer,WorkSerializer,getDocumentsSerializer,getDocumentsSerializer,InsertPersonaldocs,InsertBankdocs,getArchiveDataSerializer,SearchByEmailSerializer,SubmitFlagSerializer
#from django.core.mail import EmailMessage 
#from django.core.mail import send_mail
#from django.conf import settings


# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer

class SignupView(APIView):
	permission_classes=(permissions.AllowAny, )

	def post(self,request,format=None):
		data=self.request.data
		first_name=data['first_name']
		last_name=data['last_name']
		email=data['email']
		phone=data['phone']
		password=data['pass']
		repass=data['repass']

		if(password==repass):
			if User.objects.filter(email=email).exists():
				return Response({
						"error":"email already exists"
					})
			else:
				if(len(password)<6):
					return Response({
							"error":"password must be atleast 6 chars of length"
						})
				else:
					user=User.objects.create_user(email=email,first_name=first_name,
						last_name=last_name,phone=phone,password=password)
					user.save()
					return Response({
							"success":"user created"
						})
		else:
			return Response({
					"error":"passwords don't match"
				})


class getData(APIView):
	def post(self,request,format=None):
		query_email=self.request.data['email']
		if not UserAccount.objects.filter(email=query_email):
			return Response({
					'flag':'0'
				})
		data=UserAccount.objects.filter(email=query_email)
		serialize=CheckPrevSerializer(data,many=True)
		return Response(serialize.data)


class getPrsonalData(APIView):
	def post(self,request,format=None):
		query_email=self.request.data['email']
		if not UserAccount.objects.filter(email=query_email):
			return Response({
					'flag':'0'
				})
		data=UserAccount.objects.filter(email=query_email)
		serialize=PersonalDataSerializer(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)


class InsertIntoUserAcc(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		status={}
		if not UserAccount.objects.filter(id=query_id).exists():
			return Response({
					"error":"no data related to the id"
				})

		if 'dob' in self.request.data:
			dob=self.request.data['dob']
			date=datetime.datetime.strptime(dob,"%Y-%m-%d")
			if(date>=datetime.datetime.now()):
				return Response({
						"error":"invalid dob"
					})
			else:
				date_gap=datetime.datetime.now()-date
				if(date_gap.days/365)<18:
					return Response({
							"error":"must be 18 years old"
						})

		if 'monthly_sal' in self.request.data and 'total_work_exp' in self.request.data and 'cur_job_exp' in self.request.data:
			print("here")
			if(int(self.request.data["monthly_sal"])<=0):
				return Response({
						"error":"please put valid monthly salary amount"
					})
			if(int(float(self.request.data["cur_job_exp"]))>int(float(self.request.data["total_work_exp"]))):
				return Response({
						"error":"number of years in current job must be less of equal to total work experience"
					})

		if('form_status' in self.request.data):
			status['form_status']=self.request.data['form_status']
			del self.request.data['form_status']

		data=UserAccount.objects.get(id=query_id)
		del self.request.data['id']
		serialize=UserUpdatetSerializer(instance=data,data=self.request.data,partial=True)
		print(serialize)
		if(serialize.is_valid(raise_exception=True)):
			serialize.save()
			if status:
				obj=LoanForms.objects.get(applicant_id=query_id)
				loan_serialize=SubmitFlagSerializer(instance=obj,data=status,partial=True)
				if(loan_serialize.is_valid(raise_exception=True)):
					loan_serialize.save()
					return Response({
					"success":"data added"
				})

			return Response({
					"success":"data added"
				})



class InsertLoanView(APIView):
	#permission_classes=(permissions.IsAuthenticated, )
	def post(self,request,format=None):
		query_id=self.request.data['applicant_id']

		if not LoanForms.objects.filter(applicant_id=query_id).exists():
			if 'course_tenure' in self.request.data and 'loan_tenure' in self.request.data and 'financing_required' in self.request.data and 'course_fee' in self.request.data:
				if(int(self.request.data["loan_tenure"])>int(self.request.data["course_tenure"])):
					return Response({
						"error":"Loan tenure must not be greater than course tenure"
					})
				if(int(self.request.data["financing_required"])>int(self.request.data["course_fee"])):
					return Response({
						"error":"Financing required must not be greater than course fee amount"
					})
			else:
				return Response({
						"error":"Invalid Request !!"
					})

			serialize=LoanFormsSerializer(data=self.request.data)
			flag={'flag':self.request.data['flag']}
			del self.request.data['flag']
			if(serialize.is_valid(raise_exception=True)):

				user_data=UserAccount.objects.get(id=query_id)
				user_serialize=UserAccountSerializer(instance=user_data,data=flag,partial=True)

				if (user_serialize.is_valid(raise_exception=True)):
					serialize.save()
					user_serialize.save()

				return Response({
							"success":"saved"
						})
		else:
			return Response({
					"error":"no user"
				})


class DocumentInsertView(APIView):

	def post(self,request,format=None):
		if(len(self.request.data)==2):
			return Response({
						"error":"Data already updated"
					})
		query_id=self.request.data['id']
		 
		user_data=UserAccount.objects.get(id=query_id)
		loan_data=LoanForms.objects.get(applicant_id=query_id)

		print(self.request.data)


		obj=LoanForms.objects.get(applicant_id=query_id)
		obj_usr=UserAccount.objects.get(id=query_id)

		for i in list(self.request.data.keys()):
			if i!='id' and i!='flag':
				if i=='file1' or i=='file2' or i=='file3' or i=='file4':
					getattr(obj_usr,i).delete()
				else:
					getattr(obj,i).delete()
			if(self.request.data[i]=='undefined'):
				del self.request.data[i]
						

		del self.request.data['id']
		user_serialize=InsertPersonaldocs(instance=user_data,data=self.request.data,partial=True)
		print(user_serialize)
		if (user_serialize.is_valid(raise_exception=True)):
			if('file1' in self.request.data):
				del self.request.data['file1']
			if('file2' in self.request.data):
				del self.request.data['file2']
			if('file3' in self.request.data):
				del self.request.data['file3']
			if('file4' in self.request.data):
				del self.request.data['file4']
			serialize=InsertBankdocs(instance=loan_data,data=self.request.data,partial=True)
			print(serialize)
			if(serialize.is_valid(raise_exception=True)):
				user_serialize.save()
				serialize.save()
				return Response({
							"success":"saved"
						})
			else:
				return Response({
						"error":"server error"
					})
		else:
			return Response({
						"error":"server error"
					})


class getLoanDeatilsAll(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		if not UserAccount.objects.filter(id=query_id).exists():
			return Response({
					'error':'no user'
				})
		data=UserAccount.objects.filter(id=query_id)
		serialize=UserAccountSerializer(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)


class UpdateLoanView(APIView):
	def patch(self,request,format=None):
		query_id=self.request.data['applicant_id']
		if not LoanForms.objects.filter(applicant_id=query_id).exists():
			return Response({
					"error":"no data related to the id"
				})
		
		data=LoanForms.objects.get(applicant_id=query_id)
		del self.request.data['applicant_id']
		serialize=LoanFormsSerializer(instance=data,data=self.request.data,partial=True)
		if(serialize.is_valid(raise_exception=True)):
			serialize.save()
			return Response({
					"success":"data updated"
				})
		else:
			return Response({
					"error":"server error"
				})

class getCustomerDashboardData(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		if not UserAccount.objects.filter(id=query_id).exists():
			return Response({
					'error':'no user'
				})
		data=UserAccount.objects.filter(id=query_id)
		serialize=ApplicantDashboardSerialer(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)

class getResidenceDetails(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		if not UserAccount.objects.filter(id=query_id).exists():
			return Response({
					'error':'no user'
				})
		data=UserAccount.objects.filter(id=query_id)
		serialize= ResidenceSerializer(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)


class getWorkDetails(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		if not UserAccount.objects.filter(id=query_id).exists():
			return Response({
					'error':'no user'
				})
		data=UserAccount.objects.filter(id=query_id)
		serialize= WorkSerializer(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)


class getDocumentsDetails(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		if not UserAccount.objects.filter(id=query_id).exists():
			return Response({
					'error':'no user'
				})
		data=UserAccount.objects.filter(id=query_id)
		serialize=getDocumentsSerializer(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)


class getArchivekDetails(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		if not Archive.objects.filter(applicant_id=query_id).exists():
			return Response({
					'error':'no user'
				})
		data=Archive.objects.filter(applicant_id=query_id)
		serialize=getArchiveDataSerializer(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)


class getAllLoandata(APIView):
	def post(self,request,format=None):
		query_data=self.request.data
		per_page=1
		page_index=self.request.data['idx']
		start_at=int(page_index)*per_page
		end=(int(page_index)+1)*per_page
		data=LoanForms.objects.filter(form_status='submit').filter(sales_approve="false").select_related('applicant_id')[start_at:end]
		#data=LoanForms.objects.all().select_related('applicant_id')[start_at:end]
		#print(LoanForms.objects.all().select_related('applicant_id'))
		serialize=LoanFormsSerializer(data,many=True)
		out=serialize.data
		if(query_data['count']=="true"):
			count=LoanForms.objects.filter(form_status='submit').filter(sales_approve="false").select_related('applicant_id').count()
			out.append(count)
		return Response(out,status=status.HTTP_200_OK)


class SearchSales(APIView):
	def post(self,request,format=None):
		data=self.request.data
		if(data['type']=='email'):
			if not UserAccount.objects.filter(email=data['value'].strip()).exists():
				return Response({
						'error':'no applicant found'
					})
			get_data=UserAccount.objects.filter(email=data['value'].strip())
			serialize=SearchByEmailSerializer(get_data,many=True)
			return Response(serialize.data,status=status.HTTP_200_OK)
		elif(data['type']=='id'):
			if not LoanForms.objects.filter(id=data['value'].strip()).exists():
				return Response({
						'error':'no applicant found'
					})
			get_data=LoanForms.objects.filter(id=data['value'].strip()).select_related('applicant_id')
			serialize=LoanFormsSerializer(get_data,many=True)
			return Response(serialize.data,status=status.HTTP_200_OK)

class SalesAction(APIView):
	def post(self,request,format=None):
		data=self.request.data
		action_dict={}
		if(data['action']=='approve'):
			action_dict['sales_approve']="true"
		if(data['action']=='coapp'):
			action_dict['coapp_required']="true"
		if(data['action']=='nocoapp'):
			action_dict['coapp_required']="false"

		try:
			for i in data['id']:
				get_data=LoanForms.objects.get(id=i)
				print(get_data)
				serialize=LoanFormsSerializer(instance=get_data,data=action_dict,partial=True)
				if(serialize.is_valid(raise_exception=True)):
					serialize.save()
			return Response({
					"success":"done"
				})
		except Exception as e:
				return Response({
							"error":"server error"
						})


		
		