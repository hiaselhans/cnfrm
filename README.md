# CnfRM

**Imagine: an ORM for config**

This library lets you declare your config in a way you might know from
popular ORM's.

You get

 * expressive configuration declaration
 * popular fileformats (json, yml?)
 * command line options
 * env configuration variables
 

```python
import cnfrm


class MyConf(cnfrm.Config):
    name = cnfrm.Field("no name")
    size = cnfrm.IntegerField(required=False)
    path = cnfrm.DirectoryField(required=False)
    email = cnfrm.EmailField(required=False)
    filename = cnfrm.FileField()


# create a config instance
config = MyConf()

# start reading things, the later overwrites the former
config.read_env()
config.read_json("~/myconf.json", quiet=True)
config.read_args()

# check if the configuration is complete
config.validate()

# write config to file:
config.write_json("~/myconf.json")
```
