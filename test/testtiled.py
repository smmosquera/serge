"""Tests for the Tiled interface"""

import unittest
import os
import pygame

from helper import *

import serge.visual
import serge.registry
import serge.blocks.tiled

class TestTiled(unittest.TestCase):
    """Tests for the Tiled"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Sprites.clearItems()
        serge.blocks.tiled.Tiled.resetLayerTypes()
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanGetSprites(self):
        """testCanGetSprites: should be able to register sprites from a file"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        self.assertEqual(16, serge.visual.Sprites.getItem('tileset-2-1').width)
        self.assertEqual(16, serge.visual.Sprites.getItem('tileset-2-12').width)
        self.assertRaises(serge.registry.UnknownItem, serge.visual.Sprites.getItem, 'tileset-2-0')
        self.assertRaises(serge.registry.UnknownItem, serge.visual.Sprites.getItem, 'tileset-2-13')
    
    def testFailMissingFile(self):
        """testFailMissingFile: should fail when file is missing"""
        self.assertRaises(serge.blocks.tiled.BadTiledFile, 
            serge.blocks.tiled.Tiled, f('world-4.tmx.notthere'))
    
    def testMultipleFilesWithSameTilesetIsOk(self):
        """testMultipleFilesWithSameTilesetIsOk: should be able to register with multiple versions of tileset"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        t = serge.blocks.tiled.Tiled(f('world-4a.tmx'))

    def testMultipleTilesetsCanGetRightSprite(self):
        """testMultipleTilesetsCanGetRightSprite: should get the right sprite when multiple tilesets"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        l1, l2 = t.getLayers()
        self.assertEqual('tileset-2-2', l1.getSpriteFor((0, 0)).name)
        self.assertEqual('tileset-3-1', l2.getSpriteFor((2, 2)).name)

    def testCanCheckLayerType(self):
        """testCanCheckLayerType: should be able to check layer type"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        l1, l2 = t.getLayers()
        self.assertEqual('visual', l1.type)
        self.assertEqual('movement', l2.type)
        self.assertEqual(l1, t.getLayerByType('visual'))
        self.assertEqual(l2, t.getLayerByType('movement'))
        self.assertRaises(serge.blocks.tiled.NotFound, t.getLayerByType, 'thing')

    def testCanCheckLayerTypes(self):
        """testCanCheckLayerTypes: should be able to check layer types"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        l1, l2 = t.getLayers()
        self.assertEqual('visual', l1.type)
        self.assertEqual('movement', l2.type)
        self.assertEqual([l1], t.getLayersByType('visual'))
        self.assertEqual([l2], t.getLayersByType('movement'))
        self.assertEqual([], t.getLayersByType('thing'))
        
    def testFailBadLayerType(self):
        """testFailBadLayerType: should fail with a bad or missing layer type"""
        self.assertRaises(serge.blocks.tiled.BadLayer, 
            serge.blocks.tiled.Tiled, f('world-4-badtype.tmx'))
        self.assertRaises(serge.blocks.tiled.BadLayer, 
            serge.blocks.tiled.Tiled, f('world-4-missingtype.tmx'))

    def testCanAddLayerType(self):
        """testCanAddLayerType: should be able to add a layer type"""
        serge.blocks.tiled.Tiled.addLayerTypes(['badtype'])
        t = serge.blocks.tiled.Tiled(f('world-4-badtype.tmx'))
        
    def testCanGetTileLayer(self):
        """testCanGetTileLayer: should be able to get a tile layer"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        #
        self.assertEqual(2, len(t.getLayers()))
        l1, l2 = t.getLayers()
        #
        self.assertEqual('Tile Layer 1', l1.name)
        self.assertEqual('Tile Layer 2', l2.name)
        self.assertEqual((64, 48), l1.getSize())
        self.assertEqual((64, 48), l2.getSize())
        self.assertEqual(2, l1.tiles[0][0])
        self.assertEqual(13, l2.tiles[0][0])
        #
        # Some properties
        self.assertEqual(123, l1.test1)
        self.assertEqual(123, l1.properties['test1'])
        self.assertEqual(456, l2.test1)
        self.assertEqual('hello', l2.test2)
        self.assertRaises(AttributeError, getattr, l1, 'test2')
        
    def testCanGetObjectLayers(self):
        """testCanGetObjectLayers: should be able to get an object layer"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        #
        layers = t.getObjectLayers()
        self.assertEqual(3, len(layers))
        l1, l2, l3 = layers
        #
        # Properties
        self.assertEqual(True, l1.AllMissions)
        self.assertEqual(True, l2.Mission1a)
        self.assertEqual(True, l3.Mission1b)
        #
        # Objects
        self.assertEqual('All Missions', l1.name)
        self.assertEqual(4, len(l1.getObjects()))
        td = l1.getObject('TestDoor1')
        self.assertEqual('Door', td.object_type)
        self.assertEqual('world-5', td.leads_to)
        self.assertEqual('shop-west', td.location)
        self.assertEqual(round(41.125*16), td.x)
        self.assertEqual(round(25.250*16), td.y)
        self.assertEqual((round(0.688*16), round(3.562*16)), (td.width, td.height))
        #
        self.assertEqual('Mission1a', l2.name)
        tb = l2.getObject('Bob')
        self.assertEqual((0, 0), (tb.width, tb.height))

    def testCanDoSpritesOnObjectLayers(self):
        """testCanDoSpritesOnObjectLayers: should be able to do sprites on object layers"""
        t = serge.blocks.tiled.Tiled(f('world-5.tmx'))
        #
        layers = t.getLayersByType('adhoc-visual')
        self.assertEqual(1, len(layers))
        objects = layers[0].getObjects()
        self.assertEqual(6, len(objects))
        self.assertEqual('tileset-2-6', objects[0].sprite_name)
        
    
        
    def testFailGettingMissingObject(self):
        """testFailGettingMissingObject: should fail when getting mission object"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        #
        layers = t.getObjectLayers()
        l1, l2, l3 = layers
        self.assertRaises(serge.blocks.tiled.NotFound, l1.getObject, 'TestDoor1NotThere')                
    
    def testCanCheckWhichLayersATileIsSetOn(self):
        """testCanCheckWhichLayersATileIsSetOn: should be able to check which layers has a tile set on"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        self.assertEqual(['visual', 'movement'], [l.type for l in t.getLayersForTile((0, 0))])
        self.assertEqual(['visual'], [l.type for l in t.getLayersForTile((5, 4))])
        self.assertEqual(['visual', 'movement'], [l.type for l in t.getLayersForTile((37, 6))])
        
    def testCanCheckLayersExcludingSome(self):
        """testCanCheckLayersExcludingSome: should be able to check which layers are set with exclusions"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        self.assertEqual(['movement'], [l.type for l in t.getLayersForTile((0, 0), excluding=['visual'])])
        
    def testCanFindSetOn(self):
        """testCanFindSetOn: should be able to find the tiles that are set on a layer"""
        t = serge.blocks.tiled.Tiled(f('world-4.tmx'))
        #
        l = t.getLayer("Tile Layer 2")
        set_tiles = set(l.getLocationsWithTile())
        unset_tiles = set(l.getLocationsWithoutTile()) 
        #
        self.assertEqual(64*48, len(unset_tiles) + len(set_tiles))
        self.assertEqual(set(), unset_tiles.intersection(set_tiles))
        self.assertTrue(len(unset_tiles) > len(set_tiles))
        self.assertFalse(len(set_tiles) == 0)
        self.assertTrue((0,0) in set_tiles)
        self.assertTrue((35, 10) in set_tiles)
        self.assertFalse((14, 7) in set_tiles)
        
    def testCanGetPropertyBagArray(self):
        """testCanGetPropertyBagArray: should be able to get a property bag array"""
        t = serge.blocks.tiled.Tiled(f('world-5.tmx'))
        #
        array = t.getPropertyBagArray(
            sprite_layers=['visual'],
            boolean_layers=['movement', 'visibility'],
            property_layers=['resistance'])
        #
        a00 = array[0][0]
        self.assertEqual(False, a00.visibility)
        self.assertEqual(True, a00.movement)
        self.assertEqual(['tileset-2-2', 'tileset-3-9'], a00.sprites)
        self.assertFalse(hasattr(a00, 'resistance'))
        a12 = array[2][1]
        self.assertEqual(False, a12.visibility)
        self.assertEqual(False, a12.movement)
        self.assertEqual(['tileset-2-2', 'tileset-3-9'], a12.sprites)
        self.assertEqual(10, a12.resistance)
        a14 = array[4][1]
        self.assertEqual(['tileset-2-2'], a14.sprites)
        a54 = array[4][5]
        self.assertEqual(['tileset-2-1'], a54.sprites)
        self.assertEqual(30, a54.resistance)
        
    def testPropertyBagCanAcceptPrototype(self):
        """testPropertyBagCanAcceptPrototype: should be able to pass prototype for Bag"""
        t = serge.blocks.tiled.Tiled(f('world-5.tmx'))
        #
        default = serge.serialize.SerializedBag(resistance=0)
        array = t.getPropertyBagArray(
            sprite_layers=['visual'],
            boolean_layers=['movement', 'visibility'],
            property_layers=['resistance'],
            prototype=default)
        #
        a00 = array[0][0]
        self.assertEqual(0, a00.resistance)
        a12 = array[2][1]
        self.assertEqual(10, a12.resistance)
        a54 = array[4][5]
        self.assertEqual(30, a54.resistance)
        
    def testPropertyBagFailIfMissingLayer(self):
        """testPropertyBagFailIfMissingLayer: should fail on property bag when a layer is missing"""
        t = serge.blocks.tiled.Tiled(f('world-5.tmx'))
        #
        self.assertRaises(serge.blocks.tiled.NotFound, t.getPropertyBagArray,
            sprite_layers=['visual'],
            boolean_layers=['missing-layer-type', 'movement', 'visibility'],
            property_layers=['resistance'])
        
    def testPropertyBagCanHaveOptionalLayers(self):
        """testPropertyBagCanHaveOptionalLayers: should be able to use optional layers on the property bag"""
        t = serge.blocks.tiled.Tiled(f('world-5.tmx'))
        #
        array = t.getPropertyBagArray(
            sprite_layers=['visual'],
            boolean_layers=['missing_layer_type', 'movement', 'visibility'],
            property_layers=['resistance'],
            optional_layers=['missing_layer_type'])
        #
        self.assertFalse(array[0][0].missing_layer_type)
            
        
        

if __name__ == '__main__':
    unittest.main()
