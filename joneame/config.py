from configparser import ConfigParser
import base64


config = ConfigParser()
config.read('config.ini')

def _cfg(env, key): return config.get(env, key)
def _cfgi(env, key): return int(config.get(env, key))
def _cfgb64(env, key): return base64.b64decode(config.get(env, key))
