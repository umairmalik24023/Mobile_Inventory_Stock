from django.core.management.base import BaseCommand
from dashboard.models import Inventory
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Update inventory items with sample images'

    def handle(self, *args, **options):
        # Map of phone models to their corresponding image files
        image_mapping = {
            'iPhone 15 Pro Max': 'iphone-15-pro-max.svg',
            'Samsung Galaxy S24 Ultra': 'samsung-galaxy-s24-ultra.svg',
            'Google Pixel 8 Pro': 'google-pixel-8-pro.svg',
            'OnePlus 12': 'oneplus-12.svg',
            'Xiaomi 14 Ultra': 'xiaomi-14-ultra.svg',
            'iPhone 14': 'iphone-14.svg',
        }
        
        updated_count = 0
        
        for item in Inventory.objects.all():
            if item.model_name in image_mapping:
                # Create a simple file path for the image
                image_filename = image_mapping[item.model_name]
                image_path = f'static/img/{image_filename}'
                
                # Check if the image file exists
                if os.path.exists(os.path.join(settings.BASE_DIR, image_path)):
                    # Update the main_image field with the static path
                    item.main_image = image_path
                    item.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated: {item.model_name} with {image_filename}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Image not found: {image_path}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'No image mapping for: {item.model_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} inventory items with images')
        )
