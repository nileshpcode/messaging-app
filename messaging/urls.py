"""messaging URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


def jsFile(request):
    file = open(os.path.join('firebase-messaging-sw.js'), 'rb')
    return HttpResponse(file, content_type="application/x-javascript")


urlpatterns = [
                  url(r'^admin/', admin.site.urls),

                  url(r'^$', HomeView.as_view(), name='index'),

                  url(r'^accounts/', include('registration.backends.simple.urls')),

                  url(r'^message/', include('message.urls')),

                  url(r'^firebase-messaging-sw.js', jsFile)

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
