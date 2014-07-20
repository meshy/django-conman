class BaseHandler:
    @classmethod
    def path(cls):
        """Get dotted-path of this class"""
        return '.'.join((cls.__module__, cls.__name__))

    def __init__(self, node):
        self.node = node
