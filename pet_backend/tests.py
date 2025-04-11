from django.test import TestCase
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_user_verify, name='login_user_verify'),
    path('petconnect/menu=<str:key_inst>/', views.perfil_user, name='perfil_user'),
    path('petconnect/home', views.home, name='home'),
    path('petconnect/login', views.login, name='login'),
    path('petconnect/cadastro', views.cadastro, name='cadastro'),
    path('petconnect/complemento_info', views.complemento_info, name='complemento_info'),
    path('petconnect/post?<str:name>/=<int:id>', views.post_detail, name='post_detail'),
    path('petconnect/pub_create/user=<str:inst_hash>?', views.pubCreate, name='pub_create'),
    path('petconnect/pubs=<str:inst_hash>/', views.pubIndex, name='pubIndex'),
    path('petconnect/edit:<str:hash>?<int:id>', views.edit_post, name='edit_post'),
    path('delete/<int:id>?<str:hash>/', views.delete_post, name='delete_post'),
    path('send_request/<int:id_pub>=?<str:hash>=?<str:name>', views.request_adot, name='request_adot'),
    path('petconnect/notif?<str:hash>', views.notify_request, name='notify_request'),
    path('petconnect/favpage', views.request_fav, name='request_fav'),
    path('homepage', views.nav_barHome, name='nav_barHome')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Create your tests here.
