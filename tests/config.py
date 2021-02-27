import cnfrm

class Config(cnfrm.Config):
    email = cnfrm.EmailField()
    name = cnfrm.Field()
    age = cnfrm.IntegerField(min_value=0)
    size = cnfrm.FloatField(max_value=2.2)
    path = cnfrm.FileField(required=False)
    directory = cnfrm.DirectoryField(required=False)

def get_config():

    config = Config()
    config.read_dct({
        "email": "me@you.com",
        "name": "Donald Duck",
        "age": 20,
        "size": 1.2
    })
    return config

if __name__ == "__main__":
    config = Config()
    config2 = Config()
    config.argparse()
    print(config)
    print(config2)