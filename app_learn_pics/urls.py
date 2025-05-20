from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls), 
    path('', views.category_selection, name='category_selection'),
    path('profile/', views.profile_view, name='profile'),
    path('<str:category>/', views.show_random_image, name='show_image'),
    path('accounts/signup/', views.signup, name='signup'),
    
    # path('accounts/logout/', views.custom_logout, name='logout'),  # <-- Use /accounts/logout/ and place it AFTER the include
]
