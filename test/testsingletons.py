"""Test the singletons"""

import unittest
import os
import pygame

from helper import *

import serge.blocks.singletons


class TestSingletons(unittest.TestCase, VisualTester):
    """Tests for the singletons"""

    def setUp(self):
        """Set up the tests"""
        serge.blocks.singletons.Store.clearItems()
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanCreateSingleton(self):
        """testCanCreateSingleton: should be able to create a singleton"""
        s = serge.blocks.singletons.Store.registerItem('one')
        s.data = 1
        
    def testShouldBeOnlyOne(self):
        """testShouldBeOnlyOne: should be only one singleton"""
        s = serge.blocks.singletons.Store.registerItem('one')
        s.data = 1
        x = serge.blocks.singletons.Store.getItem('one')
        self.assertEqual(1, s.data)
        self.assertEqual(1, x.data)
        #
        x.data = 2
        self.assertEqual(2, s.data)
        self.assertEqual(2, x.data)
        
                


if __name__ == '__main__':
    unittest.main()
