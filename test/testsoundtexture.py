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
        self.a1 = serge.actor.Actor('a1', 'a1')
        self.a2 = serge.actor.Actor('a2', 'a2')
        self.a3 = serge.actor.Actor('a3', 'a3')
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
        
    def set_volume(self, volume):
        """Set our volume"""
        self.volume = volume
        
    def get_volume(self):
        """Return our volume"""
        return self.volume

    def play(self, loops=0):
        """Play the sound"""
        self.playing = True
        
    def pause(self):
        """Pause the sound"""
        self.playing = False

    stop = pause
    
if __name__ == '__main__':
    unittest.main()
