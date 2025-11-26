from django.urls import path
from . import views

urlpatterns = [
	path('', views.admin_dashboard, name='admin_dashboard'),
	path('users/', views.users_list, name='users_list'),
	path('users/new/', views.create_user_detail, name='user_new'),
	path('users/<int:user_id>/edit/', views.user_update, name='user_update'),
	path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('custom-users/<int:custom_user_id>/edit/', views.custom_user_update, name='custom_user_update'),
    path('custom-users/<int:custom_user_id>/delete/', views.custom_user_delete, name='custom_user_delete'),
	path('posts/new/', views.create_post_detail, name='post_new'),
	path('customers/', views.customers_list, name='customers_list'),
	path('customers/new/', views.create_customer_detail, name='customer_new'),
    path('contact/', views.contact_create, name='contact_create'),
    path('contacts/', views.contact_users_list, name='contact_users_list'),
	# Order Management URLs
	path('orders/', views.orders_list, name='orders_list'),
	path('orders/new/', views.create_order, name='order_new'),
	path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
	path('orders/<int:order_id>/edit/', views.order_update, name='order_update'),
	path('orders/<int:order_id>/delete/', views.order_delete, name='order_delete'),
	# Inventory Management URLs
	path('inventory/', views.inventory_list, name='inventory_list'),
	path('inventory/new/', views.create_inventory_item, name='inventory_new'),
	path('inventory/<int:item_id>/', views.inventory_detail, name='inventory_detail'),
	path('inventory/<int:item_id>/edit/', views.inventory_update, name='inventory_update'),
	path('inventory/<int:item_id>/delete/', views.inventory_delete, name='inventory_delete'),
	# API URLs
	path('api/inventory/<int:item_id>/', views.api_inventory_detail, name='api_inventory_detail'),
	# Export URLs
	path('export/orders/', views.export_orders, name='export_orders'),
	path('export/customers/', views.export_customers, name='export_customers'),
	path('export/contacts/', views.export_contacts, name='export_contacts'),
	path('export/inventory/', views.export_inventory, name='export_inventory'),
	# Reports URLs
	path('reports/', views.reports_dashboard, name='reports_dashboard'),
] 


