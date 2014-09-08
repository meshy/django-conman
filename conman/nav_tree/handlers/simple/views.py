def simple_node_view(request, handler):
    """
    Delgate handling this request to the view in handler's attribute, `view`.

    It is worth noting that `view` is not a bound method of `handler`, and so
    it is required to pass `handler` to it.
    """
    return handler.view(request, handler=handler)
