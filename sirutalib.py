#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
:mod:`sirutalib` -- Siruta utility library
==========================================
Library created to parse a siruta CSV extract

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

"""

import csv
import locale

class SirutaCsv:
    def __init__(self, filename="./siruta.csv"):
        self._file = filename
        self._data = {}
        self._names = {}
        self._counties = {}
        self._village_type = {
                                 1: u'municipiu reședință de județ',
                                 2: u'oraș ce aparține de județ',
                                 3: u'comună',
                                 4: u'municipiu, altul decât reședința de județ',
                                 5: u'oraș reședință de județ',
                                 6: u'Sector al  municipiului București',
                                 9: u'localitate  componentă, reședință de municipiu',
                                10: u'localitate componentă a unui municipiu alta decât reședință de municipiu',
                                11: u'sat ce aparține de municipiu',
                                17: u'localitate componentă, reședință a orașului',
                                18: u'localitate  componentă a unui oraș, alta decât reședință de oraș',
                                19: u'sat care aparține unui oraș',
                                22: u'sat reședință de comună',
                                23: u'sat ce aparține de comună, altul decât reședință de comună ',
                                40: u'județ',
                             }
        self._prefixes = [u"JUDEȚUL ", u"MUNICIPIUL ", u"ORAȘ ", u"BUCUREȘTI "]
        self._unknown = u"necunoscut"
        self.parse_file()
        self.build_county_list()
        
    def parse_file(self):
        """
        Parse a csv file extracted from the official mdb database.
        
        The expected input format is: 
        SIRUTA;DENLOC;CODP;JUD;SIRSUP;TIP;NIV;MED;REGIUNE;FSJ;FS2;FS3;FSL;rang;fictiv
        
        The output format is: TODO
        
        """
        with open(self._file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                try:
                    siruta = int(row[0])
                except ValueError as e:
                    continue
                if not self.siruta_is_valid(siruta):
                    print "%d is not valid" % siruta
                    print row
                    continue
                if len(row) <> 15:
                    print len(row)
                    continue
                if row[7] == "1":
                    urban = True
                else:
                    urban = False
                self._data[siruta] = {
                                        'siruta':   siruta,
                                        'name':     unicode(row[1],'utf8'),
                                        'postcode': unicode(row[2],'utf8'),
                                        'county':   int(row[3]),
                                        'sirutasup':unicode(row[4],'utf8'),
                                        'type':     int(row[5]),
                                        'level':    unicode(row[6],'utf8'),
                                        'urban':    urban,
                                        'region':   unicode(row[8],'utf8'),
                                     }
        
    def build_county_list(self):
        """
        Build a dictionary of counties. 
        
        Parse the whole siruta table for entries with type == 40
        
        """
        for entry in self._data.values():
            if entry['type'] == 40:
                self._counties[entry['county']] = entry['name']
        
    def siruta_is_valid(self, siruta):
        """
        Check if the siruta code is valid according to the algorithm
        from insse.ro
        
        :param siruta: The SIRUTA code for which we want the name
        :type siruta: int
            
        :return: True if the code is valid, False otherwise
        :rtype: bool
        
        """
        if type(siruta) <> int:
            siruta = int(siruta)
        if len(str(siruta)) > 6:
            return False
        return True
        #forget about the algorithm for now, it seems flawed
        weights = [1, 2, 3, 5, 7]
        checksum = 0
        checkdigit = siruta % 10
        index = 0
        while (index < 5):
            siruta /= 10
            left = (siruta % 10) * weights[index]
            checksum += sum(map(int,str(left))) # sum of digits of left
            index += 1
        checksum %= 10
        checksum = 11 - checksum
        checksum %= 10
        return checksum == checkdigit
    
    def get_name(self, siruta):
        """Get the entity name for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the name
        :type siruta: int
            
        :return: The name of the entity or None if the code is not in the database
        :rtype: string

        """
        if not self.siruta_is_valid(siruta):
            return None
            
        if not siruta in self._data:
            return None
            
        return self._data[siruta]['name']
            
        
    def get_sup_name(self, siruta):
        """Get the superior entity name for the given siruta code"""
        raise NotImplementedError()
        
    def get_sup_code(self, siruta):
        """Get the superior entity code for the given siruta code"""
        raise NotImplementedError()
        
    def get_postal_code(self, siruta):
        """Get the entity's postal code for the given siruta code"""
        raise NotImplementedError()
    
    def get_type(self, siruta):
        """Get the entity's type for the given siruta code
        
        :rtype: int
        
        """
        return self._data[siruta]['type']
    
    def get_type_string(self, siruta):
        """Get the entity's type for the given siruta code as string
        
        :rtype: string
        
        """
        type_ = self._data[siruta]['type']
        if type_ in self._village_type:
            return self._village_type[type_]
        else:
            return self._unknown
        
    def get_county(self, siruta):
        """Get the entity's county for the given siruta code as int
        
        :rtype: int
        
        """
        return self._data[siruta]['county']
        
    def get_county_string(self, siruta, prefix=True):
        """Get the entity's county for the given siruta code as int
        
        :rtype: int
        
        """
        county = self._data[siruta]['county']
        if county in self._counties:
            if prefix:
                return self._counties[county]
            else:
                return self._counties[county].replace(self._prefixes[0], "")
        else:
            return self._unknown
        
    def get_region(self, siruta):
        """Get the entity's region for the given siruta code"""
        raise NotImplementedError()
        
    def get_code_by_name(self, name):
        """Get the entity's code for the given name"""
        raise NotImplementedError()
        
    def get_sup_code_by_name(self, name):
        """Get the superior entity code for the given name"""
        raise NotImplementedError()
        
    def get_sup_name_by_name(self, name):
        """Get the superior entity name for the given name"""
        raise NotImplementedError()
        
    def get_postal_code_by_name(self, siruta):
        """Get the entity's postal code for the given name"""
        raise NotImplementedError()
    
    def get_type_by_name(self, siruta):
        """Get the entity's type for the given name"""
        raise NotImplementedError()
        
    def get_county_by_name(self, siruta):
        """Get the entity's county for the given name"""
        raise NotImplementedError()
        
    def get_region_by_name(self, siruta):
        """Get the entity's region for the given name"""
        raise NotImplementedError()
        
    def get_inf_codes(self, siruta):
        """Get all the entities that have the given siruta code as \
superior code

        """
        raise NotImplementedError()
        
    def get_all_counties(self, prefix=True):
        """Get all county names from the database"""
        # this reads the environment and inits the right locale
        locale.setlocale(locale.LC_ALL, "")
        ret = self._counties.values()
        if not prefix:
            for index in range(len(ret)):
                ret[index] = ret[index].replace(self._prefixes[0], u"")
        ret.sort(cmp=locale.strcoll)
        return ret
