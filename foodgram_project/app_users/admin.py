from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UseAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.register(User, UseAdmin)
