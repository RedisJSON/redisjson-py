Examples
========

Insert
------------------------------
::

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

Retrieve
---------------
::

  print 'Is there anybody... {}?'.format(
      rj.jsonget('obj', Path('.truth.coord'))
  )

Delete and Append
-----------------
::

  rj.jsondel('obj', Path('.arr[0]'))
  rj.jsonarrappend('obj', Path('.arr'), 'something')
  print '{} popped!'.format(rj.jsonarrpop('obj', Path('.arr')))

Update
--------
::

  rj.jsonset('obj', Path('.answer'), 2.17)

Pipelinining
-------------
::

  jp = rj.pipeline()
  jp.set('foo', 'bar')
  jp.jsonset('baz', Path.rootPath(), 'qaz')
  jp.execute()

Inserting non-ascii values
--------------------------
::

  obj_non_ascii = {
    'non_ascii_string': 'hyvää'
  }

  rj.jsonset('non-ascii', Path.rootPath(), obj_non_ascii)
  print '{} is a non-ascii string'.format(rj.jsonget('non-ascii', Path('.non_ascii_string'), no_escape=True))

Encoding/Decoding
-----------------

rejson-py uses Python's `json https://docs.python.org/2/library/json.html`.
The client can be set to use custom encoders/decoders at creation, or by calling
explicitly the [`setEncoder()`](API.md#setencoder) and
[`setDecoder()`](API.md#setdecoder) methods, respectively.

::

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
  """
