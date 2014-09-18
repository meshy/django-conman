from django.views.generic import RedirectView

from .models import NodeRedirect


class NodeRedirectView(RedirectView):
    """Redirect to the target Node."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        node = kwargs['handler'].node
        return NodeRedirect.objects.get(node=node).target.url
