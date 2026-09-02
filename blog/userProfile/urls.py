from gjango.urls import path
from . import views

app_name = 'UserProfile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('edit/', views.profile_edit, name='profilr_edit'),
]