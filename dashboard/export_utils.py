import csv
import io
from django.http import HttpResponse
from django.utils import timezone
from .models import Order, CustomerDetail, ContactUser, Inventory


def export_orders_to_csv(orders):
    """Export orders to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="orders_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Order Number', 'Customer Name', 'Customer Email', 'Product Name', 
        'Product Model', 'Quantity', 'Unit Price', 'Total Amount', 
        'Order Status', 'Payment Status', 'Order Date', 'Shipping Address'
    ])
    
    for order in orders:
        writer.writerow([
            order.order_number,
            f"{order.customer.first_name} {order.customer.last_name}",
            order.customer.email,
            order.product_name,
            order.product_model,
            order.quantity,
            order.unit_price,
            order.total_amount,
            order.get_order_status_display(),
            order.get_payment_status_display(),
            order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            order.shipping_address
        ])
    
    return response


def export_customers_to_csv(customers):
    """Export customers to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="customers_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'First Name', 'Last Name', 'Email', 'Phone', 'Address', 
        'City', 'Country', 'Mobile Model', 'Price', 'Purchase Date', 'Notes', 'Created At'
    ])
    
    for customer in customers:
        writer.writerow([
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.phone,
            customer.address,
            customer.city,
            customer.country,
            customer.mobile_model,
            customer.price,
            customer.purchase_date,
            customer.notes,
            customer.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response


def export_contacts_to_csv(contacts):
    """Export contact users to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="contacts_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Username', 'Email', 'Phone', 'Created At'])
    
    for contact in contacts:
        writer.writerow([
            contact.name,
            contact.username,
            contact.email,
            contact.phone,
            contact.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response


def export_inventory_to_csv(inventory_items):
    """Export inventory to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventory_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Brand', 'Model Name', 'Model Number', 'Color', 'Storage Capacity',
        'Price', 'Original Price', 'Stock Quantity', 'Status', 'Screen Size',
        'Processor', 'RAM', 'Camera', 'Battery', 'Operating System',
        'Description', 'Features', 'Featured', 'New Arrival', 'Created At'
    ])
    
    for item in inventory_items:
        writer.writerow([
            item.brand,
            item.model_name,
            item.model_number,
            item.color,
            item.storage_capacity,
            item.price,
            item.original_price,
            item.stock_quantity,
            item.get_status_display(),
            item.screen_size,
            item.processor,
            item.ram,
            item.camera_main,
            item.battery_capacity,
            item.operating_system,
            item.description,
            item.features,
            'Yes' if item.is_featured else 'No',
            'Yes' if item.is_new_arrival else 'No',
            item.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response
