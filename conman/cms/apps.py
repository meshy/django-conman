from django.apps import AppConfig


class CMSConfig(AppConfig):
    name = 'conman.cms'
    _managed_apps = set()

    def manage_app(self, app):
        if not hasattr(app, 'cms_urls'):
            msg = 'Apps managed by this app must have the `cms_urls` attribute'
            raise ValueError(msg)
        self._managed_apps.add(app)

    @property
    def managed_apps(self):
        return self._managed_apps.copy()
