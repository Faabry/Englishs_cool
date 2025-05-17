import sys
import os

path = '/home/tomtomtoto/learn_pics'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'english_school.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()