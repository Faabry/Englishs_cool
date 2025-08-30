import os
from django.conf import settings

def lessons_list(request):
    lessons_dir = os.path.join(settings.STATICFILES_DIRS[0], 'lessons')
    lesson_files = [f for f in os.listdir(lessons_dir) if f.endswith('.pdf')]
    lessons = sorted([os.path.splitext(f)[0] for f in lesson_files], key=lambda x: int(x))
    return {'lessons': lessons}