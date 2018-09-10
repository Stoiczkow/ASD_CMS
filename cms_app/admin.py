from django.contrib import admin
from .models import Machine, Order, Interruption, Realization
# Register your models here.

@admin.register(Machine)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Interruption)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Realization)
class AuthorAdmin(admin.ModelAdmin):
    pass
