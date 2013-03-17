"""Tests for the animations"""

import unittest

import serge.engine
import serge.actor
import serge.zone
import serge.blocks.animations
import serge.blocks.actors

from helper import *


class TestAnimations(unittest.TestCase, VisualTester):
    """Tests for the Animations"""

    def setUp(self):
        """Set up the tests"""
        self.a = TestAnimatedActor('a', 'a')
        self.b = TestAnimatedActor('b', 'b')
        self.c = TestAnimatedActor('c', 'c')
        self.d = TestAnimatedActor('d', 'd')
        self.z = serge.zone.Zone()
        self.z.addActor(self.a)
        self.z.addActor(self.b)
        self.z.addActor(self.c)
        self.z.addActor(self.d)

    def tearDown(self):
        """Tear down the tests"""

    def _updateActors(self, interval):
        """Update all the actors"""

    def testCanAddAnimation(self):
        """testCanAddAnimation: should be able to add an animation"""
        self.a.addAnimation(TestAnimation(), 'cycle')
        self.z.updateZone(1000, None)
        self.z.updateZone(1000, None)
        self.assertEqual(2, self.a.iteration)

    def testCanAddMultipleAnimations(self):
        """testCanAddMultipleAnimations: should be able to add multiple animations"""
        self.a.addAnimation(TestAnimation(), 'cycle-1')
        self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.z.updateZone(1000, None)
        self.z.updateZone(1000, None)
        self.assertEqual(4, self.a.iteration)

    def testFailAddingAnimationWithSameName(self):
        """testFailAddingAnimationWithSameName: should fail if add animation with the same name"""
        self.a.addAnimation(TestAnimation(), 'cycle')
        self.assertRaises(serge.blocks.animations.AnimationExists,
                          self.a.addAnimation, TestAnimation(), 'cycle')

    def testCanRemoveAnimation(self):
        """testCanRemoveAnimation: should be able to remove an animation"""
        self.a.addAnimation(TestAnimation(), 'cycle')
        self.z.updateZone(1000, None)
        self.a.removeAnimation('cycle')
        self.z.updateZone(1000, None)
        self.assertEqual(1, self.a.iteration)

    def testCanRemoveAnimationByObject(self):
        """testCanRemoveAnimationByObject: should be able to remove an animation from the object"""
        animation = self.a.addAnimation(TestAnimation(), 'cycle')
        self.z.updateZone(1000, None)
        self.a.removeAnimation(animation.name)
        self.z.updateZone(1000, None)
        self.assertEqual(1, self.a.iteration)
    
    def testCanRemoveAnimationWithWildcard(self):
        """testCanRemoveAnimationWithWildcard: should be able to remove animations with wildcard"""
        self.a.addAnimation(TestAnimation(), 'cycle-1')
        self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.z.updateZone(1000, None)
        self.a.removeAnimationsMatching('cycle-*')
        self.z.updateZone(1000, None)
        self.assertEqual(2, self.a.iteration)

    def testFailRemoveAnAnimationNotThere(self):
        """testFailRemoveAnAnimationNotThere: should fail when removing an animation that isn't there"""
        self.assertRaises(serge.blocks.animations.AnimationNotFound,
                          self.a.removeAnimation, 'cycle')

    def testCanStopAnimations(self):
        """testCanStopAnimations: should be able to stop all animations"""
        self.a.addAnimation(TestAnimation(), 'cycle-1')
        self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.a.pauseAnimations()
        self.z.updateZone(1000, None)
        self.assertEqual(0, self.a.iteration)
        self.assertTrue(self.a.animationsPaused())

    def testFailStartStopWhenNotInRightMode(self):
        """testFailStartStopWhenNotInRightMode: should fail when stopping or starting in the wrong mode"""
        self.a.addAnimation(TestAnimation(), 'cycle-1')
        self.assertRaises(serge.blocks.animations.NotPaused, self.a.unpauseAnimations)
        self.a.pauseAnimations()
        self.assertRaises(serge.blocks.animations.AlreadyPaused, self.a.pauseAnimations)

    def testSafeStartStopWhenNotInRightMode(self):
        """testSafeStartStopWhenNotInRightMode: can do safe when stopping or starting in the wrong mode"""
        self.a.addAnimation(TestAnimation(), 'cycle-1')
        self.a.unpauseAnimations(safe=True)
        self.a.pauseAnimations(safe=True)
        self.z.updateZone(1000, None)
        self.assertEqual(0, self.a.iteration)

    def testCanStartAnimations(self):
        """testCanStartAnimations: should be able to restart all animations"""
        self.a.addAnimation(TestAnimation(), 'cycle-1')
        self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.a.pauseAnimations()
        self.a.unpauseAnimations()
        self.z.updateZone(1000, None)
        self.assertEqual(2, self.a.iteration)
        self.assertFalse(self.a.animationsPaused())

    def testCanCreatePaused(self):
        """testCanCreatePaused: should be able to create an animation in paused state"""
        a = TestAnimation(paused=True)
        self.assertTrue(a.paused)
        a = TestAnimation(paused=False)
        self.assertFalse(a.paused)
        a = TestAnimation()
        self.assertFalse(a.paused)

    def testCanRestartAllAnimations(self):
        """testCanRestartAllAnimations: should be able to restart all animations"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        c2 = self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.z.updateZone(1000, None)
        self.assertEqual(1, c1.iteration)
        self.assertEqual(1, c2.iteration)
        #
        self.a.restartAnimations()
        self.assertEqual(0, c1.iteration)
        self.assertEqual(0, c2.iteration)

    def testRestartUnpause(self):
        """testRestartUnpause: restarting animations will unpause them"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        c2 = self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.a.pauseAnimations()
        self.a.restartAnimations()
        self.z.updateZone(1000, None)
        self.assertEqual(1, c1.iteration)
        self.assertEqual(1, c2.iteration)

    def testRestartWillCallUpdate(self):
        """testRestartWillCallUpdate: restarting will call an update"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        self.assertEqual(0, c1.iteration)
        self.assertEqual(0, self.a.iteration)
        self.a.restartAnimations()
        self.assertEqual(0, c1.iteration)
        self.assertEqual(1, self.a.iteration)

    def testCanCompleteAnimations(self):
        """testCanCompleteAnimations: should be able to complete the animations"""
        c1 = self.a.addAnimation(TestAnimation(1000), 'cycle-1')
        self.a.completeAnimations()
        self.assertEqual(1000, c1.current)
        self.assertEqual(1, self.a.iteration)

    def testCanGetAnimation(self):
        """testCanGetAnimation: should be able to get an animation"""
        animation = self.a.addAnimation(TestAnimation(), 'cycle')
        self.assertEqual(animation, self.a.getAnimation('cycle'))

    def testFailGetAnimationNotThere(self):
        """testFailGetAnimationNotThere: should fail when getting an animation that isn't there"""
        self.assertRaises(serge.blocks.animations.AnimationNotFound, self.a.getAnimation, 'cycle')

    def testCanClearAnimations(self):
        """testCanClearAnimations: should be able to clear all animations"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        c2 = self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.a.removeAnimations()
        self.assertSetEqual(set(), set(self.a.getAnimations()))

    def testCanGetAnimations(self):
        """testCanGetAnimations: should be able to get all animations"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        c2 = self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.assertSetEqual({c1, c2}, set(self.a.getAnimations()))

    def testStopIndividualAnimation(self):
        """testStopIndividualAnimation: should be able to stop an individual animation"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        c2 = self.a.addAnimation(TestAnimation(), 'cycle-2')
        c2.pause()
        self.z.updateZone(1000, None)
        self.assertEqual(1, self.a.iteration)
        self.assertFalse(self.a.animationsPaused())

    def testStartIndividualAnimation(self):
        """testStartIndividualAnimation: should be able to start an individual animation"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        c2 = self.a.addAnimation(TestAnimation(), 'cycle-2')
        c2.pause()
        c2.unpause()
        self.z.updateZone(1000, None)
        self.assertEqual(2, self.a.iteration)
        self.assertFalse(self.a.animationsPaused())

    def testRestartIndividualAnimation(self):
        """testRestartIndividualAnimation: should be able to restart an individual animation"""
        c1 = self.a.addAnimation(TestAnimation(), 'cycle-1')
        c2 = self.a.addAnimation(TestAnimation(), 'cycle-2')
        self.z.updateZone(1000, None)
        self.assertEqual(1, c1.iteration)
        self.assertEqual(1, c2.iteration)
        #
        c1.restart()
        #
        self.assertEqual(0, c1.iteration)
        self.assertEqual(1, c2.iteration)

    def testPropertiesOfAnimation(self):
        """testPropertiesOfAnimation: properties of animation should advance"""
        c1 = self.a.addAnimation(TestAnimation(10000), 'cycle-1')
        self.assertEqual(0, c1.iteration)
        self.assertEqual(0, c1.current)
        self.assertEqual(0, c1.fraction)
        #
        self.z.updateZone(1000, None)
        #
        self.assertEqual(1, c1.iteration)
        self.assertEqual(1000, c1.current)
        self.assertEqual(0.1, c1.fraction)
        #
        self.z.updateZone(4000, None)
        #
        self.assertEqual(2, c1.iteration)
        self.assertEqual(5000, c1.current)
        self.assertEqual(0.5, c1.fraction)

    def testPropertiesBounded(self):
        """testPropertiesBounded: properties of animation should be bounded"""
        c1 = self.a.addAnimation(TestAnimation(10000), 'cycle-1')
        self.assertEqual(0, c1.iteration)
        self.assertEqual(0, c1.current)
        self.assertEqual(0, c1.fraction)
        #
        self.z.updateZone(20000, None)
        #
        self.assertEqual(1, c1.iteration)
        self.assertEqual(10000, c1.current)
        self.assertEqual(1.0, c1.fraction)
        self.assertTrue(c1.complete)

    def testLoopAnimation(self):
        """testLoopAnimation: can loop an animation"""
        c1 = self.a.addAnimation(TestAnimation(10000, loop=True), 'cycle-1')
        self.assertEqual(0, c1.iteration)
        self.assertEqual(0, c1.current)
        self.assertEqual(0, c1.fraction)
        self.assertEqual(1, c1.direction)
        #
        self.z.updateZone(15000, None)
        #
        self.assertEqual(1, c1.iteration)
        self.assertEqual(5000, c1.current)
        self.assertEqual(0.5, c1.fraction)
        self.assertFalse(c1.complete)
        self.assertEqual(-1, c1.direction)

    def testCanPauseALoopingAnimationAtTheEndOfCycle(self):
        """testCanPauseALoopingAnimationAtTheEndOfCycle: should be able to pause an animation at end of cycle"""
        c1 = self.a.addAnimation(TestAnimation(10000, loop=True), 'cycle-1')
        #
        self.z.updateZone(5000, None)
        self.assertEqual(1, c1.iteration)
        self.assertEqual(5000, c1.current)
        self.assertEqual(0.5, c1.fraction)
        self.assertEqual(1, c1.direction)
        self.assertFalse(c1.paused)
        #
        c1.pauseAtNextCycle()
        #
        # Should now be paused
        self.z.updateZone(10000, None)
        self.z.updateZone(10000, None)
        self.assertEqual(0, c1.current)
        self.assertEqual(0, c1.fraction)
        self.assertEqual(1, c1.direction)
        self.assertTrue(c1.paused)
        #
        # Can unpause and continue
        c1.unpause()
        self.z.updateZone(10000, None)
        self.z.updateZone(10000, None)
        self.z.updateZone(2000, None)
        self.assertEqual(2000, c1.current)
        self.assertEqual(0.2, c1.fraction)
        self.assertEqual(1, c1.direction)
        self.assertFalse(c1.paused)

    def testCanUseRegistry(self):
        """testCanUseRegistry: should be able to use the animation registry"""
        base_animation = TestAnimation()
        serge.blocks.animations.Animations.registerItem('cycle-1', base_animation)
        serge.blocks.animations.Animations.registerItem('cycle-2', base_animation)
        an1 = self.a.addRegisteredAnimation('cycle-1')
        an2 = self.a.addRegisteredAnimation('cycle-2')
        an1.pause()
        self.z.updateZone(1000, None)
        self.assertEqual(1, self.a.iteration)
        self.assertFalse(self.a.animationsPaused())
        self.assertTrue(an1.paused)
        self.assertFalse(an2.paused)


class TestSpecificAnimations(unittest.TestCase, VisualTester):
    """Tests for the SpecificAnimations"""

    def setUp(self):
        """Set up the tests"""
        self.z = serge.zone.Zone()
        self.e = serge.engine.Engine()

    def tearDown(self):
        """Tear down the tests"""

    def testColourCycle(self):
        """testColourCycle: test of the colour cycling animation"""
        a = serge.blocks.actors.StringText('a', 'a', 'Test')
        self.z.addActor(a)
        #
        colour = serge.blocks.animations.ColourCycle(
            obj=a.visual,
            attribute='colour',
            start_colour=(0, 255, 0, 100),
            end_colour=(255, 0, 0, 200),
            duration=10000,
            loop=True
        )
        a.addAnimation(colour, 'colour-cycle')
        #
        self.z.updateZone(0, None)
        self.assertEqual((0, 255, 0, 100), a.visual.colour)
        self.z.updateZone(5000, None)
        self.assertEqual((255. / 2, 255. / 2, 0, 150), a.visual.colour)
        self.z.updateZone(5000, None)
        self.assertEqual((255, 0, 0, 200), a.visual.colour)
        self.z.updateZone(5000, None)
        self.assertEqual((255. / 2, 255. / 2, 0, 150), a.visual.colour)
        self.z.updateZone(5000, None)
        self.assertEqual((0, 255, 0, 100), a.visual.colour)
        self.z.updateZone(5000, None)
        self.assertEqual((255. / 2, 255. / 2, 0, 150), a.visual.colour)

    def testPulseZoom(self):
        """testPulseZoom: should be able to cycle the zoom"""
        a = serge.blocks.animations.AnimatedActor('a', 'a')
        self.z.addActor(a)
        #
        zoom = serge.blocks.animations.PulseZoom(
            0.8, 1.2, 5000, True
        )
        a.addAnimation(zoom, 'zoom-pulse')
        #
        self.z.updateZone(0, None)
        self.assertEqual(0.8, a.zoom)
        self.z.updateZone(2500, None)
        self.assertEqual(1.0, a.zoom)
        self.z.updateZone(2500, None)
        self.assertEqual(1.2, a.zoom)
        self.z.updateZone(5000, None)
        self.assertEqual(0.8, a.zoom)

    def testPulseWiggle(self):
        """testPulseWiggle: should be able to wiggle an actor"""
        a = serge.blocks.animations.AnimatedActor('a', 'a')
        self.z.addActor(a)
        #
        wiggle = serge.blocks.animations.PulseRotate(
            -45, 45, 5000, True
        )
        a.addAnimation(wiggle, 'wiggle')
        #
        # The rotation middle is the middle of the range so this is where it should start
        self.z.updateZone(0, None)
        self.assertAlmostEqual(0, a.getAngle())
        self.z.updateZone(2500, None)
        self.assertAlmostEqual(45, a.getAngle())
        self.z.updateZone(2500, None)
        self.assertAlmostEqual(0, a.getAngle())
        self.z.updateZone(2500, None)
        self.assertAlmostEqual(-45, a.getAngle())
        self.z.updateZone(2500, None)
        self.assertAlmostEqual(0, a.getAngle())


class TestAnimation(serge.blocks.animations.Animation):
    """A simple animation to help test"""

    def update(self):
        """Update the animation"""
        self.actor.iteration += 1


class TestAnimatedActor(serge.blocks.animations.AnimatedActor):
    """Test actor"""
    
    def __init__(self, tag, name):
        """Initialise the actor"""
        super(TestAnimatedActor, self).__init__(tag, name)
        #
        self.iteration = 0
        
        
if __name__ == '__main__':
    unittest.main()
