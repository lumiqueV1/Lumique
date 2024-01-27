# In Beautyswipe_v1/urls.py

from django.urls import path
from . import views

app_name = 'Beautyswipe_v1'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.ranked_photos, name='ranked_photos'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('register/', views.register_view, name='register'),
    path('submit_photo/', views.submit_photo, name='submit_photo'),
    path('vote/<int:photo_id>/', views.vote, name='vote'),
    # path('ranked-photos/', views.ranked_photos, name='ranked_photos'),  
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('about/', views.about, name='about'),
    path('ranking/', views.ranking, name='ranking'),
    path('landing', views.landing_page, name='landing_page'),
]
