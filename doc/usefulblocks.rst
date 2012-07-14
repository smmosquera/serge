Useful Building Blocks
======================

The serge engine is quite small and provides the core classes needed to construct a game. When building a game it is useful to also build upon some higher level pieces such as custom actor types, UI layouts and certain behaviours like responding to user input. This functionality is collected in the various *blocks* modules.

.. graphviz::

    digraph foo {
        pygame -> serge;
        serge -> blocks;
        blocks -> game;
        serge -> game;
        pygame -> game;
    }
    
.. toctree::

    blocks
