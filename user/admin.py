from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UsernameField, ReadOnlyPasswordHashField

from .models import User
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.admin import UserAdmin


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see this '
            'user’s password, but you can change the password using '
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'role', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )

    list_filter = ['is_active', 'is_superuser', 'role', ]

    form = UserChangeForm

    list_display = ('username', 'role')
    list_display_links = ('username',)

    search_fields = ('username', 'full_name')


admin.site.register(User, MyUserAdmin)
