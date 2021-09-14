from django.contrib.auth import authenticate
from accounts.models import UserAccount
import os
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv

load_dotenv()

def register_user(email,first_name,last_name,phone):
	filter_by_email=UserAccount.objects.filter(email=email)
	if(filter_by_email.exists()):
		try:
			registered_user=authenticate(email=email,password=os.environ.get('SOCIAL_SECRET'))
			return{
				'user':registered_user.email,
				'access':registered_user.tokens()["access"],
				'name':registered_user.first_name+' '+registered_user.last_name,
				'id':registered_user.id
				}
		except Exception as e:
			raise AuthenticationFailed('Looks like you have reset your password. Please login using email and password.')
	else:
		user={
			'first_name':first_name,
			'last_name':last_name,
			'email':email,
			'phone':phone,
			'password':os.environ.get('SOCIAL_SECRET')
			}
		user=UserAccount.objects.create_user(**user)
		user.save()
		new_user=authenticate(email=email,password=os.environ.get('SOCIAL_SECRET'))
		return{
			'user':new_user.email,
			'access':new_user.tokens()["access"],
			'name':new_user.first_name+' '+new_user.last_name,
			'id':new_user.id
			}
