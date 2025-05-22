import os
import random
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

# @login_required
def home(request):
    return render(request, 'game/home.html')

# @login_required
def category_selection(request):
    categories = ['foods', 'drinks', 'animals', 'places', 'fruits', 'objects', 'clothes', 'verbs']
    return render(request, 'game/category.html', {'categories': categories, 'current_page': 'games',})

# @login_required
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


# @login_required
def profile_view(request):
    return render(request, 'user/profile.html')


# @login_required
def memory_match(request):
    # Path to your images root
    images_root = os.path.join(settings.BASE_DIR, 'app_learn_pics', 'static', 'game', 'images')
    categories = [d for d in os.listdir(images_root) if os.path.isdir(os.path.join(images_root, d)) and d != 'verbs']
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
    if len(image_files) > 12:
        image_files = random.sample(image_files, 12)

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
    for i in range(5):
        row = []
        for j in range(5):
            if i == 2 and j == 2:  # center cell
                row.append(None)
            else:
                idx = i * 5 + j
                # Adjust idx to skip the center cell
                idx_in_pairs = i * 5 + j
                if idx_in_pairs > 2 * 5 + 2:  # after center cell
                    idx -= 1
                row.append(pairs[idx] if idx < len(pairs) else None)
        grid.append(row)
    # Example for a 5x5 grid
    col_headers = [chr(65 + i) for i in range(len(grid[0]))]  # <-- Add this line
    center_row = len(grid) // 2
    center_col = len(grid[0]) // 2
    return render(request, 'game/memory_match.html', {
        'grid': grid,
        'col_headers': col_headers,
        'center_row': center_row,
        'center_col': center_col,
        # ...other context...
    })
    

# @login_required
def slot_machine(request):
    categories = ["places", "countries", "foods", "animals"]
    tenses = ["present", "past", "future"]

    # Example word lists (replace with your real data)
    subjects = ["The boy", "My friend", "A dog", "The teacher"]
    verbs = ["visit", "eat", "see", "play in"]
    objects = {
        "places": ["the museum", "the park", "the school"],
        "countries": ["Brazil", "Japan", "Canada"],
        "parks": ["Central Park", "Hyde Park", "Ibirapuera Park"],
        "foods": ["pizza", "sushi", "ice cream"],
        "animals": ["a cat", "an elephant", "a bird"]
    }
    adjectives = ["quickly", "happily", "loudly", "carefully"]

    # Get random choices
    category = random.choice(categories)
    tense = random.choice(tenses)
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    obj = random.choice(objects[category])
    adverb = random.choice(adjectives)

    return render(request, 'game/slot_machine.html', {
        'category': category,
        'tense': tense,
        'subject': subject,
        'verb': verb,
        'object': obj,
        'adverb': adverb,
        'categories': categories,
        'tenses': tenses,
    })  
        
# @login_required
def word_battleship(request):
    size = 10
    all_words = [
    'cat', 'dog', 'apple', 'banana', 'car', 'house', 'tree', 'book', 'fish', 'star',
    'moon', 'sun', 'plane', 'train', 'phone', 'mouse', 'chair', 'table', 'shirt', 'shoe',
    'boat', 'cup', 'door', 'pen', 'pencil', 'bag', 'clock', 'lamp', 'hat', 'sock',
    'bed', 'truck', 'bike', 'bus', 'glass', 'key', 'ring', 'fork', 'spoon', 'plate',
    'ball', 'bat', 'drum', 'flag', 'frog', 'lion', 'tiger', 'bear', 'snake', 'whale',
    'ship', 'map', 'coin', 'box', 'robot', 'plane', 'candle', 'radio', 'brush', 'leaf'
]

    random.shuffle(all_words)
    words = random.sample(all_words, 10)
    grid = [[{'letter': None, 'word': None} for _ in range(size)] for _ in range(size)]
    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            direction = random.choice(['horizontal', 'vertical'])
            # ...inside your placement loop...
            if direction == 'horizontal':
                row = random.randint(0, size-1)
                col = random.randint(0, size-len(word))
                before_ok = (col == 0) or (grid[row][col-1]['letter'] is None)
                after_ok = (col+len(word) == size) or (grid[row][col+len(word)]['letter'] is None)
                # Allow overlap only if the letter matches
                cells_ok = all(
                    grid[row][col+i]['letter'] is None or grid[row][col+i]['letter'] == letter
                    for i, letter in enumerate(word)
                )
                if before_ok and after_ok and cells_ok:
                    for i, letter in enumerate(word):
                        grid[row][col+i]['letter'] = letter
                        grid[row][col+i]['word'] = word
                    placed = True
            else:  # vertical
                row = random.randint(0, size-len(word))
                col = random.randint(0, size-1)
                before_ok = (row == 0) or (grid[row-1][col]['letter'] is None)
                after_ok = (row+len(word) == size) or (grid[row+len(word)][col]['letter'] is None)
                cells_ok = all(
                    grid[row+i][col]['letter'] is None or grid[row+i][col]['letter'] == letter
                    for i, letter in enumerate(word)
                )
                if before_ok and after_ok and cells_ok:
                    for i, letter in enumerate(word):
                        grid[row+i][col]['letter'] = letter
                        grid[row+i][col]['word'] = word
                    placed = True
            attempts += 1
    col_headers = [chr(65+i) for i in range(size)]
    return render(request, 'game/word_battleship.html', {
        'grid': grid,
        'col_headers': col_headers,
    })


def hangman(request):
    import random  # Ensure random is imported

    categories = {
    "Fruit": [
        "banana", "apple", "orange", "grape", "mango", "pineapple", "strawberry", 
        "blueberry", "watermelon", "peach", "pear", "kiwi", "papaya", "coconut", "lemon"
    ],
    "Animal": [
        "elephant", "tiger", "giraffe", "monkey", "kangaroo", "alligator", "zebra", 
        "dolphin", "penguin", "rhinoceros", "hippopotamus", "lion", "panda", "eagle", "octopus"
    ],
    "Object": [
        "pencil", "laptop", "bottle", "window", "chair", "backpack", "microwave", 
        "television", "keyboard", "headphones", "camera", "hammer", "notebook", "wallet", "umbrella"
    ],
    "Country": [
        "brazil", "canada", "france", "germany", "australia", "japan", "egypt", "spain", 
        "italy", "india", "china", "argentina", "mexico", "norway", "sweden"
    ],
    "Color": [
        "red", "blue", "green", "yellow", "purple", "orange", "black", "white", 
        "pink", "brown", "gray", "turquoise", "gold", "silver", "beige"
    ],
    "Sport": [
        "soccer", "basketball", "tennis", "baseball", "volleyball", "golf", 
        "cricket", "rugby", "hockey", "boxing", "swimming", "cycling", "skiing", "surfing", "wrestling"
    ],
    "Profession": [
        "doctor", "teacher", "engineer", "chef", "lawyer", "nurse", "architect", 
        "scientist", "firefighter", "pilot", "police", "artist", "musician", "farmer", "writer"
    ],
    "Food": [
        "pizza", "hamburger", "spaghetti", "sushi", "sandwich", "pancake", "salad", 
        "steak", "taco", "burrito", "noodles", "cheesecake", "omelette", "curry", "lasagna"
    ],
    "Vehicle": [
        "car", "motorcycle", "bicycle", "airplane", "helicopter", "boat", "train", 
        "submarine", "truck", "scooter", "tram", "bus", "van", "ship", "jet"
    ],
    "Body Part": [
        "head", "shoulder", "knee", "ankle", "elbow", "wrist", "finger", 
        "toe", "eye", "nose", "mouth", "ear", "neck", "back", "stomach"
    ]
}


    # Initialize or restart game
    # GOOD: Only start a new game if there is no word, or "Play Again" is clicked
    if request.method == "GET" and (request.GET.get('new') or 
        'hangman_word' not in request.session):
    # ... start new game ...:
        
        category, words = random.choice(list(categories.items()))
        secret_word = random.choice(words).lower()
        request.session['hangman_word'] = secret_word
        request.session['hangman_category'] = category
        request.session['hangman_guesses'] = []
        request.session['hangman_lives'] = 6
        request.session['hangman_game_over'] = False  # Reset game over

    secret_word = request.session['hangman_word']
    category = request.session['hangman_category']
    guesses = request.session['hangman_guesses']
    lives = request.session['hangman_lives']
    game_over = request.session.get('hangman_game_over', False)

    message = ""
    won = False

    # Handle guess
    if request.method == "POST" and not game_over:
        guess = request.POST.get('guess', '').lower()
        if guess and guess not in guesses and guess.isalpha() and len(guess) == 1:
            guesses.append(guess)
            request.session['hangman_guesses'] = guesses
            if guess not in secret_word:
                lives -= 1
                request.session['hangman_lives'] = lives
                if lives == 0:
                    message = f"You lost! The word was '{secret_word}'."
                    game_over = True
                    request.session['hangman_game_over'] = True
            else:
                # Check win
                if all(letter in guesses for letter in secret_word):
                    message = "Congratulations! You won!"
                    won = True
                    game_over = True
                    request.session['hangman_game_over'] = True
        else:
            message = "Please enter a new, valid letter."

    # Build display word
    display_word = ' '.join([letter if letter in guesses else '_' for letter in secret_word])

    if not game_over and all(letter in guesses for letter in secret_word):
        message = "Congratulations! You won!"
        won = True
        game_over = True
        request.session['hangman_game_over'] = True

    return render(request, 'game/hangman.html', {
        'category': category,
        'display_word': display_word,
        'guesses': guesses,
        'lives': lives,
        'message': message,
        'game_over': game_over,
        'won': won,
    })
