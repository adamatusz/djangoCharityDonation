from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Donation
from .forms import (UserAdminCreationForm,
                    UserAdminChangeForm)

# Register your models here.

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    #   update form
    form = UserAdminChangeForm
#   create view
    add_form = UserAdminCreationForm
#   The fields to be used in displaying the User model.
#   These override the definitions on the base UserAdmin
#   that reference specific fields on auth.User.
    list_display = ['email', 'admin']
    list_filter = ['admin', 'staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'staff', 'admin',)}),
    )
#   add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#   overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email', 'last_name']
    ordering = ['email', 'last_name']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.register(Donation)
