from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Item, Size
from django.db.models import Q, F
from django.db.models.functions import Lower

def index(request):
    query = request.GET.get('q', '').strip()
    categories = Category.objects.all()
    
    if query:
        items = Item.objects.select_related('category').annotate(lower_name=Lower('name')).filter(
            Q(lower_name__icontains=query.lower()) |
            Q(lower_name__icontains=query.capitalize()) |
            Q(lower_name__icontains=query.upper()) |
            Q(category__name__icontains=query.lower())|
            Q(category__name__icontains=query.upper())|
            Q(category__name__icontains=query.capitalize())
            
            # KISS pattern 
        )
    else:
        items = Item.objects.all()

    context = {
        'categories': categories,
        'items': items,
        'query': query
    }
    return render(request, 'index.html', context)


def add_size(request, size_id):
    size = get_object_or_404(Size, id=size_id)

    if request.method == "POST":
        count = request.POST.get('count')
        if count.isdigit():  # Ensure input is a number
            count = int(count)
            size.left = F('left') + count  # Increment left value
            size.save()
            size.refresh_from_db()  # Update after F() operation
            return redirect('index')  # Redirect back to main page

    return render(request, 'add_size.html', {'size': size})


def remove_size(request, size_id):
    size = get_object_or_404(Size, id=size_id)

    if request.method == "POST":
        count = request.POST.get('count')
        if count.isdigit():  # Ensure input is a number
            count = int(count)
            if size.left >= count:  # Prevent negative stock
                size.left = F('left') - count  # Decrement left value
                size.save()
                size.refresh_from_db()  # Update after F() operation
            else:
                # Optional: Show a message that stock is too low
                pass  

        return redirect('index')  # Redirect back to main page

    return render(request, 'remove_size.html', {'size': size})