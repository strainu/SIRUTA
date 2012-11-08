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
    def __init__(self, filename = "./siruta.csv", countyfilename = ""):
        self._file = filename
        self._countyfile = countyfilename
        self._data = []
        self._prefixes = ['JUDEȚUL', 'MUNICIPIUL', 'ORAȘ', 'BUCUREȘTI']
        self.parseFile()
        
    def parseFile(self):
        """
        Parse a csv file extracted from the official mdb database.
        
        The expected input format is: 
        SIRUTA;DENLOC;CODP;JUD;SIRSUP;TIP;NIV;MED;REGIUNE;FSJ;FS2;FS3;FSL;rang;fictiv
        
        The output format is: TODO
        
        """
        pass
    
    def getName(self, siruta):
        """Get the entity name for the given siruta code
        
        :param siruta: The SIRUTA code for which we want the name
        :type siruta: string
            
        :return: The name of the entity or None if the code is not in the database
        :rtype: string

        """
        pass
        
    def getSupName(self, siruta):
        """Get the superior entity name for the given siruta code"""
        pass
        
    def getSupCode(self, siruta):
        """Get the superior entity code for the given siruta code"""
        pass
        
    def getPostalCode(self, siruta):
        """Get the entity's postal code for the given siruta code"""
        pass
    
    def getType(self, siruta):
        """Get the entity's type for the given siruta code"""
        pass
        
    def getCounty(self, siruta):
        """Get the entity's county for the given siruta code"""
        pass
        
    def getRegion(self, siruta):
        """Get the entity's region for the given siruta code"""
        pass
        
    def getCodeByName(self, name):
        pass
        
    def getSupCodeByName(self, name):
        """Get the superior entity code for the given name"""
        pass
        
    def getSupNameByName(self, name):
        """Get the superior entity name for the given name"""
        pass
        
    def getPostalCodeByName(self, siruta):
        """Get the entity's postal code for the given name"""
        pass
    
    def getTypeByName(self, siruta):
        """Get the entity's type for the given name"""
        pass
        
    def getCountyByName(self, siruta):
        """Get the entity's county for the given name"""
        pass
        
    def getRegionByName(self, siruta):
        """Get the entity's region for the given name"""
        pass
        
    def getInfCodes(self, siruta):
        """Get all the entities that have the given siruta code as \
superior code

        """
        pass
        
    def getAllCounties(self, prefix=True):
        """Get all county names from the database"""
        pass
