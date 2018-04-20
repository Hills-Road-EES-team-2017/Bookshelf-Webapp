from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):

    states = (
        (0,'available'),
        (1,'taking'),
        (2,'taken'),
        (3,'returning'),
        (4,'reserved'),
        (5, 'taking basket'),
        (6, 'returning basket')
    )

    colours = (
        ("R", "Red"),
        ("Y", "Yellow"),
        ("G", "Green"),
        ("C", "Cyan"),
        ("B", "Blue"),
        ("M", "Magenta"),
        ("W", "White")
    )

    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    picture = models.CharField(max_length=50, default="blank_book.png")
    description = models.CharField(max_length=500, default="Description not yet set")
    partition = models.ForeignKey('Partition', on_delete=models.SET(0), default=0)
    book_state = models.IntegerField(choices=states, default=0)
    book_width = models.IntegerField()
    partition_depth = models.IntegerField() #distance_from_partition
    customer = models.ForeignKey(User, on_delete=models.SET(0), default=0)
    last_updated = models.DateTimeField(auto_now=True)
    last_taken = models.DateTimeField(default=datetime.now)
    colour = models.CharField(max_length=1, choices=colours, default="R")
    def __str__(self):
        return self.title
    
class Partition(models.Model):
    section = models.ForeignKey('Section', on_delete=models.SET(0), default=0)
    partition_space = models.IntegerField()
    shelf_distance = models.IntegerField()
    user_distance = models.IntegerField() #distance_from_user
    #def __str__(self):
    #    return self.AutoField

class Section(models.Model):
    name = models.CharField(max_length=1)
    picture = models.CharField(max_length=50)
    def __str__(self):
        return self.name
