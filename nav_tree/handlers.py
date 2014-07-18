class BaseHandler:
    @classmethod
    def path(cls):
        """Get dotted-path of this class"""
        return '.'.join((cls.__module__, cls.__name__))
