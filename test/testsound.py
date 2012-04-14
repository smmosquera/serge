"""Tests for Sound"""

import unittest
import os
import pygame

import serge.sound
import serge.events

class TestSoundSystem(unittest.TestCase):
    """Tests for the SoundSystem"""

    def setUp(self):
        """Set up the tests"""
        self.s = serge.sound.Sounds
        self.m = serge.sound.Music
        self.s.clearItems()
        self.m.clearItems()
        self.m.setPath(os.path.join('test', 'sound'))
        self.s.unpause()
        self.m.unpause()
        serge.sound.SoundItem = TestSound
        serge.sound.MusicItem = TestMusic
        
    def tearDown(self):
        """Tear down the tests"""

    ### Basic control ###
    
    def testShouldBeAbleToCreate(self):
        """testShouldBeAbleToCreate: should be able to create a sound collection"""
        
    def testCanAddSound(self):
        """testCanAddSound: should be able to add a sound"""
        self.s.registerItem('test', '')
        self.assertEqual('sound', self.s.getItem('test').type)
    
    def testCanAddMusic(self):
        """testCanAddMusic: should be able to add music"""
        self.m.registerItem('test', 'sound.wav')
        self.assertEqual('music', self.m.getItem('test').type)
           
    def testCanFindASound(self):
        """testCanFindASound: should be able to find a sound"""
        self.s.registerItem('test1', 'test1')
        self.s.registerItem('test2', 'test2')
        self.assertEqual('test1', self.s.getItem('test1').name)
        self.assertEqual('test2', self.s.getItem('test2').name)
        
    def testCanPlaySound(self):
        """testCanPlaySound: should be able to play a sound"""
        self.s.registerItem('test1', 'test1')
        self.s.registerItem('test2', 'test2')
        self.s.play('test2')
        self.assertEqual(0, self.s.getItem('test1').played)
        self.assertEqual(1, self.s.getItem('test2').played)
        
    def testFailToFindSound(self):
        """testFailToFindSound: should fail if try to find a sound which isn't there"""
        self.assertRaises(serge.registry.UnknownItem, self.s.getItem, 'test1')
        
    def testFailToPlaySound(self):
        """testFailToPlaySound: should fail if try to play a sound which isn't there"""
        self.assertRaises(serge.registry.UnknownItem, self.s.play, 'test1')
        
    def testCanSerialize(self):
        """testCanSerialize: should be able to serialize the registry"""
        self.s.registerItem('test1', 'test1')
        self.s.registerItem('test2', 'test2')
        s = serge.serialize.Serializable.fromString(self.s.asString())
        self.assertEqual('test1', s.getItem('test1').name)
        self.assertEqual('test2', s.getItem('test2').name)

    ### Global control of sound ###
    
    def testCanPauseMusic(self):
        """testCanPauseMusic: should be able to pause music"""
        self.m.registerItem('test1', 'sound.wav')
        self.s.registerItem('test2', 'test2')
        self.m.pause()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(0, self.m.getItem('test1').played)
        self.assertEqual(1, self.s.getItem('test2').played)
        
    def testCanPauseSound(self):
        """testCanPauseSound: should be able to pause sound"""
        self.m.registerItem('test1', 'sound.wav')
        self.s.registerItem('test2', 'test2')
        self.s.pause()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(1, self.m.getItem('test1').played)
        self.assertEqual(0, self.s.getItem('test2').played)
        
    def testCanUnPauseMusic(self):
        """testCanUnPauseMusic: should be able to unpause music"""
        self.m.registerItem('test1', 'sound.wav')
        self.s.registerItem('test2', 'test2')
        self.m.pause()
        self.m.unpause()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(1, self.m.getItem('test1').played)
        self.assertEqual(1, self.s.getItem('test2').played)
        
    def testCanUnPauseSound(self):
        """testCanUnPauseSound: should be able to unpause sound"""
        self.m.registerItem('test1', 'sound.wav')
        self.s.registerItem('test2', 'test2')
        self.s.pause()
        self.s.unpause()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(1, self.m.getItem('test1').played)
        self.assertEqual(1, self.s.getItem('test2').played)
        
    def testCanToggleMusic(self):
        """testCanToggleMusic: should be able to toggle music"""
        self.m.registerItem('test1', 'sound.wav')
        self.s.registerItem('test2', 'test2')
        self.m.toggle()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(0, self.m.getItem('test1').played)
        self.assertEqual(1, self.s.getItem('test2').played)
        #
        self.m.toggle()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(1, self.m.getItem('test1').played)
        self.assertEqual(2, self.s.getItem('test2').played)
               
    def testCanToggleSound(self):
        """testCanToggleSound: should be able to toggle sound"""
        self.m.registerItem('test1', 'sound.wav')
        self.s.registerItem('test2', 'test2')
        self.s.toggle()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(1, self.m.getItem('test1').played)
        self.assertEqual(0, self.s.getItem('test2').played)
        #
        self.s.toggle()
        self.m.getItem('test1').play()
        self.s.getItem('test2').play()
        self.assertEqual(2, self.m.getItem('test1').played)
        self.assertEqual(1, self.s.getItem('test2').played)
    
    def testCanGetEventOnTrackStopping(self):
        """testCanGetEventOnTrackStopping: should be able to have a callback for track stopping"""
        self.m.registerItem('test1', 'sound.wav')
        #
        # The callback
        def doit(obj, arg):
            self._done = obj, arg
        #
        self._done = None
        serge.sound.Music.linkEvent(serge.events.E_TRACK_ENDED, doit)
        self.m.getItem('test1').play()
        self.m.isPlaying = lambda : True
        serge.sound.Music.update(1)
        #
        self.assertEqual(None, self._done)
        self.m.isPlaying = lambda : False
        serge.sound.Music.update(1)
        self.assertNotEqual(None, self._done)
        
        
        
        
        

class TestSound(serge.sound.SoundItem):
    """Sound"""
    
    type = 'sound'

    def __init__(self, name):
        """Initialise the TestSound"""
        super(TestSound, self).__init__(name)
        self.played = 0
        self.name = name
        
    def play(self, loops=0):
        """Play the sound"""
        if super(TestSound, self).play() == True:
            self.played += 1

class TestMusic(serge.sound.MusicItem):
    """Music"""
    
    type = 'music'

    def __init__(self, path):
        """Initialise the TestSound"""
        super(TestMusic, self).__init__(path)
        self.played = 0
        
    def play(self, loops=0):
        """Play the sound"""
        if super(TestMusic, self).play() == True:
            self.played += 1
    
if __name__ == '__main__':
    unittest.main()
