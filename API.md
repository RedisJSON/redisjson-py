# Package rejson Documentation


rejson-py is a package that allows storing, updating and querying objects as
JSON documents in a [Redis](https://redis.io) database that is extended with the
[ReJSON module](https://github.com/redislabsmodules/rejson). The package extends
[redis-py](https://github.com/andymccurdy/redis-py)'s interface with ReJSON's
API, and performs on-the-fly serialization/deserialization of objects to/from
JSON.

## Installation

```bash
$ pip install rejson
```

## Usage example

```python
from rejson import Client, Path

rj = Client(host='localhost', port=6379)

# Set the key `obj` to some object
obj = {
    'answer': 42,
    'arr': [None, True, 3.14],
    'truth': {
        'coord': 'out there'
    }
}
rj.jsonset('obj', Path.rootPath(), obj)

# Get something
print 'Is there anybody... {}?'.format(
    rj.jsonget('obj', Path('.truth.coord'))
)

# Delete something (or perhaps nothing), append something and pop it
rj.jsondel('obj', Path('.arr[0]'))
rj.jsonarrappend('obj', Path('.arr'), 'something')
print '{} popped!'.format(rj.jsonarrpop('obj', Path('.arr')))

# Update something else
rj.jsonset('obj', Path('.answer'), 2.17)

# And use just like the regular redis-py client
jp = rj.pipeline()
jp.set('foo', 'bar')
jp.jsonset('baz', Path.rootPath(), 'qaz')
jp.execute()
```

## Encoding/Decoding

rejson-py uses Python's [`json`](https://docs.python.org/2/library/json.html).
The client can be set to use custom encoders/decoders at creation, or by calling
explicitly the [`setEncoder()`](API.md#setencoder) and
[`setDecoder()`](API.md#setdecoder) methods, respectively.

The following shows how to use this for a custom class that's stored as
a JSON string for example:

```python
from json import JSONEncoder, JSONDecoder
from rejson import Client

class CustomClass(object):
    "Some non-JSON-serializable"
    def __init__(self, s=None):
        if s is not None:
            # deserialize the instance from the serialization
            if s.startswith('CustomClass:'):
                ...
            else:
                raise Exception('unknown format')
        else:
            # initialize the instance
            ...

    def __str__(self):
        _str = 'CustomClass:'
        # append the instance's state to the serialization
        ...
        return _str

    ...

class CustomEncoder(JSONEncoder):
    "A custom encoder for the custom class"
    def default(self, obj):
        if isinstance(obj, CustomClass):
            return str(obj)
        return json.JSONEncoder.encode(self, obj)

class TestDecoder(JSONDecoder):
    "A custom decoder for the custom class"
    def decode(self, obj):
        d = json.JSONDecoder.decode(self, obj)
        if isinstance(d, basestring) and d.startswith('CustomClass:'):
            return CustomClass(d)
        return d

# Create a new instance of CustomClass
obj = CustomClass()

# Create a new client with the custom encoder and decoder
rj = Client(encoder=CustomEncoder(), decoder=CustomDecoder())

# Store the object
rj.jsonset('custom', Path.rootPath(), obj))

# Retrieve it
obj = rj.jsonget('custom', Path.rootPath())
```

## Class Client
This class subclasses redis-py's `StrictRedis` and implements ReJSON's
commmands (prefixed with "json").

The client performs on-the-fly serialization/deserialization of objects
to/from JSON, and provides the ability to use a custom encoder/decoder.
### \_\_init\_\_
```py

def __init__(self, encoder=None, decoder=None, *args, **kwargs)

```



Creates a new ReJSON client.

``encoder`` should be an instance of a ``json.JSONEncoder`` class
``decoder`` should be an instance of a ``json.JSONDecoder`` class


### jsonarrappend
```py

def jsonarrappend(self, name, path='.', *args)

```



Appends the objects ``args`` to the array under the ``path` in key
``name``


### jsonarrindex
```py

def jsonarrindex(self, name, path, scalar, start=0, stop=-1)

```



Returns the index of ``scalar`` in the JSON array under ``path`` at key
``name``. The search can be limited using the optional inclusive
``start`` and exclusive ``stop`` indices.


### jsonarrinsert
```py

def jsonarrinsert(self, name, path, index, *args)

```



Inserts the objects ``args`` to the array at index ``index`` under the
``path` in key ``name``


### jsonarrlen
```py

def jsonarrlen(self, name, path='.')

```



Returns the length of the array JSON value under ``path`` at key
``name``


### jsonarrpop
```py

def jsonarrpop(self, name, path='.', index=-1)

```



Pops the element at ``index`` in the array JSON value under ``path`` at
key ``name``


### jsonarrtrim
```py

def jsonarrtrim(self, name, path, start, stop)

```



Trim the array JSON value under ``path`` at key ``name`` to the 
inclusive range given by ``start`` and ``stop``


### jsondel
```py

def jsondel(self, name, path='.')

```



Deletes the JSON value stored at key ``name`` under ``path``


### jsonget
```py

def jsonget(self, name, *args)

```



Get the object stored as a JSON value at key ``name``
``args`` is zero or more paths, and defaults to root path


### jsonmget
```py

def jsonmget(self, path, *args)

```



Gets the objects stored as a JSON values under ``path`` from 
keys ``args``


### jsonnumincrby
```py

def jsonnumincrby(self, name, path, number)

```



Increments the numeric (integer or floating point) JSON value under
``path`` at key ``name`` by the provided ``number``


### jsonnummultby
```py

def jsonnummultby(self, name, path, number)

```



Multiplies the numeric (integer or floating point) JSON value under
``path`` at key ``name`` with the provided ``number``


### jsonobjkeys
```py

def jsonobjkeys(self, name, path='.')

```



Returns the key names in the dictionary JSON value under ``path`` at key
``name``


### jsonobjlen
```py

def jsonobjlen(self, name, path='.')

```



Returns the length of the dictionary JSON value under ``path`` at key
``name``


### jsonset
```py

def jsonset(self, name, path, obj, nx=False, xx=False)

```



Set the JSON value at key ``name`` under the ``path`` to ``obj``
``nx`` if set to True, set ``value`` only if it does not exist
``xx`` if set to True, set ``value`` only if it exists


### jsonstrappend
```py

def jsonstrappend(self, name, string, path='.')

```



Appends to the string JSON value under ``path`` at key ``name`` the
provided ``string``


### jsonstrlen
```py

def jsonstrlen(self, name, path='.')

```



Returns the length of the string JSON value under ``path`` at key
``name``


### jsontype
```py

def jsontype(self, name, path='.')

```



Gets the type of the JSON value under ``path`` from key ``name``


### setDecoder
```py

def setDecoder(self, decoder)

```



Sets the client's decoder
``decoder`` should be an instance of a ``json.JSONDecoder`` class


### setEncoder
```py

def setEncoder(self, encoder)

```



Sets the client's encoder
``encoder`` should be an instance of a ``json.JSONEncoder`` class




## Class Path
This class represents a path in a JSON value
### \_\_init\_\_
```py

def __init__(self, path)

```



Make a new path based on the string representation in `path`




