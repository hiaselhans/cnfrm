import json
import argparse

from cnfrm.fields import Field
from cnfrm.exceptions import ValidationError, ConfigurationError


class Config():
    def __init__(self, **kwargs):
        self._values = {}

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_fieldnames(cls):
        for fieldname in dir(cls):
            field = getattr(cls, fieldname)
            if isinstance(field, Field):
                yield fieldname
    
    @classmethod
    def get_field(cls, fieldname):
        return getattr(cls, fieldname)
    
    def __getitem__(self, fieldname):
        return getattr(self, fieldname)

    def __setattr__(self, fieldname, value):
        if fieldname not in ("_values", ):
            fieldnames = self.get_fieldnames()

            if fieldname not in fieldnames:
                raise ConfigurationError(f"'{fieldname}' can not be set for configuration {self}")

        try:
            super().__setattr__(fieldname, value)
        except ValidationError:
            raise ValidationError(f"Validation failed for '{fieldname}'")
    
    def to_dct(self, include_default=True):
        dct = {}
        for fieldname in self.get_fieldnames():
            value = self[fieldname]

            if value is not None:
                default = self.get_field(fieldname).default
                if include_default or value != default:
                    dct[fieldname] = self[fieldname]
        
        return dct


    def __str__(self):
        msg = super().__str__()
        for fieldname in self.get_fieldnames():
            field = self.get_field(fieldname)
            value = self[fieldname]

            msg += f"\n{fieldname:>12}: "
            if field.required:
                msg += "!"
            else:
                msg += " "

            msg += f"\t{value or ''}"
        
        return msg

    def validate(self):
        for fieldname in self.get_fieldnames():
            field = self.get_field(fieldname)
            value = self[fieldname]

            if field.required and value is None:
                raise ValidationError(f"Required field is empty: {fieldname}")

        return True

    def read_dct(self, dct):
        fieldnames = list(self.get_fieldnames())

        for key, value in dct.items():
            if key in fieldnames:
                setattr(self, key, value)
            else:
                raise ConfigurationError(f"No field named {key}")
        
        return self

    def read_json(self, filename):
        with open(filename, "r") as infile:
            dct = json.load(infile)
        
        self.read_dct(dct)
        
        return self

    def dump_json(self, filename, include_default=True):
        dct = self.to_dct(include_default)
        with open(filename, "w") as outfile:
            json.dump(dct, outfile, indent=2)

    def argparse(self, add_configfile=True, required=True):
        parser = argparse.ArgumentParser()
        if add_configfile:
            parser.add_argument("-c")
        for fieldname in self.get_fieldnames():
            field = self.get_field(fieldname)
            if required and field.required and not field.default:
                parser.add_argument(f"--{fieldname}", type=field.base_type)
            else:
                parser.add_argument(fieldname, type=field.base_type)

        args = parser.parse_args()
        for arg, value in args._get_kwargs():
            if value is not None:
                setattr(self, arg, value)

        if add_configfile and args.c is not None:
            self.read_json(args.c)
        
        return self