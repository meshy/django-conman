from django.apps import apps
from django.views.generic import TemplateView


class CMSIndex(TemplateView):
    template_name = 'cms/index.html'

    def get_context_data(self, **kwargs):
        managed_apps = apps.get_app_config('cms').managed_apps
        return super().get_context_data(apps=managed_apps, **kwargs)
