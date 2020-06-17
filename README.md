# Configmapper

**Imagine: an ORM for config**

This library lets you declare your config in a way you might know from
popular ORM's. Get validation, defaults, popular fileformats and command
line configuration with expressive configuration declaration:

```
import confmap


class MyConf(confmapper.Config):
    name = ConfigField("no name")
    size = IntegerField(required=False)
    path = DirectoryField(required=False)
    email = EmailField(required=False)
    filename = FileField()


# create a config instance
config = MyConf()

# start reading things, the later overwrites the former
config.read_env()
config.read_json("~/myconf.json", quiet=True)
config.read_args()

# check if the configuration is complete
config.validate()

# write config to file:
config.dump_json("~/myconf.json")
```
