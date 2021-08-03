from django.contrib import admin
from django.urls import path,re_path,reverse
from .models import UserAccount,LoanForms,Archive
from django.utils.html import format_html
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from .serializer import updateFlagSerializer

# Register your models here.

def has_change_permission(self, request, obj=None):
	return False

def give_priv_sales_op(modeladmin,request,queryset):
	queryset.update(is_sales_op=True)

def give_admin_priv(modeladmin,request,queryset):
	queryset.update(is_superuser=True)

def give_priv_credit_op(modeladmin,request,queryset):
	queryset.update(is_credit_op=True)

def remove_priv_sales_op(modeladmin,request,queryset):
	queryset.update(is_sales_op=False)

def remove_priv_credit_op(modeladmin,request,queryset):
	queryset.update(is_credit_op=False)

def remove_admin_priv(modeladmin,request,queryset):
	queryset.update(is_superuser=False)

def admin_approve(modeladmin,request,queryset):
	for data in queryset:
		archive=Archive(applicant_id=data.applicant_id,inst_name=data.inst_name,
			inst_type=data.inst_type,inst_location=data.inst_location,
			class_of_student=data.class_of_student,course_name=data.course_name,
			course_tenure=data.course_tenure,course_fee=data.course_fee,financing_required=data.financing_required,
			loan_tenure=data.loan_tenure,admin_approve=True)
		archive.save()
		obj={
			'flag':'0',
			'id':data.applicant_id.id,
			'loan_flag':'sbmt'
		}
	user=UserAccount.objects.get(id=obj['id'])
	serialize=updateFlagSerializer(instance=user,data=obj,partial=True)
	if(serialize.is_valid(raise_exception=True)):
		serialize.save()
		queryset.delete()
	#queryset.delete()

def admin_reject(modeladmin,request,queryset):
	for data in queryset:
		archive=Archive(applicant_id=data.applicant_id,inst_name=data.inst_name,
			inst_type=data.inst_type,inst_location=data.inst_location,
			class_of_student=data.class_of_student,course_name=data.course_name,
			course_tenure=data.course_tenure,course_fee=data.course_fee,financing_required=data.financing_required,
			loan_tenure=data.loan_tenure,admin_approve=False)
		archive.save()
		obj={
			'flag':'0',
			'id':data.applicant_id.id,
			'loan_flag':'sbmt'
		}
	user=UserAccount.objects.get(id=obj['id'])
	serialize=updateFlagSerializer(instance=user,data=obj,partial=True)
	if(serialize.is_valid(raise_exception=True)):
		serialize.save()
		queryset.delete()
	
	#user=UserAccount(flag=0)
	#user.save()


give_priv_sales_op.short_description="Give Sales Operation Privilege"
give_priv_credit_op.short_description="Give Credit Operation Privilege"
give_admin_priv.short_description="Give Super User/Admin Privilege"
remove_priv_sales_op.short_description="Remove Sales Operation Privilege"
remove_priv_credit_op.short_description="Remove Credit Operation Privilege"
remove_admin_priv.short_description="Remove Super User/Admin Privilege"

class UserAdmin(admin.ModelAdmin):
	
	def add_view(self,request,extra_content=None):
		self.exclude=('is_superuser','is_sales_op','is_credit_op',)
		return super(UserAdmin,self).add_view(request)

	def change_view(self,request,object_id,extra_content=None):
		self.exclude = ('password',)
		return super(UserAdmin,self).change_view(request,object_id)

	def has_change_permission(self, request, obj=None):
		return False

	'''
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ['password','is_superuser','is_sales_op','is_credit_op',]
		else:
			return []
	'''
	def action(self, obj):
		return format_html(
		   #"<form method='get' action='{}'><input id='btn' style='cursor:pointer; background:#5b80b2;color:white;' type='submit' value='View More'></form>",obj.id
		   "<button type='submit' formaction='{}' method='get' id='btn' style='cursor:pointer; background:#5b80b2;color:white;'>View More</button>",obj.id
		)

	action.allow_tags = True

	list_display=('id','first_name','last_name','email','is_superuser','is_sales_op','is_credit_op','action')
	list_display_links=('id','email',)
	search_fields=('id','email','first_name','last_name',)
	actions=[give_admin_priv,give_priv_sales_op,give_priv_credit_op,remove_admin_priv,remove_priv_sales_op,remove_priv_credit_op]
	list_per_page=25
	
	def get_urls(self):
		urls = super().get_urls()
		my_urls = [path('<int:pk>', self.do_evil_view)]
		return my_urls + urls

	def do_evil_view(self, request, pk):
		print("---------------------")
		#print(pk)
		#print('doing evil with', UserAccount.objects.filter(id=pk))
		return HttpResponseRedirect('./'+str(pk)+'/change')


class LoanAdmin(admin.ModelAdmin):

	def has_change_permission(self, request, obj=None):
		return False

	def action(self, obj):
		return format_html(
		   #"<form method='get' action='{}'><input id='btn' style='cursor:pointer; background:#5b80b2;color:white;' type='submit' value='View More'></form>",obj.id
		   "<button type='submit' formaction='{}' method='get' id='btn' style='cursor:pointer; background:#5b80b2;color:white;'>View More</button>",obj.id
		)

	action.allow_tags = True

	list_display=('id','inst_name','course_fee','financing_required','coapp_required','sales_approve','action',)
	list_display_links=('id',)
	search_fields=('id',)
	actions=[admin_approve,admin_reject]
	list_per_page=25

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [path('<int:pk>', self.do_evil_view)]
		return my_urls + urls

	def do_evil_view(self, request, pk):
		print("---------------------")
		#print(pk)
		#print('doing evil with', UserAccount.objects.filter(id=pk))
		return HttpResponseRedirect('./'+str(pk)+'/change')



class ArchiveAdmin(admin.ModelAdmin):

	def has_change_permission(self, request, obj=None):
		return False

	def action(self, obj):
		return format_html(
		   #"<form method='get' action='{}'><input id='btn' style='cursor:pointer; background:#5b80b2;color:white;' type='submit' value='View More'></form>",obj.id
		   "<button type='submit' formaction='{}' method='get' id='btn' style='cursor:pointer; background:#5b80b2;color:white;'>View More</button>",obj.id
		)

	action.allow_tags = True

	list_display=('id','inst_name','inst_type','inst_location','class_of_student','course_name','course_tenure','course_fee','financing_required',
		'loan_tenure','action',)
	list_display_links=('id',)
	search_fields=('id',)
	list_per_page=25

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [path('<int:pk>', self.do_evil_view)]
		return my_urls + urls

	def do_evil_view(self, request, pk):
		print("---------------------")
		#print(pk)
		#print('doing evil with', UserAccount.objects.filter(id=pk))
		return HttpResponseRedirect('./'+str(pk)+'/change')
	

admin.site.register(UserAccount,UserAdmin)
admin.site.register(LoanForms,LoanAdmin)
admin.site.register(Archive,ArchiveAdmin)