from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "avatar",
        "email",
        "first_name",
        "last_name",
        "phone",
        "city",
        "is_active",
    )
    search_fields = ("email",)
    list_filter = ("email",)
