# 📱 Mobile Phone Images Setup Guide

## How to Add Real Mobile Phone Images

### Step 1: Add Images to assets/img Folder
1. Navigate to: `startbootstrap-landing-page-gh-pages/assets/img/`
2. Add your mobile phone images with these naming conventions:

**Recommended File Names:**
- `iphone-15-pro-max.jpg`
- `samsung-galaxy-s24-ultra.jpg`
- `google-pixel-8-pro.jpg`
- `oneplus-12.jpg`
- `xiaomi-14-ultra.jpg`
- `iphone-14.jpg`

**Or use any name that contains:**
- Brand name (e.g., `iphone`, `samsung`, `google`)
- Model name (e.g., `15-pro-max`, `galaxy-s24`)

### Step 2: Update Inventory Items
Run this command to automatically assign images:
```bash
python manage.py update_inventory_assets
```

### Step 3: View Results
- Go to: `http://127.0.0.1:8000/dashboard/inventory/`
- Your real images will now display instead of placeholders!

## Supported Image Formats
- ✅ JPG/JPEG
- ✅ PNG
- ✅ WebP

## Image Requirements
- **Resolution**: At least 800x600 pixels
- **File Size**: Under 5MB per image
- **Background**: White or neutral for best results
- **Quality**: High resolution, clear focus

## Current Status
The system is ready! Just add your images to `assets/img/` and run the update command.

## Troubleshooting
- If images don't show, check the file names match the phone models
- Make sure images are in the correct `assets/img/` folder
- Run the update command after adding new images
