#!/usr/bin/python
# -*- coding: utf-8  -*-

#  Copyright (c) 2012, Andrei Cipu <strainu@strainu.ro>
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  

"""
Library created to parse a SIRUTA CSV extract and allow simple access
to the resulting database

"""

import csv
import locale
import warnings
import os
import sys


PY2 = sys.version_info[0] < 3


class SirutaCodeWarning(UserWarning):
    """
    This class defines a new type of warning, specific for SIRUTA
    codes with errors. It is used solely to uniquely identify the
    warnings thrown by this module.
    
    """
    pass
    
"""
----------------
Siruta Database
----------------

"""

class SirutaDatabase:
    """
    The main class, representing the SIRUTA database. 
    
    It reads data from a CSV file. The expected input format is: 
    SIRUTA;DENLOC;CODP;JUD;SIRSUP;TIP;NIV;MED;REGIUNE;FSJ;FS2;FS3;FSL;rang;fictiv
    
    Documentation for these fiels can be found on the INSSE website.
    
    :param filename: the CSV file containing the data. This is either \
    an abosulte path or a path relative to the current folder
    :param enforce_warnings: treat warnings as exceptions
    
    """
    _DIA_NEUTRAL = 0x0
    _DIA_PRE93   = 0x1
    _DIA_POST93  = 0x2
    _DIA_CEDILLA = 0x4
    _DIA_COMMA   = 0x8
    _DIA_NONE    = 0x10

    def __init__(self, filename="siruta.csv", enforce_warnings=False):
        if os.path.isabs(filename):
            self._file = filename
        else:
            fname = os.path.join(
                            os.path.dirname(os.path.abspath(__file__)), 
                            filename)
            if os.path.isfile(fname): #search in the directory running the lib
                self._file = fname
            elif os.path.isfile(filename):# search in the current directory
                self._file = filename
            else:
                self.__notify_error("CSV file not found. Please set the filename parameter to a valid path relative to the current folder", enforce=True)
        self._data = {}
        self._names = {}
        self._counties = {}
        self._regions = {
            1:	u'Nord-Est',
            2:	u'Sud-Est',
            3:	u'Sud - Muntenia',
            4:	u'Sud-Vest - Oltenia',
            5:	u'Vest',
            6:	u'Nord-Vest',
            7:	u'Centru',
            8:	u'București-Ilfov',
        }
        self._village_type = {
            1:  u'municipiu reședință de județ',
            2:  u'oraș ce aparține de județ',
            3:  u'comună',
            4:  u'municipiu, altul decât reședința de județ',
            5:  u'oraș reședință de județ',
            6:  u'Sector al  municipiului București',
            9:  u'localitate  componentă, reședință de municipiu',
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
        self._dia_trans = {ord(u"Ş"): u"Ș", ord(u"ş"): u"ș", ord(u"Ţ"): u"Ț", ord(u"ţ"): u"ț"}
        self._enforce_warnings = enforce_warnings
        self._last_error = ""
        self._dia = self._DIA_NEUTRAL
        self.__parse_file()
        self.__build_county_list()
	
        
    def __notify_error(self, message, enforce=False):
        if enforce or self._enforce_warnings:
            warnings.simplefilter("error")
        else:
            warnings.simplefilter("ignore")
        self._last_error = message
        warnings.warn(message, SirutaCodeWarning, stacklevel=2)
        warnings.resetwarnings()
        
    def __parse_file(self):
        """
        Parse a csv file extracted from the official mdb database.
        
        The output format is: TODO
        
        """

        if PY2:
            text = lambda v: v.decode('utf-8')
        else:
            text = lambda v: v
        with open(self._file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                try:
                    siruta = int(row[0])
                except ValueError as e:
                    self.__notify_error("Line %s has an invalid SIRUTA code" % str(row))
                    continue
                if not self.siruta_is_valid(siruta):
                    self.__notify_error("SIRUTA code %d is not valid" % siruta)
                if len(row) != 15:
                    self.__notify_error("Line %s does not have 15 elements" % str(row))
                    continue
                if row[7] == "1":
                    urban = True
                else:
                    urban = False
                self._data[siruta] = {
                    'siruta':   siruta,
                    'name':     text(row[1]).translate(self._dia_trans),
                    'postcode': int(row[2]),
                    'county':   int(row[3]),
                    'sirutasup':int(row[4]),
                    'type':     int(row[5]),
                    'level':    text(row[6]),
                    'urban':    urban,
                    'region':   int(row[8]),
                 }
        
    def __build_county_list(self):
        """
        Build a dictionary of counties. 
        
        Parse the whole siruta table for entries with type == 40
        
        """
        for entry in self._data.values():
            if entry['type'] == 40:
                self._counties[entry['county']] = entry['name']
                
    def get_siruta_list(self, county_list=None, type_list=None):
        """
        Get a list of SIRUTA codes for entities matching the limitations
        imposed by both the ``county`` and ``type`` parameters
        
        :param county_list: List of counties for which we want the codes
        :type county_list: list
        :param type_list: List of types for which we want the codes
        :type type_list: list
            
        :return: List of codes matching the limitations or an empty list
        :rtype: list
        
        """
        ret = []
        if county_list != None and type(county_list) != list:
            self.__notify_error("Invalid county required")
            return ret
        if type_list != None and type(type_list) != list:
            self.__notify_error("Invalid type required")
            return ret
            
        for entry in self._data.values():
            if (county_list == None or entry['county'] in county_list) and\
                (type_list == None or entry['type'] in type_list):
                ret.append(entry['siruta'])
        
        return ret

    def __normalize_string(self, string):
        """
        Return a string formatting according to the current
        diacritics settings
        """

        if self._dia & self._DIA_PRE93:
            string = string.replace(u"Â", u"Î")
            string = string.replace(u"ROMÎNĂ", u"ROMÂNĂ")
	elif self._dia & self._DIA_POST93:
            string = string.replace(u"Î", u"Â")
            string = string.replace(u"Ă ", u"Î")

        if self._dia & self._DIA_CEDILLA:
            string = string.replace(u"Ș", u"Ş")
            string = string.replace(u"Ț", u"Ţ")
        elif self._dia & self._DIA_COMMA:
            string = string.replace(u"Ş", u"Ș")
            string = string.replace(u"Ţ", u"Ț")

	if self._dia & self._DIA_NONE:
            string = string.replace(u"Î", u"I")
            string = string.replace(u"Â", u"A")
            string = string.replace(u"Ă", u"A")
            string = string.replace(u"Ș", u"S")
            string = string.replace(u"Ț", u"T")

        return string
        
    def siruta_is_valid(self, siruta):
        """
        Utility function which checks if the siruta code is valid 
        according to the algorithm from insse.ro
        
        :param siruta: The SIRUTA code for which we want the name
        :type siruta: int
            
        :return: ``True`` if the code is valid, ``False`` otherwise
        :rtype: bool
        
        """
        if type(siruta) != int:
            siruta = int(siruta)
        if len(str(siruta)) > 6:
            return False
        weights = [1, 2, 3, 5, 7]
        checksum = 0
        checkdigit = siruta % 10
        index = 0
        while (index < 5):
            siruta = int(siruta / 10)
            left = (siruta % 10) * weights[index]
            checksum += sum(map(int,str(left))) # sum of digits of left
            index += 1
        checksum %= 10
        checksum = 11 - checksum
        checksum %= 10
        return checksum == checkdigit

    def get_last_error(self):
        return self._last_error

    def set_diacritics_params(self, cedilla=False, acircumflex=True, nodia=False):
	"""Choose wether to return diacritics with cedilla or \
        comma and with â or î

        :param cedilla: True if we should return diacritics with cedillas, \
        False if we should return diacritics with comma-below
        :type cedilla: bool
        :param acircumflex: True if we are to return names with Â, \
        False if names with Î are required
        :type acircumflex: bool
	:param nodia: True if diacritics should be stripped, False otherwise
	:type nodia: bool
        """
        self.reset_diacritics_params()
	if nodia == True:
            self._dia = self._dia | self._DIA_NONE

        if cedilla == True:
            self._dia = self._dia | self._DIA_CEDILLA
        else:
            self._dia = self._dia | self._DIA_COMMA

        if acircumflex == True:
            self._dia = self._dia | self._DIA_POST93
        else:
            self._dia = self._dia | self._DIA_PRE93

    def reset_diacritics_params(self):
        """Reset the parameters for diacritics to the default \
        values (i.e. what we have in the file)"""
        self._dia = self._DIA_NEUTRAL
    
    def get_name(self, siruta, prefix=True):
        """Get the entity name for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the name
        :type siruta: int
        :param prefix: True if we want the name with entity type, \
        False if we only want the name
        :type prefix: bool
            
        :return: The name of the entity or None if the code is not in \
        the database
        :rtype: string

        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        if prefix:
            return self.__normalize_string(self._data[siruta]['name'])
        else:
            name = self._data[siruta]['name']
            for i in range(len(self._prefixes)):
                name = name.replace(self._prefixes[i], "")
            return self.__normalize_string(name.strip())
        
    def get_sup_code(self, siruta):
        """Get the superior entity code for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the superior's \
        code
        :type siruta: int
            
        :return: The code of the superior entity or ``None`` if the \
        code is not in the database
        :rtype: string
        
        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        return self._data[siruta]['sirutasup']
        
    def get_sup_name(self, siruta, prefix=True):
        """Get the superior entity name for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the name of \
        the superior entity
        :type siruta: int
        :param prefix: True if we want the name with entity type, \
        False if we only want the name
        :type prefix: bool
            
        :return: The name of the superior entity or ``None`` if the \
        code is not in the database
        :rtype: string
        
        """
        supcode = self.get_sup_code(siruta)
        if supcode == None:
            return None
        
        if not supcode in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % supcode)
            return None
            
        if prefix:
            return self.__normalize_string(self._data[supcode]['name'])
        else:
            name = self._data[supcode]['name']
            for i in range(len(self._prefixes)):
                name = name.replace(self._prefixes[i], "")
            return self.__normalize_string(name.strip())
        
    def get_postal_code(self, siruta):
        """Get the entity's postal code for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the postal code
        :type siruta: int
            
        :return: The postal code of the entity, ``None`` if the SIRUTA\
        code is not in the database or ``0`` if the entity has more than\
        one postal code
        :rtype: string
        
        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        return self._data[siruta]['postcode']
    
    def get_type(self, siruta):
        """Get the entity's type for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the type
        :type siruta: int
        
        :return: the entity's type if available, ``None`` otherwise
        :rtype: int
        
        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        return self._data[siruta]['type']
    
    def get_type_string(self, siruta):
        """Get the entity's type for the given siruta code as string
        
        :param siruta: The SIRUTA code for which we want the type
        :type siruta: int
        
        :return: the village type description if available, ``None`` \
        otherwise
        :rtype: string
        
        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        type_ = self._data[siruta]['type']
        if type_ in self._village_type:
            return self.__normalize_string(self._village_type[type_])
        else:
            return None
        
    def get_county(self, siruta):
        """Get the entity's county for the given siruta code as int
        
        :param siruta: The SIRUTA code for which we want the county
        :type siruta: int
        
        :return: the county code if available, ``None`` otherwise
        :rtype: int
        
        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        return self._data[siruta]['county']
        
    def get_county_string(self, siruta, prefix=True):
        """Get the entity's county for the given siruta code as string
        
        :param siruta: The SIRUTA code for which we want the county
        :type siruta: int
        
        :rtype: string
        
        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        county = self._data[siruta]['county']
        if county in self._counties:
            if prefix:
                return self.__normalize_string(self._counties[county])
            else:
                name = self._counties[county].replace(self._prefixes[0], "")
                name = name.replace(self._prefixes[1], "")
                return self.__normalize_string(name)
        else:
            return None

    def get_county_name(self, siruta, prefix=True):
        """Alias of ``get_county_string``

        :param siruta: The SIRUTA code for which we want the county
        :type siruta: int

        :rtype: string

        """
        return self.get_county_string(siruta, prefix)
        
    def get_region(self, siruta):
        """Get the entity's region for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the region
        :type siruta: int
        
        :return: the region code if available, ``None`` otherwise
        :rtype: int
        
        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        return self._data[siruta]['region']

    def get_region_string(self, siruta):
        """Get the entity's region for the given code as string

        :param siruta: The SIRUTA code for which we want the region
        :type siruta: int

        :return: the region name if available, ``None`` otherwise
        :rtype: int

        """
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None

        region = self._data[siruta]['region']
        if region in self._regions:
            return self._regions[region]
        else:
            return None

    def get_region_name(self, siruta):
        """Alias of ``get_region_string``

        :param siruta: The SIRUTA code for which we want the region
        :type siruta: int

        :return: the region name if available, ``None`` otherwise
        :rtype: int

        """
        return self.get_region_string(siruta)

        
    def get_inf_codes(self, siruta):
        """Get all the entities that have the given siruta code as \
superior code
        
        :param siruta: The SIRUTA code for which we want the codes of \
        the inferior entities
        :type siruta: int
        
        :return: a list of entities that have siruta as their superior \
        cod, ``None`` if there are no such entities
        :rtype: list

        """
        #we could skip this check, but we don't want weird supcodes
        if not siruta in self._data:
            self.__notify_error("SIRUTA code %d is not in the database" % siruta)
            return None
            
        ret = []
        
        for entry in self._data:
            if self._data[entry]['sirutasup'] == siruta:
                ret.append(entry)
                
        return ret
        
    def get_all_counties(self, prefix=True):
        """Get all county names from the database
        
        :param prefix: If ``False``, only the county name is returned, \
        otherwise the prefix used for counties in the database is prepended
        
        :return: a list of all county names in Romania
        :rtype: list
        
        """
        # this reads the environment and inits the right locale
        locale.setlocale(locale.LC_ALL, "")
        ret = list(self._counties.values())
        if not prefix:
            for index in range(len(ret)):
                ret[index] = ret[index].replace(self._prefixes[0], u"")
                ret[index] = ret[index].replace(self._prefixes[1], u"")
                ret[index] = self.__normalize_string(ret[index])
        if PY2:
            ret.sort(cmp=locale.strcoll)
        else:
            ret.sort(key=locale.strxfrm)
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
