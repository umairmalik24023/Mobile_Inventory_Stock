from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import UserDetailForm, PostDetailForm, CustomerDetailForm, ContactUserForm, AuthUserForm, OrderForm, InventoryForm
from .models import CustomerDetail, ContactUser, UserDetail, Order, Inventory


def superuser_required(user):
	return user.is_authenticated and user.is_superuser


@user_passes_test(superuser_required)
def create_user_detail(request):
	if request.method == 'POST':
		form = UserDetailForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('admin_dashboard'))
	else:
		form = UserDetailForm()
	return render(request, 'user_form.html', {'form': form})


@user_passes_test(superuser_required)
def create_post_detail(request):
	if request.method == 'POST':
		form = PostDetailForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('admin_dashboard'))
	else:
		form = PostDetailForm()
	return render(request, 'post_form.html', {'form': form})


@user_passes_test(superuser_required)
def users_list(request):
    users = User.objects.order_by('-date_joined')
    custom_users = UserDetail.objects.order_by('-created_at')
    return render(request, 'users_list.html', {'users': users, 'custom_users': custom_users})


@user_passes_test(superuser_required)
def create_customer_detail(request):
	if request.method == 'POST':
		form = CustomerDetailForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('customers_list'))
	else:
		form = CustomerDetailForm()
	return render(request, 'customer_detail.html', {'form': form})


@user_passes_test(superuser_required)
def customers_list(request):
	customers = CustomerDetail.objects.order_by('-created_at')
	return render(request, 'customers_list.html', {'customers': customers})


def contact_create(request):
	if request.method == 'POST':
		form = ContactUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('home'))
	else:
		form = ContactUserForm()
	return render(request, 'contact.html', {'form': form})


@user_passes_test(superuser_required)
def contact_users_list(request):
	contacts = ContactUser.objects.order_by('-created_at')
	return render(request, 'contact_users.html', {'contacts': contacts})


@user_passes_test(superuser_required)
@require_http_methods(["GET", "POST"])
def user_update(request, user_id: int):
    user_obj = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AuthUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('users_list'))
    else:
        form = AuthUserForm(instance=user_obj)
    return render(request, 'users_edit.html', {'form': form, 'user_obj': user_obj})


@user_passes_test(superuser_required)
@require_http_methods(["GET", "POST"])
def custom_user_update(request, custom_user_id: int):
    custom_user = get_object_or_404(UserDetail, pk=custom_user_id)
    if request.method == 'POST':
        form = UserDetailForm(request.POST, instance=custom_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect(reverse('users_list'))
    else:
        form = UserDetailForm(instance=custom_user)
    return render(request, 'user_form.html', {'form': form})


@user_passes_test(superuser_required)
@require_http_methods(["POST"])
def user_delete(request, user_id: int):
    user_obj = get_object_or_404(User, pk=user_id)
    # Prevent deleting the currently logged-in user to avoid immediate logout/redirect
    if request.user.id == user_obj.id:
        messages.error(request, 'You cannot delete the account you are currently logged in with.')
        return redirect(reverse('users_list'))
    user_obj.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect(reverse('users_list'))


@user_passes_test(superuser_required)
@require_http_methods(["POST"])
def custom_user_delete(request, custom_user_id: int):
    custom_user = get_object_or_404(UserDetail, pk=custom_user_id)
    custom_user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect(reverse('users_list'))


# Order Management Views
@user_passes_test(superuser_required)
def orders_list(request):
    # The OrderManager automatically filters out orders without valid customers
    orders = Order.objects.select_related('customer').all()
    return render(request, 'orders_list.html', {'orders': orders})


@user_passes_test(superuser_required)
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created successfully.')
            return redirect(reverse('orders_list'))
    else:
        form = OrderForm()
    return render(request, 'order_form.html', {'form': form})


@user_passes_test(superuser_required)
@require_http_methods(["GET", "POST"])
def order_update(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully.')
            return redirect(reverse('orders_list'))
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_form.html', {'form': form, 'order': order})


@user_passes_test(superuser_required)
@require_http_methods(["POST"])
def order_delete(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    messages.success(request, 'Order deleted successfully.')
    return redirect(reverse('orders_list'))


@user_passes_test(superuser_required)
def order_detail(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_detail.html', {'order': order})


# Dashboard view with mobile shop statistics
@user_passes_test(superuser_required)
def admin_dashboard(request):
    # Get statistics for mobile shop
    total_customers = CustomerDetail.objects.count()
    total_orders = Order.objects.count()
    total_contacts = ContactUser.objects.count()
    total_users = UserDetail.objects.count()
    
    # Recent orders - OrderManager automatically filters out orders without valid customers
    recent_orders = Order.objects.select_related('customer').all()[:5]
    
    # Order status counts - OrderManager automatically filters out orders without valid customers
    pending_orders = Order.objects.filter(order_status='pending').count()
    processing_orders = Order.objects.filter(order_status='processing').count()
    shipped_orders = Order.objects.filter(order_status='shipped').count()
    delivered_orders = Order.objects.filter(order_status='delivered').count()
    
    context = {
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_contacts': total_contacts,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
    }
    return render(request, 'admin.html', context)


# Inventory Management Views
@user_passes_test(superuser_required)
def inventory_list(request):
    """Display beautiful inventory page with carousel and zoom effects"""
    # Get all inventory items
    featured_items = Inventory.objects.filter(is_featured=True, status='in_stock')
    new_arrivals = Inventory.objects.filter(is_new_arrival=True, status='in_stock')
    all_items = Inventory.objects.filter(status='in_stock')
    
    # Group by brand for better organization
    brands = Inventory.objects.values_list('brand', flat=True).distinct()
    
    context = {
        'featured_items': featured_items,
        'new_arrivals': new_arrivals,
        'all_items': all_items,
        'brands': brands,
    }
    return render(request, 'inventory.html', context)


@user_passes_test(superuser_required)
def create_inventory_item(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item created successfully.')
            return redirect(reverse('inventory_list'))
    else:
        form = InventoryForm()
    return render(request, 'inventory_form.html', {'form': form})


@user_passes_test(superuser_required)
@require_http_methods(["GET", "POST"])
def inventory_update(request, item_id: int):
    item = get_object_or_404(Inventory, pk=item_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated successfully.')
            return redirect(reverse('inventory_list'))
    else:
        form = InventoryForm(instance=item)
    return render(request, 'inventory_form.html', {'form': form, 'item': item})


@user_passes_test(superuser_required)
@require_http_methods(["POST"])
def inventory_delete(request, item_id: int):
    item = get_object_or_404(Inventory, pk=item_id)
    item.delete()
    messages.success(request, 'Inventory item deleted successfully.')
    return redirect(reverse('inventory_list'))


@user_passes_test(superuser_required)
def inventory_detail(request, item_id: int):
    item = get_object_or_404(Inventory, pk=item_id)
    return render(request, 'inventory_detail.html', {'item': item})
