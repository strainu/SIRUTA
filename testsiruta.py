#!/usr/bin/python
# -*- coding: utf-8  -*-

import sirutalib
import unittest
import mmap


class TestSirutaCsv(unittest.TestCase):
    def setUp(self):
        self._csv = sirutalib.SirutaCsv()
        pass
        
    def test_db_size(self):
        f = open(self._csv._file, "r+")
        buf = mmap.mmap(f.fileno(), 0)
        lines = 0
        readline = buf.readline
        while readline():
            lines += 1
        self.assertEqual(lines - 1, len(self._csv._data))
        
    def test_get_name(self):
        name = self._csv.get_name(10)
        self.assertEqual(name, u"JUDEȚUL ALBA")
        name = self._csv.get_name(179196)
        self.assertEqual(name, u"BUCUREȘTI SECTORUL 6")
        name = self._csv.get_name(179197)
        self.assertEqual(name, None)
        
    def test_siruta_is_valid(self):
        self.assertTrue(self._csv.siruta_is_valid(179132))
        self.assertTrue(self._csv.siruta_is_valid(29))
        #self.assertFalse(self._csv.siruta_is_valid(179197))
        
    def test_get_sup_name(self):
        pass
        
    def test_get_sup_code(self):
        pass
        
    def test_get_postal_code(self):
        pass
    
    def test_get_type(self):
        pass
        
    def test_get_county(self):
        pass
        
    def test_get_region(self):
        pass
        
    def test_get_code_by_name(self):
        pass
        
    def test_get_sup_code_by_name(self):
        pass
        
    def test_get_sup_name_by_name(self):
        pass
        
    def test_get_postal_code_by_name(self):
        pass
    
    def test_get_type_by_name(self):
        pass
        
    def test_get_county_by_name(self):
        pass
        
    def test_get_region_by_name(self):
        pass
        
    def test_get_inf_codes(self):
        pass
        
    def test_get_all_counties(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()
