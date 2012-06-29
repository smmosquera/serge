"""Tests for L-system stuff"""

import unittest

import serge.actor
import serge.blocks.lsystem

R = serge.blocks.lsystem.Rule

class TestLSystem(unittest.TestCase):
    """Tests for the LSystem"""

    def setUp(self):
        """Set up the tests"""
        self.l = serge.blocks.lsystem.LSystem()
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanAddRule(self):
        """testCanAddRule: should be able to add a rule"""
        self.l.addRule(R('1', '11'))
        
    def testCanAddRules(self):
        """testCanAddRules: should be able to add multiple rules"""
        self.l.setAxiom('0')        
        self.l.addRules([R('1', '11'), R('0', '1[0]0')])
        self.l.doSteps(2)
        self.assertEqual('11[1[0]0]1[0]0', self.l.getState())

    def testCanSetAxiom(self):
        """testCanSetAxiom: should be able to set the axiom"""
        self.l.setAxiom('1')
        self.assertEqual('1', self.l.getState())
    
    def testSettingAxiomAfterInitialDoesntReset(self):
        """testSettingAxiomAfterInitialDoesntReset: if set axiom after stepping then state doesn't change"""
        self.l.setAxiom('1')        
        self.l.addRule(R('1', '11'))
        self.l.doStep()
        self.l.setAxiom('0')        
        self.assertEqual('11', self.l.getState())
         
    def testCanReset(self):
        """testCanReset: should be able to reset"""
        self.l.setAxiom('1')        
        self.l.addRule(R('1', '11'))
        self.l.doStep()
        self.assertNotEqual('1', self.l.getState())
        self.l.reset()
        self.assertEqual('1', self.l.getState())
        
    def testCanDoAStep(self):
        """testCanDoAStep: should be able to do a step"""
        self.l.setAxiom('1')        
        self.l.addRule(R('1', '11'))
        self.l.doStep()
        self.assertEqual('11', self.l.getState())
        
    def testCanDoMultipleSteps(self):
        """testCanDoMultipleSteps: should be able to do multiple steps"""
        self.l.setAxiom('0')        
        self.l.addRule(R('1', '11'))
        self.l.addRule(R('0', '1[0]0'))
        self.l.doSteps(2)
        self.assertEqual('11[1[0]0]1[0]0', self.l.getState())
        
        
       
        

if __name__ == '__main__':
    unittest.main()
