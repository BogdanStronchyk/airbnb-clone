import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import ServiceListing, ServiceCategory
from bookings.models import Booking, Review
from users.models import UserReview
from django.utils import timezone
from datetime import timedelta
import faker

User = get_user_model()
fake = faker.Faker()

class Command(BaseCommand):
    help = 'Simulates data for users, listings, bookings, and reviews.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data simulation...'))

        # Create Categories
        categories = ['Cleaning', 'Plumbing', 'Electrical', 'Landscaping']
        for cat_name in categories:
            ServiceCategory.objects.get_or_create(name=cat_name, description=fake.text())
        
        db_categories = list(ServiceCategory.objects.all())

        # Create Users
        users = []
        for _ in range(20):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='password123',
                    is_provider=random.choice([True, False]),
                    bio=fake.text()
                )
                users.append(user)

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users.'))

        providers = [u for u in users if u.is_provider]
        guests = [u for u in users if not u.is_provider]

        # Create Listings
        listings = []
        for provider in providers:
            for _ in range(random.randint(1, 3)):
                listing = ServiceListing.objects.create(
                    provider=provider,
                    category=random.choice(db_categories),
                    title=fake.catch_phrase(),
                    description=fake.text(),
                    location=fake.city(),
                    base_price=random.uniform(50, 200),
                    pricing_type=random.choice(['per_night', 'per_hour'])
                )
                listings.append(listing)

        self.stdout.write(self.style.SUCCESS(f'Created {len(listings)} listings.'))

        # Create Bookings and Reviews
        for _ in range(50):
            guest = random.choice(guests) if guests else random.choice(users)
            listing = random.choice(listings)
            
            # Ensure guest isn't booking their own listing
            if guest == listing.provider:
                continue

            start_date = fake.date_between(start_date='-1y', end_date='today')
            end_date = start_date + timedelta(days=random.randint(1, 5))

            booking = Booking.objects.create(
                customer=guest,
                listing=listing,
                start_date=start_date,
                end_date=end_date,
                total_price=listing.base_price * (end_date - start_date).days,
                status='completed'
            )

            # Guest reviews listing
            Review.objects.create(
                booking=booking,
                reviewer=guest,
                rating=random.randint(3, 5),
                comment=fake.text()
            )

            # Guest reviews host
            UserReview.objects.create(
                reviewer=guest,
                reviewee=listing.provider,
                rating=random.randint(3, 5),
                comment=fake.text()
            )

            # Host reviews guest
            UserReview.objects.create(
                reviewer=listing.provider,
                reviewee=guest,
                rating=random.randint(3, 5),
                comment=fake.text()
            )

        self.stdout.write(self.style.SUCCESS('Successfully simulated data!'))