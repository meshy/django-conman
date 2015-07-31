from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from conman.routes.models import Route
from . import handlers


class RouteRedirect(Route):
    """
    When `route` is browsed to, browser should be redirected to `target`.

    This model holds the data required to make that connection.
    """
    handler = handlers.RouteRedirectHandler.path()
    target = models.ForeignKey('routes.Route', related_name='+')
    permanent = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        """Forbid setting target equal to self."""
        if self.target_id == self.route_ptr_id:
            raise ValidationError(_('A RouteRedirect cannot redirect to itself.'))
        return super().save(*args, **kwargs)
