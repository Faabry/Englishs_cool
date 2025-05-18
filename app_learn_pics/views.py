import os
import random
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def category_selection(request):
    categories = ['foods', 'drinks', 'animals', 'places', 'fruits', 'objects', 'clothes', 'verbs']
    return render(request, 'game/category.html', {'categories': categories, 'current_page': 'games',})

@login_required
def show_random_image(request, category):
    static_dir = os.path.join(settings.STATICFILES_DIRS[0], 'game', 'images', category)
    if not os.path.exists(static_dir):
        return render(request, 'game/category.html', {'error': 'Category not found', 'categories': ['foods', 'drinks', 'animals', 'places', 'fruits', 'objects', 'clothes', 'verbs']})

    images = os.listdir(static_dir)
    if not images:
        return render(request, 'game/category.html', {'error': 'No images found', 'categories': ['foods', 'drinks', 'animals', 'places', 'fruits', 'objects', 'clothes', 'verbs']})

    selected_image = random.choice(images)
    image_url = f'/static/game/images/{category}/{selected_image}'
    image_name = os.path.splitext(selected_image)[0]  # Get name without extension
    return render(request, 'game/category.html', {
        'selected_image': image_url,
        'image_name': image_name,
        'category': category,
        'categories': ['foods', 'drinks', 'animals', 'places', 'fruits', 'objects', 'clothes', 'verbs'],
    })
