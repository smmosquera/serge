"""Tests for the storage objects"""

import unittest
import time

import serge.render
import serge.engine
import serge.actor
import serge.visual
import serge.world
import serge.events
import serge.blocks.utils
import serge.blocks.storage

from helper import *

class TestStorage(unittest.TestCase, VisualTester):
    """Tests for the Storage"""

    def setUp(self):
        """Set up the tests"""
        removeIfThere(f('storage.db'))
        self.s = serge.blocks.storage.Storage('storage.db', os.path.join('files'))

    def tearDown(self):
        """Tear down the tests"""

    def testCanCreateStorage(self):
        """testCanCreateStorage: should be able to create a storage object"""
        pass
    
    def testCanAddATable(self):
        """testCanAddATable: should be able to add a table"""
        self.s.addTable('scores', 'create table scores (level int, date datetime, score int)')
        self.assertEqual([], self.s.get('select * from scores'))
    
    def testCanReloadATable(self):
        """testCanReloadATable: should be able to reload a table"""
        self.s.addTable('scores', 'create table scores (level int, date datetime, score int)')
        self.s.save()
        self.s.close()
        self.x = serge.blocks.storage.Storage('storage.db', os.path.join('files'))
        self.assertEqual([], self.x.get('select * from scores'))
    
    def testCanCreateMultipleTimes(self):
        """testCanCreateMultipleTimes: should be able to create multiple times"""
        self.s.addTable('scores', 'create table scores (level int, date datetime, score int)')
        self.s.save()
        self.s.close()
        #
        self.s = serge.blocks.storage.Storage('storage.db', os.path.join('files'))
        self.s.addTable('scores', 'create table scores (level int, date datetime, score int)')

    def testCanIncludeDefaultData(self):
        """testCanIncludeDefaultData: should be able to set default data"""
        self.s.addTable('scores', 'create table scores (level int, date datetime, score int)')
        self.s.addDefaultRows('scores', 'level', [
            (1, '2010-01-01', 10),
            (2, '2012-01-01', 20)])
        #
        rows = self.s.get('select * from scores order by level')
        self.assertEqual(1, rows[0][0])
        self.assertEqual(10, rows[0][2])
        self.assertEqual(2, rows[1][0])
        self.assertEqual(20, rows[1][2])

    def testDefaultDataShouldBeSupersededByAppData(self):
        """testDefaultDataShouldBeSupersededByAppData: should be able to use app data over default"""
        self.s.addTable('scores', 'create table scores (level int, date datetime, score int)')
        self.s.addDefaultRows('scores', 'level', [
            (1, '2010-01-01', 10),
            (2, '2012-01-01', 20)])
        #
        # Update the score and save
        self.s.get('update scores set score=30 where level=1')
        self.s.save()
        self.s.close()
        #
        # Now reload
        self.s = serge.blocks.storage.Storage('storage.db', os.path.join('files'))
        self.s.addDefaultRows('scores', 'level', [
            (1, '2010-01-01', 10),
            (2, '2012-01-01', 20)])
        #
        rows = self.s.get('select * from scores order by level')
        self.assertEqual(1, rows[0][0])
        self.assertEqual(30, rows[0][2])
        self.assertEqual(2, rows[1][0])
        self.assertEqual(20, rows[1][2])

    def testNewDefaultCanOverrideOldData(self):
        """testNewDefaultCanOverrideOldData: should be able to clear old data to make way for new default"""
        self.s.addTable('scores', 'create table scores (level int, date datetime, score int)')
        self.s.addDefaultRows('scores', 'level', [
            (1, '2010-01-01', 10),
            (2, '2012-01-01', 20)])
        #
        # Update the score and save
        self.s.get('update scores set score=30 where level=1')
        self.s.save()
        self.s.close()
        #
        # Now reload
        self.s = serge.blocks.storage.Storage('storage.db', os.path.join('files'))
        self.s.addDefaultRows('scores', 'level', [
            (1, '2010-01-01', 10),
            (2, '2012-01-01', 20)], override=True)
        #
        rows = self.s.get('select * from scores order by level')
        self.assertEqual(1, rows[0][0])
        self.assertEqual(10, rows[0][2])
        self.assertEqual(2, rows[1][0])
        self.assertEqual(20, rows[1][2])

    # The following test should be implemented when we have a live use-case

    '''
    def testCanUpdateTableSchema(self):
        """testCanUpdateTableSchema: should be able to update a table schema"""
        raise NotImplementedError
    
    def testTableSchemaUpdateRetainsData(self):
        """testTableSchemaUpdateRetainsData: updating the schema should retain old data"""
        raise NotImplementedError
    
    def testSchemaUpdateCanSetDefaults(self):
        """testSchemaUpdateCanSetDefaults: new schema should be able to create defaults"""
        raise NotImplementedError
    
    def testSchemaUpdateCanAlterData(self):
        """testSchemaUpdateCanAlterData: should be able to alter data in a schema update"""
        raise NotImplementedError
    
    def testSchemaUpdateCanDeleteData(self):
        """testSchemaUpdateCanDeleteData: should be able to delete data on a schema update"""
        raise NotImplementedError
    '''
    

if __name__ == '__main__':
    unittest.main()