import re
import os
from email.utils import parseaddr

from cnfrm.exceptions import ValidationError

class Field():
    def __init__(self, default=None, required=True):
        self.default = default
        self.required = required

        if default is not None:
            self.validate(default)
        
        self.value = None

    def validate(self, value):
        if self.required and value is None:
            raise ValidationError("Cannot set required field to None")
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
            raise ValidationError(f"{value} is not a valid value for {self.__class__.__name__}")

class NumberField(Field):
    def __init__(self, default=None, required=True, min_value=None, max_value=None):
        super().__init__(default, required)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value):
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Min-value constraint not satisfied: {value}")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Max-value constraint not satisfied: {value}")
        
        return super().validate(value)


class IntegerField(NumberField):

    def validate(self, value):
        int_value = int(value)
        if int_value != value:
            self._raise_validation(value)
            
        return super().validate(int_value)

class FloatField(NumberField):
    def validate(self, value):
        float_value = float(value)
        if float_value != value:
            self._raise_validation(value)

        return super().validate(float_value)

class EmailField(Field):
    rex = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9\.-]+\.[A-Z]{2,63}$")
    def validate(self, value):
        _name, addr = parseaddr(value)
        if self.rex.match(addr.upper()):
            return True
        
        raise ValidationError(f"Not a valid email address: {addr}")


class PathField(Field):
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
