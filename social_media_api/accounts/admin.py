from django.contrib import admin


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email")
    ordering = ("username",)
