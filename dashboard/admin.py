from django.contrib import admin
from .models import UserDetail, PostDetail, CustomerDetail
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
	list_display = ("first_name", "last_name", "email", "phone", "city", "country", "created_at")
	search_fields = ("first_name", "last_name", "email", "phone", "city", "country")
	list_filter = ("country", "city")
	ordering = ("-created_at",)
	list_per_page = 25


@admin.register(PostDetail)
class PostDetailAdmin(admin.ModelAdmin):
	list_display = ("title", "category", "is_published", "published_at", "created_at")
	search_fields = ("title", "category")
	list_filter = ("is_published", "category")
	ordering = ("-created_at",)
	list_per_page = 25


@admin.register(CustomerDetail)
class CustomerDetailAdmin(admin.ModelAdmin):
	list_display = ("first_name", "last_name", "phone", "mobile_model", "price", "purchase_date", "city", "created_at")
	search_fields = ("first_name", "last_name", "email", "phone", "mobile_model", "city", "country")
	list_filter = ("purchase_date", "city", "country")
	ordering = ("-created_at",)
	list_per_page = 25


# Customize built-in Users list in Django admin for a better UI/UX
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	list_display = (
		"username",
		"email",
		"first_name",
		"last_name",
		"is_active",
		"is_staff",
		"is_superuser",
		"last_login",
		"date_joined",
	)
	list_filter = ("is_staff", "is_superuser", "is_active", "groups")
	search_fields = ("username", "first_name", "last_name", "email")
	ordering = ("-date_joined",)
	list_per_page = 50
