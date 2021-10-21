from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [

    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='hrovice/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='hrovice/logout.html'), name="logout"),
    path('edit_profile/', views.edit_profile,name='edit_profile'),
    url(r'^delete_user/(?P<pk>.*)', views.delete_user, name='delete_user'),
    path('create_intern/', views.create_intern,name='create_intern'),
    path('display_interns/', views.display_interns,name='display_interns'),
    url(r'^delete_intern/(?P<pk>.*)', views.delete_intern, name='delete_intern'),
    url(r'^edit_intern/(?P<idintern>.*)', views.edit_intern, name='edit_intern'),
    url(r'^display_intern/(?P<pk>.*)', views.display_intern, name='display_intern'),
    url(r'create_attestation/(?P<owner>.*)', views.create_attestation,name='create_attestation'),
    url(r'display_user_attestations/(?P<owner>.*)', views.display_user_attestations,name='display_user_attestations'),
    url(r'^delete_attestation/(?P<pk>.*)', views.delete_attestation, name='delete_attestation'),
    url(r'^edit_attestation/(?P<idattestation>.*)', views.edit_attestation, name='edit_attestation'),
    url(r'^display_attestation/(?P<pk>.*)', views.display_attestation, name='display_attestation'),
    url(r'^make_attestation/(?P<pk>.*)', views.make_attestation, name='make_attestation'),
]