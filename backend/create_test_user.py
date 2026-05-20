import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

def create_test_user():
    username = 'testuser'
    password = 'password123'
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            password=password,
            email='testuser@example.com',
            first_name='Test',
            last_name='User'
        )
        print(f"Created test user: {username} / {password}")
    else:
        print(f"Test user {username} already exists. Password: {password}")

if __name__ == '__main__':
    create_test_user()
