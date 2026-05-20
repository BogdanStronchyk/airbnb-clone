import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from listings.models import ServiceListing
from bookings.models import Booking
from users.models import User

def simulate_occupancy():
    # Create some dummy users for the simulated bookings
    dummy_users = []
    for i in range(5):
        username = f'dummyuser{i}'
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={'password': 'password123', 'email': f'{username}@example.com'}
        )
        dummy_users.append(user)

    listings = ServiceListing.objects.all()
    today = timezone.now().date()
    
    total_simulated = 0

    for listing in listings:
        # Generate 2 to 5 random booking periods for each listing
        num_bookings = random.randint(2, 5)
        
        # Start looking for dates from today up to 60 days in the future
        current_date = today
        
        for _ in range(num_bookings):
            # Randomly jump forward 1 to 14 days before starting the next booking
            gap_days = random.randint(1, 14)
            current_date += timedelta(days=gap_days)
            
            # Booking length is randomly 3 to 10 days
            booking_length = random.randint(3, 10)
            end_date = current_date + timedelta(days=booking_length)
            
            # Create the booking
            Booking.objects.create(
                customer=random.choice(dummy_users),
                listing=listing,
                start_date=current_date,
                end_date=end_date,
                total_price=listing.base_price * booking_length,
                status='confirmed'
            )
            
            total_simulated += 1
            # Move current_date to after this booking so they don't overlap easily
            current_date = end_date

    print(f"Successfully generated {total_simulated} simulated bookings to reflect occupancy.")

if __name__ == '__main__':
    simulate_occupancy()
