from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, CustomerDetail


def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'Order Confirmation - {order.order_number}'
        
        context = {
            'order': order,
            'customer': order.customer,
            'site_name': 'Mobile Shop'
        }
        
        html_message = render_to_string('emails/order_confirmation.html', context)
        plain_message = render_to_string('emails/order_confirmation.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending order confirmation email: {e}")
        return False


def send_order_status_update_email(order):
    """Send order status update email to customer"""
    try:
        subject = f'Order Status Update - {order.order_number}'
        
        context = {
            'order': order,
            'customer': order.customer,
            'site_name': 'Mobile Shop'
        }
        
        html_message = render_to_string('emails/order_status_update.html', context)
        plain_message = render_to_string('emails/order_status_update.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending order status update email: {e}")
        return False


def send_low_stock_alert_email(inventory_item):
    """Send low stock alert email to admin"""
    try:
        subject = f'Low Stock Alert - {inventory_item.model_name}'
        
        context = {
            'item': inventory_item,
            'site_name': 'Mobile Shop'
        }
        
        html_message = render_to_string('emails/low_stock_alert.html', context)
        plain_message = render_to_string('emails/low_stock_alert.txt', context)
        
        # Send to admin email (you can configure this in settings)
        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending low stock alert email: {e}")
        return False


def send_contact_form_notification(contact_user):
    """Send notification email when contact form is submitted"""
    try:
        subject = f'New Contact Form Submission - {contact_user.name}'
        
        context = {
            'contact': contact_user,
            'site_name': 'Mobile Shop'
        }
        
        html_message = render_to_string('emails/contact_notification.html', context)
        plain_message = render_to_string('emails/contact_notification.txt', context)
        
        # Send to admin email
        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending contact notification email: {e}")
        return False
