from django.views.generic import RedirectView


class RouteRedirectView(RedirectView):
    """Redirect to the target Route."""
    permanent = False  # Set to django 1.9's default to avoid RemovedInDjango19Warning

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the route's target url.

        Save the route's redirect type for use by RedirectView.
        """
        redirect = kwargs['route']
        self.permanent = redirect.permanent
        return redirect.target.url


class URLRedirectView(RedirectView):
    """Redirect to a URLRedirect Route's target URL."""
    permanent = False  # Set to django 1.9's default to avoid RemovedInDjango19Warning

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the target url.

        Save the route's redirect type for use by RedirectView.
        """
        redirect = kwargs['route']
        self.permanent = redirect.permanent
        return redirect.target
