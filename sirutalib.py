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

class SirutaCsv:
    def __init__(self, filename="./siruta.csv", countyfilename=""):
        self._file = filename
        self._countyfile = countyfilename
        self._data = []
        self._prefixes = ['JUDEȚUL', 'MUNICIPIUL', 'ORAȘ', 'BUCUREȘTI']
        self.parse_File()
        
    def parse_file(self):
        """
        Parse a csv file extracted from the official mdb database.
        
        The expected input format is: 
        SIRUTA;DENLOC;CODP;JUD;SIRSUP;TIP;NIV;MED;REGIUNE;FSJ;FS2;FS3;FSL;rang;fictiv
        
        The output format is: TODO
        
        """
        pass
    
    def get_name(self, siruta):
        """Get the entity name for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the name
        :type siruta: string
            
        :return: The name of the entity or None if the code is not in the database
        :rtype: string

        """
        pass
        
    def get_sup_name(self, siruta):
        """Get the superior entity name for the given siruta code"""
        pass
        
    def get_sup_code(self, siruta):
        """Get the superior entity code for the given siruta code"""
        pass
        
    def get_postal_code(self, siruta):
        """Get the entity's postal code for the given siruta code"""
        pass
    
    def get_type(self, siruta):
        """Get the entity's type for the given siruta code"""
        pass
        
    def get_county(self, siruta):
        """Get the entity's county for the given siruta code"""
        pass
        
    def get_region(self, siruta):
        """Get the entity's region for the given siruta code"""
        pass
        
    def get_code_by_name(self, name):
        pass
        
    def get_sup_code_by_name(self, name):
        """Get the superior entity code for the given name"""
        pass
        
    def get_sup_name_by_name(self, name):
        """Get the superior entity name for the given name"""
        pass
        
    def get_postal_code_by_name(self, siruta):
        """Get the entity's postal code for the given name"""
        pass
    
    def get_type_by_name(self, siruta):
        """Get the entity's type for the given name"""
        pass
        
    def get_county_by_name(self, siruta):
        """Get the entity's county for the given name"""
        pass
        
    def get_region_by_name(self, siruta):
        """Get the entity's region for the given name"""
        pass
        
    def get_inf_codes(self, siruta):
        """Get all the entities that have the given siruta code as \
superior code

        """
        pass
        
    def get_all_counties(self, prefix=True):
        """Get all county names from the database"""
        pass
