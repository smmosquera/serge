"""Useful blocks for sounds"""

import math

import serge.sound
import serge.actor


class SoundTexture(serge.actor.Actor):
    """An actor that manages a number of sounds to create a texture
    
    The actor can control sounds that are produced either ambiently (everywhere)
    or at specific locations. For the sounds at specific locations the sounds
    will get louder as the listener gets closer to them.
    
    """

    def __init__(self, tag, name):
        """Initialise the SoundTexture"""
        super(SoundTexture, self).__init__(tag, name)
        #
        self.sounds = []
        self.listener = None
        self._master_volume = 1.0
        
    def setListener(self, listener):
        """Set the listener for the sounds
        
        The listener is an actor and the sounds play at a volume determined
        by the location of the listener relative to each sound.
        
        :param listener: an actor
        
        """
        self.listener = listener
        
    def getListener(self):
        """Return the listener"""
        return self.listener
        
    def addAmbientSound(self, sound):
        """Add an ambient sound to the texture
        
        An ambient sound plays at the same volume no matter where the listener
        is. Ambient sounds still get paused with the other sounds.
        
        """
        self.sounds.append(AmbientSound(sound))

    def addPositionalSound(self, sound):
        """Add a positional sound to the texture
        
        A position sound plays at one or more locations in space and its volume is dependent
        on the location of the listener.
        
        """
        self.sounds.append(sound)

    def getSounds(self):
        """Return all the sounds that we are controlling"""
        return self.sounds
   
    def set_volume(self, volume):
        """Set the master volume
        
        This affects the volume of all sounds. The target volume for a sound is multiplied
        by this master.
        
        :param volume: master volume setting (0=silent, 1=full volume)
        
        """
        self._master_volume = volume
        for sound in self.getSounds():
            sound.set_volume(volume)
       
    def get_volume(self):
        """Return the master value setting"""
        return self._master_volume
     
    def play(self, loops=0):
        """Play the sounds
        
        :param loops: number of times to loop the sounds (0=never, -1=for ever)
        
        """
        for sound in self.getSounds():
            sound.play(loops)
        
    def pause(self):
        """Pause the sounds"""
        for sound in self.getSounds():
            sound.pause()    
            
    def updateActor(self, interval, world):
        """Update the actor"""
        super(SoundTexture, self).updateActor(interval, world)
        #
        # Update the volume of all sounds
        if self.listener:
            for sound in self.getSounds():
                volume = sound.get_scaled_volume((self.listener.x, self.listener.y))
                sound.set_volume(volume*self._master_volume)
                    


class AmbientSound(serge.sound.SoundItem):
    """A sound located everywhere in space"""
    
    def __init__(self, sound):
        """Initialise the sound"""
        super(AmbientSound, self).__init__(sound=sound)
        
    def get_scaled_volume(self, listener_position, master_volume):
        """Return the sound volume according to the listener position"""
        return 1.0
               
        
class LocationalSound(AmbientSound):
    """A sound that is located somewhere in space"""
    
    def __init__(self, sound, location, dropoff):
        """Initialise the sound"""
        super(LocationalSound, self).__init__(sound)
        #
        self.location = location
        self.dropoff = dropoff
        
    def get_scaled_volume(self, listener_position):
        """Update the sound volume according to the listener position"""
        dist = math.sqrt((listener_position[0]-self.location[0])**2 +(listener_position[1]-self.location[1])**2)
        return max(0.0, 1.0-dist/self.dropoff)
       

class LocationalSounds(AmbientSound):
    """A series of sounds that are located at a number of places in space but generate only a single sound"""
    
    def __init__(self, sound, locations, dropoff):
        """Initialise the sound"""
        super(LocationalSounds, self).__init__(sound)
        #
        self.locations = locations
        self.dropoff = dropoff
        
    def get_scaled_volume(self, listener_position):
        """Update the sound volume according to the listener position"""
        total = 0.0
        for location in self.locations:
            dist = math.sqrt((listener_position[0]-location[0])**2 +(listener_position[1]-location[1])**2)
            total += max(0.0, 1.0-dist/self.dropoff)
        return min(1.0, total)
       
        
