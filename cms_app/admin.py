# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Machine, Order, Interruption, Realization, DBName
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

@admin.register(DBName)
class AuthorAdmin(admin.ModelAdmin):
    pass

