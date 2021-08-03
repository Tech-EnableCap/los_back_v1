from django.contrib.auth import authenticate
from accounts.models import UserAccount
import os
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv

load_dotenv()

def register_user(email,first_name,last_name,phone):
	filter_by_email=UserAccount.objects.filter(email=email)
	if(filter_by_email.exists()):
		registered_user=authenticate(email=email,password=os.getenv('SOCIAL_SECRET'))
		print(registered_user)
		return{
			'email':registered_user.email,
			'tokens':registered_user.tokens()
			}
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
			'email': new_user.email
			}
