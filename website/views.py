from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from datetime import datetime



from .models import Book, Customer, Partition

# Global variables (I never read a style guide...)
class v(object):
    # Tracks whether a user is logged in or not
    current_user = ""
    # Taking = True, returning = False
    usage = True
    basket = []


def basket(request):
    return render(request, 'website/basket.html', {"basket": v.basket})


def check_login():
    # Redirects to login page if there is no user
    if v.current_user == "":
        return True
    else:
        return False



def find_partition(width):
    # Gets all partitions ordered from lowest distance away
    for partition in Partition.objects.all().order_by('user_distance'):
        if partition.partition_space >= width:
            return partition
            break



def strips(book_id):  # Function from LED team
    print ("LEDS TURNED ON FOR BOOK", book_id)



def login(request):  # Login page
    v.current_user = ""
    # Starting error message (none)
    error_message = ""
    username = ""
    userpass = ""
    try:
        username = request.POST['username']
        userpass = request.POST['userpass']
        # Returns error if name entered not on database
        user = Customer.objects.get(surname=username)

        if user.password == userpass:
            v.current_user = username
            # Loads homepage URL
            return redirect('select')
        else:
            # Re-renders login page with error message (password incorrect)
            error_message = 'Incorrect password or username'
            return render(request, 'website/login.html', {'error_message': error_message})
    except:
        # If its just the default values of "" no message is displayed
        if  username == "":
            error_message = ""
        else:
            # Re-renders login page with error message (username incorrect)
            error_message = 'Incorrect password or username'
        return render(request, 'website/login.html', {'error_message': error_message})



def select(request):

    if check_login():
        return redirect('login')

    return render(request, 'website/select.html')



def taken(request):

    if check_login():
        return redirect('login')
    # User is returing books
    v.usage = False
    customer = Customer.objects.get(surname=v.current_user)
    # Retrieves book list of customers books where state is taken
    book_list = Book.objects.filter(customer=customer.id, book_state=2)
    return render(request, 'website/taken.html', {'book_list': book_list, 'current_user': v.current_user})



def homepage(request):

    if check_login():
        return redirect('login')

    book_list = []
    search = ""
    try:
        search = request.POST['search']
        # Retrieves list of all books containing search (default = "")
        book_list = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search)
    except:
        print("error")

    v.usage = True
    # Displays homepage.html where book_list is the values from line above and states is the possible string states
    return render(request, 'website/homepage.html', {'book_list': book_list, 'current_user': v.current_user, 'searched': search})


def detail(request, book_title):

    if check_login():
        return redirect('login')

    taking = v.usage
    # Retrieves book where pk is the id passed into it
    book = get_object_or_404(Book, title=book_title)
    return render(request, 'website/detail.html', {'book': book, 'current_user': v.current_user, 'taking': taking})


def basket_direct(request):

    if check_login():
        return redirect('login')

    return render(request, 'website/basket.html', {'basket': v.basket})


def basket(request, book_id):

    if check_login():
        return redirect('login')

    book = get_object_or_404(Book, pk=book_id)

    if v.usage: # If taking book
        # Set to taking
        book.book_state = 1
        book.customer = Customer.objects.get(surname=v.current_user)

    else:
        # Set to returning
        book.book_state = 3
        book.partition = find_partition(book.book_width)


    colours = ["Red","Yellow", "Green", "Cyan", "Blue", "Magenta", "White"]
    for book_colour in (Book.objects.filter(partition=book.partition, book_state=1)|Book.objects.filter(partition=book.partition, book_state = 3)):
        if book_colour.colour in colours:
            colours.remove(book_colour.colour)
    book.colour = colours[0]
    book.save()
    v.basket.append(book)
    print (v.basket)

    strips(book.id)
    return render(request, 'website/basket.html', {'basket': v.basket})

def map(request):
    sections = []
    for book in v.basket:
        sections.append(book.partition.section.name)
    zipped_books = zip(v.basket, sections)
    return render(request, 'website/maps.html', {'basket': zipped_books})


def off(request):
    for book in v.basket:
        partition = get_object_or_404(Partition, pk=book.partition.id)
        if book.book_state == 1:
            # Set to taken
            book.book_state = 2
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
        elif book.book_state == 3:
            # Set to available
            book.book_state = 0
            book.last_updated = datetime.now()
            partition.partition_space -= book.book_width
            further_books = Book.objects.filter(partition=book.partition)
            book.partition_depth = 0
            book.save()
            for other in further_books:
                book.partition_depth += other.book_width
            book.save()
            partition.save()
    v.basket = []

    return render(request, 'website/off.html')
