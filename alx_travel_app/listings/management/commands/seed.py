from django.core.management.base import BaseCommand
from listings.models import Listing, User
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **options):
        # Create a host user
        host, created = User.objects.get_or_create(
            email='host@example.com',
            defaults={'name': 'Sample Host', 'password': 'adminpass'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created host user: {host.email}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ Host user already exists: {host.email}'))

        # Create sample listings
        for _ in range(20):
            listing = Listing.objects.create(
                host=host,
                name=fake.company(),
                description=fake.paragraph(nb_sentences=3),
                location=fake.city(),
                price_per_night=random.randint(50, 500),
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Created listing: {listing.name}'))

        self.stdout.write(self.style.SUCCESS('🎉 Successfully seeded 20 listings.'))
