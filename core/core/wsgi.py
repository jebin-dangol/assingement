import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project root (the directory containing manage.py) to sys.path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Exposure for Vercel (some people use 'app' instead of 'application')
app = application

