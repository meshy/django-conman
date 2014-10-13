from django.apps import AppConfig


class CMSConfig(AppConfig):
    """
    Configuration for the CMS app.

    Third-party apps can register with manage_app to include their urls in
    the cms namespace.
    """
    name = 'conman.cms'
    _managed_apps = set()

    def manage_app(self, app):
        """Register an app with the CMS."""
        if not hasattr(app, 'cms_urls'):
            msg = 'Apps managed by this app must have the `cms_urls` attribute'
            raise ValueError(msg)
        self._managed_apps.add(app)

    @property
    def managed_apps(self):
        """The apps managed by the CMS."""
        return self._managed_apps.copy()
