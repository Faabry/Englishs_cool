from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile_view, name='profile'),
    # path('signup/', views.signup, name='signup'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('support/', views.support, name='support'),
    path('admin/', admin.site.urls), 
    path('', views.home, name='home'),  # <-- Add this line
    path('learn-pics', views.category_selection, name='category_selection'),
    path('profile/', views.profile_view, name='profile'),
    path('memory-match/', views.memory_match, name='memory_match'),
    path('slot-machine/', views.slot_machine, name='slot_machine'),
    path('word-battleship/', views.word_battleship, name='word_battleship'),
    path('hangman/', views.hangman, name='hangman'),        
    path('<str:category>/', views.show_random_image, name='show_image'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logged-out/', views.custom_logout, name='logged_out'),    
    # path('lessons/<int:lesson_number>/', views.lesson_view, name='lesson_view'),        
    path('lessons/<int:lesson_number>/<str:topic>/', views.lesson_view, name='lesson_topic_view'),
    path('lessons/<int:lesson_number>/', views.lesson_view, name='lesson_view'),            
    path('lessons/<int:lesson_number>/submit/', views.submit_lesson, name='submit_lesson'),        
]
