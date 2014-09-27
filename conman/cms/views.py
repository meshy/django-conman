from django.views.generic import TemplateView


class CMSIndex(TemplateView):
    template_name = 'cms/index.html'
