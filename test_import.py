#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotecasenac.settings')

# Configure Django
django.setup()

try:
    from biblioteca import views
    print("SUCCESS: Views module imported successfully")
    print(f"HomeView exists: {hasattr(views, 'HomeView')}")
    if hasattr(views, 'HomeView'):
        print(f"HomeView type: {type(views.HomeView)}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
