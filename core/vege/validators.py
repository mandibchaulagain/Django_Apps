# myapp/validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("Password must contain at least one numeric character."))
        if not any(char.isalpha() for char in password):
            raise ValidationError(_("Password must contain at least one letter."))

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long, "
            "contain at least one letter and one numeric character."
        )
