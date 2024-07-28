# signals.py
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.conf import settings

def create_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

post_migrate.connect(create_superuser)