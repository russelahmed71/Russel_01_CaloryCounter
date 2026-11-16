# calory/apps.py
from django.apps import AppConfig

class CaloryConfig(AppConfig):  # (This class name might be MyappConfig right now)
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calory'  # <-- CHANGE THIS from 'myapp' to 'calory'
