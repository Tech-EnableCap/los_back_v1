from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import UserAccount,LoanForms,Archive,ArchiveReject
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode




class ResetPassSerializer(serializers.Serializer):
	email=serializers.EmailField(min_length=2)
	class Meta:
		fields=['email']


class setNewPassSerializer(serializers.Serializer):
	password=serializers.CharField(min_length=8,max_length=255,write_only=True)
	token=serializers.CharField(min_length=1,max_length=255,write_only=True)
	uidb64=serializers.CharField(min_length=1,max_length=255,write_only=True)
	class Meta:
		fields=['password','token','uidb64']

	def validate(self,attrs):
		try:
			password=attrs.get('password')
			token=attrs.get('token')
			uidb64=attrs.get('uidb64')
			idx=force_str(urlsafe_base64_decode(uidb64))
			user=UserAccount.objects.get(id=idx)

			if not PasswordResetTokenGenerator().check_token(user,token):
				raise AuthenticationFailed('the reset link is invalid',401)

			user.set_password(password)
			user.save()
			return user
		except Exception as e:
			raise AuthenticationFailed('the reset link is invalid',401)

		return super().validate(attrs)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data=super(CustomTokenObtainPairSerializer,self).validate(attrs)
        data.update({'user':self.user.email})
        data.update({'name':self.user.first_name+' '+self.user.last_name})
        data.update({'id':self.user.id})
        return data

class UserUpdatetSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields='__all__'

class LoanFormsSerializer(serializers.ModelSerializer):
	applicant_id=UserUpdatetSerializer(many=False, read_only=True)
	class Meta:
		model=LoanForms
		fields='__all__'

class QuickViewSerializer(serializers.ModelSerializer):
	applicant_id=UserUpdatetSerializer(many=False, read_only=True)
	co_applicant_id=UserUpdatetSerializer(many=False, read_only=True)
	class Meta:
		model=LoanForms
		fields='__all__'

class InsertLoanFormsSerializer(serializers.ModelSerializer):
	class Meta:
		model=LoanForms
		fields='__all__'

class UserAccountSerializer(serializers.ModelSerializer):
	id_n=LoanFormsSerializer(read_only=True,many=True)
	class Meta:
		model=UserAccount
		fields=('id_n','flag',)

class SearchByEmailSerializer(serializers.ModelSerializer):
	id_n=LoanFormsSerializer(read_only=True,many=True)
	class Meta:
		model=UserAccount
		fields='__all__'

class CheckPrevSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('is_superuser','is_sales_op','is_credit_op','is_admin','flag','loan_flag','coapp_flag','phone',)


class PersonalDataSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('dob','gender','marital','flag',)


class ApplicantDashboardSerialer(serializers.ModelSerializer):
	id_n=LoanFormsSerializer(read_only=True,many=True)
	id_c=LoanFormsSerializer(read_only=True,many=True)
	class Meta:
		model=UserAccount
		fields=('id_n','first_name','last_name','email','phone','flag','loan_flag','coapp_flag','is_superuser','is_sales_op','is_credit_op','id_c','is_admin',)


class ResidenceSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('cur_res_add','cur_city','cur_state','cur_postal','cur_res','rented_by','owned_by',
			'monthly_rent','per_res_add','per_city','per_state','per_postal','flag',)

class WorkSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('emp_type','active_loan_st','tot_cur_emi','pan_num','comp_name','comp_add','comp_city',
			'comp_state','comp_postal','monthly_sal','cur_desig','total_work_exp','cur_job_exp','flag','dob',)




class getDocumentsSerializer(serializers.ModelSerializer):
	id_n=LoanFormsSerializer(read_only=True,many=True)
	class Meta:
		model=UserAccount
		fields=('file1','file2','file3','file4','id_n','flag',)


class getDocumentsSerializerCoapp(serializers.ModelSerializer):
	id_c=LoanFormsSerializer(read_only=True,many=True)
	class Meta:
		model=UserAccount
		fields=('file1','file2','file3','file4','id_c','flag',)


class InsertPersonaldocs(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('file1','file2','file3','file4','flag',)


class InsertBankdocs(serializers.ModelSerializer):
	file5=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file6=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file7=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file8=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file9=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file10=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file11=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file12=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file13=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file14=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file15=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file16=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file17=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file18=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file19=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file20=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file21=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file22=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file23=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file24=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	class Meta:
		model=LoanForms
		fields=('file5','file6','file7','file8','file9','file10','file11','file12','file13','file14','file15',
			'file16','file17','file18','file19','file20','file21','file22','file23','file24','applicant_bank_acc','applicant_ifsc',)

class CoAppInsertBankdocs(serializers.ModelSerializer):
	file25=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file26=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file27=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file28=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file29=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file30=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file31=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file32=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file33=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file34=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file35=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file36=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file37=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file38=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file39=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file40=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file41=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file42=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file43=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	file44=serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
	class Meta:
		model=LoanForms
		fields=('file25','file26','file27','file28','file29','file30','file31','file32','file33','file34','file35',
			'file36','file37','file38','file39','file40','file41','file42','file43','file44',)


class getArchiveDataSerializer(serializers.ModelSerializer):
	class Meta:
		model=ArchiveReject
		fields="__all__"

class getArchiveDataApprovedSerializer(serializers.ModelSerializer):
	class Meta:
		model=Archive
		fields="__all__"


class updateFlagSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('loan_flag','flag',)

class SubmitFlagSerializer(serializers.ModelSerializer):
	class Meta:
		model=LoanForms
		fields=('form_status',)


class AdditionalSerializer(serializers.ModelSerializer):
	class Meta:
		model=LoanForms
		fields=('loan_fig','emi_amt','month','emi_date','g_tenure','p_fee','start_date','b_date',
			'net_tenure','end_date','roi','words','num_adv','com_emi','adv_emi_rs','date_subemi','sales_remarks','credit_remarks','file_name',)


class PhoneValidateSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('phone',)


class EnachSerializer(serializers.ModelSerializer):
	class Meta:
		model=LoanForms
		fields=('enach_status','subId',)


class EsignSerializer(serializers.ModelSerializer):
	class Meta:
		model=LoanForms
		fields=('esign_status','esignId',)