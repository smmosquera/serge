"""Tests for the serialization of objects"""

import unittest

from helper import *

import serge.serialize
import serge.zone
import serge.actor
import serge.world
import serge.render

s = serge.serialize

class TestSerialization(unittest.TestCase):
    """Tests for the Serialization"""

    def setUp(self):
        """Set up the tests"""
        
        
    def tearDown(self):
        """Tear down the tests"""

    ### Basic tests ###
    
    def testCanCreateWithDefaults(self):
        """testCanCreateWithDefaults: should be able to create an object with default properties"""
        o1 = O1.createInstance()
        self.assertEqual(10, o1.xx)
        self.assertEqual(20, o1.yy)
        self.assertEqual('hello', o1.z)        
        
    def testCreateSubclassesWithDefaults(self):
        """testCreateSubclassesWithDefaults: should be able to create a subclass of object with defaults"""
        o2 = O2.createInstance()
        self.assertEqual(100, o2.xx)
        self.assertEqual(20, o2.yy)
        self.assertEqual('hello', o2.z)        
        self.assertEqual('bye', o2.a)        
        
    def testCanSeeInitialProps(self):
        """testCanSeeInitialProps: should be able to see the initial properties"""
        o2 = O2.createInstance()
        self.assertEqual(100, o2.initial_properties.xx)
        self.assertEqual(20, o2.initial_properties.yy)
        self.assertEqual('hello', o2.initial_properties.z)        
        self.assertEqual('bye', o2.initial_properties.a)        
        
    def testCanChangeLiveProperties(self):
        """testCanChangeLiveProperties: should be able to change live properties"""
        o1 = O1.createInstance()
        o1.xx = -1
        o1.yy = -2
        o1.z = 'nothing'

    def testCanRoundTripLiveProperties(self):
        """testCanRoundTripLiveProperties: should be able to serialize and then deserialize properties"""
        o1 = O2.createInstance()
        o2 = O2.createInstance()
        o1.xx = -1
        o1.yy = -2
        o1.z = 'nothing'
        o1.a = 'tomorrow'
        o3 = serge.serialize.Serializable.fromString(o1.asString())
        self.assertEqual(-1, o3.xx)
        self.assertEqual(-2, o3.yy)
        self.assertEqual('nothing', o3.z)
        self.assertEqual('tomorrow', o3.a)
        self.assertEqual(100, o2.initial_properties.xx)
        self.assertEqual(20, o2.initial_properties.yy)
        self.assertEqual('hello', o2.initial_properties.z)        
        self.assertEqual('bye', o2.initial_properties.a)        
       
    def testCanThawObject(self):
        """testCanThawObject: should be able to do thawing logic"""
        o1 = O3.createInstance()
        o1.xx = -1
        o1.yy = -2
        o1.z = 'nothing'
        o1.a = 'tomorrow'
        o3 = serge.serialize.Serializable.fromString(o1.asString())
        self.assertEqual(111, o3.xx)      
        
    def testBlankThaw(self):
        """testBlankThaw: object with no thaw should work"""
        o1 = O2.createInstance()
        o1.xx = -1
        o1.yy = -2
        o1.z = 'nothing'
        o1.a = 'tomorrow'
        o3 = serge.serialize.Serializable.fromString(o1.asString())      
        
    def testCanSerializeToFile(self):
        """testCanSerializeToFile: should be able to serialize to a file"""
        o1 = O2.createInstance()
        o1.xx = -1
        o1.toFile(j('serialized1.serge'))
        
    def testCanDeserializeFromFile(self):
        """testCanDeserializeFromFile: should be able to thaw from a file"""
        o1 = O2.createInstance()
        o1.xx = -1
        o1.toFile(j('serialized2.serge'))
        o2 = serge.serialize.Serializable.fromFile(j('serialized2.serge'))
        self.assertEqual(-1, o1.xx)
        
    def testFailSerializeToNonPath(self):
        """testFailSerializeToNonPath: should fail when serializing to something that isn't a path"""
        o1 = O2.createInstance()
        o1.xx = -1
        self.assertRaises(IOError, o1.toFile, j('something', 'serialized2.serge'))
        
    def testFailDeserializeFromInvalidFile(self):
        """testFailDeserializeFromInvalidFile: should fail when deserializing from a file that isn't valid"""
        file(j('bad.serge'), 'w').write('something bad')
        o2 = self.assertRaises(serge.serialize.InvalidFile, serge.serialize.Serializable.fromFile, j('bad.serge'))
        
        
    def testFailDeserializeNoFile(self):
        """testFailDeserializeNoFile: should fail when deserializing from a bad filename"""
        o2 = self.assertRaises(IOError, serge.serialize.Serializable.fromFile, j('serialized3.serge'))
        
    
    ### Types ###
    
    def testCanCheckTypes(self):
        """testCanCheckTypes: should be able to check types"""
        o1 = O3.createInstance()
        self.assertEqual(s.Int, o1.initial_properties.xx.__class__)
        self.assertEqual(s.String, o1.initial_properties.a.__class__)
        
    def testCanGetDescriptions(self):
        """testCanGetDescriptions: should be able to get descriptions"""
        o1 = O1.createInstance()
        self.assertEqual('The x coordinate', o1.initial_properties.xx.description)
        self.assertEqual('yy', o1.initial_properties.yy.description)
        
    def testCanGetDescriptionsInherited(self):
        """testCanGetDescriptionsInherited: inherited descriptions should override"""
        o1 = O2.createInstance()
        self.assertEqual('other x', o1.initial_properties.xx.description)
        self.assertEqual('yy', o1.initial_properties.yy.description)
        
    ### Zones ###
    
    def testCanSerializeAZone(self):
        """testCanSerializeAZone: should be able to serialize a zone"""
        #
        # Create a nice zone
        z = TestZone()
        z.active = True
        for idx in range(5):
            a = TestActor()
            a.xx = idx
            a.yy = idx*2
            a.z = str(idx)
            z.addActor(a)
        #
        # Recreate
        zz = serge.serialize.Serializable.fromString(z.asString())
        #
        # Blow away the old ones to make sure
        for a in z.actors:
            a.xx = 0
            a.yy = 0
            a.z = ''
        #
        # And test
        self.assertEqual(True, zz.active)
        xs = set()
        for a in zz.actors:
            xs.add(a.xx)
            self.assertEqual(2*a.xx, a.yy)
            self.assertEqual(str(a.xx), a.z)
            self.assertEqual(10*a.xx, a.thawed_x)
        self.assertEqual(set(range(5)), xs)


    ### Worlds ###
    
    def testCanSerializeAWorld(self):
        """testCanSerializeAWorld: should be able to serialize a world"""
        #
        # Create nice zones
        w = serge.world.World('test')
        initial_xs = set()
        for zidx in range(5):
            z = TestZone()
            for idx in range(5):
                a = TestActor()
                a.xx = idx+zidx
                if a.xx == 0:
                    z.active = True
                initial_xs.add(a.xx)
                a.yy = a.xx*2
                a.z = str(a.xx)
                z.addActor(a)
            w.zones.add(z)
        #
        # Recreate
        ww = serge.serialize.Serializable.fromString(w.asString())
        #
        # And test
        xs = set()
        for zz in ww.zones:
            for a in zz.actors:
                xs.add(a.xx)
                self.assertEqual(2*a.xx, a.yy)
                self.assertEqual(str(a.xx), a.z)
                self.assertEqual(10*a.xx, a.thawed_x)
                if a.xx == 0:
                    self.assert_(zz.active)

        self.assertEqual(initial_xs, xs)
        self.assertEqual(5, len(ww.zones))
        
        
    ### Rendering ###
                    
    def testCanSerializeLayer(self):
        """testCanSerializeLayer: should be able to serialize a layer"""
        l = TestLayer('one', 15)
        x = serge.serialize.Serializable.fromString(l.asString())
        self.assertEqual('one', x.name)
        self.assertEqual(15, x.order)
        
    def testCanSerializeRender(self):
        """testCanSerializeRender: should be able to serialize a renderer"""
        r = serge.render.Renderer()
        r.addLayer(TestLayer('one', 20))
        r.addLayer(TestLayer('two', 10))
        r.addLayer(TestLayer('three', 30))
        r.render()
        #
        x = serge.serialize.Serializable.fromString(r.asString())
        #
        x.render()
        self.assertEqual('two', r.layers[0].name)
        self.assertEqual('one', r.layers[1].name)
        self.assertEqual('three', r.layers[2].name)
        #
        self.assertEqual(1, r.layers[0].executed)
        self.assertEqual(2, r.layers[1].executed)
        self.assertEqual(3, r.layers[2].executed)
        
    
    
    
class O1(serge.serialize.Serializable):
    
    my_properties = (
        s.I('xx', 10, 'The x coordinate'),
        s.I('yy', 20),
        s.S('z', 'hello', 'text'),
    )

class O2(O1):
    
    my_properties = (
        s.I('xx', 100, 'other x'),
        s.S('a', 'bye'),
    )

class O3(O2):
    
    def init(self):
        """Thaw the object"""
        self.xx = 111


class TestZone(serge.zone.Zone):


    def __init__(self):
        """Initialise"""
        super(TestZone, self).__init__()
        self.counter = 0
        self.init()


        
    def updateZone(self, interval):
        """Update the zone"""
        self.counter += interval 
        super(TestZone, self).updateZone(interval)   


class TestActor(serge.actor.Actor, serge.serialize.Serializable):

    my_properties = (
        s.I('xx', 10, 'The x coordinate'),
        s.I('yy', 20),
        s.S('z', 'hello', 'text'),
    )

    def __init__(self):
        """Initialise"""
        super(TestActor, self).__init__('', '')
        self.counter = 0
    
    def updateActor(self, interval):
        """Update the actor"""
        self.counter += interval    
        
    def init(self):
        """Thaw the actor"""
        self.thawed_x = self.xx*10     
        

class TestLayer(serge.render.Layer, serge.common.EventAware):
    """A test layer"""
    
    count = 0
    
    def __init__(self, name, order=0):
        """Initialise the TestLayer"""
        super(TestLayer, self).__init__(name, order)
        self.initEvents()
        self.executed = 1e30
        
    def render(self, surface):
        """Render to a surface"""
        TestLayer.count += 1
        self.executed = TestLayer.count

               
if __name__ == '__main__':
    unittest.main()
