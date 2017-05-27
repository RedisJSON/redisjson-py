import json
import redis
import unittest
from unittest import TestCase
from rejson import Client, Path

class ReJSONTestCase(TestCase):
    def testJSONSetGetDelShouldSucceed(self):
        "Test basic JSONSet/Get/Del"
        rj = Client()
        rj.flushdb()

        self.assertTrue(rj.jsonset('foo', Path.rootPath(), 'bar'))
        self.assertEqual('bar', rj.jsonget('foo'))
        self.assertEqual(1, rj.jsondel('foo'))
        self.assertFalse(rj.exists('foo'))

    def testMGetShouldSucceed(self):
        "Test JSONMGet"
        rj = Client()
        rj.flushdb()

        rj.jsonset('1', Path.rootPath(), 1)
        rj.jsonset('2', Path.rootPath(), 2)
        r = rj.jsonmget(Path.rootPath(), '1', '2')
        e = [1, 2]
        self.assertListEqual(e, r)

    def testTypeShouldSucceed(self):
        "Test JSONType"
        rj = Client()
        rj.flushdb()

        rj.jsonset('1', Path.rootPath(), 1)
        self.assertEqual('integer', rj.jsontype('1'))

    def testNumIncrByShouldSucceed(self):
        "Test JSONNumIncrBy"
        rj = Client()
        rj.flushdb()

        rj.jsonset('num', Path.rootPath(), 1)
        self.assertEqual(2, rj.jsonnumincrby('num', Path.rootPath(), 1))
        self.assertEqual(2.5, rj.jsonnumincrby('num', Path.rootPath(), 0.5))
        self.assertEqual(1.25, rj.jsonnumincrby('num', Path.rootPath(), -1.25))

    def testNumMultByShouldSucceed(self):
        "Test JSONNumIncrBy"
        rj = Client()
        rj.flushdb()

        rj.jsonset('num', Path.rootPath(), 1)
        self.assertEqual(2, rj.jsonnummultby('num', Path.rootPath(), 2))
        self.assertEqual(5, rj.jsonnummultby('num', Path.rootPath(), 2.5))
        self.assertEqual(2.5, rj.jsonnummultby('num', Path.rootPath(), 0.5))

    def testStrAppendShouldSucceed(self):
        "Test JSONStrAppend"
        rj = Client()
        rj.flushdb()

        rj.jsonset('str', Path.rootPath(), 'foo')
        self.assertEqual(6, rj.jsonstrappend('str', 'bar', Path.rootPath()))
        self.assertEqual('foobar', rj.jsonget('str', Path.rootPath()))

    def testStrLenShouldSucceed(self):
        "Test JSONStrLen"
        rj = Client()
        rj.flushdb()

        rj.jsonset('str', Path.rootPath(), 'foo')
        self.assertEqual(3, rj.jsonstrlen('str', Path.rootPath()))
        rj.jsonstrappend('str', 'bar', Path.rootPath())
        self.assertEqual(6, rj.jsonstrlen('str', Path.rootPath()))

    def testArrAppendShouldSucceed(self):
        "Test JSONSArrAppend"
        rj = Client()
        rj.flushdb()

        rj.jsonset('arr', Path.rootPath(), [1])
        self.assertEqual(2, rj.jsonarrappend('arr', Path.rootPath(), 2))

    def testArrIndexShouldSucceed(self):
        "Test JSONSArrIndex"
        rj = Client()
        rj.flushdb()

        rj.jsonset('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(1, rj.jsonarrindex('arr', Path.rootPath(), 1))
        self.assertEqual(-1, rj.jsonarrindex('arr', Path.rootPath(), 1, 2))

    def testArrInsertShouldSucceed(self):
        "Test JSONSArrInsert"
        rj = Client()
        rj.flushdb()

        rj.jsonset('arr', Path.rootPath(), [0, 4])
        self.assertEqual(5, rj.jsonarrinsert('arr', Path.rootPath(), 1, *[1, 2, 3,]))
        self.assertListEqual([0, 1, 2, 3, 4], rj.jsonget('arr'))

    def testArrLenShouldSucceed(self):
        "Test JSONSArrLen"
        rj = Client()
        rj.flushdb()

        rj.jsonset('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(5, rj.jsonarrlen('arr', Path.rootPath()))

    def testArrPopShouldSucceed(self):
        "Test JSONSArrPop"
        rj = Client()
        rj.flushdb()

        rj.jsonset('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(4, rj.jsonarrpop('arr', Path.rootPath(), 4))
        self.assertEqual(3, rj.jsonarrpop('arr', Path.rootPath(), -1))
        self.assertEqual(2, rj.jsonarrpop('arr', Path.rootPath()))
        self.assertEqual(0, rj.jsonarrpop('arr', Path.rootPath(), 0))
        self.assertListEqual([1], rj.jsonget('arr'))

    def testArrTrimShouldSucceed(self):
        "Test JSONSArrPop"
        rj = Client()
        rj.flushdb()

        rj.jsonset('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(3, rj.jsonarrtrim('arr', Path.rootPath(), 1, 3))
        self.assertListEqual([1, 2, 3], rj.jsonget('arr'))

    def testObjKeysShouldSucceed(self):
        "Test JSONSObjKeys"
        rj = Client()
        rj.flushdb()

        obj = { 'foo': 'bar', 'baz': 'qaz' }
        rj.jsonset('obj', Path.rootPath(), obj)
        keys = rj.jsonobjkeys('obj', Path.rootPath())
        keys.sort()
        exp = [k for k in obj.iterkeys()]
        exp.sort()
        self.assertListEqual(exp, keys)

    def testObjLenShouldSucceed(self):
        "Test JSONSObjLen"
        rj = Client()
        rj.flushdb()

        obj = { 'foo': 'bar', 'baz': 'qaz' }
        rj.jsonset('obj', Path.rootPath(), obj)
        self.assertEqual(len(obj), rj.jsonobjlen('obj', Path.rootPath()))

    def testPipelineShouldSucceed(self):
        "Test pipeline"
        rj = Client()
        rj.flushdb()

        p = rj.pipeline()
        p.jsonset('foo', Path.rootPath(), 'bar')
        p.jsonget('foo')
        p.jsondel('foo')
        p.exists('foo')
        self.assertListEqual([ True, 'bar', 1, False ], p.execute())

    def testCustomEncoderDecoderShouldSucceed(self):
        "Test a custom encoder and decoder"
        
        class CustomClass(object):
            key = ''
            val = ''
            def __init__(self, k='', v=''):
                self.key = k
                self.val = v

        class TestEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, CustomClass):
                    return 'CustomClass:{}:{}'.format(obj.key, obj.val)
                return json.JSONEncoder.encode(self, obj)

        class TestDecoder(json.JSONDecoder):
            def decode(self, obj):
                d = json.JSONDecoder.decode(self, obj)
                if isinstance(d, basestring) and d.startswith('CustomClass:'):
                    s = d.split(':')
                    return CustomClass(k=s[1], v=s[2])
                return d

        rj = Client(encoder=TestEncoder(), decoder=TestDecoder())
        rj.flushdb()

        # Check a regular string
        self.assertTrue(rj.jsonset('foo', Path.rootPath(), 'bar'))
        self.assertEqual('string', rj.jsontype('foo', Path.rootPath()))
        self.assertEqual('bar', rj.jsonget('foo', Path.rootPath()))

        # Check the custom encoder
        self.assertTrue(rj.jsonset('cus', Path.rootPath(), CustomClass('foo', 'bar')))
        obj = rj.jsonget('cus', Path.rootPath())
        self.assertIsNotNone(obj)
        self.assertEqual(CustomClass, obj.__class__)
        self.assertEqual('foo', obj.key)
        self.assertEqual('bar', obj.val)

    def testUsageExampleShouldSucceed(self):
        "Test the usage example"

        # Create a new rejson-py client
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

if __name__ == '__main__':
    unittest.main()
