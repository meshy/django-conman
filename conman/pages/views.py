from django.views.generic import TemplateView

from . import models


class PageDetail(TemplateView):
    template_name = 'conman/pages/page_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        handler = self.kwargs['handler']
        node = handler.node
        context['handler'] = handler
        context['node'] = node
        context['page'] = models.Page.objects.get(node=node)
        return context
