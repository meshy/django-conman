from django.shortcuts import render


def page_view(request, route):
    """Handle basic 'Page' requests."""
    return render(request, 'example/page.html', {'route': route})
