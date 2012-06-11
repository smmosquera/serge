"""Tests for Events"""

import unittest
import sys

import serge.events

E_ONE = '1'
E_TWO = '2'
E_THrEE = '3'
E_FOUR = 123

class TestEvents(unittest.TestCase):
    """Tests for the Events"""

    def setUp(self):
        """Set up the tests"""
        self.b = serge.events.getEventBroadcaster()    
        self.b.initEvents()
        self.e1 = 'e1'
        self.e2 = 'e2'
        self.obj = []
        self.arg = []
        
    def tearDown(self):
        """Tear down the tests"""

    def _callback(self, obj, arg):
        """A useful callback"""
        self.obj.append(obj)
        self.arg.append(arg)
        
    def _callback2(self, obj, arg):
        """A useful callback"""
        self.obj.append(obj)
        self.arg.append(arg)
        
    def testCanRegisterEvent(self):
        """testCanRegisterEvent: should be able to register an event"""
        self.b.registerEvent(self.e1)
        
    def testFailRegisterEventAgain(self):
        """testFailRegisterEventAgain: should fail if register a duplicate event"""
        self.b.registerEvent(self.e1)
        self.assertRaises(serge.common.DuplicateEvent, self.b.registerEvent, self.e1)
        
    def testCanBroadcastAnEvent(self):
        """testCanBroadcastAnEvent: should be able to broadcast an event"""
        self.b.registerEvent(self.e1)
        self.b.processEvent((self.e1, (1, 2, 3)))
                
    def testFailBroadcastNonEvent(self):
        """testFailBroadcastNonEvent: should fail if broadcasting a non event"""
        self.assertRaises(serge.common.EventNotFound, self.b.processEvent, (self.e1, (1, 2, 3)))
        
    def testCanSubscribeToEvent(self):
        """testCanSubscribeToEvent: should be able to subscribe to an event"""
        self.b.registerEvent(self.e1)
        self.b.linkEvent(self.e1, self._callback)
        
    def testFailSubscribeToNonEvent(self):
        """testFailSubscribeToNonEvent: should fail if subscribing to an event"""
        self.assertRaises(serge.common.EventNotFound, self.b.linkEvent, self.e1, self._callback)
        
    def testBroadcastGoesToListener(self):
        """testBroadcastGoesToListener: listener should recieve an event"""
        self.b.registerEvent(self.e1)
        self.b.linkEvent(self.e1, self._callback, (1,2,3))
        self.b.processEvent((self.e1, self.b))
        self.assertEqual([self.b], self.obj)
        self.assertEqual([(1,2,3)], self.arg)
                
    def testMultipleSubcribers(self):
        """testMultipleSubcribers: should be able to have multiple subscribers"""
        self.b.registerEvent(self.e1)
        self.b.linkEvent(self.e1, self._callback, (1,2,3))
        self.b.linkEvent(self.e1, self._callback, (4,5,6))
        self.b.processEvent((self.e1, self.b))
        self.assertEqual([self.b, self.b], self.obj)
        self.assertEqual([(1,2,3), (4,5,6)], self.arg)
        
    def testCanUnlinkEvent(self):
        """testCanUnlinkEvent: shold be able to unlink an event"""
        self.b.registerEvent(self.e1)
        self.b.linkEvent(self.e1, self._callback, (1,2,3))
        self.b.unlinkEvent(self.e1, self._callback)
        self.b.processEvent((self.e1, self.b))
        self.assertEqual([], self.obj)
        self.assertEqual([], self.arg)

    def testCanUnlinkWithMultipleSubscribers(self):
        """testCanUnlinkWithMultipleSubscribers: should be able to unlink one from multiple"""
        self.b.registerEvent(self.e1)
        self.b.linkEvent(self.e1, self._callback, (1,2,3))
        self.b.linkEvent(self.e1, self._callback2, (4,5,6))
        self.b.unlinkEvent(self.e1, self._callback)
        self.b.processEvent((self.e1, self.b))
        self.assertEqual([self.b], self.obj)
        self.assertEqual([(4,5,6)], self.arg)
        
    def testFailUnlinkNotLinked(self):
        """testFailUnlinkNotLinked: should fail when inlinking an event that is not linked"""
        self.b.registerEvent(self.e1)
        self.assertRaises(serge.common.EventNotLinked, self.b.unlinkEvent, self.e1, self._callback)

    def testFailUnlinkNonEvent(self):
        """testFailUnlinkNonEvent: should fail when unlinking a not registered event"""
        self.assertRaises(serge.common.EventNotFound, self.b.unlinkEvent, self.e1, self._callback)
        
    def testCanRegisterMultiple(self):
        """testCanRegisterMultiple: should be able to register multiple in one go"""
        self.b.registerEvents([self.e1, self.e2])
        self.b.linkEvent(self.e1, self._callback, (1,2,3))
        self.b.linkEvent(self.e2, self._callback, (1,2,3))
        
    def testCanRegisterAllInAModule(self):
        """testCanRegisterAllInAModule: should be able to register all events in a module"""
        self.assertRaises(serge.common.EventNotFound, self.b.unlinkEvent, E_ONE, self._callback)
        self.assertRaises(serge.common.EventNotFound, self.b.unlinkEvent, E_TWO, self._callback)
        self.assertRaises(serge.common.EventNotFound, self.b.unlinkEvent, E_THrEE, self._callback)
        self.assertRaises(serge.common.EventNotFound, self.b.unlinkEvent, E_FOUR, self._callback)
        this = sys.modules[__name__]
        self.b.registerEventsFromModule(this)
        self.b.linkEvent(E_ONE, self._callback)        
        self.b.linkEvent(E_TWO, self._callback)
        self.assertRaises(serge.common.EventNotFound, self.b.unlinkEvent, E_THrEE, self._callback)
        self.assertRaises(serge.common.EventNotFound, self.b.unlinkEvent, E_FOUR, self._callback)
        
        
        


if __name__ == '__main__':
    unittest.main()
