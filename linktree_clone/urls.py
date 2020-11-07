"""linktree_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from user_registration import views
from registration.backends.simple.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/<username>/update/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('home/', views.index, name = 'index'),
    path('index/', views.index, name = 'index'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/register/',
        MyRegistrationView.as_view(),
        name='registration_complete'),
    path('', include('user_registration.urls')),
    path('url/', include('linktree.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
