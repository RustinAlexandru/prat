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

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

# Import Views
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('index')}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^task/details/(?P<pk>\d+)/$', views.view_task, name='viewTask'),
    url(r'^task/edit/(?P<pk>\d+)/$', views.edit_task, name='editTask'),
    url(r'^task/delete/(?P<pk>\d+)/$', views.delete_task, name='deleteTask'),
    url(r'^task/restart/(?P<pk>\d+)/$', views.restart_task, name='restartTask'),
    url(r'^task/complete/(?P<pk>\d+)/$', views.complete_task, name='completeTask'),
    url(r'^profile/edit/$', views.edit_profile, name='editProfile'),
    url(r'^profile/(?P<username>[A-Za-z0-9.]+)/$', views.view_profile, name='viewProfile'),
    url(r'^profile/$', views.view_profile, name='viewProfile'),
    url(r'^task/create/$', views.create_task, name='createTask'),
    url(r'groups/$', views.view_groups, name='viewGroups'),
    url(r'groups/create', views.create_group, name='createGroup'),
    url(r'groups/(?P<pk>\d+)/$', views.group_details, name="groupDetails"),
    url(r'^$', views.index, name='index'),
    url(r'^ongs/$', views.view_ongs, name='ongList'),
    url(r'^ong/details/(?P<pk>\d+)/$', views.ong_details, name='ongDetails'),
    url(r'^tops/$', views.view_tops, name='viewTops'),
    url(r'^tops/(?P<choice>[A-Za-z0-9]+)/$', views.view_tops, name='viewTops'),
    url(r'^shop/$', views.view_shop, name='viewShop'),
    url(r'^shop/buy/(?P<pk>\d+)/$', views.buy_theme, name='buyTheme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

