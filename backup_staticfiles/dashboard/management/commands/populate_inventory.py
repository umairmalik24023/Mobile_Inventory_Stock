from django.core.management.base import BaseCommand
from dashboard.models import Inventory
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate inventory with sample mobile phone data'

    def handle(self, *args, **options):
        # Sample mobile phone data
        sample_phones = [
            {
                'model_name': 'iPhone 15 Pro Max',
                'brand': 'apple',
                'model_number': 'A3108',
                'color': 'Natural Titanium',
                'storage_capacity': '256GB',
                'price': 1199.00,
                'original_price': 1299.00,
                'stock_quantity': 15,
                'status': 'in_stock',
                'screen_size': '6.7 inches',
                'processor': 'A17 Pro',
                'ram': '8GB',
                'camera_main': '48MP',
                'battery_capacity': '4422mAh',
                'operating_system': 'iOS 17',
                'description': 'The most advanced iPhone with titanium design, A17 Pro chip, and Pro camera system.',
                'features': 'Titanium design, A17 Pro chip, Pro camera system, Action Button, USB-C, 5G',
                'is_featured': True,
                'is_new_arrival': True,
            },
            {
                'model_name': 'Samsung Galaxy S24 Ultra',
                'brand': 'samsung',
                'model_number': 'SM-S928B',
                'color': 'Titanium Black',
                'storage_capacity': '512GB',
                'price': 1299.00,
                'original_price': 1399.00,
                'stock_quantity': 12,
                'status': 'in_stock',
                'screen_size': '6.8 inches',
                'processor': 'Snapdragon 8 Gen 3',
                'ram': '12GB',
                'camera_main': '200MP',
                'battery_capacity': '5000mAh',
                'operating_system': 'Android 14',
                'description': 'Samsung\'s flagship with S Pen, AI features, and advanced camera system.',
                'features': 'S Pen, AI features, 200MP camera, Titanium frame, 5G, Wireless charging',
                'is_featured': True,
                'is_new_arrival': True,
            },
            {
                'model_name': 'Google Pixel 8 Pro',
                'brand': 'other',
                'model_number': 'G1MNW',
                'color': 'Obsidian',
                'storage_capacity': '256GB',
                'price': 999.00,
                'stock_quantity': 8,
                'status': 'in_stock',
                'screen_size': '6.7 inches',
                'processor': 'Google Tensor G3',
                'ram': '12GB',
                'camera_main': '50MP',
                'battery_capacity': '5050mAh',
                'operating_system': 'Android 14',
                'description': 'Google\'s flagship with advanced AI features and pure Android experience.',
                'features': 'Google Tensor G3, AI features, Pure Android, 50MP camera, 5G',
                'is_featured': False,
                'is_new_arrival': True,
            },
            {
                'model_name': 'OnePlus 12',
                'brand': 'oneplus',
                'model_number': 'CPH2581',
                'color': 'Silky Black',
                'storage_capacity': '256GB',
                'price': 799.00,
                'stock_quantity': 20,
                'status': 'in_stock',
                'screen_size': '6.82 inches',
                'processor': 'Snapdragon 8 Gen 3',
                'ram': '12GB',
                'camera_main': '50MP',
                'battery_capacity': '5400mAh',
                'operating_system': 'OxygenOS 14',
                'description': 'OnePlus flagship with fast charging and smooth performance.',
                'features': 'Fast charging, Smooth performance, 50MP camera, 5G, OxygenOS',
                'is_featured': False,
                'is_new_arrival': False,
            },
            {
                'model_name': 'Xiaomi 14 Ultra',
                'brand': 'xiaomi',
                'model_number': '24030PN60G',
                'color': 'Black',
                'storage_capacity': '512GB',
                'price': 899.00,
                'stock_quantity': 5,
                'status': 'low_stock',
                'screen_size': '6.73 inches',
                'processor': 'Snapdragon 8 Gen 3',
                'ram': '16GB',
                'camera_main': '50MP',
                'battery_capacity': '5300mAh',
                'operating_system': 'MIUI 15',
                'description': 'Xiaomi\'s photography flagship with Leica partnership.',
                'features': 'Leica camera, 50MP main camera, 16GB RAM, 5G, Fast charging',
                'is_featured': True,
                'is_new_arrival': False,
            },
            {
                'model_name': 'iPhone 14',
                'brand': 'apple',
                'model_number': 'A2882',
                'color': 'Blue',
                'storage_capacity': '128GB',
                'price': 699.00,
                'stock_quantity': 0,
                'status': 'out_of_stock',
                'screen_size': '6.1 inches',
                'processor': 'A15 Bionic',
                'ram': '6GB',
                'camera_main': '12MP',
                'battery_capacity': '3279mAh',
                'operating_system': 'iOS 16',
                'description': 'Previous generation iPhone with excellent performance.',
                'features': 'A15 Bionic, 12MP camera, 5G, Face ID, MagSafe',
                'is_featured': False,
                'is_new_arrival': False,
            },
        ]

        # Create inventory items
        created_count = 0
        for phone_data in sample_phones:
            # Check if item already exists
            if not Inventory.objects.filter(
                model_name=phone_data['model_name'],
                brand=phone_data['brand'],
                color=phone_data['color']
            ).exists():
                Inventory.objects.create(**phone_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {phone_data["brand"].title()} {phone_data["model_name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} inventory items')
        )
