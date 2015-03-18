# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import City, Event, Category

admin.site.register(City)
admin.site.register(Category)
admin.site.register(Event)
