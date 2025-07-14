"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.static import serve

def serve_static(request,path_name):
    print('serving', path_name)
    return serve(request, 'static/'+path_name)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('static/<path:path_name>',serve_static),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('contacts.urls')),
]
