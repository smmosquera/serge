Engine Overview
===============

Serge is a game engine writen in Python on top of pygame.

.. graphviz::

    digraph foo {
        pygame -> serge;
        serge -> blocks;
        blocks -> game;
        serge -> game;
        pygame -> game;
    }
   
Typical game folder structure for a game.

.. graphviz::

    digraph foo {
        main -> game;
        main -> graphics;
        main -> fonts;
        main -> sounds;
        main -> music;
        main -> dist;
        main -> serge;
        serge -> blocks;
    }
    
Engine Structure.

.. graphviz::

    digraph foo {
        engine -> world [label="∞"];
        world -> zone [label="∞"];
        zone -> actor [label="∞"];
        actor -> visual [label="1"];
        engine -> renderer [label="1"];
        renderer -> layer [label="∞"];
        engine -> mouse [label="1"];
        engine -> keyboard [label="1"];
    }
    
Typical game flow.

.. actdiag::

    diagram {
        "create engine" -> "add layers" -> "add worlds" -> "add zones" -> "add actors" -> "add visuals";
        
        lane "Flow" {
            "create engine";
        }
    }
