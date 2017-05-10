import redis
from unittest import TestCase
from rejson import ReJSONClient, Path

class ReJSONTestCase(TestCase):
    def testJSONSetGetDelShouldSucceed(self):
        "Test basic JSONSet/Get/Del"
        rj = ReJSONClient()
        rj.flushdb()

        self.assertTrue(rj.JSONSet('foo', Path.rootPath(), 'bar'))
        self.assertEqual('bar', rj.JSONGet('foo'))
        self.assertEqual(1, rj.JSONDel('foo'))
        self.assertFalse(rj.exists('foo'))

    def testMGetShouldSucceed(self):
        "Test JSONMGet"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('1', Path.rootPath(), 1)
        rj.JSONSet('2', Path.rootPath(), 2)
        r = rj.JSONMGet(Path.rootPath(), '1', '2')
        e = [1, 2]
        self.assertListEqual(e, r)

    def testTypeShouldSucceed(self):
        "Test JSONType"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('1', Path.rootPath(), 1)
        self.assertEqual('integer', rj.JSONType('1'))

    def testNumIncrByShouldSucceed(self):
        "Test JSONNumIncrBy"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('num', Path.rootPath(), 1)
        self.assertEqual(2, rj.JSONNumIncrBy('num', Path.rootPath(), 1))
        self.assertEqual(2.5, rj.JSONNumIncrBy('num', Path.rootPath(), 0.5))
        self.assertEqual(1.25, rj.JSONNumIncrBy('num', Path.rootPath(), -1.25))

    def testNumMultByShouldSucceed(self):
        "Test JSONNumIncrBy"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('num', Path.rootPath(), 1)
        self.assertEqual(2, rj.JSONNumMultBy('num', Path.rootPath(), 2))
        self.assertEqual(5, rj.JSONNumMultBy('num', Path.rootPath(), 2.5))
        self.assertEqual(2.5, rj.JSONNumMultBy('num', Path.rootPath(), 0.5))

    def testStrAppendShouldSucceed(self):
        "Test JSONStrAppend"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('str', Path.rootPath(), 'foo')
        self.assertEqual(6, rj.JSONStrAppend('str', 'bar', Path.rootPath()))
        self.assertEqual('foobar', rj.JSONGet('str', Path.rootPath()))

    def testStrLenShouldSucceed(self):
        "Test JSONStrLen"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('str', Path.rootPath(), 'foo')
        self.assertEqual(3, rj.JSONStrLen('str', Path.rootPath()))
        rj.JSONStrAppend('str', 'bar', Path.rootPath())
        self.assertEqual(6, rj.JSONStrLen('str', Path.rootPath()))

    def testArrAppendShouldSucceed(self):
        "Test JSONSArrAppend"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('arr', Path.rootPath(), [1])
        self.assertEqual(2, rj.JSONArrAppend('arr', Path.rootPath(), 2))

    def testArrIndexShouldSucceed(self):
        "Test JSONSArrIndex"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(1, rj.JSONArrIndex('arr', Path.rootPath(), 1))
        self.assertEqual(-1, rj.JSONArrIndex('arr', Path.rootPath(), 1, 2))

    def testArrInsertShouldSucceed(self):
        "Test JSONSArrInsert"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('arr', Path.rootPath(), [0, 4])
        self.assertEqual(5, rj.JSONArrInsert('arr', Path.rootPath(), 1, *[1, 2, 3,]))
        self.assertListEqual([0, 1, 2, 3, 4], rj.JSONGet('arr'))

    def testArrLenShouldSucceed(self):
        "Test JSONSArrLen"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(5, rj.JSONArrLen('arr', Path.rootPath()))

    def testArrPopShouldSucceed(self):
        "Test JSONSArrPop"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(4, rj.JSONArrPop('arr', Path.rootPath(), 4))
        self.assertEqual(3, rj.JSONArrPop('arr', Path.rootPath(), -1))
        self.assertEqual(2, rj.JSONArrPop('arr', Path.rootPath()))
        self.assertEqual(0, rj.JSONArrPop('arr', Path.rootPath(), 0))
        self.assertListEqual([1], rj.JSONGet('arr'))

    def testArrTrimShouldSucceed(self):
        "Test JSONSArrPop"
        rj = ReJSONClient()
        rj.flushdb()

        rj.JSONSet('arr', Path.rootPath(), [0, 1, 2, 3, 4])
        self.assertEqual(3, rj.JSONArrTrim('arr', Path.rootPath(), 1, 3))
        self.assertListEqual([1, 2, 3], rj.JSONGet('arr'))

    def testObjKeysShouldSucceed(self):
        "Test JSONSObjKeys"
        rj = ReJSONClient()
        rj.flushdb()

        obj = { 'foo': 'bar', 'baz': 'qaz' }
        rj.JSONSet('obj', Path.rootPath(), obj)
        keys = rj.JSONObjKeys('obj', Path.rootPath())
        keys.sort()
        exp = [k for k in obj.iterkeys()]
        exp.sort()
        self.assertListEqual(exp, keys)

    def testObjLenShouldSucceed(self):
        "Test JSONSObjLen"
        rj = ReJSONClient()
        rj.flushdb()

        obj = { 'foo': 'bar', 'baz': 'qaz' }
        rj.JSONSet('obj', Path.rootPath(), obj)
        self.assertEqual(len(obj), rj.JSONObjLen('obj', Path.rootPath()))

    def testUsageExampleShouldSucceed(self):
        "Test the usage example"

        # Create a new rejson-py client
        rj = ReJSONClient(host='localhost', port=6379)

        # Set the key `obj` to some object
        obj = {
            'answer': 42,
            'arr': [None, True, 3.14],
            'truth': {
                'coord': 'out there'
            }
        }
        rj.JSONSet('obj', Path.rootPath(), obj)

        # Get something
        print 'Is there anybody... {}?'.format(
            rj.JSONGet('obj', Path('.truth.coord'))
        )

        # Delete something (or perhaps nothing), append something and pop it
        rj.JSONDel('obj', Path('.arr[0]'))
        rj.JSONArrAppend('obj', Path('.arr'), 'something')
        print '{} popped!'.format(rj.JSONArrPop('obj', Path('.arr')))

        # Update something else
        rj.JSONSet('obj', Path('.answer'), 2.17)

if __name__ == '__main__':
    unittest.main()
