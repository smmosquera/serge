"""Tests for Behaviours"""

import unittest
import os

from helper import *

import serge.engine
import serge.actor
import serge.visual
import serge.world
import serge.zone
import serge.blocks.behaviours
import serge.blocks.utils
import serge.blocks.visualblocks
import serge.blocks.directions

class TestBehaviours(unittest.TestCase):
    """Tests for the Behaviours"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Register.clearItems()
        self.w = serge.world.World('test')
        self.z = serge.zone.Zone()
        self.w.addZone(self.z)
        self.z.active = True
        self.b = serge.blocks.behaviours.BehaviourManager('bm')
        self.w.addActor(self.b)
        self.state = {}
        self.e = serge.engine.Engine()
        self.v = serge.blocks.visualblocks.Rectangle((10, 10), (255,255,255,255))
        self.k = FakeKeyboard()
                
    def tearDown(self):
        """Tear down the tests"""

    def doit(self, world, actor, interval):
        self.state['done'] = (world, actor, interval)

    def doit2(self, world, actor, interval):
        self.state['done2'] = (world, actor, interval)

    def testCanAddBehaviour(self):
        """testCanAddBehaviour: should be able to add a behaviour to an actor"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        self.b.assignBehaviour(a, self.doit, 'test')
        self.w.updateWorld(1000)
        #
        self.assertEqual((self.w, a, 1000), self.state.get('done', 'doit was not called'))

    def testCanAddBehaviourWithNoActor(self):
        """testCanAddBehaviourWithNoActor: should be able to add a behaviour to no actor in particular"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        self.b.assignBehaviour(None, self.doit, 'test')
        self.w.updateWorld(1000)
        #
        self.assertEqual((self.w, None, 1000), self.state.get('done', 'doit was not called'))
        
    def testCanRemoveBehaviour(self):
        """testCanRemoveBehaviour: should be able to remove a behaviour from an actor"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        self.b.removeBehaviour(bb)
        self.w.updateWorld(1000)
        #
        self.assert_('done' not in self.state)

    def testCanRemoveBehaviourByName(self):
        """testCanRemoveBehaviourByName: should be able to remove a behaviour by name"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        self.b.removeBehaviourByName(a, 'test')
        self.w.updateWorld(1000)
        #
        self.assert_('done' not in self.state)
        
    def testCanRemoveAllBehavioursByName(self):
        """testCanRemoveAllBehavioursByName: should be able to remove behaviours for all actors based on name"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        self.b.removeBehavioursByName('test')
        self.w.updateWorld(1000)
        #
        self.assert_('done' not in self.state)
       
    def testCanPauseBehaviour(self):
        """testCanPauseBehaviour: should be able to pause a behaviour"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        bb.pause()
        self.w.updateWorld(1000)
        #
        self.assert_('done' not in self.state)
        bb.restart()
        self.w.updateWorld(1000)
        self.assertEqual((self.w, a, 1000), self.state.get('done', 'doit was not called'))
        
    def testFailDuplicateBehaviour(self):
        """testFailDuplicateBehaviour: should fail if the same behaviour is added twice"""
        #
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        self.b.assignBehaviour(a, self.doit, 'test')
        self.assertRaises(serge.blocks.behaviours.DuplicateBehaviour, self.b.assignBehaviour, a, self.doit, 'test')
        
    def testFailRemovingMissingBehaviour(self):
        """testFailRemovingMissingBehaviour: should fail when removing a behaviour that is missing"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        self.b.removeBehaviour(bb)
        self.assertRaises(serge.blocks.behaviours.MissingBehaviour, self.b.removeBehaviour, bb)

    def testFailRemoveMissingBehaviourByName(self):
        """testFailRemoveMissingBehaviourByName: should fail when removing a behaviour by name when it is missing"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        self.b.removeBehaviourByName(a, 'test')
        self.assertRaises(serge.blocks.behaviours.MissingBehaviour, self.b.removeBehaviourByName, a, 'test')
        
    def testFailPausingAlreadyPauses(self):
        """testFailPausingAlreadyPauses: should fail if pausing something that is paused"""
        def doit(world, actor, interval):
            self.state['done'] = (world, actor, interval)
        #
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        bb.pause()
        self.assertRaises(serge.blocks.behaviours.BehaviourAlreadyPaused, bb.pause)
        
    def testFailRestartingSomethingNotPauses(self):
        """testFailRestartingSomethingNotPauses: should fail is restarting something that is not paused"""
        def doit(world, actor, interval):
            self.state['done'] = (world, actor, interval)
        #
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '')
        bb = self.b.assignBehaviour(a, self.doit, 'test')
        self.assertRaises(serge.blocks.behaviours.BehaviourNotPaused, bb.restart)

    def testBehaviourIsRemovedWhenActorIsRemoved(self):
        """testBehaviourIsRemovedWhenActorIsRemoved: actor removal from world removes the behaviour"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (1,1))
        x = self.b.assignBehaviour(a, serge.blocks.behaviours.MoveTowardsPoint((10,10), x_speed=4, y_speed=2), 'test')
        #
        self.w.updateWorld(1000)
        self.assertTrue(self.b.hasBehaviour(x))
        #
        self.w.removeActor(a)
        self.w.updateWorld(1000)
        self.assertFalse(self.b.hasBehaviour(x))
        
    
    ### Some specific behaviours ###

    def testCanMoveTowardsPoint(self):
        """testCanMoveTowardsPoint: should be able to move towards a point"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (1,1))
        self.b.assignBehaviour(a, serge.blocks.behaviours.MoveTowardsPoint((10,10), x_speed=4, y_speed=2), 'test')
        #
        self.w.updateWorld(1000)
        self.assertEqual((5,3), (a.x, a.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((9,5), (a.x, a.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((10,7), (a.x, a.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((10, 9), (a.x, a.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((10,10), (a.x, a.y))
    
    def testCanMoveTowards(self):
        """testCanMoveTowards: should be able to move towards"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (1,1))
        b = serge.blocks.utils.addVisualActorToWorld(self.w, 'b', 'b', self.v, '', (10,10))
        self.b.assignBehaviour(a, serge.blocks.behaviours.MoveTowardsActor(b, x_speed=4, y_speed=2), 'test')
        #
        self.w.updateWorld(1000)
        self.assertEqual((5,3), (a.x, a.y))
        self.assertEqual((10,10), (b.x, b.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((9,5), (a.x, a.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((10,7), (a.x, a.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((10, 9), (a.x, a.y))
        #        
        self.w.updateWorld(1000)
        self.assertEqual((10,10), (a.x, a.y))

    def testCanAvoid(self):
        """testCanAvoid: should be able to avoid another actor"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        b = serge.blocks.utils.addVisualActorToWorld(self.w, 'b', 'b', self.v, '', (10,10))
        self.b.assignBehaviour(a, serge.blocks.behaviours.AvoidActor(b, x_speed=4, y_speed=2, distance=15), 'test')
        #
        # Moves away in the y-direction
        self.w.updateWorld(1000)
        self.assertEqual((10,-2), (a.x, a.y))
        self.assertEqual((10,10), (b.x, b.y))
        #
        self.w.updateWorld(1000)
        self.assertEqual((10,-4), (a.x, a.y))
        #
        self.w.updateWorld(1000)
        self.assertEqual((10,-6), (a.x, a.y))
        #
        self.w.updateWorld(1000)
        self.assertEqual((10,-6), (a.x, a.y))
        #
        # Reset location and then move away in the x-direction
        a.x = 0 
        a.y = 10
        #
        self.w.updateWorld(1000)
        self.assertEqual((-4,10), (a.x, a.y))
        #
        self.w.updateWorld(1000)
        self.assertEqual((-8,10), (a.x, a.y))
        #
        self.w.updateWorld(1000)
        self.assertEqual((-8,10), (a.x, a.y))

    def testCanHaveOptionalBehaviour(self):
        """testCanHaveOptionalBehaviour: should be able to have an optional behaviour"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        #
        choice = serge.blocks.behaviours.Optional(
            self.doit, a, lambda actor: actor.x == 0
        )
        self.b.assignBehaviour(a, choice, 'test')
        self.assert_('done' not in self.state)
        #
        a.x = 1
        self.w.updateWorld(1000)
        self.assert_('done' not in self.state)
        #
        a.x = 0
        self.w.updateWorld(1000)
        self.assertEqual((self.w, a, 1000), self.state.get('done', 'doit was not called'))

    def testCanSelectBehaviour(self):
        """testCanSelectBehaviour: should be able to select one behaviour or another"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        #
        choice = serge.blocks.behaviours.TwoOptions(
            self.doit, self.doit2, a, lambda actor: actor.x == 0
        )
        self.b.assignBehaviour(a, choice, 'test')
        self.assert_('done' not in self.state)
        self.assert_('done2' not in self.state)
        #
        a.x = 0
        self.w.updateWorld(1000)
        self.assertEqual((self.w, a, 1000), self.state.get('done', 'doit was not called'))
        self.assert_('done2' not in self.state)
        #
        del(self.state['done'])
        a.x = 1
        self.w.updateWorld(1000)
        self.assertEqual((self.w, a, 1000), self.state.get('done2', 'doit was not called'))
        self.assert_('done' not in self.state)


    def testCanHaveTimer(self):
        """testCanHaveTimer: should be able to use a timer"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        #
        choice = serge.blocks.behaviours.TimedCallback(2000, self.doit)
        self.b.assignBehaviour(a, choice, 'test')
        self.assert_('done' not in self.state)
        #
        self.w.updateWorld(1999)
        # On 1999 now - not fired
        self.assert_('done' not in self.state)
        # Now on 2001 - should fire
        self.w.updateWorld(2)
        self.assert_('done' in self.state)
        #
        del(self.state['done'])
        self.assert_('done' not in self.state)
        self.w.updateWorld(1998)
        # Now on 3999 - not firing again
        self.assert_('done' not in self.state)
        self.w.updateWorld(2)
        # Now on 4001 - should fire
        self.assert_('done' in self.state)
        
    def testCanHaveOneShotTimer(self):
        """testCanHaveOneShotTimer: should be able to use a one-shot timer"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        #
        choice = serge.blocks.behaviours.TimedOneshotCallback(2000, self.doit)
        self.b.assignBehaviour(a, choice, 'test')
        self.assert_('done' not in self.state)
        #
        self.w.updateWorld(1999)
        # On 1999 now - not fired
        self.assert_('done' not in self.state)
        # Now on 2001 - should fire
        self.w.updateWorld(2)
        self.assert_('done' in self.state)
        #
        del(self.state['done'])
        self.assert_('done' not in self.state)
        self.w.updateWorld(1998)
        # Now on 3999 - not firing again
        self.assert_('done' not in self.state)
        self.w.updateWorld(2)
        # Now on 4001 - should not fire
        self.assert_('done' not in self.state)
        
    def testKeyboardNSEWToVectorAttribute(self):
        """testKeyboardNSEWToVectorAttribute: can use keyboard to set an attribute on actor"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        self.e._keyboard = self.k
        self._direction = None
        self.b.assignBehaviour(a, serge.blocks.behaviours.KeyboardNSEWToVectorCallback(self._doDirection,
             serge.events.E_KEY_DOWN), 'keys')
        #
        # Without any keys the method should not be called
        self.w.updateWorld(1000)
        self.assertEqual(None, self._direction)
        #
        # With left should get west
        for k, d in ((pygame.K_LEFT, 'w'), (pygame.K_RIGHT, 'e'), (pygame.K_UP, 'n'), (pygame.K_DOWN, 's')):
            self.k.down_states[k] = True
            self.w.updateWorld(1000)
            self.assertEqual(serge.blocks.directions.getVectorFromCardinal(d), self._direction)
            self.k.down_states[k] = False

    def testUsingComplete(self):
        """testUsingComplete: should be able to use complete to stop something being called"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        x = self.b.assignBehaviour(a, OneOffBehaviour(), 'test')
        self.assertEqual(0, x._behaviour.done)
        self.w.updateWorld(1000)        
        self.assertEqual(1, x._behaviour.done)
        self.w.updateWorld(1000)        
        self.assertEqual(1, x._behaviour.done)
        
    def _doDirection(self, vector):
        """Callback for setting direction"""
        self._direction = vector

    def testParallaxBehaviour(self):
        """testParallaxBehaviour: should be able to use parallax behaviour"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,0))
        b = serge.blocks.utils.addVisualActorToWorld(self.w, 'b', 'b', self.v, '', (20,0))
        c = serge.blocks.utils.addVisualActorToWorld(self.w, 'c', 'c', self.v, '', (20,0))
        x = self.b.assignBehaviour(b, serge.blocks.behaviours.ParallaxMotion(a, (0.5, 0.0)), 'test')        
        y = self.b.assignBehaviour(c, serge.blocks.behaviours.ParallaxMotion(a, (0.0, 0.5)), 'test')        
        #
        self.assertEqual((10,0), (a.x, a.y))
        self.assertEqual((20,0), (b.x, b.y))
        self.assertEqual((20,0), (c.x, c.y))
        #
        a.moveTo(20, 10)
        self.w.updateWorld(1000)
        self.assertEqual((20,10), (a.x, a.y))
        self.assertEqual((25,0), (b.x, b.y))
        self.assertEqual((20,5), (c.x, c.y))
        
    def testCanRemoveActorWhenOutOfRange(self):
        """testCanRemoveActorWhenOutOfRange: should be able to remove an actor when it is out of range"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,20))
        x = self.b.assignBehaviour(a, serge.blocks.behaviours.RemoveWhenOutOfRange((0.0, 100.0), (10.0, 50.0)), 'test')
        #
        self.w.updateWorld(1000)
        self.assertTrue(self.w.hasActor(a)) 
        self.assertTrue(x.isRunning())   
        self.assertTrue(self.b.hasBehaviour(x))
        #
        a.moveTo(0.1, 10.1)
        self.w.updateWorld(1000)
        self.assertTrue(self.w.hasActor(a))    
        #
        a.moveTo(-1,10)
        self.w.updateWorld(1000)
        self.assertFalse(self.w.hasActor(a))    
        self.assertFalse(x.isRunning())
        self.assertFalse(self.b.hasBehaviour(x))    
        
    def testCanMoveWithConstantVelocity(self):
        """testCanMoveWithConstantVelocity: should be able to move an actor with a velocity"""
        a = serge.blocks.utils.addVisualActorToWorld(self.w, 'a', 'a', self.v, '', (10,20))
        x = self.b.assignBehaviour(a, serge.blocks.behaviours.ConstantVelocity(1.0, 2.0), 'test')
        #
        self.assertEqual((10,20), (a.x, a.y))
        self.w.updateWorld(1000)
        self.assertEqual((11,22), (a.x, a.y))
            
        
class OneOffBehaviour(serge.blocks.behaviours.Behaviour):
    """A behaviour that should happen once"""

    def __init__(self):
        """Intitialise"""
        super(OneOffBehaviour, self).__init__()
        self.done = 0
        
    def __call__(self, world, actor, interval):
        """Initialise the OneOffBehaviour"""
        self.done += 1
        return serge.blocks.behaviours.B_FINISHED
        

                
if __name__ == '__main__':
    unittest.main()
