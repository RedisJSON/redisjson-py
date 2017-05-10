from sys import stdout
import json
from redis import StrictRedis, exceptions
from redis._compat import (b, basestring, bytes, imap, iteritems, iterkeys,
                           itervalues, izip, long, nativestr, unicode,
                           safe_unicode)
from .path import Path

def str_path(p):
    "Returns the string representation of a path if it is of class Path"
    if isinstance(p, Path):
        return p.strPath
    else:
        return p

def bulk_of_jsons(b):
    "Replace serialized JSON values with objects in a bulk array response (list)"
    for index, item in enumerate(b):
        if item is not None:
            b[index] = json.loads(item)
    return b

class Client(StrictRedis):
    """
    Implementation of ReJSON commands

    This class provides an interface for ReJSON's commands and performs on-the-fly
    serialization/deserialization of objects to/from JSON.
    """

    MODULE_INFO = {
        'name': 'ReJSON',
        'ver':  1
    }

    MODULE_CALLBACKS = {
            'JSON.DEL': lambda r: int(r),
            'JSON.GET': lambda r: json.loads(r),
            'JSON.MGET': bulk_of_jsons,
            'JSON.SET': lambda r: r and nativestr(r) == 'OK',
    }

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        
        self.__checkPrerequirements()
        
        # Inject the callbacks for the module's commands
        self.response_callbacks.update(self.MODULE_CALLBACKS)

    def __checkPrerequirements(self):
        "Checks that the module is ready"
        try:
            reply = self.execute_command('MODULE', 'LIST')
        except exceptions.ResponseError as e:
            if e.message.startswith('unknown command'):
                raise exceptions.RedisError('Modules are not supported '
                                            'on your Redis server - consider '
                                            'upgrading to a newer version.')
        finally:
            info = self.MODULE_INFO
            for r in reply:
                module = dict(zip(r[0::2], r[1::2]))
                if info['name'] == module['name'] and \
                    info['ver'] <= module['ver']:
                    return
            raise exceptions.RedisError('ReJSON is not loaded - follow the '
                                        'instructions at http://rejson.io')

    def JSONDel(self, name, path=Path.rootPath()):
        """
        Deletes the JSON value stored at key ``name`` under ``path``
        """
        return self.execute_command('JSON.DEL', name, str_path(path))

    def JSONGet(self, name, *args):
        """
        Get the object stored as a JSON value at key ``name``
        ``args`` is zero or more paths, and defaults to root path
        """
        pieces = [name]
        if len(args) == 0:
            pieces.append(Path.rootPath())
        else:
            for p in args:
                    pieces.append(str_path(p))
        return self.execute_command('JSON.GET', *pieces)

    def JSONMGet(self, path, *args):
        """
        Gets the objects stored as a JSON values under ``path`` from 
        keys ``args``
        """
        pieces = []
        pieces.extend(args)
        pieces.append(str_path(path))
        return self.execute_command('JSON.MGET', *pieces)

    def JSONSet(self, name, path, obj, nx=False, xx=False):
        """
        Set the JSON value at key ``name`` under the ``path`` to ``obj``
        ``nx`` if set to True, set ``value`` only if it does not exist
        ``xx`` if set to True, set ``value`` only if it exists
        """
        pieces = [name, str_path(path), json.dumps(obj)]

        # Handle existential modifiers
        if nx and xx:
            raise Exception('nx and xx are mutually exclusive: use one, the '
                            'other or neither - but not both')
        elif nx:
            pieces.append('NX')
        elif xx:
            pieces.append('XX')

        return self.execute_command('JSON.SET', *pieces)

    def JSONType(self, name, path=Path.rootPath()):
        """
        Gets the type of the JSON value under ``path`` from key ``name``
        """
        return self.execute_command('JSON.TYPE', name, str_path(path))
