from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

def fileName(instance,fileName):
	return 'media/'.join(['files',str(instance.email),fileName])

class UserAccountManager(BaseUserManager):
	def create_user(self,email,first_name,last_name,phone,password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not first_name or not last_name:
			raise ValueError('Name fields must not be empty')
		if not phone:
			raise ValueError('Phone number required')

		email=self.normalize_email(email)
		user=self.model(email=email,first_name=first_name,last_name=last_name,phone=phone)

		user.set_password(password)
		user.save()
		return user

	def create_superuser(self,email,first_name,last_name,phone,password):
		user=self.create_user(email,first_name,last_name,phone,password)
		user.is_superuser=True
		user.is_staff=True

		user.save()
		return user

class UserAccount(AbstractBaseUser,PermissionsMixin):
	first_name=models.CharField(max_length=255)
	last_name=models.CharField(max_length=255)
	email=models.EmailField(max_length=255,unique=True)
	phone=models.CharField(max_length=255)
	is_active=models.BooleanField(default=True)
	is_staff=models.BooleanField(default=True)
	is_sales_op=models.BooleanField(default=False)
	is_credit_op=models.BooleanField(default=False)
	is_admin=models.BooleanField(default=False)

	dob=models.DateField(blank=True,null=True)
	gender=models.CharField(max_length=50,null=True)
	marital=models.CharField(max_length=50,null=True)

	cur_res_add=models.TextField(null=True)
	cur_city=models.TextField(null=True)
	cur_state=models.TextField(null=True)
	cur_postal=models.TextField(null=True)
	cur_res=models.CharField(max_length=50,null=True)
	rented_by=models.CharField(max_length=50,null=True)
	owned_by=models.CharField(max_length=50,null=True)
	monthly_rent=models.TextField(null=True)
	per_res_add=models.TextField(null=True)
	per_city=models.TextField(null=True)
	per_state=models.TextField(null=True)
	per_postal=models.TextField(null=True)

	emp_type=models.CharField(max_length=50,null=True)
	active_loan_st=models.BooleanField(default=False)
	tot_cur_emi=models.CharField(max_length=50,null=True)
	pan_num=models.CharField(max_length=50,null=True)
	comp_name=models.TextField(null=True)
	comp_add=models.TextField(null=True)
	comp_city=models.TextField(null=True)
	comp_state=models.TextField(null=True)
	comp_postal=models.TextField(null=True)
	monthly_sal=models.TextField(null=True)
	cur_desig=models.TextField(null=True)
	total_work_exp=models.CharField(max_length=50,null=True)
	cur_job_exp=models.CharField(max_length=50,null=True)

	file1=models.FileField(upload_to=fileName,blank=False,null=True)
	file2=models.FileField(upload_to=fileName,blank=False,null=True)
	file3=models.FileField(upload_to=fileName,blank=False,null=True)
	file4=models.FileField(upload_to=fileName,blank=False,null=True)
	

	flag=models.CharField(max_length=50,default=0)
	loan_flag=models.CharField(max_length=50,blank=True,default="not sbmt")
	coapp_flag=models.CharField(max_length=50,blank=True,default="not sbmt")

	pan_status=models.CharField(max_length=255,default='not_chked')

	objects=UserAccountManager()

	USERNAME_FIELD='email'
	REQUIRED_FIELDS=['first_name','last_name','phone']

	def get_full_name(self):
		return self.first_name+' '+self.last_name

	def get_short_name(self):
		return self.first_name

	def __str__(self):
		return self.email

	def tokens(self):
		refresh=RefreshToken.for_user(self)
		return {
		    'refresh':str(refresh),
		    'access':str(refresh.access_token)
		}


class Archive(models.Model):
	applicant_id=models.ForeignKey(UserAccount,related_name='id_ar',on_delete=models.CASCADE)
	coapp_id=models.ForeignKey(UserAccount,related_name='id_ar_c',on_delete=models.CASCADE)
	inst_name=models.TextField(null=True)
	inst_type=models.TextField(null=True)
	inst_location=models.TextField(null=True)
	class_of_student=models.CharField(max_length=50,null=True)
	course_name=models.TextField(null=True)
	course_tenure=models.CharField(max_length=50,null=True)
	course_fee=models.TextField(null=True)
	financing_required=models.TextField(null=True)
	loan_tenure=models.CharField(max_length=50,null=True)
	admin_approve=models.BooleanField(default=False)


class ArchiveReject(models.Model):
	applicant_id=models.ForeignKey(UserAccount,related_name='id_re',on_delete=models.CASCADE)
	coapp_id=models.ForeignKey(UserAccount,related_name='id_re_c',on_delete=models.CASCADE)
	inst_name=models.TextField(null=True)
	inst_type=models.TextField(null=True)
	inst_location=models.TextField(null=True)
	class_of_student=models.CharField(max_length=50,null=True)
	course_name=models.TextField(null=True)
	course_tenure=models.CharField(max_length=50,null=True)
	course_fee=models.TextField(null=True)
	financing_required=models.TextField(null=True)
	loan_tenure=models.CharField(max_length=50,null=True)
	admin_approve=models.BooleanField(default=False)


class LoanForms(models.Model):
	applicant_id=models.ForeignKey(UserAccount,related_name='id_n',on_delete=models.CASCADE)
	co_applicant_id=models.ForeignKey(UserAccount,related_name='id_c',default='',on_delete=models.CASCADE)
	email=models.EmailField(max_length=255,null=True)
	inst_name=models.TextField(null=True)
	inst_type=models.TextField(null=True)
	inst_location=models.TextField(null=True)
	class_of_student=models.CharField(max_length=50,null=True)
	course_name=models.TextField(null=True)
	course_tenure=models.CharField(max_length=50,null=True)
	course_fee=models.TextField(null=True)
	financing_required=models.TextField(null=True)
	loan_tenure=models.CharField(max_length=50,null=True)

	file5=models.FileField(upload_to=fileName,blank=True,null=True)
	file6=models.FileField(upload_to=fileName,blank=True,null=True)
	file7=models.FileField(upload_to=fileName,blank=True,null=True)
	file8=models.FileField(upload_to=fileName,blank=True,null=True)
	file9=models.FileField(upload_to=fileName,blank=True,null=True)
	file10=models.FileField(upload_to=fileName,blank=True,null=True)
	file11=models.FileField(upload_to=fileName,blank=True,null=True)
	file12=models.FileField(upload_to=fileName,blank=True,null=True)
	file13=models.FileField(upload_to=fileName,blank=True,null=True)
	file14=models.FileField(upload_to=fileName,blank=True,null=True)
	file15=models.FileField(upload_to=fileName,blank=True,null=True)
	file16=models.FileField(upload_to=fileName,blank=True,null=True)
	file17=models.FileField(upload_to=fileName,blank=True,null=True)
	file18=models.FileField(upload_to=fileName,blank=True,null=True)
	file19=models.FileField(upload_to=fileName,blank=True,null=True)
	file20=models.FileField(upload_to=fileName,blank=True,null=True)
	file21=models.FileField(upload_to=fileName,blank=True,null=True)
	file22=models.FileField(upload_to=fileName,blank=True,null=True)
	file23=models.FileField(upload_to=fileName,blank=True,null=True)
	file24=models.FileField(upload_to=fileName,blank=True,null=True)


	file25=models.FileField(upload_to=fileName,blank=True,null=True)
	file26=models.FileField(upload_to=fileName,blank=True,null=True)
	file27=models.FileField(upload_to=fileName,blank=True,null=True)
	file28=models.FileField(upload_to=fileName,blank=True,null=True)
	file29=models.FileField(upload_to=fileName,blank=True,null=True)
	file30=models.FileField(upload_to=fileName,blank=True,null=True)
	file31=models.FileField(upload_to=fileName,blank=True,null=True)
	file32=models.FileField(upload_to=fileName,blank=True,null=True)
	file33=models.FileField(upload_to=fileName,blank=True,null=True)
	file34=models.FileField(upload_to=fileName,blank=True,null=True)
	file35=models.FileField(upload_to=fileName,blank=True,null=True)
	file36=models.FileField(upload_to=fileName,blank=True,null=True)
	file37=models.FileField(upload_to=fileName,blank=True,null=True)
	file38=models.FileField(upload_to=fileName,blank=True,null=True)
	file39=models.FileField(upload_to=fileName,blank=True,null=True)
	file40=models.FileField(upload_to=fileName,blank=True,null=True)
	file41=models.FileField(upload_to=fileName,blank=True,null=True)
	file42=models.FileField(upload_to=fileName,blank=True,null=True)
	file43=models.FileField(upload_to=fileName,blank=True,null=True)
	file44=models.FileField(upload_to=fileName,blank=True,null=True)


	coapp_required=models.CharField(max_length=255,default='false')
	coapp_first_name=models.CharField(max_length=255,null=True)
	coapp_last_name=models.CharField(max_length=255,null=True)
	coapp_phone=models.CharField(max_length=255,null=True)
	relation_to_applicant=models.CharField(max_length=50,null=True)
	applicant_bank_acc=models.CharField(max_length=255,default='')
	coapp_ban_acc=models.CharField(max_length=255,default='')
	applicant_ifsc=models.CharField(max_length=255,default='')
	coapp_ifsc=models.CharField(max_length=255,default='')
	applicant_entity=models.TextField(null=True)
	coapp_entity=models.TextField(null=True)
	sales_approve=models.CharField(max_length=50,default='false')
	sales_remarks=models.TextField(null=True)
	credit_approve=models.CharField(max_length=50,default='false')
	credit_remarks=models.TextField(null=True)
	form_status=models.CharField(max_length=255,default='false')

	loan_fig=models.CharField(max_length=255,default='')
	emi_amt=models.CharField(max_length=255,default='')
	month=models.CharField(max_length=255,default='')
	emi_date=models.DateField(blank=True,null=True)
	g_tenure=models.CharField(max_length=255,default='')
	p_fee=models.CharField(max_length=255,default='')
	start_date=models.DateField(blank=True,null=True)
	b_date=models.DateField(blank=True,null=True)
	net_tenure=models.CharField(max_length=255,default='')
	end_date=models.DateField(blank=True,null=True)
	roi=models.CharField(max_length=255,default='')
	words=models.CharField(max_length=1000,default='')
	num_adv=models.CharField(max_length=255,default='')
	com_emi=models.CharField(max_length=255,default='')
	adv_emi_rs=models.CharField(max_length=255,default='')
	date_subemi=models.DateField(blank=True,null=True)
	file_name=models.CharField(max_length=1000,default='')

	Process_fee_id=models.CharField(max_length=255,default='')
	Process_status=models.CharField(max_length=255,default='')

	enach_status=models.CharField(max_length=255,default='')
	subId=models.CharField(max_length=255,default='')

	esign_status=models.CharField(max_length=255,default='')
	esignId=models.CharField(max_length=255,default='')


	'''
	no_of_advance_emi=models.CharField(max_length=50,null=True)
	loan_in_fig=models.TextField(null=True)
	net_tenure=models.CharField(max_length=255,null=True)
	emi_amt=models.TextField(null=True)
	'''


