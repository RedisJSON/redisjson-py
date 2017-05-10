import redis
from unittest import TestCase
from rejson import Client, Path

class ReJSONTestCase(TestCase):
    
    def testJSONSetGetDelShouldSucceed(self):
        "Test basic JSONSet/Get/Del"
        rj = Client()
        rj.flushdb()

        self.assertTrue(rj.JSONSet('foo', Path.rootPath(), 'bar'))
        self.assertEqual('bar', rj.JSONGet('foo'))
        self.assertEqual(1, rj.JSONDel('foo'))
        self.assertFalse(rj.exists('foo'))

    def testMGetShouldSucceed(self):
        "Test JSONMGet"
        rj = Client()
        rj.flushdb()

        rj.JSONSet('1', Path.rootPath(), 1)
        rj.JSONSet('2', Path.rootPath(), 2)
        r = rj.JSONMGet(Path.rootPath(), '1', '2')
        e = [1, 2]
        self.assertListEqual(e, r)

    def testTypeShouldSucceed(self):
        "Test JSONType"
        rj = Client()
        rj.flushdb()

        rj.JSONSet('1', Path.rootPath(), 1)
        self.assertEqual('integer', rj.JSONType('1'))

    def testNumIncrByShouldSucceed(self):
        "Test JSONNumIncrBy"
        rj = Client()
        rj.flushdb()

        rj.JSONSet('num', Path.rootPath(), 1)
        self.assertEqual(2, rj.JSONNumIncrBy('num', Path.rootPath(), 1))
        self.assertEqual(2.5, rj.JSONNumIncrBy('num', Path.rootPath(), 0.5))
        self.assertEqual(1.25, rj.JSONNumIncrBy('num', Path.rootPath(), -1.25))

    def testNumMultByShouldSucceed(self):
        "Test JSONNumIncrBy"
        rj = Client()
        rj.flushdb()

        rj.JSONSet('num', Path.rootPath(), 1)
        self.assertEqual(2, rj.JSONNumMultBy('num', Path.rootPath(), 2))
        self.assertEqual(5, rj.JSONNumMultBy('num', Path.rootPath(), 2.5))
        self.assertEqual(2.5, rj.JSONNumMultBy('num', Path.rootPath(), 0.5))

    def testStrAppendShouldSucceed(self):
        "Test JSONStrAppend"
        rj = Client()
        rj.flushdb()

        rj.JSONSet('str', Path.rootPath(), 'foo')
        self.assertEqual(6, rj.JSONStrAppend('str', 'bar', Path.rootPath()))
        self.assertEqual('foobar', rj.JSONGet('str', Path.rootPath()))

    def testStrLenShouldSucceed(self):
        "Test JSONStrLen"
        rj = Client()
        rj.flushdb()

        rj.JSONSet('str', Path.rootPath(), 'foo')
        self.assertEqual(3, rj.JSONStrLen('str', Path.rootPath()))
        rj.JSONStrAppend('str', 'bar', Path.rootPath())
        self.assertEqual(6, rj.JSONStrLen('str', Path.rootPath()))

    def testUsageExampleShouldSucceed(self):
        "Test the usage example"

        # Create a new rejson-py client
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

if __name__ == '__main__':
    unittest.main()
