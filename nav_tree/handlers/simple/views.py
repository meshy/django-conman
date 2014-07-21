def simple_node_view(request, handler):
    return handler.view(request, handler=handler)
