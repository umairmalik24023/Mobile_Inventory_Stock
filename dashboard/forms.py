from django import forms
from django.contrib.auth.models import User
from .models import UserDetail, PostDetail, CustomerDetail, ContactUser, Order, Inventory


class UserDetailForm(forms.ModelForm):
	class Meta:
		model = UserDetail
		fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'country']
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
			'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555-123-4567'}),
			'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, number, apartment'}),
			'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
			'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
		}


class PostDetailForm(forms.ModelForm):
	class Meta:
		model = PostDetail
		fields = ['title', 'description', 'category', 'is_published', 'published_at']
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amazing post title'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Write your post content...'}),
			'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category (optional)'}),
			'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
		}


class CustomerDetailForm(forms.ModelForm):
	class Meta:
		model = CustomerDetail
		fields = [
			'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'country',
			'mobile_model', 'price', 'purchase_date', 'notes'
		]
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
			'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555-123-4567'}),
			'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, number, apartment'}),
			'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
			'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
			'mobile_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. iPhone 15 Pro'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
			'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Notes (optional)'}),
		}


class ContactUserForm(forms.ModelForm):
	class Meta:
		model = ContactUser
		fields = ['name', 'username', 'email', 'phone']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
			'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred username'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
			'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555-123-4567'}),
		}


class AuthUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
			'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
			'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}


class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = [
			'customer', 'inventory_item', 'product_name', 'product_model', 'quantity', 'unit_price',
			'order_status', 'payment_status', 'shipping_address', 'notes'
		]
		widgets = {
			'customer': forms.Select(attrs={'class': 'form-control'}),
			'inventory_item': forms.Select(attrs={'class': 'form-control', 'id': 'id_inventory_item'}),
			'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-filled from inventory', 'readonly': True}),
			'product_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-filled from inventory', 'readonly': True}),
			'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1', 'id': 'id_quantity'}),
			'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Auto-filled from inventory', 'readonly': True}),
			'order_status': forms.Select(attrs={'class': 'form-control'}),
			'payment_status': forms.Select(attrs={'class': 'form-control'}),
			'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Complete shipping address'}),
			'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Order notes (optional)'}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Set default values
		self.fields['order_status'].initial = 'pending'
		self.fields['payment_status'].initial = 'pending'
		# Only show customers that exist in the database
		self.fields['customer'].queryset = CustomerDetail.objects.all()
		# Only show available inventory items
		self.fields['inventory_item'].queryset = Inventory.objects.filter(status='in_stock', stock_quantity__gt=0)
		self.fields['inventory_item'].empty_label = "Select a product from inventory"
		
		# Add help text
		self.fields['inventory_item'].help_text = "Select a product to auto-fill product details"
		self.fields['quantity'].help_text = "Enter quantity (stock will be automatically updated)"


class InventoryForm(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = [
			'model_name', 'brand', 'model_number', 'color', 'storage_capacity',
			'price', 'original_price', 'stock_quantity', 'status',
			'main_image', 'image_2', 'image_3', 'image_4',
			'screen_size', 'processor', 'ram', 'camera_main', 'battery_capacity', 'operating_system',
			'description', 'features', 'is_featured', 'is_new_arrival'
		]
		widgets = {
			'model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. iPhone 15 Pro Max'}),
			'brand': forms.Select(attrs={'class': 'form-control'}),
			'model_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A3108'}),
			'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Space Black'}),
			'storage_capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 256GB'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
			'original_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
			'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '0'}),
			'status': forms.Select(attrs={'class': 'form-control'}),
			'main_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'image_2': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'image_3': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'image_4': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'screen_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 6.1 inches'}),
			'processor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A17 Pro'}),
			'ram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 8GB'}),
			'camera_main': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 48MP'}),
			'battery_capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 4000mAh'}),
			'operating_system': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. iOS 17'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Product description...'}),
			'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Key features separated by commas'}),
			'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'is_new_arrival': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Set default values
		self.fields['status'].initial = 'in_stock'
		self.fields['stock_quantity'].initial = 0

