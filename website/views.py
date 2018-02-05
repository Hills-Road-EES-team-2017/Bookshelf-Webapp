from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.db.models import Q

from .models import Book, Customer, Partition

class v(object):
    current_user = ""
    usage = True

def check_login():
    if v.current_user == "":
        return True
    else:
        return False


def strips(book_id): #Function from LED team
    print ("LEDS TURNED ON FOR BOOK", book_id) #...number x

def login(request):  #Login page
    #Starting error message (none)
    v.current_user = ""
    error_message = ""
    username = ""
    userpass = ""
    try:
        #Returns error if name entered not on database
        username = request.POST['username']
        userpass = request.POST['userpass']
        user = Customer.objects.get(surname=username)

        if user.password == userpass:
            #Loads homepage URL
            v.current_user = username
            return redirect('select')
        else:
            #Re-renders login page with error message (password incorrect)
            error_message = 'Incorrect password or username'
            return render(request, 'website/login.html', {'error_message': error_message})
    except:
        #If not the first load of the page with defaul values of ""
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

    v.usage = False
    book_list = []
    customer = Customer.objects.get(surname=v.current_user)
    book_list = Book.objects.filter(customer=customer.id)
    return render(request, 'website/taken.html', {'book_list': book_list})



def homepage(request):

    if check_login():
        return redirect('login')
        #pass

    book_list = []
    search = ""
    try:
        search = request.POST['search']
        # Retrieves list of all books containing search (default = "")
        book_list = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search)
    except:
        print("error")

    v.usage = True
    #Displays homepage.html where book_list is the values from line above and states is the possible string states
    return render(request, 'website/homepage.html', {'book_list': book_list, 'current_user': v.current_user, 'searched': search})



def detail(request, book_title):

    if check_login():
        return redirect('login')

    taking = v.usage
    #Retrieves book where pk is the id passed into it
    book = get_object_or_404(Book, title=book_title)
    return render(request, 'website/detail.html', {'book': book, 'current_user': v.current_user, 'taking': taking})



def LEDs(request, book_title): #Pass parameter for LED function?

    if check_login():
        return redirect('login')


    #########################

    #Code to update database

    #########################
    book = get_object_or_404(Book, title=book_title)
    strips(book.id)

    partition = get_object_or_404(Partition, pk=int(book.partition.id))
    return render(request, 'website/LEDs.html', {'book': book, 'partition': partition})
