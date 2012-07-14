The Serge engine.





What's New
==========

0.2.3
    New SurfaceDrawing class in serge.visual - helps with creating custom visual elements
    New attribute "update_angle" causes physics engine angles to propagate to the actor when set to True (default=False)
    Fixed bug in block.visual.Circle and CircleText where it was drawn at the incorrect location
    Added parameter visual_size to PhysicalConditions which causes size to match the actor's visual size
    Added block for implementing behaviours
    Added Font handling
    Added Global Sound and Music handling
    Added ability to specify a stroke width and colour for rectangle and circle blocks
    Added Mountable actors
    Added ActorCollections
    Added Music Playlists
0.2.4
    Adding actor to composite actors is ok if the actor is already in the world    
    Removing child from composite actor can leave in the world
    Added global event broadcasting system
    Added fadeout for music
    Added scheduled actor removal from the world
    Added visible property for actors
    Behaviours can now return B_COMPLETE to pause themselves
    Theme can now be updated from a string
    Added ProgressBar visualblock
    Added ParallaxMotion behaviour
0.2.5
    Added Screenshot behaviour
    Behavior manager can now register all events in a module
    Can register multiple sprites from single tileset
    Transparency works properly now for Rectangles and Circles
    Fixed bug with size of actor not updating after zooming
    Sprites can be registered by file pattern 
    Rotations now use filtering for improved quality
    Added MovieMaker util to help recording gameplay
    Support rotation of Mounted Actors without pymunk
0.2.6
    Added MuteButton and utility to add to many worlds
    Added ability to clear actors with a tag from a world
    Added ToggledMenu block
    Fixed bug in SimpleVecs when you change a vector length
    Incorporated pymunk vec2d implementation
0.3
    Significantly extended the game created by the createGame utility. Includes help, credits and start screens
    Added block to track and report achievements
0.3.1
    Simplified template game with new text utilities
    Implemented conversation system
    Fixed issues with camera system
    Added block to interface to Tiled files
    Added block to darken a surface
0.3.2
    Added setSize method to directly set the size of a drawing
    Added a block for animate and then die actors
0.3.3
    Added a parameter in common to set the number of pygame audio channels to use
    Added behaviour to remove an actor when it is out of range
    Added behaviour to move an actor with a constant velocity
0.3.4
    Added duplicateItem method to registry to allow creation of aliased items
    Implemented a dragndrop block to help with drag and drop operations
    Added a finite state machine block
    forEach iteration can now work with setting attributes as well as method calls
    Added a spring towards point behaviour
    Added a behaviour sequence to control behaviours that run in sequences
    Generalized the tiled block to allow it to be used for general tile maps
    Implemented a block to help with fractal lines and shapes
    Implemented a block to help with running time intensive operations asynchronously 
    The number of physics steps used by pymunk can now be configured
    Fixed issue with animated sprites not advancing properly if the framerate of the animation was high
0.3.5
    Zones can now implement wouldContain to select actors based on certain criteria
    Improved text entry widget
    Keyboard now includes additional methods to help deal with entering text
    Added an L-system block to be used to generate plants, vegetation etc
0.4 
    First stand-alone release of the engine
    Includes documentation and two tutorials
    
