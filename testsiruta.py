#!/usr/bin/python
# -*- coding: utf-8  -*-
u"""
Copyright (c) 2012, Andrei Cipu <strainu@strainu.ro>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the original author nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

u"""

import unittest
import mmap
import operator


county_names = [
    u"ALBA",
    u"ARAD",
    u"ARGEȘ",
    u"BACĂU",
    u"BIHOR",
    u"BISTRIȚA-NĂSĂUD",
    u"BOTOȘANI",
    u"BRAȘOV",
    u"BRĂILA",
    u"BUZĂU",
    u"CARAȘ-SEVERIN",
    u"CĂLĂRAȘI",
    u"CLUJ",
    u"CONSTANȚA",
    u"COVASNA",
    u"DÂMBOVIȚA",
    u"DOLJ",
    u"GALAȚI",
    u"GIURGIU",
    u"GORJ",
    u"HARGHITA",
    u"HUNEDOARA",
    u"IALOMIȚA",
    u"IAȘI",
    u"ILFOV",
    u"MARAMUREȘ",
    u"MEHEDINȚI",
    u"MUREȘ",
    u"NEAMȚ",
    u"OLT",
    u"PRAHOVA",
    u"SATU MARE",
    u"SĂLAJ",
    u"SIBIU",
    u"SUCEAVA",
    u"TELEORMAN",
    u"TIMIȘ",
    u"TULCEA",
    u"VASLUI",
    u"VÂLCEA",
    u"VRANCEA",
]


class TestSirutaCsv(unittest.TestCase):
    _csv = None
    
    def setUp(self):
        import sirutalib
        if TestSirutaCsv._csv is None:
            TestSirutaCsv._csv = sirutalib.SirutaCsv()
        
    def test_db_size(self):
        f = open(self._csv._file, "r+")
        buf = mmap.mmap(f.fileno(), 0)
        lines = 0
        readline = buf.readline
        while readline():
            lines += 1
        self.assertEqual(lines - 1, len(self._csv._data))
        
    def test_county_name(self):
        self.assertEqual(u"JUDEȚUL ALBA", self._csv._counties[1])
        self.assertEqual(u"JUDEȚUL ARAD", self._csv._counties[2])
        self.assertEqual(u"JUDEȚUL ARGEȘ", self._csv._counties[3])
        
    def test_get_name(self):
        import sirutalib
        name = self._csv.get_name(10)
        self.assertEqual(name, u"JUDEȚUL ALBA")
        name = self._csv.get_name(179196)
        self.assertEqual(name, u"BUCUREȘTI SECTORUL 6")
        #correct, but inexistent code
        name = self._csv.get_name(500)
        self.assertEqual(name, None)
        self._csv._enforceWarnings = True
        try:
            self.assertRaises(sirutalib.SirutaCodeWarning, 
                              self._csv.get_name, 179197)
        finally:
            self._csv._enforceWarnings = False
        
    def test_siruta_is_valid(self):
        self.assertTrue(self._csv.siruta_is_valid(179132))
        self.assertTrue(self._csv.siruta_is_valid(29))
        self.assertFalse(self._csv.siruta_is_valid("1234567"))
        #this is a real, wrong SIRUTA code
        self.assertFalse(self._csv.siruta_is_valid(86453))
        #this is an imaginary, wrong SIRUTA code
        self.assertFalse(self._csv.siruta_is_valid(179197))
        
    def test_get_sup_code(self):
        self.assertEqual(self._csv.get_sup_code(10), 1)
        #this is an imaginary, wrong SIRUTA code
        self.assertEqual(self._csv.get_sup_code(179197), None)
        
    def test_get_sup_name(self):
        self.assertEqual(self._csv.get_sup_name(10), None)
        self.assertEqual(self._csv.get_sup_name(1017), 
                         u"JUDEȚUL ALBA")
        #this is an imaginary, wrong SIRUTA code
        self.assertEqual(self._csv.get_sup_name(179197), None)
        
    def test_get_postal_code(self):
        self.assertEqual(self._csv.get_postal_code(10), 0)
        self.assertEqual(self._csv.get_postal_code(1035), 510001)
        #this is an imaginary, wrong SIRUTA code
        self.assertEqual(self._csv.get_postal_code(179197), None)
    
    def test_get_type(self):
        self.assertEqual(self._csv.get_type(179132), 9)
        self.assertEqual(self._csv.get_type(86453), 3)
        #this is an imaginary, wrong SIRUTA code
        self.assertEqual(self._csv.get_type(179197), None)
        
    def test_get_county(self):
        self.assertEqual(self._csv.get_county(179132), 40)
        self.assertEqual(self._csv.get_county(86453), 19)
        self.assertEqual(self._csv.get_county(179197), None)
    
    def test_get_type_string(self):
        self.assertEqual(self._csv.get_type_string(179132), 
                         u"localitate  componentă, reședință de municipiu")
        self.assertEqual(self._csv.get_type_string(86453), u"comună")
        self.assertEqual(self._csv.get_type_string(179197), None)
        
    def test_get_county_string(self):
        self.assertEqual(self._csv.get_county_string(179132), 
                         u"MUNICIPIUL BUCUREȘTI")
        self.assertEqual(self._csv.get_county_string(86453), 
                         u"JUDEȚUL HARGHITA")
        self.assertEqual(self._csv.get_county_string(86453, prefix=False), 
                         u"HARGHITA")
        self.assertEqual(self._csv.get_county_string(179197), None)
        
    def test_get_region(self):
        self.assertEqual(self._csv.get_region(179132), 8)
        self.assertEqual(self._csv.get_region(86453), 7)
        #this is an imaginary, wrong SIRUTA code
        self.assertEqual(self._csv.get_region(179197), None)
        
    def test_get_code_by_name(self):
        self.assertRaises(NotImplementedError, self._csv.get_code_by_name, "JUDEȚUL ALBA")
        
    def test_get_sup_code_by_name(self):
        self.assertRaises(NotImplementedError, self._csv.get_sup_code_by_name, "JUDEȚUL ALBA")
        
    def test_get_sup_name_by_name(self):
        self.assertRaises(NotImplementedError, self._csv.get_sup_name_by_name, "JUDEȚUL ALBA")
        
    def test_get_postal_code_by_name(self):
        self.assertRaises(NotImplementedError, self._csv.get_postal_code_by_name, "JUDEȚUL ALBA")
    
    def test_get_type_by_name(self):
        self.assertRaises(NotImplementedError, self._csv.get_type_by_name, "JUDEȚUL ALBA")
        
    def test_get_county_by_name(self):
        self.assertRaises(NotImplementedError, self._csv.get_county_by_name, "JUDEȚUL ALBA")
        
    def test_get_region_by_name(self):
        self.assertRaises(NotImplementedError, self._csv.get_region_by_name, "JUDEȚUL ALBA")
        
    def test_get_inf_codes(self):
        self.assertItemsEqual(self._csv.get_inf_codes(86453), [84139])
        self.assertItemsEqual(self._csv.get_inf_codes(85984), 
                         [85993,86008,86017,86026,86035,86044,86053,
                         86062,86071,86080,86099,86106,86115,86124])
        #this is an imaginary, wrong SIRUTA code
        self.assertEqual(self._csv.get_inf_codes(179197), None)
        
    def test_get_all_counties(self):
        self.maxDiff = None
        
        county_names_without_prefix = county_names + [u"MUNICIPIUL BUCUREȘTI"]
        self.assertItemsEqual(self._csv.get_all_counties(prefix=False), county_names_without_prefix)
        
        county_names_with_prefix = map(operator.add, [u"JUDEȚUL "]*len(county_names), county_names)
        county_names_with_prefix.append(u"MUNICIPIUL BUCUREȘTI")
        self.assertItemsEqual(self._csv.get_all_counties(prefix=True), county_names_with_prefix)
    
    
if __name__ == '__main__':
    unittest.main()
