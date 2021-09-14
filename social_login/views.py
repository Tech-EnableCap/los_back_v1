from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import GoogleSocialAuthSerializer

# Create your views here.

class GoogleSocialAuthView(APIView):

	serializer_class=GoogleSocialAuthSerializer

	def post(self,request):
		serializer=self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		data=((serializer.validated_data)['auth_token'])
		return Response(data,status=status.HTTP_200_OK)