from django.views.generic import DetailView

from . import models


class PageDetail(DetailView):
    """
    Show a Page in all its glory!

    Requires `handler` in the kwargs in order to:
      - add it to the `context`, and
      - get the Page instance.
    """
    def get_object(self):
        self.handler = self.kwargs['handler']
        return models.Page.objects.get(node=self.handler.node)

    def get_context_data(self, **kwargs):
        kwargs['handler'] = self.handler
        return super().get_context_data(**kwargs)
