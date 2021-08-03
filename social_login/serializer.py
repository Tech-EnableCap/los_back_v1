from rest_framework import serializers
from . import google
from .register import register_user
import os
from dotenv import load_dotenv
from rest_framework.exceptions import AuthenticationFailed

load_dotenv()

class GoogleSocialAuthSerializer(serializers.Serializer):
	auth_token=serializers.CharField()

	def validate_auth_token(self,auth_token):
		user_data=google.Google.validate(auth_token)
		try:
		    user_data['sub']
		except:
		    raise serializers.ValidationError('The token is invalid or expired. Please login again.')

		if user_data['aud']!=os.getenv('GOOGLE_CLIENT_ID'):
		    raise AuthenticationFailed('3rd party developer detected!! request aborted.')


		email=user_data['email']
		first_name='jj'
		last_name='kk'
		phone='not added'

		return register_user(email=email,first_name=first_name,last_name=last_name,phone=phone)