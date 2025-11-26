from django.db import models

# Create your models here.


class UserDetail(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'User Details'
		ordering = ['-created_at']

	def __str__(self) -> str:  # type: ignore[override]
		return f"{self.first_name} {self.last_name}"


class PostDetail(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	category = models.CharField(max_length=100, blank=True)
	is_published = models.BooleanField(default=False)
	published_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'Post Details'
		ordering = ['-created_at']

	def __str__(self) -> str:  # type: ignore[override]
		return self.title


class CustomerDetail(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=20)
	address = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=100, blank=True)
	mobile_model = models.CharField(max_length=150)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	purchase_date = models.DateField()
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'Customer Details'
		ordering = ['-created_at']

	def __str__(self) -> str:  # type: ignore[override]
		return f"{self.first_name} {self.last_name} - {self.mobile_model}"


class ContactUser(models.Model):
	name = models.CharField(max_length=150)
	username = models.CharField(max_length=150)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:  # type: ignore[override]
		return f"{self.name} ({self.username})"


class OrderManager(models.Manager):
	def get_queryset(self):
		# Always filter out orders without valid customers
		return super().get_queryset().filter(customer__isnull=False)

class Order(models.Model):
	ORDER_STATUS_CHOICES = [
		('pending', 'Pending'),
		('processing', 'Processing'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
		('returned', 'Returned'),
	]
	
	PAYMENT_STATUS_CHOICES = [
		('pending', 'Pending'),
		('paid', 'Paid'),
		('failed', 'Failed'),
		('refunded', 'Refunded'),
	]
	
	# Foreign key relationship to CustomerDetail
	customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE, related_name='orders', null=False, blank=False)
	# Foreign key relationship to Inventory (will be defined later)
	inventory_item = models.ForeignKey('Inventory', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
	order_number = models.CharField(max_length=50, unique=True)
	product_name = models.CharField(max_length=200)
	product_model = models.CharField(max_length=150)
	quantity = models.PositiveIntegerField(default=1)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
	payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
	order_date = models.DateTimeField(auto_now_add=True)
	shipping_address = models.TextField()
	notes = models.TextField(blank=True)
	
	objects = OrderManager()
	
	class Meta:
		db_table = 'Orders'
		ordering = ['-order_date']
	
	def __str__(self) -> str:  # type: ignore[override]
		return f"Order #{self.order_number} - {self.customer.first_name} {self.customer.last_name}"
	
	def save(self, *args, **kwargs):
		# Auto-generate order number if not provided
		if not self.order_number:
			import uuid
			self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
		
		# Auto-populate product details from inventory if inventory_item is selected
		if self.inventory_item:
			self.product_name = f"{self.inventory_item.brand} {self.inventory_item.model_name}"
			self.product_model = self.inventory_item.model_name
			self.unit_price = self.inventory_item.price
		
		# Calculate total amount
		self.total_amount = self.quantity * self.unit_price
		
		# Handle stock management and email notifications
		is_new = self.pk is None
		old_status = None
		if not is_new:
			old_order = Order.objects.get(pk=self.pk)
			old_status = old_order.order_status
		
		super().save(*args, **kwargs)
		
		# Update stock based on order status changes
		if self.inventory_item:
			self.update_stock_on_status_change(old_status, is_new)
		
		# Send email notifications
		self.send_email_notifications(old_status, is_new)
	
	def update_stock_on_status_change(self, old_status, is_new):
		"""Update inventory stock based on order status changes"""
		if is_new and self.order_status in ['pending', 'processing']:
			# New order - reduce stock
			self.inventory_item.stock_quantity = max(0, self.inventory_item.stock_quantity - self.quantity)
			self.inventory_item.save()
		elif not is_new and old_status != self.order_status:
			# Status change
			if old_status in ['pending', 'processing'] and self.order_status in ['cancelled', 'returned']:
				# Order cancelled/returned - restore stock
				self.inventory_item.stock_quantity += self.quantity
				self.inventory_item.save()
			elif old_status in ['cancelled', 'returned'] and self.order_status in ['pending', 'processing']:
				# Order reactivated - reduce stock again
				self.inventory_item.stock_quantity = max(0, self.inventory_item.stock_quantity - self.quantity)
				self.inventory_item.save()
	
	def send_email_notifications(self, old_status, is_new):
		"""Send email notifications based on order status changes"""
		try:
			from .email_utils import send_order_confirmation_email, send_order_status_update_email
			
			if is_new and self.customer.email:
				# Send order confirmation email for new orders
				send_order_confirmation_email(self)
			elif not is_new and old_status != self.order_status and self.customer.email:
				# Send status update email when status changes
				send_order_status_update_email(self)
		except Exception as e:
			print(f"Error sending email notifications: {e}")
	
	def delete(self, *args, **kwargs):
		"""Restore stock when order is deleted"""
		if self.inventory_item and self.order_status in ['pending', 'processing']:
			self.inventory_item.stock_quantity += self.quantity
			self.inventory_item.save()
		super().delete(*args, **kwargs)


class Inventory(models.Model):
	BRAND_CHOICES = [
		('apple', 'Apple'),
		('samsung', 'Samsung'),
		('xiaomi', 'Xiaomi'),
		('oneplus', 'OnePlus'),
		('huawei', 'Huawei'),
		('oppo', 'OPPO'),
		('vivo', 'Vivo'),
		('realme', 'Realme'),
		('nokia', 'Nokia'),
		('motorola', 'Motorola'),
		('other', 'Other'),
	]
	
	STATUS_CHOICES = [
		('in_stock', 'In Stock'),
		('low_stock', 'Low Stock'),
		('out_of_stock', 'Out of Stock'),
		('discontinued', 'Discontinued'),
	]
	
	# Basic Information
	model_name = models.CharField(max_length=200)
	brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
	model_number = models.CharField(max_length=100, blank=True)
	color = models.CharField(max_length=50)
	storage_capacity = models.CharField(max_length=20)  # e.g., "128GB", "256GB"
	
	# Pricing and Stock
	price = models.DecimalField(max_digits=10, decimal_places=2)
	original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	stock_quantity = models.PositiveIntegerField(default=0)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
	
	# Images
	main_image = models.ImageField(upload_to='inventory/', help_text="Main product image")
	image_2 = models.ImageField(upload_to='inventory/', blank=True, null=True)
	image_3 = models.ImageField(upload_to='inventory/', blank=True, null=True)
	image_4 = models.ImageField(upload_to='inventory/', blank=True, null=True)
	
	# Specifications
	screen_size = models.CharField(max_length=20, blank=True)  # e.g., "6.1 inches"
	processor = models.CharField(max_length=100, blank=True)
	ram = models.CharField(max_length=20, blank=True)  # e.g., "8GB"
	camera_main = models.CharField(max_length=50, blank=True)  # e.g., "48MP"
	battery_capacity = models.CharField(max_length=20, blank=True)  # e.g., "4000mAh"
	operating_system = models.CharField(max_length=50, blank=True)
	
	# Additional Information
	description = models.TextField(blank=True)
	features = models.TextField(blank=True, help_text="Key features separated by commas")
	is_featured = models.BooleanField(default=False)
	is_new_arrival = models.BooleanField(default=False)
	
	# Timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'Inventory'
		ordering = ['-created_at']
		verbose_name_plural = 'Inventory Items'
	
	def __str__(self) -> str:  # type: ignore[override]
		return f"{self.brand} {self.model_name} ({self.color})"
	
	@property
	def is_on_sale(self):
		return self.original_price and self.original_price > self.price
	
	@property
	def discount_percentage(self):
		if self.is_on_sale:
			return round(((self.original_price - self.price) / self.original_price) * 100)
		return 0
	
	@property
	def all_images(self):
		"""Return list of all available images"""
		images = [self.main_image]
		if self.image_2:
			images.append(self.image_2)
		if self.image_3:
			images.append(self.image_3)
		if self.image_4:
			images.append(self.image_4)
		return [img for img in images if img]
	
	def is_available(self, quantity=1):
		"""Check if item is available in requested quantity"""
		return self.status == 'in_stock' and self.stock_quantity >= quantity
	
	def get_availability_status(self):
		"""Get human-readable availability status"""
		if self.status == 'out_of_stock':
			return 'Out of Stock'
		elif self.status == 'discontinued':
			return 'Discontinued'
		elif self.stock_quantity == 0:
			return 'Out of Stock'
		elif self.stock_quantity <= 5:
			return f'Low Stock ({self.stock_quantity} left)'
		else:
			return f'In Stock ({self.stock_quantity} available)'
	
	def save(self, *args, **kwargs):
		"""Override save to send low stock alerts"""
		old_stock = None
		if self.pk:
			try:
				old_item = Inventory.objects.get(pk=self.pk)
				old_stock = old_item.stock_quantity
			except Inventory.DoesNotExist:
				pass
		
		super().save(*args, **kwargs)
		
		# Send low stock alert if stock dropped below threshold
		if old_stock and old_stock > 5 and self.stock_quantity <= 5 and self.stock_quantity > 0:
			try:
				from .email_utils import send_low_stock_alert_email
				send_low_stock_alert_email(self)
			except Exception as e:
				print(f"Error sending low stock alert: {e}")