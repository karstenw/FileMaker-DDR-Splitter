
# -*- coding: utf-8 -*-

import sys
import os

import pdb

class ReferenceCollector(object):
    """A 2-pass data collector.
    
    1. pass
        collect all references by value (file, type, name, [to], [id], [scriptline])
            -> (file, type, name, scriptline)
        
    2. pass
        convert all types to ID
        convert all files to ID
        convert all names to ID
        convert all tuples to ID
        create referencetable ID -> ID
        create filetable ID,name
        create BTtable ID,name
        create TOtable ID,name,btID
        
    """
    def __init__(self):

        self.references = {}
        
        # (file, type, name, scriptline) -> ID
        self.objects = {}
        self.objectsReverse = {}
        self.objectID = 1

        self.filemakerAttributes = {}

        self.fileReferences = {}


        #
        # for now this is only chaotic sugar coating
        #
        
        # (fileID, 
        self.tables = {}
        self.tablesID = 1

        # (name, 
        self.files = {}
        self.filesID = 1

        # (name, bt, to) -> id
        self.layouts = {}
        self.layoutsID = 1

        
        self.variables = {}

        
    def pp(self):
        pass

    def addObject(self, obj):
        """retrieve ID for object. Add obj to collection if necessary."""

        if 0: #obj == "":
            pdb.set_trace()
        
        # xmlref, typ, name, *rest = obj

        if obj in self.objects:
            return self.objects[ obj ]
        else:
            i = self.objectID
            self.objects[ obj ] = i
            self.objectsReverse[ i ] = obj
            self.objectID += 1
            return i


    def addFileReference(self, xmlsource, xmldest, name, id_, pathList):
        if xmlsource not in self.fileReferences:
            self.fileReferences[xmlsource] = {
                                                name: {
                                                    'id': id_,
                                                    'pathList': pathList,
                                                    'destination': xmldest}}
        else:
            d = self.fileReferences[xmlsource]
            if name not in d:
                d[name] = {'id': id_,'pathList': pathList,'destination': xmldest}
            else:
                # checking for double entries here?
                d[name] = {'id': id_,'pathList': pathList,'destination': xmldest}
                


    def addReference(self, ref1, ref2):
        """ref1 object refers to ref2 object
        
        objects are ALWAYS passed by value. E.g. (file, type, name) tuples."""
        
        idref1 = self.addObject( ref1 )
        idref2 = self.addObject( ref2 )
        
        if idref1 not in self.references:
            self.references[ idref1 ] = [ idref2, ]
        else:
            if idref2 not in self.references[ idref1 ]:
                self.references[ idref1 ].append( idref2 )


    def addFilemakerAttribute(self, idobj, name, value):
        # pdb.set_trace()
        if idobj not in self.filemakerAttributes:
            self.filemakerAttributes[ idobj ] = {name:value}
        else:
            d = self.filemakerAttributes[ idobj ]
            
            if name not in d:
                d[name] = value
            else:
                # should i check unequal values here?
                d[name] = value

