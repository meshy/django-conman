def simple_route_view(request, route):
    """
    Delgate handling this request to the view in handler's attribute, `view`.

    It is worth noting that `view` is not a bound method of `handler`, and so
    it is required to pass `handler` to it.
    """
    return route.get_handler().view(request, route=route)
