from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Partition
from .algorithms import find_partitions_for_returning_books
from .forms import AddBookForm
from .LED_functions import initialise, send_32bits, LED_function
import RPi.GPIO as GPIO
import time
import spidev

class Ghost_partition:
    def __init__(self, level=0):
        self.book_level = level


spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 1000000
spi.bits_per_word = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)
GPIO.setup(22,GPIO.IN)
GPIO.setwarnings(False)

speed = 0.0000025
number_of_LEDs = 60
number_of_strips = 10
LEDs = [ [int]*number_of_LEDs, ]*number_of_strips

initialise()

def show_book_order(partition): # For testing return mechanism
    books = Book.objects.filter(partition=partition.id)
    ordered_books = sorted(books, key=lambda p: p.partition_depth, reverse=False)
    for book in ordered_books:
        print(book.title,book.book_width,book.partition_depth)
    print()


def get_basket(user): # Retrieves list of books in the user's basket
    basket = Book.objects.filter(customer=user.id, book_state=5)|Book.objects.filter(customer=user.id, book_state=6)
    list_basket = []
    for book in basket: # Creates a python list rather than a django queryset
        list_basket.append(book)
    return list_basket


def get_returning_books(user): # Gets a list of books that were in the user's basket before checkout
    returning_books = Book.objects.filter(customer=user.id, book_state=1)|Book.objects.filter(customer=user.id,book_state=3)
    list_basket = []
    for book in returning_books: # Creates python list rather than a django queryset
        list_basket.append(book)
    return list_basket


def LED_on(book):  # Formulates appropriate input for strips function
    partition = Partition.objects.get(pk=book.partition.id)
    shelf = partition.id
    distance = partition.shelf_distance + book.partition_depth + int(book.book_width/2)
    colour = book.colour
    LED_function(shelf, distance, colour)

def LED_off(book):
    partition = Partition.objects.get(pk=book.partition.id)
    shelf = partition.id
    distance = partition.shelf_distance + book.partition_depth + int(book.book_width/2)
    colour = "O"
    LED_function(shelf, distance, colour)

@login_required
def taken(request): # View for list of user's taken books
    customer = request.user
    # Retrieves book list of customers books where state is taken
    book_list = Book.objects.filter(customer=customer.id, book_state=2)
    return render(request, 'website/taken.html', {'book_list': book_list, 'current_user': request.user.username})


@login_required
def homepage(request): # View for list of all books in library
    book_list = []
    search = ""
    add_button = is_master(request.user) # For adding the 'add book' button if on certain account

    ## show_book_order(Partition.objects.get(pk=11))

    try: # Inital load of page will yield error, as there is no post request
        search = request.POST['search']
        # Retrieves list of all books containing search (default = "")
        book_list = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search)
    except:
        pass

    # Displays homepage.html where book_list is the values from line above and states is the possible string states
    return render(request, 'website/homepage.html', {'book_list': book_list, 'current_user': request.user.username, 'searched': search, 'add_button': add_button})

@login_required
def detail(request, book_title): # View for details of each book individually
    # Retrieves book based on title
    book = get_object_or_404(Book, title=book_title)
    if book.book_state == 0: # If available
        taking = 0 # Context variable for HMTL
    elif book.book_state == 2 and book.customer == request.user: #Only if book is taken by user logged in
        taking = 1
    else:
        taking = 2
    master = is_master(request.user) # For adding 'delete book' button if on certain account
    return render(request, 'website/detail.html', {'book': book, 'current_user': request.user.username, 'taking': taking, 'master': master})

@login_required
def basket(request): # View for displaying user's basket
    user_basket = get_basket(request.user)
    return render(request, 'website/basket.html', {'basket': user_basket, 'current_user':request.user.username})

@login_required
def update_basket(request, book_id): # Non-user view for updating the record of a book being added to basket
    book = get_object_or_404(Book, pk=book_id)
    AVAILABLE = 0
    TAKEN = 2
    TAKING_BASKET = 5
    RETURNING_BASKET = 6

    if book.book_state == AVAILABLE: # If taking book
        # Set to taking
        book.book_state = TAKING_BASKET
        book.customer = request.user

    elif book.book_state == TAKEN and book.customer == request.user:
        book.book_state = RETURNING_BASKET
    else:
        return redirect('homepage')
    book.save()
    return redirect('basket')

@login_required
def delete_basket(request, book_id): # Non-user view for deleting a book from the basket

    AVAILABLE = 0
    TAKEN = 2
    TAKING_BASKET = 5
    RETURNING_BASKET = 6

    basket = get_basket(request.user)
    book = get_object_or_404(Book, pk=book_id)
    if book in basket:
        if book.book_state == TAKING_BASKET:
            book.book_state = AVAILABLE
        elif book.book_state == RETURNING_BASKET:
            book.book_State = TAKEN
        book.save()
    return redirect('basket')

@login_required
def map(request): # View for displaying details of position about books
    ghost_partitions = []
    
    user_basket = get_basket(request.user)
    returning_basket = []
    # Isolates books that are being returned
    for book in user_basket:
        if book.book_state == 6:
            returning_basket.append(book)
    found_partitions = find_partitions_for_returning_books(returning_basket, Partition.objects.all())


    for each_part in found_partitions:
        ghost_partitions.append(Ghost_partition(level=0))
        books = Book.objects.filter(partition=each_part)
        for other in books:
            if other.book_state!=2 and other.book_state!=3 and other.book_state!=6:
                ghost_partitions[-1].book_level += other.book_width



    sections = []
    index = 0
    for book in user_basket:
        # Assigns a new partition to books being returned
        if book in returning_basket:
            book.partition = found_partitions[index]
            book.partition_depth = ghost_partitions[user_basket.index(book)].book_level
            ghost_partitions[user_basket.index(book)].book_level += book.book_width
            book.save()
            index += 1
        # Adds section of all books to the list of sections for HMTL
        sections.append(book.partition.section.name)

    colours = ["R", "Y", "G", "C", "B", "M", "W"]
    led_books = Book.objects.filter(partition__section=book.partition.section).exclude(pk=book.id) # Books in same section
    led_books = led_books.filter(book_state=1)|led_books.filter(book_state=3) # Books with colours in use and same section
    for basket_book in user_basket:
        for live_book in led_books:
            if live_book.colour in colours:
                colours.remove(live_book.colour)
        basket_book.colour = colours[0]
        basket_book.save()
        colours.remove(colours[0])

    zipped_books = zip(user_basket, sections)
    return render(request, 'website/maps.html', {'basket': zipped_books})
@login_required
def leds(request): # Non-user view for turning on LEDs and updating the states of books

    TAKING = 1
    RETURNING = 3
    TAKING_BASKET = 5
    RETURNING_BASKET = 6

    basket = get_basket(request.user)
    # Updates relevent fields of books being taken/returned
    for book in basket:
        if book.book_state == TAKING_BASKET:
            book.book_state = TAKING
            book.last_updated = datetime.now()
        elif book.book_state == RETURNING_BASKET:
            book.book_state = RETURNING
            book.last_updated = datetime.now()
        book.save()
        #Turns on LEDs
        LED_on(book)
    show_book_order(Partition.objects.get(pk=1))
    return redirect('off')

@login_required
def off(request):
    return render(request, 'website/off.html')

@login_required
def leds_off(request): # Placeholder view to simulate pressing of button, with changes of states included
    AVAILABLE = 0
    TAKING = 1
    TAKEN = 2
    RETURNING = 3
    user_basket = get_returning_books(request.user)
    for book in user_basket:
        partition = get_object_or_404(Partition, pk=book.partition.id)
        if book.book_state == TAKING:
            # Set to taken
            book.book_state = TAKEN
            book.last_taken = datetime.now()
            book.last_updated = datetime.now()
            # Space on the partition increased
            partition.partition_space += book.book_width
            # All other books on partition
            further_books = Book.objects.filter(partition=book.partition).exclude(pk=book.id)
            for other in further_books:
                # Books on the partition further right than selected book
                if other.partition_depth > book.partition_depth:
                    # Moved to the left
                    other.partition_depth -= book.book_width
                    other.save()

        elif book.book_state == RETURNING:
            # Set to available
            book.book_state = AVAILABLE
            book.last_updated = datetime.now()
            partition.partition_space -= book.book_width
            further_books = Book.objects.filter(partition=book.partition).exclude(pk=book.id)
            # Sets partition depth to 0, then adds on book width of all other books on partition
            book.partition_depth = 0
            book.save()
            for other in further_books:
                if other.book_state!=2 and other.book_state!=3 and other.book_state!=6:
                    print(other.title, other.book_state)
                    book.partition_depth += other.book_width
        book.save()
        partition.save()
        LED_off(book)

        
    return redirect('homepage')

def is_master(user): # Function to determine if the 'master' superuser is logged in
    if user.username == 'master' and user.is_superuser:
        return True
    else:
        return False

@user_passes_test(is_master)
def delete_book(request, book_id): # Non-user view which deletes book from database
    book = Book.objects.get(pk=book_id)
    if book.book_state == 2:
        book.delete()
    return redirect('homepage')

@user_passes_test(is_master)
def add_book(request): # Master-only view which allows new book to be created
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_title = form.cleaned_data['new_title']
            new_author = form.cleaned_data['new_author']
            new_width = form.cleaned_data['new_width']
            new_book = Book(title=new_title, author=new_author, partition=Partition.objects.all()[0], book_state=2, book_width=new_width, partition_depth=100, customer=request.user, last_taken=datetime.now(), colour='R')
            new_book.save()
            return redirect('homepage')
        else:
            return render(request, 'website/add.html', {'form': form})
    else:
        form = AddBookForm()

    return render(request, 'website/add.html', {'form': form})
