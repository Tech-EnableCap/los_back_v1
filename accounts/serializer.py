from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import UserAccount,LoanForms,Archive


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
		fields=('is_superuser','is_sales_op','is_credit_op','flag','loan_flag',)


class PersonalDataSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('dob','gender','marital','flag',)


class ApplicantDashboardSerialer(serializers.ModelSerializer):
	id_n=LoanFormsSerializer(read_only=True,many=True)
	class Meta:
		model=UserAccount
		fields=('id_n','first_name','last_name','email','phone','flag','loan_flag','is_superuser','is_sales_op','is_credit_op',)


class ResidenceSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('cur_res_add','cur_city','cur_state','cur_postal','cur_res','rented_by','owned_by',
			'monthly_rent','per_res_add','per_city','per_state','per_postal','flag',)

class WorkSerializer(serializers.ModelSerializer):
	class Meta:
		model=UserAccount
		fields=('emp_type','active_loan_st','tot_cur_emi','pan_num','comp_name','comp_add','comp_city',
			'comp_state','comp_postal','monthly_sal','cur_desig','total_work_exp','cur_job_exp','flag',)




class getDocumentsSerializer(serializers.ModelSerializer):
	id_n=LoanFormsSerializer(read_only=True,many=True)
	class Meta:
		model=UserAccount
		fields=('file1','file2','file3','file4','id_n','flag',)

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
			'file16','file17','file18','file19','file20','file21','file22','file23','file24',)

class getArchiveDataSerializer(serializers.ModelSerializer):
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