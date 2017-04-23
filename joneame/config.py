from configparser import ConfigParser


config = ConfigParser()
config.readfp(open('config.ini'))

def _cfg(env, key): return config.get(env, key)
def _cfgi(env, key): return int(config.get(env, key))
