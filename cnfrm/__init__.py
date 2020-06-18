import json

from cnfrm.exceptions import *
from cnfrm.fields import *


class Config():
    def __init__(self):
        pass

    @classmethod
    def field_names(cls):
        for fieldname in dir(cls):
            field = getattr(cls, fieldname)
            if isinstance(field, Field):
                yield fieldname
    
    @classmethod
    def field(cls, fieldname):
        return getattr(cls, fieldname)
    
    def __getitem__(self, fieldname):
        return getattr(self, fieldname)
    
    def to_dct(self, include_default=True):
        dct = {}
        for fieldname in self.field_names():
            value = self[fieldname]

            if value is not None:
                default = self.field(fieldname).default
                if include_default or value != default:
                    dct[fieldname] = self[fieldname]
        
        return dct


    def __str__(self):
        msg = super().__str__()
        for fieldname in self.field_names():
            field = self.field(fieldname)
            value = self[fieldname]

            msg += f"\n{fieldname:>12}: "
            if field.required:
                msg += "!"
            else:
                msg += " "

            msg += f"\t{value or ''}"
        
        return msg

    def validate(self):
        for fieldname in self.field_names():
            field = self.field(fieldname)
            value = self[fieldname]

            if field.required and value is None:
                raise ValidationError(f"Required field is empty: {fieldname}")

        return True

    def read_dct(self, dct):
        fieldnames = list(self.field_names())

        for key, value in dct.items():
            if key in fieldnames:
                setattr(self, key, value)
            else:
                raise ConfigurationError(f"No field named {key}")

    def read_json(self, filename):
        with open(filename, "r") as infile:
            dct = json.load(infile)
        
        self.read_dct(dct)

    def dump_json(self, filename, include_default=True):
        dct = self.to_dct(include_default)
        with open(filename, "w") as outfile:
            json.dump(dct, outfile)
