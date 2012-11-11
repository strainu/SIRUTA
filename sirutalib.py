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
import warnings

class SirutaCodeWarning(UserWarning):
    """
    This class defines a new type of warning, specific for SIRUTA
    codes with errors
    
    """
    pass

class SirutaCsv:
    def __init__(self, filename="./siruta.csv", enforceWarnings=False):
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
        self._enforceWarnings = enforceWarnings
        self.parse_file()
        self.build_county_list()
        
    def notify_error(self, message, enforce=False):
        if enforce or self._enforceWarnings:
            warnings.simplefilter("error")
        else:
            warnings.simplefilter("ignore")
        warnings.warn(message, SirutaCodeWarning, stacklevel=2)
        warnings.resetwarnings()
        
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
                    self.notify_error("SIRUTA code %d is not valid" % siruta)
                if len(row) <> 15:
                    continue
                if row[7] == "1":
                    urban = True
                else:
                    urban = False
                self._data[siruta] = {
                                        'siruta':   siruta,
                                        'name':     unicode(row[1],'utf8'),
                                        'postcode': int(row[2]),
                                        'county':   int(row[3]),
                                        'sirutasup':int(row[4]),
                                        'type':     int(row[5]),
                                        'level':    unicode(row[6],'utf8'),
                                        'urban':    urban,
                                        'region':   int(row[8]),
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
            
        :return: The name of the entity or None if the code is not in \
        the database
        :rtype: string

        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        return self._data[siruta]['name']
        
    def get_sup_code(self, siruta):
        """Get the superior entity code for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the superior's \
        code
        :type siruta: int
            
        :return: The code of the superior entity or None if the code \
        is not in the database
        :rtype: string
        
        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        return self._data[siruta]['sirutasup']
        
    def get_sup_name(self, siruta):
        """Get the superior entity name for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the name of \
        the superior entity
        :type siruta: int
            
        :return: The name of the superior entity or None if the code \
        is not in the database
        :rtype: string
        
        """
        supcode = self.get_sup_code(siruta)
        if supcode == None:
            return None
        
        if not self.siruta_is_valid(supcode):
            self.notify_error("The SIRUTA code of the superior entity" \
            "(%d) is not valid for code %s" % (supcode,siruta))
            
        if not supcode in self._data:
            return None
            
        return self._data[supcode]['name']
        
    def get_postal_code(self, siruta):
        """Get the entity's postal code for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the postal code
        :type siruta: int
            
        :return: The postal code of the entity or None if the SIRUTA \
        code is not in the database
        :rtype: string
        
        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        return self._data[siruta]['postcode']
    
    def get_type(self, siruta):
        """Get the entity's type for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the type
        :type siruta: int
        
        :return: the entity's type if available, None otherwise
        :rtype: int
        
        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        return self._data[siruta]['type']
    
    def get_type_string(self, siruta):
        """Get the entity's type for the given siruta code as string
        
        :param siruta: The SIRUTA code for which we want the type
        :type siruta: int
        
        :return: the village type description if available, None otherwise
        :rtype: string
        
        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        type_ = self._data[siruta]['type']
        if type_ in self._village_type:
            return self._village_type[type_]
        else:
            return None
        
    def get_county(self, siruta):
        """Get the entity's county for the given siruta code as int
        
        :param siruta: The SIRUTA code for which we want the county
        :type siruta: int
        
        :return: the county code if available, None otherwise
        :rtype: int
        
        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        return self._data[siruta]['county']
        
    def get_county_string(self, siruta, prefix=True):
        """Get the entity's county for the given siruta code as int
        
        :param siruta: The SIRUTA code for which we want the county
        :type siruta: int
        
        :rtype: int
        
        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        county = self._data[siruta]['county']
        if county in self._counties:
            if prefix:
                return self._counties[county]
            else:
                return self._counties[county].replace(self._prefixes[0], "")
        else:
            return None
        
    def get_region(self, siruta):
        """Get the entity's region for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the region
        :type siruta: int
        
        :return: the region code if available, None otherwise
        :rtype: int
        
        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        if not siruta in self._data:
            return None
            
        return self._data[siruta]['region']
        
    def get_inf_codes(self, siruta):
        """Get all the entities that have the given siruta code as \
superior code
        
        :param siruta: The SIRUTA code for which we want the codes of \
        the inferior entities
        :type siruta: int
        
        :return: a list of entities that have siruta as their superior \
        cod, None if there are no such entities
        :rtype: list

        """
        if not self.siruta_is_valid(siruta):
            self.notify_error("SIRUTA code %d is not valid" % siruta)
            
        #we could skip this check, but we don't want weird supcodes
        if not siruta in self._data:
            return None
            
        ret = []
        
        for entry in self._data:
            if self._data[entry]['sirutasup'] == siruta:
                ret.append(entry)
                
        return ret
        
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
        
    def get_code_by_name(self, name):
        """Get the entity's code for the given name"""
        raise NotImplementedError()
        
    def get_sup_code_by_name(self, name):
        """Get the superior entity code for the given name"""
        raise NotImplementedError()
        
    def get_sup_name_by_name(self, name):
        """Get the superior entity name for the given name"""
        raise NotImplementedError()
        
    def get_postal_code_by_name(self, name):
        """Get the entity's postal code for the given name"""
        raise NotImplementedError()
    
    def get_type_by_name(self, name):
        """Get the entity's type for the given name"""
        raise NotImplementedError()
        
    def get_county_by_name(self, name):
        """Get the entity's county for the given name"""
        raise NotImplementedError()
        
    def get_region_by_name(self, name):
        """Get the entity's region for the given name"""
        raise NotImplementedError()
