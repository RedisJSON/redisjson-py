import six
import json
from redis import StrictRedis
from redis.client import Pipeline
from redis._compat import (long, nativestr)
from .path import Path


def str_path(p):
    "Returns the string representation of a path if it is of class Path"
    if isinstance(p, Path):
        return p.strPath
    else:
        return p


def bulk_of_jsons(d):
    "Replace serialized JSON values with objects in a bulk array response (list)"
    def _f(b):
        for index, item in enumerate(b):
            if item is not None:
                b[index] = d(item)
        return b
    return _f


class Client(StrictRedis):
    """
    This class subclasses redis-py's `StrictRedis` and implements ReJSON's
    commmands (prefixed with "json").

    The client performs on-the-fly serialization/deserialization of objects
    to/from JSON, and provides the ability to use a custom encoder/decoder.
    """

    _encoder = None
    _encode = None
    _decoder = None

    def __init__(self, encoder=None, decoder=None, *args, **kwargs):
        """
        Creates a new ReJSON client.

        ``encoder`` should be an instance of a ``json.JSONEncoder`` class
        ``decoder`` should be an instance of a ``json.JSONDecoder`` class
        """
        self.setEncoder(encoder)
        self.setDecoder(decoder)
        StrictRedis.__init__(self, *args, **kwargs)

        # Set the module commands' callbacks
        MODULE_CALLBACKS = {
                'JSON.DEL': long,
                'JSON.CLEAR': long,
                'JSON.GET': self._decode,
                'JSON.MGET': bulk_of_jsons(self._decode),
                'JSON.SET': lambda r: r and nativestr(r) == 'OK',
                'JSON.NUMINCRBY': self._decode,
                'JSON.NUMMULTBY': self._decode,
                'JSON.TOGGLE': lambda b: b == 'true',
                'JSON.STRAPPEND': long,
                'JSON.STRLEN': long,
                'JSON.ARRAPPEND': long,
                'JSON.ARRINDEX': long,
                'JSON.ARRINSERT': long,
                'JSON.ARRLEN': long,
                'JSON.ARRPOP': self._decode,
                'JSON.ARRTRIM': long,
                'JSON.OBJLEN': long,
                'JSON.DEBUG': long,
        }
        for k, v in six.iteritems(MODULE_CALLBACKS):
            self.set_response_callback(k, v)

    def setEncoder(self, encoder):
        """
        Sets the client's encoder
        ``encoder`` should be an instance of a ``json.JSONEncoder`` class
        """
        if not encoder:
            self._encoder = json.JSONEncoder()
        else:
            self._encoder = encoder
        self._encode = self._encoder.encode

    def setDecoder(self, decoder):
        """
        Sets the client's decoder
        ``decoder`` should be an instance of a ``json.JSONDecoder`` class
        """
        if not decoder:
            self._decoder = json.JSONDecoder()
        else:
            self._decoder = decoder

    def _decode(self, s, *args, **kwargs):
        return self._decoder.decode(s, *args, **kwargs) if s is not None else None

    def jsondel(self, name, path=Path.rootPath()):
        """
        Deletes the JSON value stored at key ``name`` under ``path``
        """
        return self.execute_command('JSON.DEL', name, str_path(path))

    def jsonclear(self, name, path=Path.rootPath()):
        """
        Emptying arrays and objects (to have zero slots/keys without
        deleting the array/object) returning the count of cleared paths
        (ignoring non-array and non-objects paths)
        """
        return self.execute_command('JSON.CLEAR', name, str_path(path))

    def jsonget(self, name, *args, no_escape=False):
        """
        Get the object stored as a JSON value at key ``name``
        ``args`` is zero or more paths, and defaults to root path
        ```no_escape`` is a boolean flag to add no_escape option to get non-ascii characters
        """
        pieces = [name]
        if no_escape:
            pieces.append('noescape')

        if len(args) == 0:
            pieces.append(Path.rootPath())

        else:
            for p in args:
                pieces.append(str_path(p))

        return self.execute_command('JSON.GET', *pieces)

    def jsonmget(self, path, *args):
        """
        Gets the objects stored as a JSON values under ``path`` from 
        keys ``args``
        """
        pieces = []
        pieces.extend(args)
        pieces.append(str_path(path))
        return self.execute_command('JSON.MGET', *pieces)

    def jsonset(self, name, path, obj, nx=False, xx=False):
        """
        Set the JSON value at key ``name`` under the ``path`` to ``obj``
        ``nx`` if set to True, set ``value`` only if it does not exist
        ``xx`` if set to True, set ``value`` only if it exists
        """
        pieces = [name, str_path(path), self._encode(obj)]

        # Handle existential modifiers
        if nx and xx:
            raise Exception('nx and xx are mutually exclusive: use one, the '
                            'other or neither - but not both')
        elif nx:
            pieces.append('NX')
        elif xx:
            pieces.append('XX')
        return self.execute_command('JSON.SET', *pieces)

    def jsontype(self, name, path=Path.rootPath()):
        """
        Gets the type of the JSON value under ``path`` from key ``name``
        """
        return self.execute_command('JSON.TYPE', name, str_path(path))

    def jsonnumincrby(self, name, path, number):
        """
        Increments the numeric (integer or floating point) JSON value under
        ``path`` at key ``name`` by the provided ``number``
        """
        return self.execute_command('JSON.NUMINCRBY', name, str_path(path), self._encode(number))

    def jsonnummultby(self, name, path, number):
        """
        Multiplies the numeric (integer or floating point) JSON value under
        ``path`` at key ``name`` with the provided ``number``
        """
        return self.execute_command('JSON.NUMMULTBY', name, str_path(path), self._encode(number))

    def jsontoggle(self, name, path=Path.rootPath()):
        """
        Toggle boolean value under ``path`` at key ``name``,
        Returning the new value.
        """
        return self.execute_command('JSON.TOGGLE', name, str_path(path))

    def jsonstrappend(self, name, string, path=Path.rootPath()):
        """
        Appends to the string JSON value under ``path`` at key ``name`` the
        provided ``string``
        """
        return self.execute_command('JSON.STRAPPEND', name, str_path(path), self._encode(string))

    def jsonstrlen(self, name, path=Path.rootPath()):
        """
        Returns the length of the string JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.STRLEN', name, str_path(path))

    def jsonarrappend(self, name, path=Path.rootPath(), *args):
        """
        Appends the objects ``args`` to the array under the ``path` in key
        ``name``
        """
        pieces = [name, str_path(path)]
        for o in args:
            pieces.append(self._encode(o))
        return self.execute_command('JSON.ARRAPPEND', *pieces)

    def jsonarrindex(self, name, path, scalar, start=0, stop=-1):
        """
        Returns the index of ``scalar`` in the JSON array under ``path`` at key
        ``name``. The search can be limited using the optional inclusive
        ``start`` and exclusive ``stop`` indices.
        """
        return self.execute_command('JSON.ARRINDEX', name, str_path(path), self._encode(scalar), start, stop)

    def jsonarrinsert(self, name, path, index, *args):
        """
        Inserts the objects ``args`` to the array at index ``index`` under the
        ``path` in key ``name``
        """
        pieces = [name, str_path(path), index]
        for o in args:
            pieces.append(self._encode(o))
        return self.execute_command('JSON.ARRINSERT', *pieces)

    def jsonarrlen(self, name, path=Path.rootPath()):
        """
        Returns the length of the array JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.ARRLEN', name, str_path(path))

    def jsonarrpop(self, name, path=Path.rootPath(), index=-1):
        """
        Pops the element at ``index`` in the array JSON value under ``path`` at
        key ``name``
        """
        return self.execute_command('JSON.ARRPOP', name, str_path(path), index)

    def jsonarrtrim(self, name, path, start, stop):
        """
        Trim the array JSON value under ``path`` at key ``name`` to the 
        inclusive range given by ``start`` and ``stop``
        """
        return self.execute_command('JSON.ARRTRIM', name, str_path(path), start, stop)

    def jsonobjkeys(self, name, path=Path.rootPath()):
        """
        Returns the key names in the dictionary JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.OBJKEYS', name, str_path(path))

    def jsonobjlen(self, name, path=Path.rootPath()):
        """
        Returns the length of the dictionary JSON value under ``path`` at key
        ``name``
        """
        return self.execute_command('JSON.OBJLEN', name, str_path(path))

    def jsondebugmemory(self, name, path=Path.rootPath()):
        """
        Returns the memory usage in bytes of a value under ``path`` from key ``name``.
        """
        return self.execute_command("JSON.DEBUG", "MEMORY", name, str_path(path))

    def pipeline(self, transaction=True, shard_hint=None):
        """
        Return a new pipeline object that can queue multiple commands for
        later execution. ``transaction`` indicates whether all commands
        should be executed atomically. Apart from making a group of operations
        atomic, pipelines are useful for reducing the back-and-forth overhead
        between the client and server.

        Overridden in order to provide the right client through the pipeline.
        """
        p = Pipeline(
            connection_pool=self.connection_pool,
            response_callbacks=self.response_callbacks,
            transaction=transaction,
            shard_hint=shard_hint)
        p.setEncoder(self._encoder)
        p.setDecoder(self._decoder)
        return p

class Pipeline(Pipeline, Client):
    "Pipeline for ReJSONClient"
