from django.views.generic import RedirectView

from .models import NodeRedirect


class NodeRedirectView(RedirectView):
    """Redirect to the target Node."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        redirect = NodeRedirect.objects.get(node=kwargs['handler'].node)
        self.permanent = redirect.permanent
        return redirect.target.url
