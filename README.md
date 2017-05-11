# ReJSON Python Client

rejson-py is a package that allows storing, updating and querying objects as
JSON documents in a [Redis](https://redis.io) database that is extended with the
[ReJSON module](https://github.com/redislabsmodules/rejson). The package extends
[redis-py](https://github.com/andymccurdy/redis-py)'s interface with ReJSON's
API, and performs on-the-fly serialization/deserialization of objects to/from
JSON.

## Installation

```bash
$ pip install rejson-py
```

## Usage example

```python
from rejson import ReJSONClient, Path

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

## License 

[BSD 2-Clause](LICENSE)