from django.contrib import admin

from .models import Partition, Book, Section

admin.site.register(Section)
admin.site.register(Partition)
admin.site.register(Book)
