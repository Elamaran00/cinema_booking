from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .models import Movie, Showtime, Cinema, Booking, Seat
from .forms import UserRegistrationForm, BookingForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import logout

def home(request):
    now = timezone.now()
    movies = Movie.objects.all()
    upcoming_showtimes = Showtime.objects.filter(start_time__gte=now).order_by('start_time')[:5]
    return render(request, 'booking/home.html', {
        'movies': movies,
        'upcoming_showtimes': upcoming_showtimes,
    })


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'booking/movie_list.html', {'movies': movies})


@login_required(login_url='login')
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    now = timezone.now()
    showtimes = Showtime.objects.filter(movie=movie, start_time__gte=now).order_by('start_time')
    return render(request, 'booking/movie_detail.html', {
        'movie': movie,
        'showtimes': showtimes,
    })


@login_required(login_url='login')
def showtime_detail(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = showtime.seats.all().order_by('row', 'number')

    # Group seats by row
    seat_rows = {}
    for seat in seats:
        seat_rows.setdefault(seat.row, []).append(seat)

    if request.method == 'POST':
        # Get selected seats
        selected_seat_ids = [s for s in request.POST.get('seats', '').split(',') if s]

        if not selected_seat_ids:
            messages.error(request, 'Please select at least one seat.')
            return render(request, 'booking/showtime_detail.html', {'showtime': showtime, 'seat_rows': seat_rows})

        selected_seats = Seat.objects.filter(id__in=selected_seat_ids, showtime=showtime)

        # Check availability
        unavailable_seats = selected_seats.filter(is_available=False)
        if unavailable_seats.exists():
            seat_numbers = [f"{seat.row}{seat.number}" for seat in unavailable_seats]
            messages.error(request, f"Seats unavailable: {', '.join(seat_numbers)}")
            return render(request, 'booking/showtime_detail.html', {'showtime': showtime, 'seat_rows': seat_rows})

        # Create booking
        total_price = showtime.price * selected_seats.count()
        booking = Booking.objects.create(user=request.user, showtime=showtime, total_price=total_price, is_confirmed=True)
        booking.seats.set(selected_seats)

        # Mark seats unavailable
        selected_seats.update(is_available=False)

        messages.success(request, 'Booking confirmed successfully!')
        return redirect('booking_confirmation', booking_id=booking.id)

    return render(request, 'booking/showtime_detail.html', {'showtime': showtime, 'seat_rows': seat_rows})


@login_required(login_url='login')
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})


# def register(request):
    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()

    #         # Auto-login new user
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password1')
    #         user = authenticate(username=username, password=password)

    #         if user:
    #             login(request, user)
    #             messages.success(request, f'Welcome {user.username}, your account was created successfully!')
    #             return redirect('home')  # ✅ go home instead of login page
    # else:
    #     form = UserRegistrationForm()

    # return render(request, 'booking/register.html', {'form': form})


@login_required(login_url='login')
def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(genre__icontains=query) |
        Q(language__icontains=query)
    )
    return render(request, 'booking/search_results.html', {'movies': movies, 'query': query})



# def register_view(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Auto login after register
#             return redirect("home")  # Redirect to home page
#     else:
#         form = UserCreationForm()
#     return render(request, "register.html", {"form": form})


# Login Page
# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("home")  
#     else:
#         form = AuthenticationForm()
#     return render(request, "login.html", {"form": form})


# # Logout Page


# def logout_view(request):
#     logout(request)  
#     return redirect("login")   # 👈 use the url name, not "login.html"

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('movie_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')