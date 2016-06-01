from configparser import ConfigParser

config = ConfigParser()
config.readfp(open('config.ini'))

_cfg = lambda env, key: config.get(env, key)
_cfgi = lambda env, key: int(config.get(env, key))
