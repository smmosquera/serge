"""Test file for conversation system"""


import unittest
import pygame
import os
import time

from helper import *

import serge.events
import serge.blocks.conversation

pygame.init()

class TestConversation(unittest.TestCase):
    """Tests for the Conversation"""

    def setUp(self):
        """Set up the tests"""
        self.c = serge.blocks.conversation.ConversationManager.fromXMLFile(f('map1.mm'))
        self.c.setCallback(self._getCallback)
        self.d = {}
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanLoadFromXMLFile(self):
        """testCanLoadFromXMLFile: should be able to load from an XML file"""
        pass # Done in the setup
        
    def testFailLoadInvalidXML(self):
        """testFailLoadInvalidXML: should raise and error if loading an invalid XML file"""
        self.assertRaises(serge.blocks.conversation.InvalidFile,
            serge.blocks.conversation.ConversationManager.fromXMLFile, f('map2.mm'))
        
    def testFailCannotFindNode(self):
        """testFailCannotFindNode: should fail when trying to find a non-existent node"""
        self.assertRaises(serge.blocks.conversation.NodeNotFound, self.c.findNode, 'Not there')
    
    def testCanGetText(self):
        """testCanGetText: should be able to get text"""
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        self.assertEqual('Hello is this your first time', child.getText())
        
    def testCanGetMultiLineText(self):
        """testCanGetMultiLineText: should be able to get multi line text"""
        node = self.c.findNode('Subsequent visits')
        child = node.getChild()
        self.assertEqual('Some long text.\nWith multiple lines\nand stuff', child.getText())
        
    def testCanGetOptions(self):
        """testCanGetOptions: should be able to get options"""
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        self.assertEqual(['Yes', 'No'], [option.getText() for option in child.getChildren()])

    def testCanMoveNextWithVariables(self):
        """testCanMoveNextWithVariables: should be able to move next with variables working"""
        node = self.c.findNode('Other Place')
        node.moveNext()
        self.assertEqual('Do you want to tango', node.getText())
        self.assertEqual(123, node.getVariable('a'))
            
    def testCanMoveOn(self):
        """testCanMoveOn: should be able to move from one node to another"""
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        child.chooseOption('No')
        self.assertEqual('Ok, well, my mistake', child.getText())
        #
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        child.chooseOption('Yes')
        self.assertEqual('Ok, good what would you like to do', child.getText())

    def testFindingNodeUsesVariables(self):
        """testFindingNodeUsesVariables: finding a node should return the proper variables"""
        node = self.c.findNode('Dupe2')
        self.assertEqual('Dupe1', node.getVariable('return-to'))        
 
    def testCanCheckIfConversationOver(self):
        """testCanCheckIfConversationOver: should be able to check if the conversation is over"""
        self._over = False
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        child.linkEvent(serge.blocks.conversation.E_CONVERSATION_ENDED, self._conversationOver)
        child.chooseOption('No')
        self.assertFalse(self._over)
        child.chooseOption('Leave')
        self.assertTrue(self._over)
       
    def _conversationOver(self, obj, arg):
        """The conversation ended"""
        self._over = True
        
    def testFailToMoveOnBadOption(self):
        """testFailToMoveOnBadOption: should fail when specifying a bad option"""
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        self.assertRaises(serge.blocks.conversation.BadOption, child.chooseOption, 'Baa')
    
    def testCanFollowLinks(self):
        """testCanFollowLinks: should be able to follow links from one place to another"""
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        child.chooseOption('Yes')
        child.chooseOption('Buy')
        self.assertEqual('Ok, they are yours', child.getText())
        
    def testCanSetVariables(self):
        """testCanSetVariables: should be able to set variables"""
        node = self.c.findNode('Other Place')
        child = node.getChild()
        child.chooseOption('yes')
        self.assertTrue(self.c.getVariable('do-tango'))
        #
        node = self.c.findNode('Other Place')
        child = node.getChild()
        child.chooseOption('no')
        self.assertFalse(self.c.getVariable('do-tango'))
        
    def testCanCallCallback(self):
        """testCanCallCallback: should be able to call a callback"""
        node = self.c.findNode('Subsequent visits')
        self._data = self._node = None
        child = node.getChild()
        child.chooseOption('Leave')
        #
        self.assertEqual('the-way-ahead', self._data)
        self.assertEqual('Leave', self._node.getText())
        self.assertEqual('No worries, come back soon', child.getText())
        
    def _getCallback(self, node, data):
        """Callback test"""
        self._node = node
        self._data = data

    def testCanUseLevelsToDissambiguate(self):
        """testCanUseLevelsToDissambiguate: should be able to use levels"""
        child = self.c.findNode('Dupe1', 'How are you')
        self.assertEqual(['Ok', 'Fine'], [option.getText() for option in child.getChildren()])      
        child = self.c.findNode('Dupe2', 'How are you')
        self.assertEqual(['Bad', 'Worse'], [option.getText() for option in child.getChildren()])      

    def testWhenCompleteShouldReturnToRoot(self):
        """testWhenCompleteShouldReturnToRoot: should return to the root when you are complete"""
        node = self.c.findNode('Initial Visit')
        child = node.getChild()
        child.chooseOption('No')
        child.chooseOption('Leave')
        self.assertEqual('Bomb Shop', child.getText())
        
    def testCanReturnToMe(self):
        """testCanReturnToMe: should be able to return to a particular node when complete"""
        node = self.c.findNode('Dupe1')
        child = node.getChild()
        child.chooseOption('Ok')
        self.assertEqual(['Ok', 'Fine'], [option.getText() for option in child.getChildren()])
        
    def testCanReturnToOther(self):
        """testCanReturnToOther: should be able to return to another when complete"""
        node = self.c.findNode('Dupe2')
        child = node.getChild()
        child.chooseOption('Bad')
        self.assertEqual(['Ok', 'Fine'], [option.getText() for option in child.getChildren()])
        
    def testCanCombineReturnToMeAndOther(self):
        """testCanCombineReturnToMeAndOther: should be able to combine a return to me and return to other"""
        node = self.c.findNode('Dupe2')
        child = node.getChild()
        child.chooseOption('Bad')
        child.chooseOption('Ok')
        self.assertEqual(['Ok', 'Fine'], [option.getText() for option in child.getChildren()])
    
    def testEndOfLineCanMoveNext(self):
        """testEndOfLineCanMoveNext: should be able to move next from the end of the line"""
        node = self.c.findNode('Ending')
        node.moveNext()
        node.chooseOption('Yep')
        node.moveNext()
        self.assertEqual('Good?', node.getText())
        
    def testCanDoConditionals(self):
        """testCanDoConditionals: should be able to do conditionals"""
        waiting = self.c.findNode('Wait for complete')
        waiting.moveNext()
        going = self.c.findNode('setting branch')
        #
        # Before should go to the default - which is the first
        self.assertEqual('You are not ready yet', waiting.getText())
        self.assertEqual('You are not ready yet', waiting.getText())
        #
        # Choosing the False line should keep on default
        going.moveNext()
        going.chooseOption('no')
        self.assertEqual('You are not ready yet', waiting.getText())
        #
        # Now choosing the true line should go
        going.chooseOption('yes')
        self.assertEqual('congratulations, you are ready', waiting.getText())
        
              
        
        
           
    

if __name__ == '__main__':
    unittest.main()        
