"""Tests for Geometry stuff"""

import unittest

import serge.geometry
import serge.actor
import serge.blocks.visualblocks

class TestGeometry(unittest.TestCase):
    """Tests for the Geometry"""

    def setUp(self):
        """Set up the tests"""
        
        
    def tearDown(self):
        """Tear down the tests"""

    ### Spatial object ###
    
    def testCreateFromRect(self):
        """testCreateFromRect: should be able to create from rect"""
        s = serge.geometry.Rectangle(10, 20, 30, 40)
        for x in range(10, 40):
            for y in range(20, 60):
                p1 = serge.geometry.Point(x, y)
                self.assertEqual(True, p1.isInside(s))
        for x in [9, 41]:
            for y in [19, 61]:
                p1 = serge.geometry.Point(x, y)
                self.assertEqual(False, p1.isInside(s))
        
    def testCreateFromCenter(self):
        """testCreateFromCenter: should be able to create from center"""
        s = serge.geometry.Rectangle.fromCenter(10, 20, 10, 10)
        for x in range(5, 15):
            for y in range(15, 25):
                p1 = serge.geometry.Point(x, y)
                self.assertEqual(True, p1.isInside(s))
        for x in [4, 16]:
            for y in [14, 26]:
                p1 = serge.geometry.Point(x, y)
                self.assertEqual(False, p1.isInside(s))

    def testCanOverlap(self):
        """testCanOverlap: can determine overlaps"""
        s = serge.geometry.Rectangle.fromCenter(10, 20, 10, 10)
        for x in range(5, 15):
            for y in range(15, 25):
                p1 = serge.geometry.Rectangle(x, y, 3, 3)
                self.assertEqual(True, p1.isOverlapping(s))
        for x in [2, 16]:
            for y in [12, 26]:
                p1 = serge.geometry.Rectangle(x, y, 3, 3)
                self.assertEqual(False, p1.isOverlapping(s))
        
    def testIsInsidePoint(self):
        """testIsInsidePoint: if try is inside for point should get false"""
        s = serge.geometry.Rectangle.fromCenter(10, 20, 10, 10)
        for x in range(5, 15):
            for y in range(15, 25):
                p1 = serge.geometry.Point(x, y)
                self.assertEqual(False, s.isInside(p1))
        for x in [4, 16]:
            for y in [14, 26]:
                p1 = serge.geometry.Point(x, y)
                self.assertEqual(False, s.isInside(p1))
        
    def testIsOverlappingPoint(self):
        """testIsOverlappingPoint: overlapping for point should workd"""
        s = serge.geometry.Rectangle.fromCenter(10, 20, 10, 10)
        for x in range(5, 15):
            for y in range(15, 25):
                p1 = serge.geometry.Rectangle(x, y, 3, 3)
                self.assertEqual(True, s.isOverlapping(p1))
        for x in [2, 16]:
            for y in [12, 26]:
                p1 = serge.geometry.Rectangle(x, y, 3, 3)
                self.assertEqual(False, s.isOverlapping(p1))

    def testCanFindArea(self):
        """testCanFindArea: should be able to find the area"""
        s = serge.geometry.Rectangle.fromCenter(10, 20, 5, 5)
        self.assertEqual(25, s.getArea())        
    
    def testCanFindAreaPoint(self):
        """testCanFindAreaPoint: should be able to find the area of a point"""
        s = serge.geometry.Point(10, 20)
        self.assert_(s.getArea() < 1e-5)        
    

    ### Spatial bits ###
                    
    def testCanSetSpatial(self):
        """testCanSetSpatial: should be able to set spatial coords"""
        a = serge.geometry.Rectangle()
        a.setSpatial(50, 50, 5, 5)

    def testCanSetSpatialWithoutSize(self):
        """testCanSetSpatialWithoutSize: should be able to set spatial without size"""
        a = serge.geometry.Rectangle()
        a.setSpatial(50, 50, 5, 5)
        a.setOrigin(60, 65)
        self.assertEqual([60, 65, 5, 5], list(a.getSpatial()))
        
    def testCanGetSpatial(self):
        """testCanGetSpatial: should be able to get spatial coords"""
        a = serge.geometry.Rectangle()
        a.setSpatial(50, 60, 5, 6)
        x, y, w, h = a.getSpatial()
        self.assertEqual(50, x)
        self.assertEqual(60, y)
        self.assertEqual(5, w)
        self.assertEqual(6, h)

    def testCanGetSpatialCentered(self):
        """testCanGetSpatialCentered: should be able to get spatial coords by the center"""
        a = serge.geometry.Rectangle()
        a.setSpatialCentered(50, 60, 5, 6)
        x, y, w, h = a.getSpatialCentered()
        self.assertEqual(50, x)
        self.assertEqual(60, y)
        self.assertEqual(5, w)
        self.assertEqual(6, h)

    def testCanGetInterchangeCentered(self):
        """testCanGetInterchangeCentered: should be able to interchange centered and non centered"""
        a = serge.geometry.Rectangle()
        a.setSpatialCentered(50, 60, 10, 20)
        x, y, w, h = a.getSpatial()
        self.assertEqual(45, x)
        self.assertEqual(50, y)
        self.assertEqual(10, w)
        self.assertEqual(20, h)

    def testCanMove(self):
        """testCanMove: should be able to move the actor"""
        a = serge.geometry.Rectangle()
        a.setSpatial(50, 60, 5, 6)
        a.move(1, -1)        
        x, y, w, h = a.getSpatial()
        self.assertEqual(51, x)
        self.assertEqual(59, y)
        self.assertEqual(5, w)
        self.assertEqual(6, h)

    def testCanResize(self):
        """testCanResize: should be able to resize"""
        a = serge.geometry.Rectangle()
        a.setSpatial(50, 60, 6, 8)
        a.resizeBy(2, 4)        
        x, y, w, h = a.getSpatial()
        self.assertEqual(49, x)
        self.assertEqual(58, y)
        self.assertEqual(8, w)
        self.assertEqual(12, h)
    
    def testCanResizeTo(self):
        """testCanResizeTo: can resize to a new size"""
        a = serge.geometry.Rectangle()
        a.setSpatial(50, 60, 6, 8)
        a.resizeTo(8, 12)        
        x, y, w, h = a.getSpatial()
        self.assertEqual(49, x)
        self.assertEqual(58, y)
        self.assertEqual(8, w)
        self.assertEqual(12, h)
        
    
    def testCanScale(self):
        """testCanScale: should be able to scale the object"""
        a = serge.geometry.Rectangle()
        a.setSpatial(50, 60, 10, 20)
        a.scale(2.0)        
        x, y, w, h = a.getSpatial()
        self.assertEqual(45, x)
        self.assertEqual(50, y)
        self.assertEqual(20, w)
        self.assertEqual(40, h)

    def testCanLock(self):
        """testCanLock: should be able to lock the actor"""
        a = serge.actor.Actor('a')
        a.setSpatial(50, 60, 5, 6)
        a.move(1, -1)        
        x, y, w, h = a.getSpatial()
        self.assertEqual(51, x)
        self.assertEqual(59, y)
        self.assertEqual(5, w)
        self.assertEqual(6, h)
        #
        a.lock = serge.actor.PositionLock('because')
        #
        self.assertRaises(serge.actor.PositionLocked, setattr, a, 'x', 10)
        self.assertRaises(serge.actor.PositionLocked, setattr, a, 'y', 10)
        self.assertRaises(serge.actor.PositionLocked, a.move, 1, 1)
        self.assertRaises(serge.actor.PositionLocked, a.moveTo, 1, 1)
        self.assertRaises(serge.actor.PositionLocked, a.setOrigin, 1, 1)

        
    ### Simple access ###
    
    def testShouldBeAbleToUseSimpleAccess(self):
        """testShouldBeAbleToUseSimpleAccess: should be able to use nice variables to access things"""
        a = serge.geometry.Rectangle()
        a.setSpatialCentered(50, 60, 10, 20)
        self.assertEqual(50, a.x)
        self.assertEqual(60, a.y)
        self.assertEqual(10, a.width)
        self.assertEqual(20, a.height)
        
        
    ### Distance from etc ###
    
    def testCanGetDistanceFrom(self):
        """testCanGetDistanceFrom: should be able to get distance"""
        a = serge.geometry.Rectangle()
        a.setSpatialCentered(50, 60, 10, 20)
        b = serge.geometry.Rectangle()
        b.setSpatialCentered(60, 60, 10, 20)
        #
        self.assertEqual(10, a.getDistanceFrom(b))
        self.assertEqual(10, b.getDistanceFrom(a))
        self.assertEqual(10, a.getDistanceFrom((60, 60)))
        self.assertEqual(10, b.getDistanceFrom((50, 60)))

        
            


if __name__ == '__main__':
    unittest.main()
