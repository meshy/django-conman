from django.db.models.expressions import Func


class CharCount(Func):
    """
    Count the occurrences of a char within a field.

    Works by finding the difference in length between the whole string, and the
    string with the char removed.
    """
    template = "CHAR_LENGTH(%(field)s) - CHAR_LENGTH(REPLACE(%(field)s, '%(char)s', ''))"

    def __init__(self, field, *, char, **extra):
        """
        Add some validation to the invocation.

        "Char" must always:

        - be passed as a keyword argument
        - be exactly one character.
        """
        if len(char) != 1:
            raise ValueError('CharCount must count exactly one char.')
        super().__init__(field, char=char, **extra)
