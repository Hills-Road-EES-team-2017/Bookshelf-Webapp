from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Partition
from .algorithms import find_partitions_for_returning_books
from .forms import AddBookForm
from django.http import HttpResponseRedirect


def get_basket(user):
    basket = Book.objects.filter(customer=user.id)
    obj_basket = []
    for book in basket:
        obj_basket.append(book)
    return obj_basket



#def add_to_basket(request, book_id):
#    customer = request.user
#    customer.profile.basket += str(book_id)+','
#    customer.save()

#def remove_from_basket(request, id):
#    customer = request.user
#    customer.profile.basket = customer.profile.basket.replace((str(id)+','),'')
#    customer.save()

def strips(basket):  # Function from LED team
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
    if is_master(request.user):
        add_button = True
    else:
        add_button = False

    try:
        search = request.POST['search']
        # Retrieves list of all books containing search (default = "")
        book_list = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search)
    except:
        print("error")

    # Displays homepage.html where book_list is the values from line above and states is the possible string states
    return render(request, 'website/homepage.html', {'book_list': book_list, 'current_user': request.user.username, 'searched': search, 'add_button': add_button})

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
    user_basket = get_basket(request.user)
    return render(request, 'website/basket.html', {'basket': user_basket, 'current_user':request.user.username})

@login_required
def update_basket(request, book_id):
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
        if not str(book.id) in request.user.profile.basket:
            book.book_state = RETURNING_BASKET
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
def delete_basket(request, book_id):

    AVAILABLE = 0
    TAKING = 1
    TAKEN = 2
    RETURNING = 3
    RESERVED = 4
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
def map(request):
    user_basket = get_basket(request.user)
    returning_basket = []
    for book in user_basket:
        if book.book_state == 6:
            returning_basket.append(book)
    #found_partitions = find_partitions_for_returning_books(returning_basket, Partition.objects.all())
    found_partitions = []
    #TEMPORARY FIXXXXX
    for x in range(len(returning_basket)):
        found_partitions.append(Partition.objects.all()[0])
    #ENDTEMP FIXXXXX
    sections = []
    index = 0
    for book in user_basket:
        if book.book_state == 6:
            book.partition = found_partitions[index]
            book.save()
            index += 1
        sections.append(book.partition.section.name)
    zipped_books = zip(user_basket, sections)
    return render(request, 'website/maps.html', {'basket': zipped_books})
@login_required
def leds(request):

    AVAILABLE = 0
    TAKING = 1
    TAKEN = 2
    RETURNING = 3
    RESERVED = 4
    TAKING_BASKET = 5
    RETURNING_BASKET = 6

    basket = get_basket(request.user)
    for book in basket:
        if book.book_state == TAKING_BASKET:
            book.book_state = TAKING
            book.last_updated = datetime.now()
        elif book.book_state == RETURNING_BASKET:
            book.book_state = RETURNING
            book.last_updated = datetime.now()
        book.save()
    strips(get_basket(request.user))
    return redirect('off')

@login_required
def off(request):
    AVAILABLE = 0
    TAKING = 1
    TAKEN = 2
    RETURNING = 3
    RESERVED = 4
    TAKING_BASKET = 5
    RETURNING_BASKET = 6
    user_basket = get_basket(request.user)
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
                # Books on the partition further right than selected book
                if other.partition_depth>book.partition_depth:
                    # Moved to the left
                    other.partition_depth -= book.book_width
                    other.save()

        elif book.book_state == RETURNING:
            # Set to available
            book.book_state = AVAILABLE
            book.last_updated = datetime.now()
            partition.partition_space -= book.book_width
            further_books = Book.objects.filter(partition=book.partition)
            # Sets partition depth to 0, then adds on book width of all other books on partition
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

def is_master(user):
    if user.username == 'master' and user.is_superuser:
        return True
    else:
        return False

@user_passes_test(is_master)
def delete_books_in_basket(request, basket):
    for book in basket:
        if book.book_state == 2:
            book.delete()

@user_passes_test(is_master)
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_title = form.cleaned_data['new_title']
            new_author = form.cleaned_data['new_author']
            new_width = form.cleaned_data['new_width']
            new_book = Book(title=new_title, author=new_author, partition=Partition.objects.all()[0], book_state=2, book_width=new_width, partition_depth=0, customer=request.user, last_taken=datetime.now(), colour='R')
            new_book.save()
            return redirect('homepage')
        else:
            return render(request, 'website/add.html', {'form': form})
    else:
        form = AddBookForm()

    return render(request, 'website/add.html', {'form': form})