"""los_back_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
admin.site.site_header=settings.ADMIN_SITE_HEADER
admin.site.site_url="https://www.enablecap.in"

urlpatterns = [
	path('api-auth/',include('rest_framework.urls')),
	path('api/token/',views.CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
	path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
	path('api/accounts/',include('accounts.urls')),
    path('api/',include('social_login.urls')),
    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+=[re_path(r'^.*',TemplateView.as_view(template_name='index.html'))]

