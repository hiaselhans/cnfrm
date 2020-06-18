import re
import os
from email.utils import parseaddr

from cnfrm.exceptions import ValidationError

class ConfigField():
    def __init__(self, default=None, required=True):
        self.default = default
        self.required = required

        if default is not None:
            self.validate(default)
        
        self.value = None

    def validate(self, value):
        return True
    
    def _raise_validation(self, value):
        raise ValidationError(f"{value} is not valid for {self.__class__.__name__}")

    def is_valid(self):
        if not self.required:
            return True
        
        if self.value is not None:
            return True
        if self.default is not None:
            return True
        
        return False

    
    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.value is not None:
            return self.value
        
        return self.default
    
    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value
        else:
            # Usually validate should have raised already.
            # Let's do it again. Just in case...
            raise ValueError(f"{value} is not a valid value for {self.__class__.__name__}")

class IntegerField(ConfigField):
    def validate(self, value):
        if int(value) != value:
            self._raise_validation(value)
        
        return True

class FloatField(ConfigField):
    def validate(self, value):
        if float(value) != value:
            self._raise_validation(value)

        return True

class EmailField(ConfigField):
    rex = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9\.-]+\.[A-Z]{2,63}$")
    def validate(self, value):
        _name, addr = parseaddr(value)
        if self.rex.match(addr.upper()):
            return True
        
        raise ValidationError(f"Not a valid email address: {addr}")


class PathField(ConfigField):
    pass
        
class FileField(PathField):
    def validate(self, value):
        if not os.path.isfile(value):
            raise ValidationError(f"Not a file: {value}")
        
        return True

class DirectoryField(PathField):
    def validate(self, value):
        if not os.path.isdir(value):
            raise ValidationError(f"Not a directory: {value}")

        return True