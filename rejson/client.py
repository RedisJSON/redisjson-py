from sys import stdout
import json
from redis import StrictRedis, exceptions
from redis.client import BasePipeline
from redis._compat import (long, nativestr)
from .path import Path

def str_path(p):
    "Returns the string representation of a path if it is of class Path"
    if isinstance(p, Path):
        return p.strPath
    else:
        return p

def float_or_long(n):
    "Return a number from a Redis reply"
    if isinstance(n, str):
        return float(n)
    else:
        return long(n)

def long_or_none(r):
    "Return a long or None from a Redis reply"
    if r:
        return long(r)
    return r

def json_or_none(r):
    "Return a deserialized JSON object or None"
    if r:
        return json.loads(r)
    return r

def bulk_of_jsons(b):
    "Replace serialized JSON values with objects in a bulk array response (list)"
    for index, item in enumerate(b):
        if item is not None:
            b[index] = json.loads(item)
    return b

class ReJSONClient(StrictRedis):
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
            'JSON.DEL': long,
            'JSON.GET': json_or_none,
            'JSON.MGET': bulk_of_jsons,
            'JSON.SET': lambda r: r and nativestr(r) == 'OK',
            'JSON.NUMINCRBY': float_or_long,
            'JSON.NUMMULTBY': float_or_long,
            'JSON.STRAPPEND': long_or_none,
            'JSON.STRLEN': long_or_none,
            'JSON.ARRAPPEND': long_or_none,
            'JSON.ARRINDEX': long_or_none,
            'JSON.ARRINSERT': long_or_none,
            'JSON.ARRLEN': long_or_none,
            'JSON.ARRPOP': json_or_none,
            'JSON.ARRTRIM': long_or_none,
            'JSON.OBJLEN': long_or_none,
    }

    def __init__(self, *args, **kwargs):
        super(ReJSONClient, self).__init__(*args, **kwargs)
        self.__checkPrerequirements()
        # Set the module commands' callbacks
        for k, v in self.MODULE_CALLBACKS.iteritems():
            self.set_response_callback(k, v)

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

    def JSONNumIncrBy(self, name, path, number):
        """
        Increments the numeric (integer or floating point) JSON value under
        ``path`` at key ``name`` by the provided ``number``
        """
        return self.execute_command('JSON.NUMINCRBY', name, str_path(path), json.dumps(number))

    def JSONNumMultBy(self, name, path, number):
        """
        Multiplies the numeric (integer or floating point) JSON value under
        ``path`` at key ``name`` with the provided ``number``
        """
        return self.execute_command('JSON.NUMMULTBY', name, str_path(path), json.dumps(number))

    def JSONStrAppend(self, name, string, path=Path.rootPath()):
        """
        Appends to the string JSON value under ``path`` at key ``name`` the
        provided ``string``
        """
        return self.execute_command('JSON.STRAPPEND', name, str_path(path), json.dumps(string))

    def JSONStrLen(self, name, path=Path.rootPath()):
        """
        Returns the length of the string JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.STRLEN', name, str_path(path))

    def JSONArrAppend(self, name, path=Path.rootPath(), *args):
        """
        Appends the objects ``args`` to the array under the ``path` in key
        ``name``
        """
        pieces = [name, str_path(path)]
        for o in args:
            pieces.append(json.dumps(o))
        return self.execute_command('JSON.ARRAPPEND', *pieces)

    def JSONArrIndex(self, name, path, scalar, start=0, stop=-1):
        """
        Returns the index of ``scalar`` in the JSON array under ``path`` at key
        ``name``. The search can be limited using the optional inclusive
        ``start`` and exclusive ``stop`` indices.
        """
        return self.execute_command('JSON.ARRINDEX', name, str_path(path), json.dumps(scalar), start, stop)

    def JSONArrInsert(self, name, path, index, *args):
        """
        Inserts the objects ``args`` to the array at index ``index`` under the
        ``path` in key ``name``
        """
        pieces = [name, str_path(path), index]
        for o in args:
            pieces.append(json.dumps(o))
        return self.execute_command('JSON.ARRINSERT', *pieces)

    def JSONArrLen(self, name, path=Path.rootPath()):
        """
        Returns the length of the array JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.ARRLEN', name, str_path(path))

    def JSONArrPop(self, name, path=Path.rootPath(), index=-1):
        """
        Pops the element at ``index`` in the array JSON value under ``path`` at
        key ``name``
        """
        return self.execute_command('JSON.ARRPOP', name, str_path(path), index)

    def JSONArrTrim(self, name, path, start, stop):
        """
        Trim the array JSON value under ``path`` at key ``name`` to the 
        inclusive range given by ``start`` and ``stop``
        """
        return self.execute_command('JSON.ARRTRIM', name, str_path(path), start, stop)

    def JSONObjKeys(self, name, path=Path.rootPath()):
        """
        Returns the key names in the dictionary JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.OBJKEYS', name, str_path(path))

    def JSONObjLen(self, name, path=Path.rootPath()):
        """
        Returns the length of the dictionary JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.OBJLEN', name, str_path(path))
