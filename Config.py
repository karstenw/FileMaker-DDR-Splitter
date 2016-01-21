
# -*- coding: utf-8 -*-

import sys
import os



class Config(object):
    """Just a class to carry all the options.
    
    Defaults to command line usage.
    """
    def __init__(self):
        self.accounts = True
        self.assets = True
        self.basetables = True
        self.customfunctions = True
        self.custommenus = True
        self.custommenusets = True
        self.privileges = True
        self.extendedprivileges = True
        self.filereferences = True

        self.layouts = True
        self.layoutGroups = True
        self.layoutOrder = True

        self.relationships = True

        self.scripts = True
        self.scriptGroups = True
        self.scriptOrder = True
        
        self.valueLists = True
        
        self.summaryfile = ""
        self.exportfolder = ""
        
        self.ignoreFilenameIDs = False
        self.logfunction = None

    def pp(self):
        print "accounts", repr(self.accounts)
        print "assets", repr(self.assets)
        print "basetables", repr(self.basetables)
        print "customfunctions", repr(self.customfunctions)
        print "custommenus", repr(self.custommenus)
        print "custommenusets", repr(self.custommenusets)
        print "privileges", repr(self.privileges)
        print "extendedprivileges", repr(self.extendedprivileges)
        print "filereferences", repr(self.filereferences)
        print "layouts", repr(self.layouts)
        print "layoutGroups", repr(self.layoutGroups)
        print "layoutOrder", repr(self.layoutOrder)

        print "relationships", repr(self.relationships)

        print "scripts", repr(self.scripts)
        print "scriptGroups", repr(self.scriptGroups)
        print "scriptOrder", repr(self.scriptOrder)

        print "valueLists", repr(self.valueLists)

        print "summaryfile", repr(self.summaryfile)
        print "exportfolder", repr(self.exportfolder)
        print "ignoreFilenameIDs", repr(self.ignoreFilenameIDs)
        print "logfunction", repr(self.logfunction)
