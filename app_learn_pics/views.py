import os
import random
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

@login_required
def home(request):
    return render(request, 'game/home.html')

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

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


@login_required
def profile_view(request):
    return render(request, 'user/profile.html')


import random
# ...existing code...

@login_required
def memory_match(request):
    # Path to your images root
    images_root = os.path.join(settings.BASE_DIR, 'app_learn_pics', 'static', 'game', 'images')
    categories = [d for d in os.listdir(images_root) if os.path.isdir(os.path.join(images_root, d))]
    image_files = []

    # Collect images from each category folder
    for category in categories:
        category_dir = os.path.join(images_root, category)
        for f in os.listdir(category_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_files.append({
                    'filename': f,
                    'category': category
                })

    # Limit to 20 images (randomly chosen if more)
    if len(image_files) > 20:
        image_files = random.sample(image_files, 20)

    # Prepare pairs: each image and its name
    pairs = []
    for img in image_files:
        name = os.path.splitext(img['filename'])[0].replace('_', ' ').capitalize()
        img_url = f'/static/game/images/{img["category"]}/{img["filename"]}'
        pairs.append({'type': 'image', 'value': f'{img["category"]}/{img["filename"]}', 'display': img_url})
        pairs.append({'type': 'word', 'value': f'{img["category"]}/{img["filename"]}', 'display': name})

    # Shuffle cards
    random.shuffle(pairs)

    # Reshape into 8 rows x 5 columns (if less than 40, fill with None)
    grid = []
    for i in range(8):
        row = []
        for j in range(5):
            idx = i * 5 + j
            row.append(pairs[idx] if idx < len(pairs) else None)
        grid.append(row)

    return render(request, 'game/memory_match.html', {
        'grid': grid,
        'col_headers': ['A', 'B', 'C', 'D', 'E'],
        'row_headers': range(1, 9),
    })