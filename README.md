# ReJSON Python Client

This is a package that allows storing, updating and querying objects as JSON
documents in a [Redis](https://redis.io) database that is extended with the
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
from rejson import Client, Path

rj = Client(host='localhost', port=6379)

# Set the key `obj` to some object
rj.JSONSet('obj', Path.rootPath(), {
    'answer': 42,
    'arr': [None, True, 3.14],
    'truth': {
        'coord': 'out there'
    }
})

# Get something
question = 'Is there anybody... {}?'.format(
    rj.JSONGet('obj', Path('.truth.coord'))
)

# Delete something (or perhaps nothing)
rj.JSONDel('obj', Path('.arr[0]'))

# Update something
rj.JSONSet('obj', Path('.answer'), 2.17)
```