from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.category_selection, name='category_selection'),
    path('<str:category>/', views.show_random_image, name='show_image'),
    path('accounts/', include('django.contrib.auth.urls')),
]
