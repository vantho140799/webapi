from django.shortcuts import render

from .models import ColoringBook

def profile_view(request):
    coloring_books = ColoringBook.objects.all() 
    return render(request, 'pages/social.html', {'coloring_books': coloring_books})