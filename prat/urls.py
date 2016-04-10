"""prat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

# Import Views
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('index')}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/edit/$', views.edit_profile, name='editProfile'),
    url(r'^profile/(?P<username>[A-Za-z0-9]+)/$', views.view_profile, name='viewProfile'),
    url(r'^profile/$', views.view_profile, name='viewProfile'),
    url(r'^create_task/$', views.create_task, name='createTask'),
    url(r'^$', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

