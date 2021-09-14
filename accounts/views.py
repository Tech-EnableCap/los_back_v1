from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import datetime
from rest_framework import status
User=get_user_model()
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import UserAccount,LoanForms,Archive,ArchiveReject
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer,UserAccountSerializer,LoanFormsSerializer,CheckPrevSerializer,PersonalDataSerializer,ApplicantDashboardSerialer,ResidenceSerializer,UserUpdatetSerializer,WorkSerializer,getDocumentsSerializer,getDocumentsSerializer,InsertPersonaldocs,InsertBankdocs,getArchiveDataSerializer,SearchByEmailSerializer,SubmitFlagSerializer,AdditionalSerializer,InsertLoanFormsSerializer,CoAppInsertBankdocs,getDocumentsSerializerCoapp,QuickViewSerializer,getArchiveDataApprovedSerializer
from .serializer import ResetPassSerializer,setNewPassSerializer,PhoneValidateSerializer,EnachSerializer,EsignSerializer
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

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




class RequestPass(APIView):
	permission_classes=(permissions.AllowAny, )
	serializer_class=ResetPassSerializer

	def post(self,request):
		serializer=self.serializer_class(data=request.data)
		email=request.data['email']

		if UserAccount.objects.filter(email=email).exists():
			user=UserAccount.objects.get(email=email)
			uidb64=urlsafe_base64_encode(force_bytes(user.id))
			token=PasswordResetTokenGenerator().make_token(user)
			current_site=os.getenv('DOMAIN')
			relativelink=uidb64+"/"+token
			#current_site=get_current_site(request=request).domain

			#relativelink=reverse('password_reset_confirm',kwargs={
					#'uidb64':uidb64,
					#'token':token
				#})

			absurl="http://"+current_site+"/"+relativelink
			subject="Reset Your Account Password"  
			msg="Hello, \nAs you have requested a password reset to your profile account, please click on the below link to reset your password: \n\n"+absurl+"\n\nThe URL is to be used for one attempt ONLY.\n\nIf you don’t wish to reset your password, disregard this email and no action will be taken.\n\nThanks,\nTeam EnableCap" 
			to=user.email
			res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])

		return Response({
				'success':'We have sent you a link to reset your password'
			},status=status.HTTP_200_OK)



class GenEsign(APIView):
	def post(self,request,format=None):
		body={}
		if(self.request.data['json']['isCoapp']['coapp']=="true"):
			coords={
				self.request.data['json']['data']['appEmail'] : {
                    "1": [
                        {
                            "llx": 160,
                            "lly": 177,
                            "urx": 286,
                            "ury": 194
                        }
                    ],
                    "3": [
                        {
                            "llx": 67,
                            "lly": 144,
                            "urx": 202,
                            "ury": 168
                        }
                    ],
                    "7": [
                        {
                            "llx": 161,
                            "lly": 507,
                            "urx": 287,
                            "ury": 535
                        }
                    ]
                },
                self.request.data['json']['data']['coAppEmail'] : {
                    "1": [
                        {
                            "llx": 433,
                            "lly": 158,
                            "urx": 578,
                            "ury": 191
                        }
                    ],
                    "7": [
                        {
                            "llx": 440,
                            "lly": 496,
                            "urx": 585,
                            "ury": 526
                        }
                    ]
                }
			}
			body['signers']=[
				{
					'identifier' : self.request.data['json']['data']['appEmail'],
                	'name' : self.request.data['json']['formData']['borrower_name'],
                	'sign_type' : 'electronic',
				},
				{
					'identifier' : self.request.data['json']['data']['coAppEmail'],
                	'name' : self.request.data['json']['formData']['guarantor_name'],
                	'sign_type' : 'electronic',
				}
			]
			body['templates'] = [
				{
	            	'template_key' : 'TMP210407181952499T116TA1GMP9ORJ',
	            	'template_values' : self.request.data['json']['formData']
	        	}
        	]
		else:
			coords={
				'0' : {
                    "1": [
                        {
                            "llx": 160,
                            "lly": 177,
                            "urx": 286,
                            "ury": 194
                        }
                    ],
                    "3": [
                        {
                            "llx": 67,
                            "lly": 144,
                            "urx": 202,
                            "ury": 168
                        }
                    ],
                    "7": [
                        {
                            "llx": 161,
                            "lly": 507,
                            "urx": 287,
                            "ury": 535
                        }
                    ]
                }
			}
			body['signers']=[
				{
					'identifier' : self.request.data['json']['data']['appPhone'],
                	'name' : 'appName',
                	'sign_type' : 'electronic',
				}
			]
			body['templates'] = [
				{
	            	'template_key' : 'TMP2103311223419059MCFY81KLAEYJB',
	            	'template_values' : self.request.data['json']['formData']
	        	}
        	]

		body['send_sign_link'] = True;
		body['notify_signers'] = True;
		body['file_name'] =  self.request.data['json']['data']['fileName'] + ".pdf";
		body['display_on_page'] = 'custom';
		body['sign_coordinates'] = coords;

		#print(json.dumps(body))
		#print(self.request.data['json']['header'])
		#print("///////////////////")

		req=requests.post("https://api.digio.in/v2/client/template/multi_templates/create_sign_request",data=json.dumps(body),headers=self.request.data['json']['header'])
		print(json.loads(req.text))
		response_data=json.loads(req.text)
		if("id" in response_data):
			esign_data={}
			esign_data['esignId']=response_data["id"]
			esign_data["esign_status"]="requested"
			loan_id=self.request.data['json']['data']['fileName'].split("_")[1]
			get_data=LoanForms.objects.get(id=loan_id)
			serialize=EsignSerializer(instance=get_data,data=esign_data,partial=True)
			if(serialize.is_valid(raise_exception=True)):
				serialize.save()
				return Response({
						"success":"done"
					})
			else:
				return Response({
						"error":"server error"
					})
		else:
			return Response({
						"error":"server error"
					})



class GetEquifax(APIView):
	def post(self,request,format=None):
		body={
	        "RequestHeader":{
	           "CustomerId": os.environ.get("efxCustId"),   
	           "UserId": os.environ.get("efxUserId"), 
	           "Password": os.environ.get("efxPassword"), 
	           "MemberNumber": os.environ.get("efxMemberNo"),   
	           "SecurityCode":os.environ.get("efxSecurityCode"), 
	           "CustRefField":"",
	           "ProductCode":[
	              "CCR"
	           ]
	        },
	        "RequestBody":{
	           "InquiryPurpose":"00",
	           "FirstName":"",  
	           "MiddleName":"",
	           "LastName":"", 
	           "DOB":"", 
	           "InquiryAddresses":[
	              {
	                 "seq":"1",
	                 "AddressType":[
	                    "H"
	                 ],
	                 "AddressLine1":"", 
	                 "State":"", 
	                 "Postal":"" 
	              }
	           ],
	           "InquiryPhones":[
	              {
	                 "seq":"1",
	                 "Number":"", 
	                 "PhoneType":[
	                    "M"
	                 ]
	              }
	           ],
	           "IDDetails":[
	              {
	                 "seq":"1",
	                 "IDType":"T",
	                 "IDValue":"", 
	                 "Source":"Inquiry"
	              },
	              {
	                 "seq":"2",
	                 "IDType":"P",
	                 "IDValue":"",
	                 "Source":"Inquiry"
	              },
	              {
	                 "seq":"3",
	                 "IDType":"V",
	                 "IDValue":"",
	                 "Source":"Inquiry"
	              },
	              {
	                 "seq":"4",
	                 "IDType":"D",
	                 "IDValue":"",
	                 "Source":"Inquiry"
	              },
	              {
	                 "seq":"5",
	                 "IDType":"M",
	                 "IDValue":"",
	                 "Source":"Inquiry"
	              },
	              {
	                 "seq":"6",
	                 "IDType":"R",
	                 "IDValue":"",
	                 "Source":"Inquiry"
	              },
	              {
	                 "seq":"7",
	                 "IDType":"O",
	                 "IDValue":"",
	                 "Source":"Inquiry"
	              }
	           ],
	           "MFIDetails":{
	              "FamilyDetails":[
	                 {
	                    "seq":"1",
	                    "AdditionalNameType":"K02",
	                    "AdditionalName":""
	                 },
	                 {
	                    "seq":"2",
	                    "AdditionalNameType":"K02",
	                    "AdditionalName":""
	                 }
	              ]
	           }
	        },
	        "Score":[
	           {
	              "Type":"ERS",
	              "Version":"3.1"
	           }
	        ]
     	}
		body["RequestBody"]["FirstName"]=self.request.data["fname"]
		body["RequestBody"]["MiddleName"]=self.request.data["mname"]
		body["RequestBody"]["LastName"]=self.request.data["lname"]
		body["RequestBody"]["DOB"]=self.request.data["dob"]
		body["RequestBody"]["InquiryAddresses"][0]["AddressLine1"]=self.request.data["addr1"]
		body["RequestBody"]["InquiryAddresses"][0]["State"]=self.request.data["state"]
		body["RequestBody"]["InquiryAddresses"][0]["Postal"]=self.request.data["postal"]
		body["RequestBody"]["InquiryPhones"][0]["Number"]=self.request.data["mob"]
		body["RequestBody"]["IDDetails"][0]["IDValue"]=self.request.data["pan"]
		body["RequestHeader"]["CustRefField"]="EFX"+self.request.data["pan"]

		print(body)
		
		req=requests.post("https://ists.equifax.co.in/cir360service/cir360report",data=body)
		print(json.loads(req.text))
		return Response({
						'success':'ok'
					})



class PasswordTokenCheck(APIView):
	permission_classes=(permissions.AllowAny, )
	def post(self,request):
		try:
			uidb64=self.request.data['id']
			token=self.request.data['token']
			idx=smart_str(urlsafe_base64_decode(uidb64))
			user=UserAccount.objects.get(id=idx)

			if not PasswordResetTokenGenerator().check_token(user,token):
				return Response({
						'error':'token invalid, please request a new one'
					},status=status.HTTP_401_UNAUTHORIZED)

			return Response({
						'success':'credentials valid',
						'uidb64':uidb64,
						'token':token
					},status=status.HTTP_200_OK)

		except DjangoUnicodeDecodeError as e:
			return Response({
						'error':'token invalid, please request a new one'
					},status=status.HTTP_401_UNAUTHORIZED)


class setNewPass(APIView):
	permission_classes=(permissions.AllowAny, )
	serializer_class=setNewPassSerializer

	def patch(self,request):
		serializer=self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response({
				'success':'password reset'
			},status=status.HTTP_200_OK)




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
						"error":"Invalid Date of Birth"
					})
			else:
				date_gap=datetime.datetime.now()-date
				if(date_gap.days/365)<18:
					return Response({
							"error":"User must be 18 years old or above."
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
			if(self.request.data['mode']=='coapp'):
				insert_flag={
					'flag':self.request.data['flag']
				} 
				data=UserAccount.objects.get(id=query_id)
				email=data.email
				serialize=UserUpdatetSerializer(instance=data,data=insert_flag,partial=True)
				if(serialize.is_valid(raise_exception=True)):
					serialize.save()
					subject="SUBJECT - Thank You for Choosing EnableCap"  
					msg="Hello,\nYour loan application has beed submitted\nOur team will reach out to you soon. If you have any additional queries, you may call us at  +91 76050 10116.\n\nThanks,\nTeam EnableCap"  
					to=email
					res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
					if(res==1):
						return Response({
							"success":"data added"
						})
					else:
						msg="Server Error"
				else:
					Response({
						"success":"data added"
					})
			status['form_status']=self.request.data['form_status']
			del self.request.data['form_status']

		data=UserAccount.objects.get(id=query_id)
		email=data.email
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
					subject="SUBJECT - Thank You for Choosing EnableCap"  
					msg="Hello,\nYour loan application has beed submitted\nOur team will reach out to you soon. If you have any additional queries, you may call us at  +91 76050 10116.\n\nThanks,\nTeam EnableCap"  
					to=email
					res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
					if(res==1):
						return Response({
							"success":"data added"
						})
					else:
						msg="Server Error"

			return Response({
						"success":"data added"
					})



class InsertLoanView(APIView):
	#permission_classes=(permissions.IsAuthenticated, )
	def post(self,request,format=None):
		query_id=self.request.data['applicant_id']

		print(self.request.data)

		if not LoanForms.objects.filter(applicant_id=query_id).exists():
			if 'course_tenure' in self.request.data and 'loan_tenure' in self.request.data and 'financing_required' in self.request.data and 'course_fee' in self.request.data:
				if(int(self.request.data["loan_tenure"])>int(self.request.data["course_tenure"])):
					return Response({
						"error":"Loan tenure should not be greater than course tenure"
					})
				if(int(self.request.data["financing_required"])>int(self.request.data["course_fee"])):
					return Response({
						"error":"Amount of financing required must be greater than zero and should not exceed Course Fee Amount"
					})
			else:
				return Response({
						"error":"Invalid Request !!"
					})

			serialize=InsertLoanFormsSerializer(data=self.request.data)
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
		query_id=self.request.data['id']
		 
		user_data=UserAccount.objects.get(id=query_id)
		loan_data=LoanForms.objects.get(applicant_id=query_id)

		print(self.request.data)

		if(len(self.request.data)==4):
			bank_dict={}
			bank_dict['applicant_bank_acc']=self.request.data['applicant_bank_acc']
			bank_dict['applicant_ifsc']=self.request.data['applicant_ifsc']
			serialize=InsertBankdocs(instance=loan_data,data=bank_dict,partial=True)
			if(serialize.is_valid(raise_exception=True)):
				serialize.save()
				return Response({
							"success":"saved"
						})


		obj=LoanForms.objects.get(applicant_id=query_id)
		obj_usr=UserAccount.objects.get(id=query_id)

		for i in list(self.request.data.keys()):
			print(i)
			if i!='id' and i!='flag' and i!='applicant_bank_acc' and i!='applicant_ifsc':
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


class DocumentInsertViewCoApp(APIView):

	def post(self,request,format=None):
		query_id=self.request.data['id']
		 
		user_data=UserAccount.objects.get(id=query_id)
		loan_data=LoanForms.objects.get(co_applicant_id=query_id)

		print(self.request.data)

		if(len(self.request.data)==4):
			bank_dict={}
			bank_dict['coapp_ban_acc']=self.request.data['coapp_ban_acc']
			bank_dict['coapp_ifsc']=self.request.data['coapp_ifsc']
			serialize=InsertBankdocs(instance=loan_data,data=bank_dict,partial=True)
			if(serialize.is_valid(raise_exception=True)):
				serialize.save()
				return Response({
							"success":"saved"
						})


		obj=LoanForms.objects.get(co_applicant_id=query_id)
		obj_usr=UserAccount.objects.get(id=query_id)

		for i in list(self.request.data.keys()):
			if i!='id' and i!='flag' and i!='coapp_ban_acc' and i!='coapp_ifsc':
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
			serialize=CoAppInsertBankdocs(instance=loan_data,data=self.request.data,partial=True)
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

		if 'course_tenure' in self.request.data and 'loan_tenure' in self.request.data and 'financing_required' in self.request.data and 'course_fee' in self.request.data:
			if(int(self.request.data["loan_tenure"])>int(self.request.data["course_tenure"])):
				return Response({
					"error":"Loan tenure should not be greater than course tenure"
				})
			if(int(self.request.data["financing_required"])>int(self.request.data["course_fee"])):
				return Response({
					"error":"Amount of financing required must be greater than zero and should not exceed Course Fee Amount"
				})
		else:
			return Response({
					"error":"Invalid Request !!"
				})
			
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

class getDocumentsDetailsCoapp(APIView):
	def post(self,request,format=None):
		query_id=self.request.data['id']
		if not UserAccount.objects.filter(id=query_id).exists():
			return Response({
					'error':'no user'
				})
		data=UserAccount.objects.filter(id=query_id)
		serialize=getDocumentsSerializerCoapp(data,many=True)
		return Response(serialize.data,status=status.HTTP_200_OK)


class getArchivekDetails(APIView):
	def post(self,request,format=None):
		out=[]
		query_id=self.request.data['id']
		if not ArchiveReject.objects.filter(applicant_id=query_id).exists() and not ArchiveReject.objects.filter(coapp_id=query_id).exists() and not Archive.objects.filter(applicant_id=query_id).exists() and not Archive.objects.filter(coapp_id=query_id).exists():
			return Response({
					'error':'no user'
				})
		if(ArchiveReject.objects.filter(applicant_id=query_id).exists()):
			data1=ArchiveReject.objects.filter(applicant_id=query_id)
			serialize1=getArchiveDataSerializer(data1,many=True)
			print(serialize1.data)
			out+=serialize1.data
		if(ArchiveReject.objects.filter(coapp_id=query_id).exists()):
			data2=ArchiveReject.objects.filter(coapp_id=query_id)
			serialize2=getArchiveDataSerializer(data2,many=True)
			print(serialize2.data)
			out+=serialize2.data
		if(Archive.objects.filter(applicant_id=query_id).exists()):
			data3=Archive.objects.filter(applicant_id=query_id)
			serialize3=getArchiveDataApprovedSerializer(data3,many=True)
			print(serialize3.data)
			out+=serialize3.data
		if(Archive.objects.filter(coapp_id=query_id).exists()):
			data4=Archive.objects.filter(coapp_id=query_id)
			serialize4=getArchiveDataApprovedSerializer(data4,many=True)
			print(serialize4.data)
			out+=serialize4.data

		#out=serialize1.data+serialize2.data+serialize3.data+serialize4.data
		return Response(out[::-1],status=status.HTTP_200_OK)


class getAllLoandata(APIView):
	def post(self,request,format=None):
		query_data=self.request.data
		per_page=1
		page_index=self.request.data['idx']
		start_at=int(page_index)*per_page
		end=(int(page_index)+1)*per_page
		if(query_data["type"]=="sales"):
			data=LoanForms.objects.filter(form_status='submit').filter(sales_approve="false").select_related('applicant_id')[start_at:end]
		elif(query_data["type"]=="credit"):
			data=LoanForms.objects.filter(form_status='submit').filter(sales_approve="true").filter(credit_approve="false").select_related('applicant_id')[start_at:end]
		elif(query_data["type"]=="admin"):
			data=LoanForms.objects.filter(form_status='submit').filter(sales_approve="true").filter(credit_approve="true").select_related('applicant_id')[start_at:end]
		#data=LoanForms.objects.all().select_related('applicant_id')[start_at:end]
		#print(LoanForms.objects.all().select_related('applicant_id'))
		serialize=QuickViewSerializer(data,many=True)
		out=serialize.data
		if(query_data['count']=="true"):
			if(query_data["type"]=="sales"):
				count=LoanForms.objects.filter(form_status='submit').filter(sales_approve="false").select_related('applicant_id').count()
			elif(query_data["type"]=="credit"):
				count=LoanForms.objects.filter(form_status='submit').filter(sales_approve="true").filter(credit_approve="false").select_related('applicant_id').count()
			elif(query_data["type"]=="admin"):
				count=LoanForms.objects.filter(form_status='submit').filter(sales_approve="true").filter(credit_approve="true").select_related('applicant_id').count()
			out.append(count)
		return Response(out,status=status.HTTP_200_OK)


class SearchSales(APIView):
	def post(self,request,format=None):
		try:
			data=self.request.data
			print(data)
			if(data["type_prev"]=="sales"):
				if(data['type']=='email'):
					if not LoanForms.objects.filter(email=data['value'].strip()).exists():
						return Response({
								'error':'no applicant found'
							})
					get_data=LoanForms.objects.filter(email=data['value'].strip()).filter(form_status='submit').filter(sales_approve="false").select_related('applicant_id')
					serialize=LoanFormsSerializer(get_data,many=True)
					return Response(serialize.data,status=status.HTTP_200_OK)
				elif(data['type']=='id'):
					if not LoanForms.objects.filter(id=data['value'].strip()).exists():
						return Response({
								'error':'no applicant found'
							})
					get_data=LoanForms.objects.filter(id=data['value'].strip()).filter(form_status='submit').filter(sales_approve="false").select_related('applicant_id')
					serialize=LoanFormsSerializer(get_data,many=True)
					return Response(serialize.data,status=status.HTTP_200_OK)

			elif(data["type_prev"]=="credit"):
				if(data['type']=='email'):
					if not LoanForms.objects.filter(email=data['value'].strip()).exists():
						return Response({
								'error':'no applicant found'
							})
					get_data=LoanForms.objects.filter(email=data['value'].strip()).filter(form_status='submit').filter(sales_approve="true").fiter(credit_approve="false").select_related('applicant_id')
					serialize=LoanFormsSerializer(get_data,many=True)
					return Response(serialize.data,status=status.HTTP_200_OK)
				elif(data['type']=='id'):
					if not LoanForms.objects.filter(id=data['value'].strip()).exists():
						return Response({
								'error':'no applicant found'
							})
					get_data=LoanForms.objects.filter(id=data['value'].strip()).filter(form_status='submit').filter(sales_approve="true").fiter(credit_approve="false").select_related('applicant_id')
					serialize=LoanFormsSerializer(get_data,many=True)
					
					return Response(serialize.data,status=status.HTTP_200_OK)

			elif(data["type_prev"]=="admin"):
				if(data['type']=='email'):
					if not LoanForms.objects.filter(email=data['value'].strip()).exists():
						return Response({
								'error':'no applicant found'
							})
					get_data=LoanForms.objects.filter(email=data['value'].strip()).filter(form_status='submit').filter(credit_approve="true").select_related('applicant_id')
					serialize=LoanFormsSerializer(get_data,many=True)
					return Response(serialize.data,status=status.HTTP_200_OK)
				elif(data['type']=='id'):
					if not LoanForms.objects.filter(id=data['value'].strip()).exists():
						return Response({
								'error':'no applicant found'
							})
					get_data=LoanForms.objects.filter(id=data['value'].strip()).filter(form_status='submit').filter(credit_approve="true").select_related('applicant_id')
					serialize=LoanFormsSerializer(get_data,many=True)
					
					return Response(serialize.data,status=status.HTTP_200_OK)

		except Exception as e:
			return Response({
					"error":str(e)
				})

class SalesAction(APIView):
	def post(self,request,format=None):
		data=self.request.data
		action_dict={}

		if(data['action']=='approve'):
			if(data["type"]=="sales"):
				action_dict['sales_approve']="true"
			elif(data["type"]=="credit"):
				action_dict['credit_approve']="true"

		if(data['action']=='coapp'):
			action_dict['coapp_required']="true"
		if(data['action']=='nocoapp'):
			action_dict['coapp_required']="false"

		if(data['action']=='init_process'):
			action_dict['Process_status']='requested'

		try:
			for i in data['id']:
				get_data=LoanForms.objects.get(id=i)
				email=get_data.email
				if(data['action']=='reject'):
					obj_coapp={
						'flag':'0',
						'loan_flag':'sbmt',
						'coapp_flag':'not sbmt'
					}
					obj_app={
						'flag':'0',
						'loan_flag':'sbmt'
					}

					
					try:
						archive=ArchiveReject(applicant_id=get_data.applicant_id,inst_name=get_data.inst_name,
							inst_type=get_data.inst_type,inst_location=get_data.inst_location,
							class_of_student=get_data.class_of_student,course_name=get_data.course_name,
							course_tenure=get_data.course_tenure,course_fee=get_data.course_fee,financing_required=get_data.financing_required,coapp_id=get_data.co_applicant_id,
							loan_tenure=get_data.loan_tenure,admin_approve=False)
					except ObjectDoesNotExist:
						archive=ArchiveReject(applicant_id=get_data.applicant_id,inst_name=get_data.inst_name,
							inst_type=get_data.inst_type,inst_location=get_data.inst_location,
							class_of_student=get_data.class_of_student,course_name=get_data.course_name,
							course_tenure=get_data.course_tenure,course_fee=get_data.course_fee,financing_required=get_data.financing_required,coapp_id=None,
							loan_tenure=get_data.loan_tenure,admin_approve=False)
					archive.save()

					applicant=UserAccount.objects.get(id=get_data.applicant_id.id)
					app_sr=CheckPrevSerializer(instance=applicant,data=obj_app,partial=True)
					if(app_sr.is_valid(raise_exception=True)):
						app_sr.save()
					
					try:
						co_applicant=UserAccount.objects.get(id=get_data.co_applicant_id.id)
						coapp_sr=CheckPrevSerializer(instance=co_applicant,data=obj_coapp,partial=True)
						if(coapp_sr.is_valid(raise_exception=True)):
							coapp_sr.save()
					except Exception as e:
						pass

					
					get_data.delete()

					if(data['type']=='sales'):
						subject="Rejected"
						msg="Hello, your loan application with id "+str(i)+" has been rejected by our sales team"
					if(data['type']=="credit"):
						subject="Rejected"
						msg="Hello, your loan application with id "+str(i)+" has been rejected by our credit team"
					if(data['type']=="admin"):
						subject="Rejected"
						msg="Hello, your loan application with id "+str(i)+" has been rejected"
					to=email
					res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])

				elif(data['action']=='approve' and data["type"]=="admin"):
					obj_coapp={
						'flag':'0',
						'loan_flag':'sbmt',
						'coapp_flag':'not sbmt'
					}
					obj_app={
						'flag':'0',
						'loan_flag':'sbmt'
					}

					
					archive=Archive(applicant_id=get_data.applicant_id,inst_name=get_data.inst_name,
						inst_type=get_data.inst_type,inst_location=get_data.inst_location,
						class_of_student=get_data.class_of_student,course_name=get_data.course_name,
						course_tenure=get_data.course_tenure,course_fee=get_data.course_fee,financing_required=get_data.financing_required,coapp_id=get_data.co_applicant_id,
						loan_tenure=get_data.loan_tenure,admin_approve=True)
					archive.save()

					applicant=UserAccount.objects.get(id=get_data.applicant_id.id)
					app_sr=CheckPrevSerializer(instance=applicant,data=obj_app,partial=True)
					if(app_sr.is_valid(raise_exception=True)):
						app_sr.save()
					
					try:
						co_applicant=UserAccount.objects.get(id=get_data.co_applicant_id.id)
						coapp_sr=CheckPrevSerializer(instance=co_applicant,data=obj_coapp,partial=True)
						if(coapp_sr.is_valid(raise_exception=True)):
							coapp_sr.save()
					except Exception as e:
						pass

					
					get_data.delete()

					subject="Approved"
					msg="Hello, your loan application with id "+str(i)+" has been approved"
					to=email
					res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
					
				else:
					if(data['action']=='coapp'):
						serialize=LoanFormsSerializer(instance=get_data,data=action_dict,partial=True)
						if(serialize.is_valid(raise_exception=True)):
							serialize.save()
							subject="Co-applicant Required"  
							msg="Hello, your loan application with id "+str(i)+" required co-applicant"
					elif(data['action']=='nocoapp'):
						serialize=LoanFormsSerializer(instance=get_data,data=action_dict,partial=True)
						if(serialize.is_valid(raise_exception=True)):
							serialize.save()
							subject="Co-applicant not Required"  
							msg="Hello, your loan application with id "+str(i)+" not required co-applicant"
					elif(data['action']=='approve'):
						serialize=LoanFormsSerializer(instance=get_data,data=action_dict,partial=True)
						if(serialize.is_valid(raise_exception=True)):
							serialize.save()
							subject="Loan Approved by"+data['type']+"Team"  
							msg="Hello, your loan application with id "+str(i)+" has been approved by our "+data['type']+" team"
					elif(data['action']=='init_process'):
						del data['id']
						del data['action']
						del data['type']
						req=requests.post("https://test.cashfree.com/api/v1/order/create",data=data)
						print(json.loads(req.text))
						req=json.loads(req.text)
						if(req['status']=='ERROR'):
							return Response({
								"error":req['reason']
							})
						else:
							serialize=LoanFormsSerializer(instance=get_data,data=action_dict,partial=True)
							if(serialize.is_valid(raise_exception=True)):
								serialize.save()
							subject="Precessing Fee Required"  
							msg="Hello, your loan application with id "+str(i)+" reuires processing fee "+req['paymentLink']

					elif(data['action']=='e_nach'):
						print("here")
						del data['id']
						del data['action']
						del data['type']
						body={
							"planId":data["planId"],
            				"planName":data["planName"],
           					"type":data["type2"],
            				"maxAmount":float(data["maxAmount"]),
						}
						header={
							"Content-Type":data["content-type"],
            				"X-Client-Id":data["X-Client-Id"],
            				"X-Client-Secret":data["X-Client-Secret"]
						}
						req=requests.post(data["cf_pln"],data=json.dumps(body),headers=header)
						req=json.loads(req.text)
						print(req)
						if(req['status']=='OK'):
							body={
								"subscriptionId":"SUB"+data["planId"],
								"planId":data["planId"],
	            				"customerName":data["customerName"],
				                "customerEmail":data["customerEmail"],
				                "customerPhone":data["customerPhone"],
				                "expiresOn":str(datetime.datetime.strptime(data["emi_end_date"],"%Y-%m-%d")),
				                "returnUrl":data["returnUrl"]
							}
							req=requests.post(data["cf_sub"],data=json.dumps(body),headers=header)
							req=json.loads(req.text)
							if(req['status']=='OK'):
								enach_dict={}
								enach_dict['enach_status']=req['subStatus']
								enach_dict['subId']=req['subReferenceId']
								link=req['authLink']
								serialize=EnachSerializer(instance=get_data,data=enach_dict,partial=True)
								if(serialize.is_valid(raise_exception=True)):
									serialize.save()
								subject="Enach Initialized"  
								msg="Hello, Enach initialized for your loan application with id "+str(i)+". Click On "+link
						else:
							return Response({
								"error":req['message']
							})

						'''
						if(req['status']=='ERROR'):
							return Response({
								"error":req['reason']
							})
						else:
							serialize=LoanFormsSerializer(instance=get_data,data=action_dict,partial=True)
							if(serialize.is_valid(raise_exception=True)):
								serialize.save()
							subject="Precessing Fee Required"  
							msg="Hello, your loan application with id "+str(i)+" reuires processing fee "+req['paymentLink']
						'''
					to=email
					res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
	
			
			return Response({
					"success":"done"
				})
		except Exception as e:
				print(e)
				return Response({
							"error":"server error"
						})


class InsertAdditional(APIView):
	def patch(self,request,format=None):
		data=self.request.data
		for key in list(data.keys()):
			if(data[key]==''):
				del data[key]

		if not LoanForms.objects.filter(id=data['loan_id']).exists():
			Response({
					"error":"no user"
				})
		obj=LoanForms.objects.get(id=data['loan_id'])
		del data['loan_id']
		print(data)
		serialize=AdditionalSerializer(instance=obj,data=data,partial=True)
		if(serialize.is_valid(raise_exception=True)):
			serialize.save()
			return Response({
					"success":"data updated"
				})
		else:
			Response({
					"error":"server error"
				})


class CoAppData(APIView):
	def post(self,request,format=None):
		data=self.request.data
		try:
			if(data['type']=='email'):
				if not LoanForms.objects.filter(email=data['value']).exists():
					Response({
						"error":"no user"
					})
				get_data=LoanForms.objects.filter(email=data['value']).filter(coapp_required="true").filter(coapp_first_name=None).select_related('applicant_id')
				serialize=LoanFormsSerializer(get_data,many=True)
				return Response(serialize.data,status=status.HTTP_200_OK)
			if(data['type']=='id'):
				if not LoanForms.objects.filter(email=data['value']).exists():
					Response({
						"error":"no user"
					})
				get_data=LoanForms.objects.filter(id=data['value']).filter(coapp_required="true").filter(coapp_first_name=None).select_related('applicant_id')
				serialize=LoanFormsSerializer(get_data,many=True)
				return Response(serialize.data,status=status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({
						"error":"server error"
					})

class DeleteLoanRow(APIView):
	def post(self,request,format=None):
		query_data=self.request.data
		try:
			user_flag=UserAccount.objects.get(id=query_data['id'])
			data={
				'coapp_flag':'coapp',
				'flag':query_data['flag']
			}
			serialize=CheckPrevSerializer(instance=user_flag,data=data,partial=True)
			if(serialize.is_valid(raise_exception=True)):
				get_data=LoanForms.objects.get(applicant_id=query_data['id'])
				get_data.delete()
				serialize.save()
				return Response({
						'success':'removed'
					})
		except Exception as e:
			print(e)
			return Response({
						"error":"server error"
					})


'''
class CoAppRequest(APIView):
	def post(self,request,format=None):
		html_content=render_to_string('index.html')
		text_content=strip_tags(html_content)
		to="singharoysagnik007@gmail.com"
		email=EmailMultiAlternatives(
			"test",
			text_content,
			settings.EMAIL_HOST_USER,
			[to]
		)
		email.attach_alternative(html_content,"text/html")
		email.send()
		return Response({
				'success':'mail send'
			})
'''

class CoAppRequest(APIView):
	def post(self,request,format=None):
		get_data=self.request.data
		try:
			obj=LoanForms.objects.get(id=get_data['loan_id'])
			coapp_obj=UserAccount.objects.get(id=get_data['co_applicant_id'])
			co_app_data={
				'co_applicant_id':get_data['co_applicant_id'],
				'coapp_first_name':get_data['coapp_first_name'],
				'coapp_last_name':get_data['coapp_last_name'],
				'relation_to_applicant':get_data['relation_to_applicant']
			}
			flag={
				'flag':get_data['flag'],
				'coapp_flag':'req '+str(get_data['applicant_id'])
			}
			serialize=LoanFormsSerializer(instance=obj,data=co_app_data,partial=True)
			if(serialize.is_valid(raise_exception=True)):
				co_app_serialize=CheckPrevSerializer(instance=coapp_obj,data=flag,partial=True)
				if(co_app_serialize.is_valid(raise_exception=True)):
					serialize.save()
					co_app_serialize.save()
					subject="Co Applicant Registered"
					msg="Hello "+str(get_data['applicant_name'])+" ,your "+str(get_data['relation_to_applicant'])+" "+str(get_data['coapp_first_name'])+" "+str(get_data['coapp_last_name'])+" has registered as your co applicant for your loan with ID "+str(get_data['loan_id'])
					to=str(get_data['applicant_email'])
					send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
					return Response({
								'success':'added'
							})
				else:
					return Response({
								'error':'server error'
							})
			else:
				return Response({
							'error':'server error'
						})
		except Exception as e:
			print(e)
			return Response({
						"error":"server error"
					})



class VerifyPhone(APIView):
	def patch(self,request,format=None):
		get_data=self.request.data
		query_id=get_data['id']
		del get_data['id']
		user=UserAccount.objects.get(id=query_id)
		serialize=PhoneValidateSerializer(instance=user,data=get_data,partial=True)
		if(serialize.is_valid(raise_exception=True)):
			serialize.save()
			return Response({
					'success':'verified'
				})
		else:
			return Response({
					'error':'server error'
				})
