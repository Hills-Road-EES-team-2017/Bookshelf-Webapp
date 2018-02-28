from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Book,Profile, Partition


def get_basket(basket):
    # e.g. basket = '3,5,1,8,4,'
    obj_basket = []
    for id in range(0,len(basket),2):
        print (basket[id])
        obj_basket.append(get_object_or_404(Book, pk=int(basket[id])))
    return obj_basket

def add_to_basket(request, book_id):
    customer = request.user
    customer.profile.basket += str(book_id)+','
    customer.save()

def remove_from_basket(request, id):
    customer = request.user
    customer.profile.basket = customer.profile.basket.replace((str(id)+','),'')
    customer.save()

def find_partition(width):
    # Gets all partitions ordered from lowest distance away
    for partition in Partition.objects.all().order_by('user_distance'):
        if partition.partition_space >= width:
            return partition
            break


def strips(basket):  # Function from LED team
    basket = get_basket(basket)
    for book in basket:
        print ("LEDS TURNED ON FOR BOOK", book.id)


@login_required
def select(request):
    return render(request, 'website/select.html')


@login_required
def taken(request):

    # User is returing books
    customer = request.user
    # Retrieves book list of customers books where state is taken
    book_list = Book.objects.filter(customer=customer.id, book_state=2)
    return render(request, 'website/taken.html', {'book_list': book_list, 'current_user': request.user.username})


@login_required
def homepage(request):
    book_list = []
    search = ""
    try:
        search = request.POST['search']
        # Retrieves list of all books containing search (default = "")
        book_list = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search)
    except:
        print("error")

    # Displays homepage.html where book_list is the values from line above and states is the possible string states
    return render(request, 'website/homepage.html', {'book_list': book_list, 'current_user': request.user.username, 'searched': search})

@login_required
def detail(request, book_title):
    # Retrieves book where pk is the id passed into it
    book = get_object_or_404(Book, title=book_title)
    if book.book_state == 0:
        taking = 0
    elif book.book_state == 2 and book.customer == request.user:
        taking = 1
    else:
        taking = 2
    return render(request, 'website/detail.html', {'book': book, 'current_user': request.user.username, 'taking': taking})

@login_required
def basket(request):
    user_basket = get_basket(request.user.profile.basket)
    return render(request, 'website/basket.html', {'basket': user_basket, 'current_user':request.user.username})

@login_required
def update_basket(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    AVAILABLE = 0
    TAKEN = 2
    RESERVED = 4

    if book.book_state == AVAILABLE: # If taking book
        # Set to taking
        book.book_state = RESERVED
        book.customer = request.user
        add_to_basket(request, book.id)

    elif book.book_state == TAKEN and book.customer == request.user:
        if not str(book.id) in request.user.profile.basket:
            add_to_basket(request, book.id)
    else:
        return redirect('homepage')

    colours = ["Red","Yellow", "Green", "Cyan", "Blue", "Magenta", "White"]
    for book_colour in (Book.objects.filter(partition=book.partition, book_state=1)|Book.objects.filter(partition=book.partition, book_state = 3)):
        if book_colour.colour in colours:
            colours.remove(book_colour.colour)
    book.colour = colours[0]
    book.save()
    return redirect('basket')


@login_required
def map(request):
    user_basket = get_basket(request.user.profile.basket)
    sections = []
    for book in user_basket:
        sections.append(book.partition.section.name)
    zipped_books = zip(user_basket, sections)
    return render(request, 'website/maps.html', {'basket': zipped_books})

def leds(request):

    AVAILABLE = 0
    TAKING = 1
    TAKEN = 2
    RETURNING = 3
    RESERVED = 4

    basket = get_basket(request.user.profile.basket)
    for book in basket:
        if book.book_state == RESERVED:
            book.book_state = TAKING
            book.last_updated = datetime.now()
        elif book.book_state == TAKEN:
            book.book_state = RETURNING
            book.last_updated = datetime.now()
        book.save()
    strips(request.user.profile.basket)
    return redirect('off')

@login_required
def off(request):
    AVAILABLE = 0
    TAKING = 1
    TAKEN = 2
    RETURNING = 3
    RESERVED = 4
    user_basket = get_basket(request.user.profile.basket)
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
            further_books = Book.objects.filter(partition=book.partition)
            for other in further_books:
                # Books on the partition further right than selected boo
                if other.partition_depth>book.partition_depth:
                    # Moved to the left
                    other.partition_depth -= book.partition_depth
                    other.save()

            book.save()
            partition.save()
        elif book.book_state == RETURNING:
            # Set to available
            book.book_state = AVAILABLE
            book.last_updated = datetime.now()
            partition.partition_space -= book.book_width
            further_books = Book.objects.filter(partition=book.partition)
            book.partition_depth = 0
            book.save()
            for other in further_books:
                book.partition_depth += other.book_width
            book.save()
            partition.save()
    customer = request.user
    customer.profile.basket = ''
    customer.save()

    return render(request, 'website/off.html')
