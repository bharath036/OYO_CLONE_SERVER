import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Set up Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OYO_CLONE.settings")

# Initialize Django
django.setup()

# Import necessary models
from accounts.models import Hotelvendor, Hotel, Ameneties
from faker import Faker
import random
from random import choice

fake = Faker()

def create_hotels():
    hotel_vendors = Hotelvendor.objects.all()
    if not hotel_vendors:
        print("No Hotelvendors found. Run create_users() first.")
        return

    for _ in range(100):
        hotel_vendor = choice(hotel_vendors)
        amenities = list(Ameneties.objects.all())

        hotel = Hotel.objects.create(
            hotel_name=fake.company(),
            hotel_description=fake.text(),
            hotel_slug=fake.slug(),
            hotel_owner=hotel_vendor,
            hotel_price=fake.random_number(digits=4) / 100.0,
            hotel_offer_price=fake.random_number(digits=4) / 100.0,
            hotel_location=fake.address(),
            is_active=fake.boolean()
        )

        # Add random amenities
        hotel.ameneties.set(random.sample(amenities, min(len(amenities), 5)))

        print(f"Created hotel: {hotel.hotel_name}")

if __name__ == "__main__":
    create_hotels()
