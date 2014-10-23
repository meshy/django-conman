from django.views.generic import RedirectView


class RouteRedirectView(RedirectView):
    """Redirect to the target Route."""
    def get_redirect_url(self, *args, **kwargs):
        """
        Return the route's target url.

        Save the route's redirect type for use by RedirectView.
        """
        redirect = kwargs['route']
        self.permanent = redirect.permanent
        return redirect.target.url
