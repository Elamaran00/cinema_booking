from django.contrib import admin
from .models import Cinema, Movie, Showtime, Seat, Booking

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'total_theaters']
    search_fields = ['name', 'location']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'language', 'rating']
    list_filter = ['genre', 'language', 'rating']
    search_fields = ['title', 'description']

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'cinema', 'start_time', 'end_time', 'price']
    list_filter = ['cinema', 'start_time']
    search_fields = ['movie__title', 'cinema__name']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['showtime', 'row', 'number', 'is_available']
    list_filter = ['showtime', 'is_available']
    search_fields = ['showtime__movie__title']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'showtime', 'total_price', 'booking_time', 'is_confirmed']
    list_filter = ['is_confirmed', 'booking_time']
    search_fields = ['user__username', 'showtime__movie__title']