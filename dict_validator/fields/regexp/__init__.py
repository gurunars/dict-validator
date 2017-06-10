"""
This package contains most frequently used subclasses of
:class:`dict_validator.fields.StringField`.

 - :class:`EmailField`
 - :class:`PhoneField`
 - :class:`UrlField`
 - :class:`NameField`
 - :class:`SlugField`
 - :class:`PascalCaseField`
 - :class:`CamelCaseField`
 - :class:`UnderscoreCaseField`

"""

from .email_field import EmailField
from .phone_field import PhoneField
from .url_field import UrlField
from .name_field import NameField
from .slug_field import SlugField
from .camel_case_field import CamelCaseField
from .pascal_case_field import PascalCaseField
from .underscore_case_field import UnderscoreCaseField

__all__ = ["EmailField", "PhoneField", "UrlField", "NameField", "SlugField",
           "PascalCaseField", "CamelCaseField", "UnderscoreCaseField"]
