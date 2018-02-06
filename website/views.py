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



def return_(request, book_title):

    if check_login():
        return redirect('login')

    book = get_object_or_404(Book, title=book_title)

    # Set to returning
    book.book_state = 3
    book.save()
    #    if True: # If button pressed within time
    #        # Set to available
    #        book.book_state = 0
    #        book.partition = find_partition(book.book_width)
    #        book.save()
    #    else:
    #        # Set to taken again
    #        book.book_state = 2
    #        book.save()



    strips(book.id)

    partition = get_object_or_404(Partition, pk=int(book.partition.id))
    return render(request, 'website/LEDs.html', {'book': book, 'partition': partition})


def take(request, book_title):

    if check_login():
        return redirect('login')

    book = get_object_or_404(Book, title=book_title)

    # If the customer is taking a book
        # Set to taking
    book.book_state = 1
    book.save()
        #if True:  # If button pressed within time
        #    # Set to taken
        #    book.book_state = 2
        #    book.customer = Customer.objects.get(surname=v.current_user)
        #    book.last_taken = datetime.now()
        #    book.save()
        #else:
        #    # Set to available again
        #    book.book_state = 0
        #    book.save()

    strips(book.id)

    partition = get_object_or_404(Partition, pk=int(book.partition.id))
    return render(request, 'website/LEDs.html', {'book': book, 'partition': partition})


def off(request, book_title):
    book = get_object_or_404(Book, title=book_title)
    if v.usage:
        # Set to taken
        book.book_state = 2
        book.customer = Customer.objects.get(surname=v.current_user)
        book.last_taken = datetime.now()
        book.save()
    else:
      # Set to available
        book.book_state = 0
        book.partition = find_partition(book.book_width)
        book.save()

    return render(request, 'website/off.html', {'book': book})
