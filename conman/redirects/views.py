from django.views.generic import RedirectView


class NodeRedirectView(RedirectView):
    """Redirect to the target Node."""
    def get_redirect_url(self, *args, **kwargs):
        redirect = kwargs['handler'].node.noderedirect
        self.permanent = redirect.permanent
        return redirect.target.url
