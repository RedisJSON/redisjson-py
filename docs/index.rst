Welcome to rejson's documentation!
=====================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   introduction
   examples
   Reference </py-modindex.html#http://>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

rejson-py is a package that allows storing, updating and querying objects as
JSON documents in a `Redis https://redis.io` database that is extended with the
`ReJSON module https://github.com/redislabsmodules/rejson`. The package extends
`redis-py https://github.com/andymccurdy/redis-py`'s interface with ReJSON's
API, and performs on-the-fly serialization/deserialization of objects to/from
JSON.
