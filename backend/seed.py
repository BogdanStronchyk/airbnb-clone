import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from listings.models import ServiceCategory, ServiceListing
from users.models import User
from decimal import Decimal

def seed_data():
    categories = [
        {'name': 'Skiing Resort', 'description': 'Winter sports and mountain stays', 'icon': 'snow'},
        {'name': 'Eco Cabin', 'description': 'Nature stays in sustainable cabins', 'icon': 'tree'},
        {'name': 'Paragliding', 'description': 'Tandem flights and courses', 'icon': 'wind'},
        {'name': 'City Tour', 'description': 'Guided historical and cultural tours', 'icon': 'map'},
    ]

    for cat_data in categories:
        category, created = ServiceCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'icon': cat_data['icon']}
        )
        if created:
            print(f"Created category: {category.name}")

    if not User.objects.filter(username='provider1').exists():
        User.objects.create_user(
            username='provider1',
            password='password123',
            email='provider1@example.com',
            is_provider=True,
            first_name='John',
            last_name='Provider'
        )
        print("Created test provider user: provider1")

    provider = User.objects.get(username='provider1')
    
    listings = [
        {
            'title': 'Alpine Ski Chalet',
            'category': 'Skiing Resort',
            'location': 'Zermatt, Switzerland',
            'base_price': Decimal('250.00'),
            'description': 'Beautiful chalet right on the slopes. Perfect for winter enthusiasts.',
            'images': ['https://images.unsplash.com/photo-1482862549707-f63cb32c5fd9?auto=format&fit=crop&q=80&w=800'],
            'specific_attributes': {'difficulty': 'intermediate', 'has_rental': True, 'season': 'winter'}
        },
        {
            'title': 'Redwood Eco Cabin',
            'category': 'Eco Cabin',
            'location': 'Big Sur, California',
            'base_price': Decimal('180.00'),
            'description': 'Secluded cabin among the redwoods. Sustainable living at its best.',
            'images': ['https://images.unsplash.com/photo-1449156730764-56a99f646648?auto=format&fit=crop&q=80&w=800'],
            'specific_attributes': {'solar_powered': True, 'wifi': False, 'pets_allowed': True}
        },
        {
            'title': 'Tandem Paragliding Over the Alps',
            'category': 'Paragliding',
            'location': 'Interlaken, Switzerland',
            'base_price': Decimal('150.00'),
            'description': 'Experience the thrill of flight with a certified instructor.',
            'images': ['https://images.unsplash.com/photo-1596464716127-f2a82984de30?auto=format&fit=crop&q=80&w=800'],
            'specific_attributes': {'duration_mins': 45, 'max_weight_kg': 100, 'min_age': 12}
        },
        {
            'title': 'Historic Rome Walking Tour',
            'category': 'City Tour',
            'location': 'Rome, Italy',
            'base_price': Decimal('45.00'),
            'description': 'Explore the Colosseum and Roman Forum with a local expert.',
            'images': ['https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&q=80&w=800'],
            'specific_attributes': {'walking_dist_km': 5, 'includes_entry_fees': False, 'group_size_max': 12}
        }
    ]

    for list_data in listings:
        cat = ServiceCategory.objects.get(name=list_data['category'])
        listing, created = ServiceListing.objects.get_or_create(
            title=list_data['title'],
            defaults={
                'provider': provider,
                'category': cat,
                'location': list_data['location'],
                'base_price': list_data['base_price'],
                'description': list_data['description'],
                'images': list_data['images'],
                'specific_attributes': list_data['specific_attributes']
            }
        )
        if created:
            print(f"Created listing: {listing.title}")

if __name__ == '__main__':
    seed_data()
