from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from conman.routes.handlers import ViewHandler
from conman.routes.managers import RouteManager
from conman.routes.models import Route

from . import views


class RouteRedirect(Route):
    """
    When `route` is browsed to, browser should be redirected to `target`.

    This model holds the data required to make that connection.
    """
    target = models.ForeignKey(
        'routes.Route',
        help_text=_('Browsers will be redirected to this route.'),
        on_delete=models.CASCADE,
        related_name='+',
    )
    permanent = models.BooleanField(
        default=False,
        help_text=_('If permanent, this redirect will be cached by browsers.'),
    )

    handler_class = ViewHandler
    view = views.RouteRedirectView.as_view()

    objects = RouteManager()

    def clean(self):
        """Forbid setting target equal to self."""
        if self.target_id == self.route_ptr_id:
            error = {'target': _('A RouteRedirect cannot redirect to itself.')}
            raise ValidationError(error)

    def save(self, *args, **kwargs):
        """Validate the Redirect before saving."""
        self.clean()
        return super().save(*args, **kwargs)


class URLRedirect(Route):
    """A `Route` that redirects to an arbitrary URL."""
    target = models.URLField(
        max_length=2000,
        help_text=_('Browsers will be redirected to this URL.'),
    )
    permanent = models.BooleanField(
        default=False,
        help_text=_('If permanent, this redirect will be cached by browsers.'),
    )

    handler_class = ViewHandler
    view = views.URLRedirectView.as_view()

    objects = RouteManager()

    class Meta:
        verbose_name = 'URL redirect'
