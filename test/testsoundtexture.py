"""Tests for SoundTexture items"""

import unittest
import os
import pygame
import math
import time

from helper import *

import serge.sound
import serge.actor
import serge.blocks.sounds

class TestSoundTexture(unittest.TestCase):
    """Tests for the SoundTexture"""

    def setUp(self):
        """Set up the tests"""
        self.a1 = serge.actor.Actor('a', 'a1')
        self.a2 = serge.actor.Actor('a', 'a2')
        self.a3 = serge.actor.Actor('b', 'a3')
        self.w = serge.world.World('one')
        self.z = serge.zone.Zone()
        self.w.addZone(self.z)
        self.z.active = True
        self.w.addActor(self.a1)
        self.w.addActor(self.a2)
        self.w.addActor(self.a3)
        #
        self.t = serge.blocks.sounds.SoundTexture('s', 's')
        #
        self.s1 = DummySound()
        self.s2 = DummySound()
        self.s3 = DummySound()
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanAddAmbientSounds(self):
        """testCanAddAmbientSounds: should be able to add ambient sounds"""
        self.t.addAmbientSound(self.s1)
        self.t.addAmbientSound(self.s2)
        self.assertEqual([self.s1, self.s2], [s._sound for s in self.t.getSounds()])
        
    def testCanPauseAll(self):
        """testCanPauseAll: should be able to pause all"""
        self.t.addAmbientSound(self.s1)
        self.t.addAmbientSound(self.s2)
        self.assertEqual([False, False], [s.playing for s in [self.s1, self.s2]])
        self.t.play()
        self.assertNotEqual([False, False], [s.playing for s in [self.s1, self.s2]])
        self.t.pause()
        self.assertEqual([False, False], [s.playing for s in [self.s1, self.s2]])

    def testCanStopAll(self):
        """testCanStopAll: should be able to stop all"""
        self.t.addAmbientSound(self.s1)
        self.t.addAmbientSound(self.s2)
        self.assertEqual([False, False], [s.playing for s in [self.s1, self.s2]])
        self.t.play()
        self.assertNotEqual([False, False], [s.playing for s in [self.s1, self.s2]])
        self.t.stop()
        self.assertEqual([False, False], [s.playing for s in [self.s1, self.s2]])

    def testCanPlayAll(self):
        """testCanPlayAll: should be able to play all"""
        self.t.addAmbientSound(self.s1)
        self.t.addAmbientSound(self.s2)
        self.assertEqual([False, False], [s.playing for s in [self.s1, self.s2]])
        self.t.play()
        self.assertEqual([True, True], [s.playing for s in [self.s1, self.s2]])
    
    def testCanSetMasterVolume(self):
        """testCanSetMasterVolume: should be able to set the master volume"""
        self.t.addAmbientSound(self.s1)
        self.t.addAmbientSound(self.s2)
        self.assertEqual([1,1], [s.get_volume() for s in [self.s1, self.s2]])
        self.t.set_volume(0.5)
        self.assertEqual([0.5, 0.5], [s.get_volume() for s in [self.s1, self.s2]])
        
    def testCanSetListener(self):
        """testCanSetListener: should be able to set the listener"""
        self.t.setListener(self.a1)
        
    def testCanGetListener(self):
        """testCanGetListener: should be able to get the listener"""
        self.t.setListener(self.a1)
        self.assertEqual(self.a1, self.t.getListener())
                
    def testCanAddPositionalSound(self):
        """testCanAddPositionalSound: should be able to add a positional sound"""
        x1 = serge.blocks.sounds.LocationalSound(self.s1, (100, 50), 50)
        self.t.addPositionalSound(x1)
        x = self.t.getSounds()
        self.assertEqual([x1], x)
        self.assertEqual((100,50), x[0].location)
        self.assertEqual(50, x[0].dropoff)

    def testFailIfPositionalUpdateAndNoListener(self):
        """testFailIfPositionalUpdateAndNoListener: should fail if do an updateActor and no listener set"""
        self.t.addAmbientSound(self.s1)
        self.t.updateActor(0, None)

    def testDontFailIfNoPositionalUpdateAndNoListener(self):
        """testDontFailIfNoPositionalUpdateAndNoListener: should not fail if no positional and do an updateActor and no listener set"""
        x1 = serge.blocks.sounds.LocationalSound(self.s1, (100, 50), 50)
        self.t.addPositionalSound(x1)
        #
        # If you don't set a listener with positional sounds then throw an error
        # No strictly necessary but it is confusing to debug when you do this and it
        # is almost certainly not what you want to do
        self.assertRaises(serge.blocks.sounds.NoListener, self.t.updateActor, 0, None)
            
    def testVolumeOfPositionalSoundAffectsVolume(self):
        """testVolumeOfPositionalSoundAffectsVolume: volume should be dependent on listener position"""
        x1 = serge.blocks.sounds.LocationalSound(self.s1, (100, 50), 50)
        self.t.addPositionalSound(x1)
        self.t.setListener(self.a1)
        #
        # Move to edge of listening range
        self.a1.moveTo(100,100)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())
        #
        # Move to origin of range
        self.a1.moveTo(100,50)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
        #
        # Move to middle of range
        self.a1.moveTo(100,75)
        self.t.updateActor(0, None)
        self.assertEqual(0.5, x1.get_volume())
        
    def testMasterVolumeAffectsPositionalVolume(self):
        """testMasterVolumeAffectsPositionalVolume: master volume should also affect positional volume"""
        x1 = serge.blocks.sounds.LocationalSound(self.s1, (100, 50), 50)
        self.t.addPositionalSound(x1)
        self.t.setListener(self.a1)
        #
        # Move to middle of range
        self.a1.moveTo(100,75)
        self.t.updateActor(0, None)
        self.assertEqual(0.5, x1.get_volume())
        self.t.set_volume(0.5)        
        self.t.updateActor(0, None)
        self.assertEqual(0.25, x1.get_volume())
    
    def testCanMovePositionalSound(self):
        """testCanMovePositionalSound: should be able to move a positional sound"""
        x1 = serge.blocks.sounds.LocationalSound(self.s1, (100, 50), 50)
        self.t.addPositionalSound(x1)
        self.t.setListener(self.a1)
        #
        # Move to edge of listening range
        self.a1.moveTo(100,100)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())
        #
        x1.location = (100,100)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
    
    def testCanPositionSoundsOnActors(self):
        """testCanPositionSoundsOnActors: should be able to have sounds positioned on actors"""
        x1 = serge.blocks.sounds.ActorsWithTagSound(self.s1, self.w, 'a', 50)
        self.t.addPositionalSound(x1)
        self.t.setListener(self.a3)
        #
        self.a1.moveTo(100, 50)
        self.a2.moveTo(200,100)
        #
        # Move to edge of listening range
        self.a3.moveTo(50,50)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())
        self.a3.moveTo(300,100)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())
        #
        # Move to origin of listening range
        self.a3.moveTo(100,50)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
        self.a3.moveTo(200,100)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
        #
        # Move to middle of listening range
        self.a3.moveTo(150,75)
        self.t.updateActor(0, None)
        self.assertEqual(0.0, x1.get_volume())

    def testPositionSoundsOnActorsOnRemoval(self):
        """testPositionSoundsOnActorsOnRemoval: when removing actors with sounds the sound goes away"""
        x1 = serge.blocks.sounds.ActorsWithTagSound(self.s1, self.w, 'a', 50)
        self.t.addPositionalSound(x1)
        self.t.setListener(self.a3)
        #
        self.a1.moveTo(100, 50)
        self.a2.moveTo(200,100)
        #
        # Move to origin of listening range
        self.a3.moveTo(100,50)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
        self.a3.moveTo(200,100)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
        #
        self.w.removeActor(self.a1)        
        self.a3.moveTo(100,50)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())
        self.a3.moveTo(200,100)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
         
                
    def testCanHaveMultiplePositionalSounds(self):
        """testCanHaveMultiplePositionalSounds: should be able to associate multiple positional sounds with a single sound"""
        x1 = serge.blocks.sounds.LocationalSounds(self.s1, [(100, 50),(200,100)], 50)
        self.t.addPositionalSound(x1)
        x = self.t.getSounds()
        self.t.setListener(self.a1)
        #
        self.assertEqual([x1], x)
        self.assertEqual([(100,50), (200,100)], x[0].locations)
        self.assertEqual(50, x[0].dropoff)
        #
        # Move to edge of listening range
        self.a1.moveTo(50,50)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())
        self.a1.moveTo(300,100)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())
        #
        # Move to origin of listening range
        self.a1.moveTo(100,50)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
        self.a1.moveTo(200,100)
        self.t.updateActor(0, None)
        self.assertEqual(1, x1.get_volume())
        #
        # Move to middle of listening range
        self.a1.moveTo(150,75)
        self.t.updateActor(0, None)
        self.assertEqual(0.0, x1.get_volume())
        
    def testCanUsePositionalSoundDamping(self):
        """testCanUsePositionalSoundDamping: should be able to damp variations in sound change when doing positional"""
        self.t = serge.blocks.sounds.SoundTexture('s', 's', damping=0.5)
        x1 = serge.blocks.sounds.LocationalSound(self.s1, (100, 50), 50)
        self.t.addPositionalSound(x1)
        self.t.setListener(self.a1)
        #
        # Move to edge of listening range - should start at 0
        self.a1.moveTo(100,100)
        self.t.updateActor(100000, None)
        self.assertEqual(0, x1.get_volume())        
        #
        # Immediately move to full volume position, but should not change because of damping
        self.a1.moveTo(100,50)
        self.t.updateActor(0, None)
        self.assertEqual(0, x1.get_volume())        
        #
        # Now wait 1 second, should change by 50%
        self.t.updateActor(1000, None)
        self.assertEqual(0.5, x1.get_volume())        
        #
        # Now wait 1 second, should change by 50%
        self.t.updateActor(1000, None)
        self.assertEqual(0.75, x1.get_volume())        
        #
        # Now move out of range
        self.a1.moveTo(100,100)
        self.t.updateActor(0, None)
        self.assertEqual(0.75, x1.get_volume())        
        self.t.updateActor(100000, None)
        self.assertEqual(0, x1.get_volume())        

    def testCanUseRegionBased(self):
        """testCanUseRegionBased: should be able to use a region for sounds"""
        x1 = serge.blocks.sounds.RectangularRegionSound(self.s1, (51,41,23,33))
        self.t.addPositionalSound(x1)
        x = self.t.getSounds()
        self.t.setListener(self.a1)
        #
        # Out of range is zero
        for x, y in ((50,40), (50,40+35), (50+25,40+35), (50+25,40)):
            self.a1.moveTo(x, y)         
            self.t.updateActor(0, None)
            self.assertEqual(0, x1.get_volume())        
        #
        # In range should be full volume
        for x, y in ((51,41), (51,41+32), (51+21,41+32), (51+21,41)):
            self.a1.moveTo(x, y)         
            self.t.updateActor(0, None)
            self.assertEqual(1, x1.get_volume())        
            
    def testCanUseRandomSounds(self):
        """testCanUseRandomSounds: should be able to do random sounds"""
        self.t.addRandomSound(self.s1, 0)
        self.t.addRandomSound(self.s2, 1)
        self.t.addRandomSound(self.s3, .5)        
        #
        # Should play according to the probability
        self.t.play()
        for x in range(1000):
            self.t.updateActor(1000,None)
        self.assertEqual(0, self.s1._played)
        self.assertEqual(1000, self.s2._played)
        self.assertTrue(100 < self.s3._played < 900)
        
    def testRandomSoundsObeyPauseAndStop(self):
        """testRandomSoundsObeyPauseAndStop: using random sounds should still be able to use pause and play"""
        self.t.addRandomSound(self.s2, 1)
        #
        self.t.play()
        self.t.updateActor(1000,None)
        self.assertEqual(1, self.s2._played)
        #
        self.t.pause()
        self.t.updateActor(1000,None)
        self.assertEqual(1, self.s2._played)
        #
        self.t.play()
        self.t.updateActor(1000,None)
        self.assertEqual(2, self.s2._played)
        #
        self.t.stop()
        self.t.updateActor(1000,None)
        self.assertEqual(2, self.s2._played)
    
        
               
        
class LowLevelSound(object):
    """Mimics of pygame sound object"""
    
    stop = lambda s : None
    play = lambda s : None
    pause = lambda s : None

class DummySound(serge.sound.SoundItem):
    """A sound to use for testing"""

    def __init__(self):
        """Initialise the DummySound"""
        self.volume = 1.0
        self.playing = False
        self._sound = LowLevelSound()
        self._played = 0
        
    def set_volume(self, volume):
        """Set our volume"""
        self.volume = volume
        
    def get_volume(self):
        """Return our volume"""
        return self.volume

    def play(self, loops=0):
        """Play the sound"""
        self.playing = True
        self._played += 1
        
    def pause(self):
        """Pause the sound"""
        self.playing = False

    stop = pause
    
if __name__ == '__main__':
    unittest.main()
