
# -*- coding: utf-8 -*-

import sys, os
import thread

import re

import pdb
kwdbg = False

import pprint
pp = pprint.pprint

import objc

import Foundation
NSObject = Foundation.NSObject
NSUserDefaults = Foundation.NSUserDefaults
NSMutableDictionary = Foundation.NSMutableDictionary

import AppKit
NSWindowController = AppKit.NSWindowController

import PyObjCTools
import PyObjCTools.AppHelper

import Config
import ddrsplit

class FMPDDRSWindowController (NSWindowController):

    cbAssets = objc.IBOutlet()
    rbAssets = objc.IBOutlet()

    cbBaseTables = objc.IBOutlet()
    cbAccounts = objc.IBOutlet()
    cbCustomFunctions = objc.IBOutlet()
    cbCustomMenus = objc.IBOutlet()
    cbCustomMenuSets = objc.IBOutlet()
    cbPrivileges = objc.IBOutlet()
    cbExtendedPrivileges = objc.IBOutlet()
    cbFileReferences = objc.IBOutlet()
    cbRelationships = objc.IBOutlet()
    cbValueLists = objc.IBOutlet()

    cbLayouts = objc.IBOutlet()
    cbLayoutFolders = objc.IBOutlet()
    cbLayoutOrder = objc.IBOutlet()
    
    cbScripts = objc.IBOutlet()
    cbScriptFolders = objc.IBOutlet()
    cbScriptOrder = objc.IBOutlet()

    tbSummaryFile = objc.IBOutlet()
    tbExportFolder = objc.IBOutlet()

    summaryFile = None
    saveFolder = None


    def awakeFromNib(self):
        # pdb.set_trace()
        defaults = NSUserDefaults.standardUserDefaults()

        # self.optValueVisible.setState_( defaults.objectForKey_( u'optValueColumn') )

        # self.cbAssets.setState_(defaults.boolForKey_( u"assets" ))

        self.cbBaseTables.setState_(defaults.boolForKey_( u"basetables" ))

        # self.cbAssets.setState_(defaults.boolForKey_( u"assets" ))
        # self.rbAssets.setState_(objc.IBOutlet())

        self.cbAccounts.setState_(defaults.boolForKey_( u"accounts" ))

        self.cbCustomFunctions.setState_(defaults.boolForKey_( u"customfunctions" ))

        self.cbCustomMenus.setState_(defaults.boolForKey_( u"custommenus" ))
        self.cbCustomMenuSets.setState_(defaults.boolForKey_( u"custommenusets" ))

        self.cbPrivileges.setState_(defaults.boolForKey_( u"privileges" ))
        self.cbExtendedPrivileges.setState_(defaults.boolForKey_( u"extendedprivileges" ))

        self.cbFileReferences.setState_(defaults.boolForKey_( u"filereferences" ))

        self.cbRelationships.setState_(defaults.boolForKey_( u"relationships" ))

        self.cbValueLists.setState_(defaults.boolForKey_( u"valuelists" ))

        self.cbLayouts.setState_(defaults.boolForKey_( u"layouts" ))
        self.cbLayoutFolders.setState_(defaults.boolForKey_( u"layoutgroups" ))
        self.cbLayoutOrder.setState_(defaults.boolForKey_( u"layoutfolders" ))


        self.cbScripts.setState_(defaults.boolForKey_( u"scripts" ))
        self.cbScriptFolders.setState_(defaults.boolForKey_( u"scriptgroups" ))
        self.cbScriptOrder.setState_(defaults.boolForKey_( u"scriptorder" ))

        self.tbSummaryFile.setStringValue_(defaults.stringForKey_( u"summaryfile" ))
        self.tbExportFolder.setStringValue_(defaults.stringForKey_( u"exportfolder" ))



    @objc.IBAction
    def openSummary_(self, sender):
        print "open summary file"
        
        summary = getSummaryFileDialog()
        if summary and os.path.exists( summary ):
            self.summaryFile = summary
            print repr( summary ) 
            self.tbSummaryFile.setStringValue_( unicode(summary) )

    @objc.IBAction
    def openSaveFolder_(self, sender):
        print "get save folder"
        folder = getFolderDialog()
        if folder and os.path.exists( folder ):
            self.saveFolder = folder
            print repr(folder)
            self.tbExportFolder.setStringValue_( unicode(folder) )

    @objc.IBAction
    def doExport_(self, sender):

        pdb.set_trace()
        
        cfg = Config.Config()
        defaults = NSUserDefaults.standardUserDefaults()

        cfg.accounts = self.cbAccounts.state()
        defaults.setObject_forKey_(cfg.accounts, u'accounts')

        cfg.assets = self.cbAssets.state()
        defaults.setObject_forKey_(cfg.assets, u'assets')

        cfg.basetables = self.cbBaseTables.state()
        defaults.setObject_forKey_(cfg.basetables, u'basetables')

        cfg.customfunctions = self.cbCustomFunctions.state()
        defaults.setObject_forKey_(cfg.customfunctions, u'customfunctions')

        cfg.custommenus = self.cbCustomMenus.state()
        defaults.setObject_forKey_(cfg.custommenus, u'custommenus')

        cfg.custommenusets = self.cbCustomMenuSets.state()
        defaults.setObject_forKey_(cfg.custommenusets, u'custommenusets')


        cfg.privileges = self.cbPrivileges.state()
        defaults.setObject_forKey_(cfg.privileges, u'privileges')

        cfg.extendedprivileges = self.cbExtendedPrivileges.state()
        defaults.setObject_forKey_(cfg.extendedprivileges, u'extendedprivileges')

        cfg.filereferences = self.cbFileReferences.state()
        defaults.setObject_forKey_(cfg.filereferences, u'filereferences')

        cfg.layouts = self.cbLayouts.state()
        defaults.setObject_forKey_(cfg.layouts, u'layouts')

        cfg.layoutGroups = self.cbLayoutFolders.state()
        defaults.setObject_forKey_(cfg.layoutGroups, u'layoutGroups')

        cfg.layoutOrder = self.cbLayoutOrder.state()
        defaults.setObject_forKey_(cfg.layoutOrder, u'layoutOrder')


        cfg.relationships = self.cbRelationships.state()
        defaults.setObject_forKey_(cfg.relationships, u'relationships')

        cfg.scripts = self.cbScripts.state()
        defaults.setObject_forKey_(cfg.scripts, u'scripts')

        cfg.scriptGroups = self.cbScriptFolders.state()
        defaults.setObject_forKey_(cfg.scriptGroups, u'scriptGroups')

        cfg.scriptOrder = self.cbScriptOrder.state()
        defaults.setObject_forKey_(cfg.scriptOrder, u'scriptOrder')
        
        cfg.valueLists = self.cbValueLists.state()
        defaults.setObject_forKey_(cfg.valueLists, u'valueLists')

        
        cfg.summaryfile = self.tbSummaryFile.stringValue()
        defaults.setObject_forKey_(cfg.summaryfile, u'summaryfile')

        cfg.exportfolder = self.tbExportFolder.stringValue()
        defaults.setObject_forKey_(cfg.exportfolder, u'exportfolder')

        # pdb.set_trace()
        cfg.pp()
        ddrsplit.main(cfg)
        
        

    def setstatus_show_(self, appendage, showit=False):
        """
        Update the status Textfield

        Append appendage to the existing text.

        Scroll to end if showit.
        """

        # need unicode
        s = appendage
        if type(s) != unicode:
            s = unicode(appendage, "utf-8")

        # self.logfile.msg( (s.encode("utf-8")).strip(" \t\r\n"), flush=False )

        #if self.messageSupress:
        #    return

        # view
        myView = self.status

        # model
        storage = myView.textStorage()

        # where in the string
        l = storage.length()
        endRange = NSMakeRange(l, 0)

        # merge it
        try:
            t = NSAttributedString.alloc().initWithString_(s)
            storage.appendAttributedString_(t)
        except Exception, v:
            print
            print "ERROR status inserting:", v
            print

        # scroll if needed
        # 2010-02-23 Fast fix for crashes
        # 2010-02-26 perhaps scrolling and appending should be different calls
        if showit: #False: # s == u"" and showit:
            try:
                self.status.scrollRangeToVisible_(endRange)
                self.status.setNeedsDisplay_(True)
            except Exception, v:
                print
                print "ERROR status scrolling:", v
                print


class FMPDDRSAppDelegate(NSObject):

    def applicationDidFinishLaunching_(self, notification):
        print "finished launching"

    @objc.IBAction
    def terminate_(self, sender):
        print "terminate_"

    @objc.IBAction
    def orderFrontStandardAboutPanel_(self, sender):
        print "orderFrontStandardAboutPanel_"

    def initialize(self):
        # default settings for preferences
        userdefaults = NSMutableDictionary.dictionary()

        userdefaults.setObject_forKey_(True,       u'accounts')
        userdefaults.setObject_forKey_(True,       u'assets')
        userdefaults.setObject_forKey_(True,       u'basetables')
        userdefaults.setObject_forKey_(True,       u'customfunctions')
        userdefaults.setObject_forKey_(True,       u'custommenus')
        userdefaults.setObject_forKey_(True,       u'custommenusets')
        userdefaults.setObject_forKey_(True,       u'privileges')
        userdefaults.setObject_forKey_(True,       u'extendedprivileges')
        userdefaults.setObject_forKey_(True,       u'filereferences')
        userdefaults.setObject_forKey_(True,       u'layouts')
        userdefaults.setObject_forKey_(True,       u'layoutGroups')
        userdefaults.setObject_forKey_(True,       u'layoutOrder')
        userdefaults.setObject_forKey_(True,       u'relationships')
        userdefaults.setObject_forKey_(True,       u'scripts')
        userdefaults.setObject_forKey_(True,       u'scriptGroups')
        userdefaults.setObject_forKey_(True,       u'scriptOrder')
        userdefaults.setObject_forKey_(True,       u'valueLists')
        userdefaults.setObject_forKey_(u"",        u'summaryfile')
        userdefaults.setObject_forKey_(u"",        u'exportfolder')
        NSUserDefaults.standardUserDefaults().registerDefaults_(userdefaults)


    def applicationShouldTerminate_(self, aNotification):
        """Store preferences before quitting."""

        #defaults = NSUserDefaults.standardUserDefaults()
        #defaults.setObject_forKey_(self.visitedURLs, u'lastURLsVisited')
        #userdefaults.setObject_forKey_(True,       u'accounts')
        return True


def getFolderDialog():
    panel = AppKit.NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(False)
    panel.setCanChooseDirectories_(True)
    panel.setAllowsMultipleSelection_(False)
    rval = panel.runModalForTypes_([])
    if rval != 0:
        f = [unicode(t) for t in panel.filenames()]
        return f[0]
    else:
        return False

def getSummaryFileDialog():
    panel = AppKit.NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    panel.setAllowsMultipleSelection_(False)
    rval = panel.runModalForTypes_( ['xml'] )
    if rval != 0:
        f = [unicode(t) for t in panel.filenames()]
        return f[0]
    else:
        return False

def callFromWorkerMsg( message, scrollit=False ):
    PyObjCTools.AppHelper.callAfter( statwrap, message=message, dummy=scrollit)


def statwrap(message, dummy=True):
    appl = NSApplication.sharedApplication()
    delg = appl.delegate()
    try:
        delg.setstatus_show_(message, dummy)
    except Exception, v:
        print
        print "STATUS WRAPPER ERROR:", v
        print


if __name__ == "__main__":
    PyObjCTools.AppHelper.runEventLoop()
