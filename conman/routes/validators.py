from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_end_in_slash(path):
    """URL path fragments end with a slash."""
    if not path.endswith('/'):
        msg = _('Last character must be "/".')
        raise ValidationError(msg)


def validate_start_in_slash(path):
    """URL path fragments start with a slash."""
    if not path.startswith('/'):
        msg = _('First character must be "/".')
        raise ValidationError(msg)


def validate_no_questionmark(path):
    """URL path fragments do not contain question marks."""
    if '?' in path:
        msg = _('Question mark ("?") is not allowed.')
        raise ValidationError(msg)
