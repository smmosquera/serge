.. seqdiag::

  diagram {
    game; engine; world; zone; actor;
    game -> engine [label="addWorld"];
    game <-- engine;
    game ->> world [label="addZone"];
    game <-- world;
    game ->> world [label="addActor"];
    world ->> actor [label="addedToWorld"];
    world <-- actor;
    world ->> zone [label="addActor"];
    world <-- zone;
    game <-- world;
    game ->> engine [label="run"];
    engine ->> world [label="updateWorld"];
    world ->> zone [label="updateZone"];
    zone ->> actor [label="updateActor"];
    zone <<-- actor;
    world <<-- zone;
    engine <<-- world;
    engine ->> world [label="renderTo"];
    world ->> actor [label="renderTo"];
    world <<-- actor;
    engine <<-- world;
  }
  
.. actdiag::

    diagram {
        "create engine" -> "add world" -> "add zone" -> "add actor";
        
        lane engine {
            "create engine";
        }
        lane world {
            "add world";
        }
    }
  
.. aafig::

    +----+
    | Hi |
    +----+
    
  
