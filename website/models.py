from django.db import models
import enum

class BookState(enum.Enum):
    pass

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    partition = models.ForeignKey('Partition', on_delete=models.SET(0))
    book_state = models.IntegerField()
    book_width = models.IntegerField()
    partition_depth = models.IntegerField() #distance_from_partition
    customer = models.ForeignKey('Customer', on_delete=models.SET(0))
    last_updated = models.DateTimeField()
    colour = models.CharField(max_length=1)
    def __str__(self):
        return self.title
    
class Partition(models.Model):
    partition_position = models.CharField(max_length=1)
    partition_space = models.IntegerField()
    shelf_distance = models.IntegerField()
    user_distance = models.IntegerField() #distance_from_user
    #def __str__(self):
    #    return self.AutoField

class Customer(models.Model):
    surname = models.CharField(max_length=30)
    email = models.EmailField()
    card_number = models.IntegerField()
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.surname
    
