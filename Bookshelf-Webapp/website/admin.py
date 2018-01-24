from django.contrib import admin

from .models import Customer, Partition, Book

admin.site.register(Customer)
admin.site.register(Partition)
admin.site.register(Book)
