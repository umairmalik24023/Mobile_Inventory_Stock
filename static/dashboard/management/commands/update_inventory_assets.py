from django.core.management.base import BaseCommand
from dashboard.models import Inventory
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Update inventory items to use images from assets/img folder'

    def handle(self, *args, **options):
        # Map of phone models to their corresponding image files in assets/img
        image_mapping = {
            'iPhone 15 Pro Max': 'iphone-15-pro-max.jpg',
            'Samsung Galaxy S24 Ultra': 'samsung-galaxy-s24-ultra.jpg',
            'Google Pixel 8 Pro': 'google-pixel-8-pro.jpg',
            'OnePlus 12': 'oneplus-12.jpg',
            'Xiaomi 14 Ultra': 'xiaomi-14-ultra.jpg',
            'iPhone 14': 'iphone-14.jpg',
            # Add more mappings as needed
            'iPhone 13': 'iphone-13.jpg',
            'Samsung Galaxy S23': 'samsung-galaxy-s23.jpg',
            'Google Pixel 7': 'google-pixel-7.jpg',
            'OnePlus 11': 'oneplus-11.jpg',
            'Xiaomi 13': 'xiaomi-13.jpg',
        }
        
        updated_count = 0
        assets_path = os.path.join(settings.BASE_DIR, 'assets', 'img')
        
        for item in Inventory.objects.all():
            # Try to find a matching image file
            image_found = False
            
            # First, try exact model name match
            if item.model_name in image_mapping:
                image_filename = image_mapping[item.model_name]
                image_path = os.path.join(assets_path, image_filename)
                
                if os.path.exists(image_path):
                    # Update the main_image field with the assets path
                    item.main_image = f'assets/img/{image_filename}'
                    item.save()
                    updated_count += 1
                    image_found = True
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated: {item.model_name} with {image_filename}')
                    )
            
            # If no exact match, try to find similar files
            if not image_found:
                # Look for files that contain the brand name
                brand_lower = item.brand.lower().replace(' ', '-')
                model_lower = item.model_name.lower().replace(' ', '-')
                
                # Search for files in assets/img that might match
                try:
                    for filename in os.listdir(assets_path):
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            filename_lower = filename.lower()
                            # Check if filename contains brand or model
                            if (brand_lower in filename_lower or 
                                model_lower in filename_lower or
                                any(word in filename_lower for word in model_lower.split('-'))):
                                
                                item.main_image = f'assets/img/{filename}'
                                item.save()
                                updated_count += 1
                                image_found = True
                                self.stdout.write(
                                    self.style.SUCCESS(f'Updated: {item.model_name} with {filename} (auto-matched)')
                                )
                                break
                except OSError:
                    self.stdout.write(
                        self.style.WARNING(f'Could not read assets/img directory')
                    )
            
            if not image_found:
                self.stdout.write(
                    self.style.WARNING(f'No image found for: {item.model_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} inventory items with real images')
        )
        
        # Show available images in assets/img
        self.stdout.write('\nAvailable images in assets/img:')
        try:
            for filename in os.listdir(assets_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    self.stdout.write(f'  - {filename}')
        except OSError:
            self.stdout.write('  - Could not list files in assets/img')
