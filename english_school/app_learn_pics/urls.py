from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_selection, name='category_selection'),
    path('<str:category>/', views.show_random_image, name='show_image'),
]
