# Package rejson Documentation 
 rejson-py is a package that allows storing, updating and querying objects as JSON documents in a [Redis](https://redis.io) database that is extended with the [ReJSON module](https://github.com/redislabsmodules/rejson). The package extends [redis-py](https://github.com/andymccurdy/redis-py)'s interface with ReJSON's API, and performs on-the-fly serialization/deserialization of objects to/from JSON. 
## Class Client
This class subclasses redis-py's `StrictRedis` and implements ReJSON's commmands (prefixed with "json").  The client performs on-the-fly serialization/deserialization of objects to/from JSON, and provides the ability to use a custom encoder/decoder.
### \_\_init\_\_
```py 
def __init__(self, encoder=None, decoder=None, *args, **kwargs) 
``` 
 
Creates a new ReJSON client.   ``encoder`` is an instance of a ``json.JSONEncoder`` class. ``decoder`` is an instance of a ``json.JSONDecoder`` class.
 
### append
```py 
def append(self, key, value) 
``` 
 
Appends the string ``value`` to the value at ``key``. If ``key`` doesn't already exist, create it with a value of ``value``. Returns the new length of the value at ``key``.
 
### bgrewriteaof
```py 
def bgrewriteaof(self) 
``` 
 
Tell the Redis server to rewrite the AOF file from data in memory.
 
### bgsave
```py 
def bgsave(self) 
``` 
 
Tell the Redis server to save its data to disk.  Unlike save(), this method is asynchronous and returns immediately.
 
### bitcount
```py 
def bitcount(self, key, start=None, end=None) 
``` 
 
Returns the count of set bits in the value of ``key``.  Optional ``start`` and ``end`` paramaters indicate which bytes to consider
 
### bitop
```py 
def bitop(self, operation, dest, *keys) 
``` 
 
Perform a bitwise operation using ``operation`` between ``keys`` and store the result in ``dest``.
 
### bitpos
```py 
def bitpos(self, key, bit, start=None, end=None) 
``` 
 
Return the position of the first bit set to 1 or 0 in a string. ``start`` and ``end`` difines search range. The range is interpreted as a range of bytes and not a range of bits, so start=0 and end=2 means to look at the first three bytes.
 
### blpop
```py 
def blpop(self, keys, timeout=0) 
``` 
 
LPOP a value off of the first non-empty list named in the ``keys`` list.  If none of the lists in ``keys`` has a value to LPOP, then block for ``timeout`` seconds, or until a value gets pushed on to one of the lists.  If timeout is 0, then block indefinitely.
 
### brpop
```py 
def brpop(self, keys, timeout=0) 
``` 
 
RPOP a value off of the first non-empty list named in the ``keys`` list.  If none of the lists in ``keys`` has a value to LPOP, then block for ``timeout`` seconds, or until a value gets pushed on to one of the lists.  If timeout is 0, then block indefinitely.
 
### brpoplpush
```py 
def brpoplpush(self, src, dst, timeout=0) 
``` 
 
Pop a value off the tail of ``src``, push it on the head of ``dst`` and then return it.  This command blocks until a value is in ``src`` or until ``timeout`` seconds elapse, whichever is first. A ``timeout`` value of 0 blocks forever.
 
### client\_getname
```py 
def client_getname(self) 
``` 
 
Returns the current connection name
 
### client\_kill
```py 
def client_kill(self, address) 
``` 
 
Disconnects the client at ``address`` (ip:port)
 
### client\_list
```py 
def client_list(self) 
``` 
 
Returns a list of currently connected clients
 
### client\_setname
```py 
def client_setname(self, name) 
``` 
 
Sets the current connection name
 
### config\_get
```py 
def config_get(self, pattern='*') 
``` 
 
Return a dictionary of configuration based on the ``pattern``
 
### config\_resetstat
```py 
def config_resetstat(self) 
``` 
 
Reset runtime statistics
 
### config\_rewrite
```py 
def config_rewrite(self) 
``` 
 
Rewrite config file with the minimal change to reflect running config
 
### config\_set
```py 
def config_set(self, name, value) 
``` 
 
Set config item ``name`` with ``value``
 
### dbsize
```py 
def dbsize(self) 
``` 
 
Returns the number of keys in the current database
 
### debug\_object
```py 
def debug_object(self, key) 
``` 
 
Returns version specific meta information about a given key
 
### decr
```py 
def decr(self, name, amount=1) 
``` 
 
Decrements the value of ``key`` by ``amount``.  If no key exists, the value will be initialized as 0 - ``amount``
 
### delete
```py 
def delete(self, *names) 
``` 
 
Delete one or more keys specified by ``names``
 
### dump
```py 
def dump(self, name) 
``` 
 
Return a serialized version of the value stored at the specified key. If key does not exist a nil bulk reply is returned.
 
### echo
```py 
def echo(self, value) 
``` 
 
Echo the string back from the server
 
### eval
```py 
def eval(self, script, numkeys, *keys_and_args) 
``` 
 
Execute the Lua ``script``, specifying the ``numkeys`` the script will touch and the key names and argument values in ``keys_and_args``. Returns the result of the script.  In practice, use the object returned by ``register_script``. This function exists purely for Redis API completion.
 
### evalsha
```py 
def evalsha(self, sha, numkeys, *keys_and_args) 
``` 
 
Use the ``sha`` to execute a Lua script already registered via EVAL or SCRIPT LOAD. Specify the ``numkeys`` the script will touch and the key names and argument values in ``keys_and_args``. Returns the result of the script.  In practice, use the object returned by ``register_script``. This function exists purely for Redis API completion.
 
### execute\_command
```py 
def execute_command(self, *args, **options) 
``` 
 
Execute a command and return a parsed response
 
### exists
```py 
def exists(self, name) 
``` 
 
Returns a boolean indicating whether key ``name`` exists
 
### expire
```py 
def expire(self, name, time) 
``` 
 
Set an expire flag on key ``name`` for ``time`` seconds. ``time`` can be represented by an integer or a Python timedelta object.
 
### expireat
```py 
def expireat(self, name, when) 
``` 
 
Set an expire flag on key ``name``. ``when`` can be represented as an integer indicating unix time or a Python datetime object.
 
### flushall
```py 
def flushall(self) 
``` 
 
Delete all keys in all databases on the current host
 
### flushdb
```py 
def flushdb(self) 
``` 
 
Delete all keys in the current database
 
### from\_url
```py 
def from_url(cls, url, db=None, **kwargs) 
``` 
 
Return a Redis client object configured from the given URL.  For example::      redis://[:password]@localhost:6379/0     unix://[:password]@/path/to/socket.sock?db=0  There are several ways to specify a database number. The parse function will return the first specified option:     1. A ``db`` querystring option, e.g. redis://localhost?db=0     2. If using the redis:// scheme, the path argument of the url, e.g.        redis://localhost/0     3. The ``db`` argument to this function.  If none of these options are specified, db=0 is used.  Any additional querystring arguments and keyword arguments will be passed along to the ConnectionPool class's initializer. In the case of conflicting arguments, querystring arguments always win.
 
### get
```py 
def get(self, name) 
``` 
 
Return the value at key ``name``, or None if the key doesn't exist
 
### getbit
```py 
def getbit(self, name, offset) 
``` 
 
Returns a boolean indicating the value of ``offset`` in ``name``
 
### getrange
```py 
def getrange(self, key, start, end) 
``` 
 
Returns the substring of the string value stored at ``key``, determined by the offsets ``start`` and ``end`` (both are inclusive)
 
### getset
```py 
def getset(self, name, value) 
``` 
 
Sets the value at key ``name`` to ``value`` and returns the old value at key ``name`` atomically.
 
### hdel
```py 
def hdel(self, name, *keys) 
``` 
 
Delete ``keys`` from hash ``name``
 
### hexists
```py 
def hexists(self, name, key) 
``` 
 
Returns a boolean indicating if ``key`` exists within hash ``name``
 
### hget
```py 
def hget(self, name, key) 
``` 
 
Return the value of ``key`` within the hash ``name``
 
### hgetall
```py 
def hgetall(self, name) 
``` 
 
Return a Python dict of the hash's name/value pairs
 
### hincrby
```py 
def hincrby(self, name, key, amount=1) 
``` 
 
Increment the value of ``key`` in hash ``name`` by ``amount``
 
### hincrbyfloat
```py 
def hincrbyfloat(self, name, key, amount=1.0) 
``` 
 
Increment the value of ``key`` in hash ``name`` by floating ``amount``
 
### hkeys
```py 
def hkeys(self, name) 
``` 
 
Return the list of keys within hash ``name``
 
### hlen
```py 
def hlen(self, name) 
``` 
 
Return the number of elements in hash ``name``
 
### hmget
```py 
def hmget(self, name, keys, *args) 
``` 
 
Returns a list of values ordered identically to ``keys``
 
### hmset
```py 
def hmset(self, name, mapping) 
``` 
 
Set key to value within hash ``name`` for each corresponding key and value from the ``mapping`` dict.
 
### hscan
```py 
def hscan(self, name, cursor=0, match=None, count=None) 
``` 
 
Incrementally return key/value slices in a hash. Also return a cursor indicating the scan position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns
 
### hscan\_iter
```py 
def hscan_iter(self, name, match=None, count=None) 
``` 
 
Make an iterator using the HSCAN command so that the client doesn't need to remember the cursor position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns
 
### hset
```py 
def hset(self, name, key, value) 
``` 
 
Set ``key`` to ``value`` within hash ``name`` Returns 1 if HSET created a new field, otherwise 0
 
### hsetnx
```py 
def hsetnx(self, name, key, value) 
``` 
 
Set ``key`` to ``value`` within hash ``name`` if ``key`` does not exist.  Returns 1 if HSETNX created a field, otherwise 0.
 
### hvals
```py 
def hvals(self, name) 
``` 
 
Return the list of values within hash ``name``
 
### incr
```py 
def incr(self, name, amount=1) 
``` 
 
Increments the value of ``key`` by ``amount``.  If no key exists, the value will be initialized as ``amount``
 
### incrby
```py 
def incrby(self, name, amount=1) 
``` 
 
Increments the value of ``key`` by ``amount``.  If no key exists, the value will be initialized as ``amount``
 
### incrbyfloat
```py 
def incrbyfloat(self, name, amount=1.0) 
``` 
 
Increments the value at key ``name`` by floating ``amount``. If no key exists, the value will be initialized as ``amount``
 
### info
```py 
def info(self, section=None) 
``` 
 
Returns a dictionary containing information about the Redis server  The ``section`` option can be used to select a specific section of information  The section option is not supported by older versions of Redis Server, and will generate ResponseError
 
### jsonarrappend
```py 
def jsonarrappend(self, name, path='.', *args) 
``` 
 
Appends the objects ``args`` to the array under the ``path` in key ``name``
 
### jsonarrindex
```py 
def jsonarrindex(self, name, path, scalar, start=0, stop=-1) 
``` 
 
Returns the index of ``scalar`` in the JSON array under ``path`` at key ``name``. The search can be limited using the optional inclusive ``start`` and exclusive ``stop`` indices.
 
### jsonarrinsert
```py 
def jsonarrinsert(self, name, path, index, *args) 
``` 
 
Inserts the objects ``args`` to the array at index ``index`` under the ``path` in key ``name``
 
### jsonarrlen
```py 
def jsonarrlen(self, name, path='.') 
``` 
 
Returns the length of the array JSON value under ``path`` at key ``name``
 
### jsonarrpop
```py 
def jsonarrpop(self, name, path='.', index=-1) 
``` 
 
Pops the element at ``index`` in the array JSON value under ``path`` at key ``name``
 
### jsonarrtrim
```py 
def jsonarrtrim(self, name, path, start, stop) 
``` 
 
Trim the array JSON value under ``path`` at key ``name`` to the  inclusive range given by ``start`` and ``stop``
 
### jsondel
```py 
def jsondel(self, name, path='.') 
``` 
 
Deletes the JSON value stored at key ``name`` under ``path``
 
### jsonget
```py 
def jsonget(self, name, *args) 
``` 
 
Get the object stored as a JSON value at key ``name`` ``args`` is zero or more paths, and defaults to root path
 
### jsonmget
```py 
def jsonmget(self, path, *args) 
``` 
 
Gets the objects stored as a JSON values under ``path`` from  keys ``args``
 
### jsonnumincrby
```py 
def jsonnumincrby(self, name, path, number) 
``` 
 
Increments the numeric (integer or floating point) JSON value under ``path`` at key ``name`` by the provided ``number``
 
### jsonnummultby
```py 
def jsonnummultby(self, name, path, number) 
``` 
 
Multiplies the numeric (integer or floating point) JSON value under ``path`` at key ``name`` with the provided ``number``
 
### jsonobjkeys
```py 
def jsonobjkeys(self, name, path='.') 
``` 
 
Returns the key names in the dictionary JSON value under ``path`` at key ``name``
 
### jsonobjlen
```py 
def jsonobjlen(self, name, path='.') 
``` 
 
Returns the length of the dictionary JSON value under ``path`` at key ``name``
 
### jsonset
```py 
def jsonset(self, name, path, obj, nx=False, xx=False) 
``` 
 
Set the JSON value at key ``name`` under the ``path`` to ``obj`` ``nx`` if set to True, set ``value`` only if it does not exist ``xx`` if set to True, set ``value`` only if it exists
 
### jsonstrappend
```py 
def jsonstrappend(self, name, string, path='.') 
``` 
 
Appends to the string JSON value under ``path`` at key ``name`` the provided ``string``
 
### jsonstrlen
```py 
def jsonstrlen(self, name, path='.') 
``` 
 
Returns the length of the string JSON value under ``path`` at key ``name``
 
### jsontype
```py 
def jsontype(self, name, path='.') 
``` 
 
Gets the type of the JSON value under ``path`` from key ``name``
 
### keys
```py 
def keys(self, pattern='*') 
``` 
 
Returns a list of keys matching ``pattern``
 
### lastsave
```py 
def lastsave(self) 
``` 
 
Return a Python datetime object representing the last time the Redis database was saved to disk
 
### lindex
```py 
def lindex(self, name, index) 
``` 
 
Return the item from list ``name`` at position ``index``  Negative indexes are supported and will return an item at the end of the list
 
### linsert
```py 
def linsert(self, name, where, refvalue, value) 
``` 
 
Insert ``value`` in list ``name`` either immediately before or after [``where``] ``refvalue``  Returns the new length of the list on success or -1 if ``refvalue`` is not in the list.
 
### llen
```py 
def llen(self, name) 
``` 
 
Return the length of the list ``name``
 
### lock
```py 
def lock(self, name, timeout=None, sleep=0.1, blocking_timeout=None, lock_class=None, thread_local=True) 
``` 
 
Return a new Lock object using key ``name`` that mimics the behavior of threading.Lock.  If specified, ``timeout`` indicates a maximum life for the lock. By default, it will remain locked until release() is called.  ``sleep`` indicates the amount of time to sleep per loop iteration when the lock is in blocking mode and another client is currently holding the lock.  ``blocking_timeout`` indicates the maximum amount of time in seconds to spend trying to acquire the lock. A value of ``None`` indicates continue trying forever. ``blocking_timeout`` can be specified as a float or integer, both representing the number of seconds to wait.  ``lock_class`` forces the specified lock implementation.  ``thread_local`` indicates whether the lock token is placed in thread-local storage. By default, the token is placed in thread local storage so that a thread only sees its token, not a token set by another thread. Consider the following timeline:      time: 0, thread-1 acquires `my-lock`, with a timeout of 5 seconds.              thread-1 sets the token to "abc"     time: 1, thread-2 blocks trying to acquire `my-lock` using the              Lock instance.     time: 5, thread-1 has not yet completed. redis expires the lock              key.     time: 5, thread-2 acquired `my-lock` now that it's available.              thread-2 sets the token to "xyz"     time: 6, thread-1 finishes its work and calls release(). if the              token is *not* stored in thread local storage, then              thread-1 would see the token value as "xyz" and would be              able to successfully release the thread-2's lock.  In some use cases it's necessary to disable thread local storage. For example, if you have code where one thread acquires a lock and passes that lock instance to a worker thread to release later. If thread local storage isn't disabled in this case, the worker thread won't see the token set by the thread that acquired the lock. Our assumption is that these cases aren't common and as such default to using thread local storage.        
 
### lpop
```py 
def lpop(self, name) 
``` 
 
Remove and return the first item of the list ``name``
 
### lpush
```py 
def lpush(self, name, *values) 
``` 
 
Push ``values`` onto the head of the list ``name``
 
### lpushx
```py 
def lpushx(self, name, value) 
``` 
 
Push ``value`` onto the head of the list ``name`` if ``name`` exists
 
### lrange
```py 
def lrange(self, name, start, end) 
``` 
 
Return a slice of the list ``name`` between position ``start`` and ``end``  ``start`` and ``end`` can be negative numbers just like Python slicing notation
 
### lrem
```py 
def lrem(self, name, count, value) 
``` 
 
Remove the first ``count`` occurrences of elements equal to ``value`` from the list stored at ``name``.  The count argument influences the operation in the following ways:     count > 0: Remove elements equal to value moving from head to tail.     count < 0: Remove elements equal to value moving from tail to head.     count = 0: Remove all elements equal to value.
 
### lset
```py 
def lset(self, name, index, value) 
``` 
 
Set ``position`` of list ``name`` to ``value``
 
### ltrim
```py 
def ltrim(self, name, start, end) 
``` 
 
Trim the list ``name``, removing all values not within the slice between ``start`` and ``end``  ``start`` and ``end`` can be negative numbers just like Python slicing notation
 
### mget
```py 
def mget(self, keys, *args) 
``` 
 
Returns a list of values ordered identically to ``keys``
 
### move
```py 
def move(self, name, db) 
``` 
 
Moves the key ``name`` to a different Redis database ``db``
 
### mset
```py 
def mset(self, *args, **kwargs) 
``` 
 
Sets key/values based on a mapping. Mapping can be supplied as a single dictionary argument or as kwargs.
 
### msetnx
```py 
def msetnx(self, *args, **kwargs) 
``` 
 
Sets key/values based on a mapping if none of the keys are already set. Mapping can be supplied as a single dictionary argument or as kwargs. Returns a boolean indicating if the operation was successful.
 
### object
```py 
def object(self, infotype, key) 
``` 
 
Return the encoding, idletime, or refcount about the key
 
### parse\_response
```py 
def parse_response(self, connection, command_name, **options) 
``` 
 
Parses a response from the Redis server
 
### persist
```py 
def persist(self, name) 
``` 
 
Removes an expiration on ``name``
 
### pexpire
```py 
def pexpire(self, name, time) 
``` 
 
Set an expire flag on key ``name`` for ``time`` milliseconds. ``time`` can be represented by an integer or a Python timedelta object.
 
### pexpireat
```py 
def pexpireat(self, name, when) 
``` 
 
Set an expire flag on key ``name``. ``when`` can be represented as an integer representing unix time in milliseconds (unix time * 1000) or a Python datetime object.
 
### pfadd
```py 
def pfadd(self, name, *values) 
``` 
 
Adds the specified elements to the specified HyperLogLog.
 
### pfcount
```py 
def pfcount(self, *sources) 
``` 
 
Return the approximated cardinality of the set observed by the HyperLogLog at key(s).
 
### pfmerge
```py 
def pfmerge(self, dest, *sources) 
``` 
 
Merge N different HyperLogLogs into a single one.
 
### ping
```py 
def ping(self) 
``` 
 
Ping the Redis server
 
### pipeline
```py 
def pipeline(self, transaction=True, shard_hint=None) 
``` 
 
Return a new pipeline object that can queue multiple commands for later execution. ``transaction`` indicates whether all commands should be executed atomically. Apart from making a group of operations atomic, pipelines are useful for reducing the back-and-forth overhead between the client and server.
 
### psetex
```py 
def psetex(self, name, time_ms, value) 
``` 
 
Set the value of key ``name`` to ``value`` that expires in ``time_ms`` milliseconds. ``time_ms`` can be represented by an integer or a Python timedelta object
 
### pttl
```py 
def pttl(self, name) 
``` 
 
Returns the number of milliseconds until the key ``name`` will expire
 
### publish
```py 
def publish(self, channel, message) 
``` 
 
Publish ``message`` on ``channel``. Returns the number of subscribers the message was delivered to.
 
### pubsub
```py 
def pubsub(self, **kwargs) 
``` 
 
Return a Publish/Subscribe object. With this object, you can subscribe to channels and listen for messages that get published to them.
 
### randomkey
```py 
def randomkey(self) 
``` 
 
Returns the name of a random key
 
### register\_script
```py 
def register_script(self, script) 
``` 
 
Register a Lua ``script`` specifying the ``keys`` it will touch. Returns a Script object that is callable and hides the complexity of deal with scripts, keys, and shas. This is the preferred way to work with Lua scripts.
 
### rename
```py 
def rename(self, src, dst) 
``` 
 
Rename key ``src`` to ``dst``
 
### renamenx
```py 
def renamenx(self, src, dst) 
``` 
 
Rename key ``src`` to ``dst`` if ``dst`` doesn't already exist
 
### restore
```py 
def restore(self, name, ttl, value) 
``` 
 
Create a key using the provided serialized value, previously obtained using DUMP.
 
### rpop
```py 
def rpop(self, name) 
``` 
 
Remove and return the last item of the list ``name``
 
### rpoplpush
```py 
def rpoplpush(self, src, dst) 
``` 
 
RPOP a value off of the ``src`` list and atomically LPUSH it on to the ``dst`` list.  Returns the value.
 
### rpush
```py 
def rpush(self, name, *values) 
``` 
 
Push ``values`` onto the tail of the list ``name``
 
### rpushx
```py 
def rpushx(self, name, value) 
``` 
 
Push ``value`` onto the tail of the list ``name`` if ``name`` exists
 
### sadd
```py 
def sadd(self, name, *values) 
``` 
 
Add ``value(s)`` to set ``name``
 
### save
```py 
def save(self) 
``` 
 
Tell the Redis server to save its data to disk, blocking until the save is complete
 
### scan
```py 
def scan(self, cursor=0, match=None, count=None) 
``` 
 
Incrementally return lists of key names. Also return a cursor indicating the scan position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns
 
### scan\_iter
```py 
def scan_iter(self, match=None, count=None) 
``` 
 
Make an iterator using the SCAN command so that the client doesn't need to remember the cursor position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns
 
### scard
```py 
def scard(self, name) 
``` 
 
Return the number of elements in set ``name``
 
### script\_exists
```py 
def script_exists(self, *args) 
``` 
 
Check if a script exists in the script cache by specifying the SHAs of each script as ``args``. Returns a list of boolean values indicating if if each already script exists in the cache.
 
### script\_flush
```py 
def script_flush(self) 
``` 
 
Flush all scripts from the script cache
 
### script\_kill
```py 
def script_kill(self) 
``` 
 
Kill the currently executing Lua script
 
### script\_load
```py 
def script_load(self, script) 
``` 
 
Load a Lua ``script`` into the script cache. Returns the SHA.
 
### sdiff
```py 
def sdiff(self, keys, *args) 
``` 
 
Return the difference of sets specified by ``keys``
 
### sdiffstore
```py 
def sdiffstore(self, dest, keys, *args) 
``` 
 
Store the difference of sets specified by ``keys`` into a new set named ``dest``.  Returns the number of keys in the new set.
 
### sentinel
```py 
def sentinel(self, *args) 
``` 
 
Redis Sentinel's SENTINEL command.
 
### sentinel\_get\_master\_addr\_by\_name
```py 
def sentinel_get_master_addr_by_name(self, service_name) 
``` 
 
Returns a (host, port) pair for the given ``service_name``
 
### sentinel\_master
```py 
def sentinel_master(self, service_name) 
``` 
 
Returns a dictionary containing the specified masters state.
 
### sentinel\_masters
```py 
def sentinel_masters(self) 
``` 
 
Returns a list of dictionaries containing each master's state.
 
### sentinel\_monitor
```py 
def sentinel_monitor(self, name, ip, port, quorum) 
``` 
 
Add a new master to Sentinel to be monitored
 
### sentinel\_remove
```py 
def sentinel_remove(self, name) 
``` 
 
Remove a master from Sentinel's monitoring
 
### sentinel\_sentinels
```py 
def sentinel_sentinels(self, service_name) 
``` 
 
Returns a list of sentinels for ``service_name``
 
### sentinel\_set
```py 
def sentinel_set(self, name, option, value) 
``` 
 
Set Sentinel monitoring parameters for a given master
 
### sentinel\_slaves
```py 
def sentinel_slaves(self, service_name) 
``` 
 
Returns a list of slaves for ``service_name``
 
### set
```py 
def set(self, name, value, ex=None, px=None, nx=False, xx=False) 
``` 
 
Set the value at key ``name`` to ``value``  ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.  ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.  ``nx`` if set to True, set the value at key ``name`` to ``value`` if it     does not already exist.  ``xx`` if set to True, set the value at key ``name`` to ``value`` if it     already exists.
 
### setDecoder
```py 
def setDecoder(self, decoder) 
``` 
 
Sets the decoder
 
### setEncoder
```py 
def setEncoder(self, encoder) 
``` 
 
Sets the encoder
 
### set\_response\_callback
```py 
def set_response_callback(self, command, callback) 
``` 
 
Set a custom Response Callback
 
### setbit
```py 
def setbit(self, name, offset, value) 
``` 
 
Flag the ``offset`` in ``name`` as ``value``. Returns a boolean indicating the previous value of ``offset``.
 
### setex
```py 
def setex(self, name, time, value) 
``` 
 
Set the value of key ``name`` to ``value`` that expires in ``time`` seconds. ``time`` can be represented by an integer or a Python timedelta object.
 
### setnx
```py 
def setnx(self, name, value) 
``` 
 
Set the value of key ``name`` to ``value`` if key doesn't exist
 
### setrange
```py 
def setrange(self, name, offset, value) 
``` 
 
Overwrite bytes in the value of ``name`` starting at ``offset`` with ``value``. If ``offset`` plus the length of ``value`` exceeds the length of the original value, the new value will be larger than before. If ``offset`` exceeds the length of the original value, null bytes will be used to pad between the end of the previous value and the start of what's being injected.  Returns the length of the new string.
 
### shutdown
```py 
def shutdown(self) 
``` 
 
Shutdown the server
 
### sinter
```py 
def sinter(self, keys, *args) 
``` 
 
Return the intersection of sets specified by ``keys``
 
### sinterstore
```py 
def sinterstore(self, dest, keys, *args) 
``` 
 
Store the intersection of sets specified by ``keys`` into a new set named ``dest``.  Returns the number of keys in the new set.
 
### sismember
```py 
def sismember(self, name, value) 
``` 
 
Return a boolean indicating if ``value`` is a member of set ``name``
 
### slaveof
```py 
def slaveof(self, host=None, port=None) 
``` 
 
Set the server to be a replicated slave of the instance identified by the ``host`` and ``port``. If called without arguments, the instance is promoted to a master instead.
 
### slowlog\_get
```py 
def slowlog_get(self, num=None) 
``` 
 
Get the entries from the slowlog. If ``num`` is specified, get the most recent ``num`` items.
 
### slowlog\_len
```py 
def slowlog_len(self) 
``` 
 
Get the number of items in the slowlog
 
### slowlog\_reset
```py 
def slowlog_reset(self) 
``` 
 
Remove all items in the slowlog
 
### smembers
```py 
def smembers(self, name) 
``` 
 
Return all members of the set ``name``
 
### smove
```py 
def smove(self, src, dst, value) 
``` 
 
Move ``value`` from set ``src`` to set ``dst`` atomically
 
### sort
```py 
def sort(self, name, start=None, num=None, by=None, get=None, desc=False, alpha=False, store=None, groups=False) 
``` 
 
Sort and return the list, set or sorted set at ``name``.  ``start`` and ``num`` allow for paging through the sorted data  ``by`` allows using an external key to weight and sort the items.     Use an "*" to indicate where in the key the item value is located  ``get`` allows for returning items from external keys rather than the     sorted data itself.  Use an "*" to indicate where int he key     the item value is located  ``desc`` allows for reversing the sort  ``alpha`` allows for sorting lexicographically rather than numerically  ``store`` allows for storing the result of the sort into     the key ``store``  ``groups`` if set to True and if ``get`` contains at least two     elements, sort will return a list of tuples, each containing the     values fetched from the arguments to ``get``.
 
### spop
```py 
def spop(self, name) 
``` 
 
Remove and return a random member of set ``name``
 
### srandmember
```py 
def srandmember(self, name, number=None) 
``` 
 
If ``number`` is None, returns a random member of set ``name``.  If ``number`` is supplied, returns a list of ``number`` random memebers of set ``name``. Note this is only available when running Redis 2.6+.
 
### srem
```py 
def srem(self, name, *values) 
``` 
 
Remove ``values`` from set ``name``
 
### sscan
```py 
def sscan(self, name, cursor=0, match=None, count=None) 
``` 
 
Incrementally return lists of elements in a set. Also return a cursor indicating the scan position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns
 
### sscan\_iter
```py 
def sscan_iter(self, name, match=None, count=None) 
``` 
 
Make an iterator using the SSCAN command so that the client doesn't need to remember the cursor position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns
 
### strlen
```py 
def strlen(self, name) 
``` 
 
Return the number of bytes stored in the value of ``name``
 
### substr
```py 
def substr(self, name, start, end=-1) 
``` 
 
Return a substring of the string at key ``name``. ``start`` and ``end`` are 0-based integers specifying the portion of the string to return.
 
### sunion
```py 
def sunion(self, keys, *args) 
``` 
 
Return the union of sets specified by ``keys``
 
### sunionstore
```py 
def sunionstore(self, dest, keys, *args) 
``` 
 
Store the union of sets specified by ``keys`` into a new set named ``dest``.  Returns the number of keys in the new set.
 
### time
```py 
def time(self) 
``` 
 
Returns the server time as a 2-item tuple of ints: (seconds since epoch, microseconds into this second).
 
### transaction
```py 
def transaction(self, func, *watches, **kwargs) 
``` 
 
Convenience method for executing the callable `func` as a transaction while watching all keys specified in `watches`. The 'func' callable should expect a single argument which is a Pipeline object.
 
### ttl
```py 
def ttl(self, name) 
``` 
 
Returns the number of seconds until the key ``name`` will expire
 
### type
```py 
def type(self, name) 
``` 
 
Returns the type of key ``name``
 
### unwatch
```py 
def unwatch(self) 
``` 
 
Unwatches the value at key ``name``, or None of the key doesn't exist
 
### wait
```py 
def wait(self, num_replicas, timeout) 
``` 
 
Redis synchronous replication That returns the number of replicas that processed the query when we finally have at least ``num_replicas``, or when the ``timeout`` was reached.
 
### watch
```py 
def watch(self, *names) 
``` 
 
Watches the values at keys ``names``, or None if the key doesn't exist
 
### zadd
```py 
def zadd(self, name, *args, **kwargs) 
``` 
 
Set any number of score, element-name pairs to the key ``name``. Pairs can be specified in two ways:  As *args, in the form of: score1, name1, score2, name2, ... or as **kwargs, in the form of: name1=score1, name2=score2, ...  The following example would add four values to the 'my-key' key: redis.zadd('my-key', 1.1, 'name1', 2.2, 'name2', name3=3.3, name4=4.4)
 
### zcard
```py 
def zcard(self, name) 
``` 
 
Return the number of elements in the sorted set ``name``
 
### zcount
```py 
def zcount(self, name, min, max) 
``` 
 
Returns the number of elements in the sorted set at key ``name`` with a score between ``min`` and ``max``.
 
### zincrby
```py 
def zincrby(self, name, value, amount=1) 
``` 
 
Increment the score of ``value`` in sorted set ``name`` by ``amount``
 
### zinterstore
```py 
def zinterstore(self, dest, keys, aggregate=None) 
``` 
 
Intersect multiple sorted sets specified by ``keys`` into a new sorted set, ``dest``. Scores in the destination will be aggregated based on the ``aggregate``, or SUM if none is provided.
 
### zlexcount
```py 
def zlexcount(self, name, min, max) 
``` 
 
Return the number of items in the sorted set ``name`` between the lexicographical range ``min`` and ``max``.
 
### zrange
```py 
def zrange(self, name, start, end, desc=False, withscores=False, score_cast_func=<type 'float'>) 
``` 
 
Return a range of values from sorted set ``name`` between ``start`` and ``end`` sorted in ascending order.  ``start`` and ``end`` can be negative, indicating the end of the range.  ``desc`` a boolean indicating whether to sort the results descendingly  ``withscores`` indicates to return the scores along with the values. The return type is a list of (value, score) pairs  ``score_cast_func`` a callable used to cast the score return value
 
### zrangebylex
```py 
def zrangebylex(self, name, min, max, start=None, num=None) 
``` 
 
Return the lexicographical range of values from sorted set ``name`` between ``min`` and ``max``.  If ``start`` and ``num`` are specified, then return a slice of the range.
 
### zrangebyscore
```py 
def zrangebyscore(self, name, min, max, start=None, num=None, withscores=False, score_cast_func=<type 'float'>) 
``` 
 
Return a range of values from the sorted set ``name`` with scores between ``min`` and ``max``.  If ``start`` and ``num`` are specified, then return a slice of the range.  ``withscores`` indicates to return the scores along with the values. The return type is a list of (value, score) pairs  `score_cast_func`` a callable used to cast the score return value
 
### zrank
```py 
def zrank(self, name, value) 
``` 
 
Returns a 0-based value indicating the rank of ``value`` in sorted set ``name``
 
### zrem
```py 
def zrem(self, name, *values) 
``` 
 
Remove member ``values`` from sorted set ``name``
 
### zremrangebylex
```py 
def zremrangebylex(self, name, min, max) 
``` 
 
Remove all elements in the sorted set ``name`` between the lexicographical range specified by ``min`` and ``max``.  Returns the number of elements removed.
 
### zremrangebyrank
```py 
def zremrangebyrank(self, name, min, max) 
``` 
 
Remove all elements in the sorted set ``name`` with ranks between ``min`` and ``max``. Values are 0-based, ordered from smallest score to largest. Values can be negative indicating the highest scores. Returns the number of elements removed
 
### zremrangebyscore
```py 
def zremrangebyscore(self, name, min, max) 
``` 
 
Remove all elements in the sorted set ``name`` with scores between ``min`` and ``max``. Returns the number of elements removed.
 
### zrevrange
```py 
def zrevrange(self, name, start, end, withscores=False, score_cast_func=<type 'float'>) 
``` 
 
Return a range of values from sorted set ``name`` between ``start`` and ``end`` sorted in descending order.  ``start`` and ``end`` can be negative, indicating the end of the range.  ``withscores`` indicates to return the scores along with the values The return type is a list of (value, score) pairs  ``score_cast_func`` a callable used to cast the score return value
 
### zrevrangebylex
```py 
def zrevrangebylex(self, name, max, min, start=None, num=None) 
``` 
 
Return the reversed lexicographical range of values from sorted set ``name`` between ``max`` and ``min``.  If ``start`` and ``num`` are specified, then return a slice of the range.
 
### zrevrangebyscore
```py 
def zrevrangebyscore(self, name, max, min, start=None, num=None, withscores=False, score_cast_func=<type 'float'>) 
``` 
 
Return a range of values from the sorted set ``name`` with scores between ``min`` and ``max`` in descending order.  If ``start`` and ``num`` are specified, then return a slice of the range.  ``withscores`` indicates to return the scores along with the values. The return type is a list of (value, score) pairs  ``score_cast_func`` a callable used to cast the score return value
 
### zrevrank
```py 
def zrevrank(self, name, value) 
``` 
 
Returns a 0-based value indicating the descending rank of ``value`` in sorted set ``name``
 
### zscan
```py 
def zscan(self, name, cursor=0, match=None, count=None, score_cast_func=<type 'float'>) 
``` 
 
Incrementally return lists of elements in a sorted set. Also return a cursor indicating the scan position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns  ``score_cast_func`` a callable used to cast the score return value
 
### zscan\_iter
```py 
def zscan_iter(self, name, match=None, count=None, score_cast_func=<type 'float'>) 
``` 
 
Make an iterator using the ZSCAN command so that the client doesn't need to remember the cursor position.  ``match`` allows for filtering the keys by pattern  ``count`` allows for hint the minimum number of returns  ``score_cast_func`` a callable used to cast the score return value
 
### zscore
```py 
def zscore(self, name, value) 
``` 
 
Return the score of element ``value`` in sorted set ``name``
 
### zunionstore
```py 
def zunionstore(self, dest, keys, aggregate=None) 
``` 
 
Union multiple sorted sets specified by ``keys`` into a new sorted set, ``dest``. Scores in the destination will be aggregated based on the ``aggregate``, or SUM if none is provided.
 
 
## Class Path
None
### \_\_init\_\_
```py 
def __init__(self, path) 
``` 
 
 
