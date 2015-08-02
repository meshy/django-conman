from django.views.generic import DetailView


class PageDetail(DetailView):
    """Show a Page in all its glory."""
    def get_object(self):
        """Return the Page Route passed in kwargs for rendering."""
        return self.kwargs['route']
