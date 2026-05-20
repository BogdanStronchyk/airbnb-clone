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
        # --- Skiing Resort (10) ---
        {'title': 'Alpine Ski Chalet', 'category': 'Skiing Resort', 'location': 'Zermatt, Switzerland', 'base_price': Decimal('250.00'), 'description': 'Beautiful chalet right on the slopes. Perfect for winter enthusiasts.', 'images': ['https://images.unsplash.com/photo-1482862549707-f63cb32c5fd9?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'intermediate', 'has_rental': True, 'season': 'winter'}},
        {'title': 'Whistler Mountain Lodge', 'category': 'Skiing Resort', 'location': 'Whistler, Canada', 'base_price': Decimal('300.00'), 'description': 'Cozy lodge near the base of Whistler mountain. Great access to lifts.', 'images': ['https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'advanced', 'has_rental': False, 'season': 'winter'}},
        {'title': 'Chamonix Peak View', 'category': 'Skiing Resort', 'location': 'Chamonix, France', 'base_price': Decimal('220.00'), 'description': 'Stunning views of Mont Blanc from your living room.', 'images': ['https://images.unsplash.com/photo-1463162788506-69a37e54f7fb?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'all-levels', 'has_rental': True, 'season': 'winter'}},
        {'title': 'Aspen Powder Cabin', 'category': 'Skiing Resort', 'location': 'Aspen, USA', 'base_price': Decimal('450.00'), 'description': 'Luxury cabin with ski-in/ski-out access in the heart of Aspen.', 'images': ['https://images.unsplash.com/photo-1418985991508-e47386d96a71?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'intermediate', 'has_rental': True, 'season': 'winter'}},
        {'title': 'Niseko Snow Retreat', 'category': 'Skiing Resort', 'location': 'Niseko, Japan', 'base_price': Decimal('180.00'), 'description': 'Experience the famous Japow (Japan Powder) from this traditional retreat.', 'images': ['https://images.unsplash.com/photo-1551524164-687a55dd1126?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'advanced', 'has_rental': False, 'season': 'winter'}},
        {'title': 'St. Anton Luxury Condo', 'category': 'Skiing Resort', 'location': 'St. Anton, Austria', 'base_price': Decimal('350.00'), 'description': 'Modern condo near the legendary aprés-ski spots of St. Anton.', 'images': ['https://images.unsplash.com/photo-1550505096-7c96a32d1f67?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'expert', 'has_rental': True, 'season': 'winter'}},
        {'title': 'Cortina Family Chalet', 'category': 'Skiing Resort', 'location': 'Cortina d\'Ampezzo, Italy', 'base_price': Decimal('280.00'), 'description': 'Spacious chalet perfect for families visiting the Dolomites.', 'images': ['https://images.unsplash.com/photo-1483726234545-481d6e880fc6?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'beginner', 'has_rental': True, 'season': 'winter'}},
        {'title': 'Banff Alpine Suite', 'category': 'Skiing Resort', 'location': 'Banff, Canada', 'base_price': Decimal('210.00'), 'description': 'Cozy suite located right in the town of Banff, a short bus ride to the slopes.', 'images': ['https://images.unsplash.com/photo-1489066601267-37fb1220a273?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'all-levels', 'has_rental': True, 'season': 'winter'}},
        {'title': 'Verbier Mountain View', 'category': 'Skiing Resort', 'location': 'Verbier, Switzerland', 'base_price': Decimal('400.00'), 'description': 'Exclusive apartment with panoramic views of the Swiss Alps.', 'images': ['https://images.unsplash.com/photo-1502758715874-8809e5b72111?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'advanced', 'has_rental': False, 'season': 'winter'}},
        {'title': 'Queenstown Ski Condo', 'category': 'Skiing Resort', 'location': 'Queenstown, New Zealand', 'base_price': Decimal('190.00'), 'description': 'Ski the Remarkables and Coronet Peak from this central condo.', 'images': ['https://images.unsplash.com/photo-1519690889869-e705e59f72d1?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'difficulty': 'all-levels', 'has_rental': True, 'season': 'winter'}},

        # --- Eco Cabin (10) ---
        {'title': 'Redwood Eco Cabin', 'category': 'Eco Cabin', 'location': 'Big Sur, USA', 'base_price': Decimal('180.00'), 'description': 'Secluded cabin among the redwoods. Sustainable living at its best.', 'images': ['https://images.unsplash.com/photo-1449156730764-56a99f646648?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': False, 'pets_allowed': True}},
        {'title': 'Norwegian Forest Retreat', 'category': 'Eco Cabin', 'location': 'Oslo, Norway', 'base_price': Decimal('150.00'), 'description': 'Minimalist off-grid cabin in the dense Norwegian woods.', 'images': ['https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': False, 'pets_allowed': False}},
        {'title': 'Costa Rican Jungle Treehouse', 'category': 'Eco Cabin', 'location': 'Monteverde, Costa Rica', 'base_price': Decimal('120.00'), 'description': 'Sleep in the canopy in this eco-friendly treehouse.', 'images': ['https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': True, 'pets_allowed': False}},
        {'title': 'Scottish Fjord Cabin', 'category': 'Eco Cabin', 'location': 'Isle of Skye, Scotland', 'base_price': Decimal('140.00'), 'description': 'Cozy cabin overlooking a loch, built with sustainable materials.', 'images': ['https://images.unsplash.com/photo-1440658172027-bf30c85c2b04?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': False, 'wifi': True, 'pets_allowed': True}},
        {'title': 'Bali Rainforest Pod', 'category': 'Eco Cabin', 'location': 'Ubud, Indonesia', 'base_price': Decimal('90.00'), 'description': 'Open-air bamboo pod immersed in the Balinese jungle.', 'images': ['https://images.unsplash.com/photo-1510007551061-007eb78eb605?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': True, 'pets_allowed': False}},
        {'title': 'Tasmanian Eco Pod', 'category': 'Eco Cabin', 'location': 'Hobart, Australia', 'base_price': Decimal('160.00'), 'description': 'Modern eco-pod with stunning views of the Tasmanian wilderness.', 'images': ['https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': True, 'pets_allowed': False}},
        {'title': 'Patagonia Wilderness Hut', 'category': 'Eco Cabin', 'location': 'Torres del Paine, Chile', 'base_price': Decimal('200.00'), 'description': 'Remote hut for hikers, fully sustained by wind and solar power.', 'images': ['https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': False, 'pets_allowed': False}},
        {'title': 'Swedish Lakeside Cottage', 'category': 'Eco Cabin', 'location': 'Dalarna, Sweden', 'base_price': Decimal('130.00'), 'description': 'Traditional red cottage by a quiet lake, powered by nature.', 'images': ['https://images.unsplash.com/photo-1498307833015-e7b400441eb8?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': False, 'pets_allowed': True}},
        {'title': 'Amazon Canopy Lodge', 'category': 'Eco Cabin', 'location': 'Manaus, Brazil', 'base_price': Decimal('110.00'), 'description': 'Eco-lodge deep in the Amazon, accessible only by boat.', 'images': ['https://images.unsplash.com/photo-1505322022379-7a5223c34e81?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': True, 'wifi': False, 'pets_allowed': False}},
        {'title': 'Icelandic Aurora Cabin', 'category': 'Eco Cabin', 'location': 'Reykjavik, Iceland', 'base_price': Decimal('250.00'), 'description': 'Glass-roofed cabin perfect for watching the Northern Lights.', 'images': ['https://images.unsplash.com/photo-1520627763690-6ee5e08b1a20?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'solar_powered': False, 'wifi': True, 'pets_allowed': False}},

        # --- Paragliding (10) ---
        {'title': 'Tandem Paragliding Over the Alps', 'category': 'Paragliding', 'location': 'Interlaken, Switzerland', 'base_price': Decimal('150.00'), 'description': 'Experience the thrill of flight with a certified instructor.', 'images': ['https://images.unsplash.com/photo-1596464716127-f2a82984de30?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 45, 'max_weight_kg': 100, 'min_age': 12}},
        {'title': 'Rio de Janeiro Coastal Flight', 'category': 'Paragliding', 'location': 'Rio de Janeiro, Brazil', 'base_price': Decimal('120.00'), 'description': 'Fly over the stunning beaches and mountains of Rio.', 'images': ['https://images.unsplash.com/photo-1522818625501-c8da7f607d73?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 30, 'max_weight_kg': 95, 'min_age': 16}},
        {'title': 'Oludeniz Sunset Glide', 'category': 'Paragliding', 'location': 'Oludeniz, Turkey', 'base_price': Decimal('110.00'), 'description': 'Soar above the famous Blue Lagoon during sunset.', 'images': ['https://images.unsplash.com/photo-1506462945848-ac8ea6f609cc?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 40, 'max_weight_kg': 110, 'min_age': 10}},
        {'title': 'Cape Town Alpine Soar', 'category': 'Paragliding', 'location': 'Cape Town, South Africa', 'base_price': Decimal('130.00'), 'description': 'Launch from Signal Hill and land near the Atlantic ocean.', 'images': ['https://images.unsplash.com/photo-1533035336122-4327d347d2fe?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 25, 'max_weight_kg': 105, 'min_age': 14}},
        {'title': 'Pokhara Mountain Thermal', 'category': 'Paragliding', 'location': 'Pokhara, Nepal', 'base_price': Decimal('90.00'), 'description': 'Glide alongside eagles with views of the Annapurna range.', 'images': ['https://images.unsplash.com/photo-1466378415715-38dbbc07a933?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 60, 'max_weight_kg': 90, 'min_age': 18}},
        {'title': 'Lima Urban Canopy Flight', 'category': 'Paragliding', 'location': 'Lima, Peru', 'base_price': Decimal('85.00'), 'description': 'Fly over the cliffs of Miraflores overlooking the Pacific.', 'images': ['https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 20, 'max_weight_kg': 100, 'min_age': 12}},
        {'title': 'Tenerife Thermal Discovery', 'category': 'Paragliding', 'location': 'Tenerife, Spain', 'base_price': Decimal('140.00'), 'description': 'Explore the volcanic landscapes of Tenerife from the air.', 'images': ['https://images.unsplash.com/photo-1521685368305-64d8a573b98c?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 50, 'max_weight_kg': 115, 'min_age': 15}},
        {'title': 'Annecy Acrobatic Flight', 'category': 'Paragliding', 'location': 'Annecy, France', 'base_price': Decimal('180.00'), 'description': 'For adrenaline junkies: an acrobatic tandem flight over Lake Annecy.', 'images': ['https://images.unsplash.com/photo-1534008101407-1ebf81dfad9c?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 30, 'max_weight_kg': 85, 'min_age': 18}},
        {'title': 'Queenstown Remarkables Jump', 'category': 'Paragliding', 'location': 'Queenstown, New Zealand', 'base_price': Decimal('160.00'), 'description': 'Breathtaking views of Lake Wakatipu and the surrounding mountains.', 'images': ['https://images.unsplash.com/photo-1506544777-64cfbe1142df?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 35, 'max_weight_kg': 100, 'min_age': 14}},
        {'title': 'Iquique Desert Soar', 'category': 'Paragliding', 'location': 'Iquique, Chile', 'base_price': Decimal('100.00'), 'description': 'Launch from the massive sand dunes and land on the beach.', 'images': ['https://images.unsplash.com/photo-1520627763690-6ee5e08b1a20?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'duration_mins': 45, 'max_weight_kg': 110, 'min_age': 16}},

        # --- City Tour (10) ---
        {'title': 'Historic Rome Walking Tour', 'category': 'City Tour', 'location': 'Rome, Italy', 'base_price': Decimal('45.00'), 'description': 'Explore the Colosseum and Roman Forum with a local expert.', 'images': ['https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 5, 'includes_entry_fees': False, 'group_size_max': 12}},
        {'title': 'Kyoto Temples & Gardens', 'category': 'City Tour', 'location': 'Kyoto, Japan', 'base_price': Decimal('60.00'), 'description': 'A guided tour of Kyoto\'s most serene Zen gardens and ancient temples.', 'images': ['https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 7, 'includes_entry_fees': True, 'group_size_max': 8}},
        {'title': 'New York City Architecture Walk', 'category': 'City Tour', 'location': 'New York, USA', 'base_price': Decimal('50.00'), 'description': 'Discover the history behind Manhattan\'s iconic skyscrapers.', 'images': ['https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 6, 'includes_entry_fees': False, 'group_size_max': 15}},
        {'title': 'Parisian Gastronomy Tour', 'category': 'City Tour', 'location': 'Paris, France', 'base_price': Decimal('85.00'), 'description': 'Taste your way through Montmartre\'s best bakeries and cheese shops.', 'images': ['https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 3, 'includes_entry_fees': True, 'group_size_max': 6}},
        {'title': 'London Royal History Walk', 'category': 'City Tour', 'location': 'London, UK', 'base_price': Decimal('40.00'), 'description': 'Visit Buckingham Palace, Westminster, and learn about the monarchy.', 'images': ['https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 8, 'includes_entry_fees': False, 'group_size_max': 20}},
        {'title': 'Barcelona Tapas & Gothic Quarter', 'category': 'City Tour', 'location': 'Barcelona, Spain', 'base_price': Decimal('70.00'), 'description': 'An evening stroll through the Gothic Quarter followed by authentic tapas.', 'images': ['https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 4, 'includes_entry_fees': True, 'group_size_max': 10}},
        {'title': 'Istanbul Old City Exploration', 'category': 'City Tour', 'location': 'Istanbul, Turkey', 'base_price': Decimal('35.00'), 'description': 'Discover the Hagia Sophia, Blue Mosque, and the Grand Bazaar.', 'images': ['https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 5, 'includes_entry_fees': False, 'group_size_max': 12}},
        {'title': 'Berlin Street Art Bike Tour', 'category': 'City Tour', 'location': 'Berlin, Germany', 'base_price': Decimal('45.00'), 'description': 'Cycle through Berlin\'s alternative neighborhoods to see world-class street art.', 'images': ['https://images.unsplash.com/photo-1560930950-5cc20e8cbe14?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 15, 'includes_entry_fees': True, 'group_size_max': 10}},
        {'title': 'Cairo Bosphorus Boat & Walk', 'category': 'City Tour', 'location': 'Cairo, Egypt', 'base_price': Decimal('55.00'), 'description': 'Explore Islamic Cairo and take a traditional Felucca ride on the Nile.', 'images': ['https://images.unsplash.com/photo-1572252009286-268acec5ca0a?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 4, 'includes_entry_fees': True, 'group_size_max': 8}},
        {'title': 'Sydney Coastal Walk & Harbor', 'category': 'City Tour', 'location': 'Sydney, Australia', 'base_price': Decimal('50.00'), 'description': 'A guided walk from Bondi to Coogee, ending at the Sydney Opera House.', 'images': ['https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&q=80&w=800'], 'specific_attributes': {'walking_dist_km': 10, 'includes_entry_fees': False, 'group_size_max': 15}},
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
