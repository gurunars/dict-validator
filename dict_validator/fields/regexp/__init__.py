"""
This package contains most frequently used subclasses of
:class:`dict_validator.fields.String`.

 - :class:`Email`
 - :class:`Phone`
 - :class:`Url`
 - :class:`Name`
 - :class:`Slug`
 - :class:`PascalCase`
 - :class:`CamelCase`
 - :class:`UnderscoreCase`

"""

from .email_field import Email
from .phone_field import Phone
from .url_field import Url
from .name_field import Name
from .slug_field import Slug
from .camel_case_field import CamelCase
from .pascal_case_field import PascalCase
from .underscore_case_field import UnderscoreCase

__all__ = ["Email", "Phone", "Url", "Name", "Slug",
           "PascalCase", "CamelCase", "UnderscoreCase"]
