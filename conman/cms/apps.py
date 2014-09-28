from django.apps import AppConfig


class CMSConfig(AppConfig):
    name = 'conman.cms'
    _managed_apps = set()

    def manage_app(self, app):
        self._managed_apps.add(app)

    @property
    def managed_apps(self):
        return self._managed_apps.copy()
