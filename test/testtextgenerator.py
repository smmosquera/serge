"""Tests for the Text Generator part"""

import unittest
import time

import serge.render
import serge.engine
import serge.actor
import serge.visual
import serge.world
import serge.events
import serge.blocks.utils
import serge.blocks.textgenerator

from helper import *


class TestTextGenerator(unittest.TestCase, VisualTester):
    """Tests for the TextGenerator"""
    
    def setUp(self):
        """Set up the tests"""
        self.t = serge.blocks.textgenerator.TextGenerator()
        self.e1 = '''
                        colour: red
                        colour: blue
                        colour: green
                        name: bob
                        name: fred
                        thing: this
                        size: big
                        size: small
                        colourname: @{colour}@ @{name}@
                        cn: @{colourname}@
                    '''
        self.e2 = '''
                        colour {
                        red
                        blue
                        green
                        }
                        name {
                        bob
                        fred
                        }
                        thing: this
                        size: big
                        size: small
                        colourname: @{colour}@ @{name}@
                        cn: @{colourname}@
                  '''
        self.e3 = '''
                        sex: male
                        sex: female
                        male-name: bob
                        female-name: alice
                        name: @{@{sex}@-name}@
                  '''
                    
    def tearDown(self):
        """Tear down the tests"""
    
    def testCanCreate(self):
        """testCanCreate: should be able to create the generator"""
        self.assert_(self.t is not None)
    
    def testCanAddExamplesByMethod(self):
        """testCanAddExamplesByMethod: should be able to add examples by using the methods"""
        self.t.addExample('colour', 'red')
        self.assertEqual('red', self.t.getRandomFormCompletion('colour'))
        
    def testCanAddExampleFromText(self):
        """testCanAddExampleFromText: should be able to add examples from text"""
        self.t.addExamplesFromText('colour: red\nname: bob\n\n\tthing : this')
        self.assertEqual('red', self.t.getRandomFormCompletion('colour'))
        self.assertEqual('bob', self.t.getRandomFormCompletion('name'))
        self.assertEqual('this', self.t.getRandomFormCompletion('thing'))

    def testMultiExampleText(self):
        """testMultiExampleText: should be able to use multiexamples in text"""
        self.t.addExamplesFromText(self.e2)
        s = self.t.getRandomSentence('@{colour}@ @{name}@')
        a, b = s.split(' ')
        self.assertEqual(True, a in ['red', 'blue', 'green'])
        self.assertEqual(True, b in ['bob', 'fred'])
    
    def testSingleReplacement(self):
        """testSingleReplacement: should be able to do a single replacement"""
        self.t.addExamplesFromText(self.e1)
        s = self.t.getRandomSentence('@{thing}@')
        self.assertEqual('this', s)
        
    def testSingleOneFromMany(self):
        """testSingleOneFromMany: should be able to do a one from many replacement"""
        self.t.addExamplesFromText(self.e1)
        s = self.t.getRandomSentence('@{colour}@')
        self.assertEqual(True, s in ['red', 'blue', 'green'])
    
    def testTwoSinglesInOne(self):
        """testTwoSinglesInOne: should be able to do two examples of a single replacement"""
        self.t.addExamplesFromText(self.e1)
        s = self.t.getRandomSentence('@{colour}@ @{name}@')
        a, b = s.split(' ')
        self.assertEqual(True, a in ['red', 'blue', 'green'])
        self.assertEqual(True, b in ['bob', 'fred'])
    
    def testDoubleLevelReplacement(self):
        """testDoubleLevelReplacement: should be able to do a two level replacement"""
        self.t.addExamplesFromText(self.e1)
        s = self.t.getRandomSentence('@{colourname}@')
        a, b = s.split(' ')
        self.assertEqual(True, a in ['red', 'blue', 'green'])
        self.assertEqual(True, b in ['bob', 'fred'])
    
    def testRecursizeRepalcement(self):
        """testRecursizeRepalcement: should be able to do recursive replacement"""
        self.t.addExamplesFromText(self.e1)
        s = self.t.getRandomSentence('@{cn}@')
        a, b = s.split(' ')
        self.assertEqual(True, a in ['red', 'blue', 'green'])
        self.assertEqual(True, b in ['bob', 'fred'])
    
    def testNestedReplacement(self):
        """testNestedReplacement: should be able to do a nested replacement"""
        self.t.addExamplesFromText(self.e3)
        self.assertEqual('bob', self.t.getRandomSentence('@{name}@', {'sex':'male'}))
        self.assertEqual('alice', self.t.getRandomSentence('@{name}@', {'sex':'female'}))
    
    def testCanCheckPropertiesAfterwards(self):
        """testCanCheckPropertiesAfterwards: shold be able to check properties afterwars"""
        self.t.addExamplesFromText(self.e3)
        p = {'sex':'male'}
        self.assertEqual('bob', self.t.getRandomSentence('@{name}@', p))
        self.assertEqual('bob', self.t.getRandomSentence('@{name}@', p))
        
if __name__ == '__main__':
    unittest.main()
        
        
    
        
            