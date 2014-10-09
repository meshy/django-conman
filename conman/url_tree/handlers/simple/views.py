def simple_node_view(request, node):
    """
    Delgate handling this request to the view in handler's attribute, `view`.

    It is worth noting that `view` is not a bound method of `handler`, and so
    it is required to pass `handler` to it.
    """
    return node.get_handler().view(request, node=node)
