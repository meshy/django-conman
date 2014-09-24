from django.views.generic import DetailView


class PageDetail(DetailView):
    """
    Show a Page in all its glory!

    Requires `handler` in the kwargs in order to get the Page instance.
    """
    def get_object(self):
        return self.kwargs['node']
