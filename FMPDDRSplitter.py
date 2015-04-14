
# -*- coding: utf-8 -*-

import sys
import os

import traceback

import thread

import time
import re

import pdb
kwdbg = False

import pprint
pp = pprint.pprint

import thread

import objc

import Foundation
NSObject = Foundation.NSObject
NSUserDefaults = Foundation.NSUserDefaults
NSMutableDictionary = Foundation.NSMutableDictionary
NSMakeRange = Foundation.NSMakeRange
NSAttributedString = Foundation.NSAttributedString
NSAutoreleasePool = Foundation.NSAutoreleasePool

import AppKit
NSWindowController = AppKit.NSWindowController
NSApplication = AppKit.NSApplication

import PyObjCTools
import PyObjCTools.AppHelper

import Config
import ddrsplit

gIsRunning = False
gLastUpdate = 0.0


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

    tfStatusText = objc.IBOutlet()
    rbAssets = objc.IBOutlet()

    btOpenSummary = objc.IBOutlet()
    btOpenExport = objc.IBOutlet()
    btCancel = objc.IBOutlet()
    btExport = objc.IBOutlet()

    summaryFile = None
    saveFolder = None

    def awakeFromNib(self):
        defaults = NSUserDefaults.standardUserDefaults()

        self.cbAssets.setState_(defaults.boolForKey_( u"assets" ))

        self.cbBaseTables.setState_(defaults.boolForKey_( u"basetables" ))

        self.cbAccounts.setState_(defaults.boolForKey_( u"accounts" ))

        self.cbCustomFunctions.setState_(defaults.boolForKey_( u"customfunctions" ))

        self.cbCustomMenus.setState_(defaults.boolForKey_( u"custommenus" ))
        self.cbCustomMenuSets.setState_(defaults.boolForKey_( u"custommenusets" ))

        self.cbPrivileges.setState_(defaults.boolForKey_( u"privileges" ))
        self.cbExtendedPrivileges.setState_(defaults.boolForKey_( u"extendedprivileges" ))

        self.cbFileReferences.setState_(defaults.boolForKey_( u"filereferences" ))

        self.cbRelationships.setState_(defaults.boolForKey_( u"relationships" ))

        self.cbValueLists.setState_(defaults.boolForKey_( u"valueLists" ))

        self.cbLayouts.setState_(defaults.boolForKey_( u"layouts" ))
        self.cbLayoutFolders.setState_(defaults.boolForKey_( u"layoutGroups" ))
        self.cbLayoutOrder.setState_(defaults.boolForKey_( u"layoutOrder" ))

        self.cbScripts.setState_(defaults.boolForKey_( u"scripts" ))
        self.cbScriptFolders.setState_(defaults.boolForKey_( u"scriptGroups" ))
        self.cbScriptOrder.setState_(defaults.boolForKey_( u"scriptOrder" ))

        self.tbSummaryFile.setStringValue_(defaults.stringForKey_( u"summaryfile" ))
        self.tbExportFolder.setStringValue_(defaults.stringForKey_( u"exportfolder" ))

    @objc.IBAction
    def openSummary_(self, sender):
        summary = getSummaryFileDialog()
        if summary and os.path.exists( summary ):
            self.summaryFile = unicode(summary)
            self.tbSummaryFile.setStringValue_( self.summaryFile )

    @objc.IBAction
    def openSaveFolder_(self, sender):
        folder = getFolderDialog()
        if folder and os.path.exists( folder ):
            self.saveFolder = unicode(folder)
            self.tbExportFolder.setStringValue_( self.saveFolder )

    @objc.IBAction
    def doCancel_(self, sender):
        ddrsplit.gCancel = True

    @objc.IBAction
    def doExport_(self, sender):

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
        
        cfg.logfunction = callFromWorkerMsg_

        if 1:
            thread.start_new_thread(threadwrapper, (cfg, ) )
        else:
            threadwrapper(cfg)

    def setButtons(self):
        if gIsRunning:
            self.btOpenSummary.setEnabled_( False )
            self.btOpenExport.setEnabled_( False )
            self.btCancel.setEnabled_( True )
            self.btExport.setEnabled_( False )
        else:
            self.btOpenSummary.setEnabled_( True )
            self.btOpenExport.setEnabled_( True )
            self.btCancel.setEnabled_( False )
            self.btExport.setEnabled_( True )
            

class FMPDDRSAppDelegate(NSObject):

    def applicationDidFinishLaunching_(self, notification):
        global gIsRunning
        gIsRunning = False
        app = NSApplication.sharedApplication()
        app.activateIgnoringOtherApps_(True)
        # ugly hack
        wins = app.windows()
        if not wins:
            return
        win = wins[0]
        controller = win.windowController()
        controller.setButtons()

    @objc.IBAction
    def terminate_(self, sender):
        pass

    @objc.IBAction
    def orderFrontStandardAboutPanel_(self, sender):
        pass

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
        userdefaults = NSUserDefaults.standardUserDefaults()
        app = NSApplication.sharedApplication()
        app.activateIgnoringOtherApps_(True)
        win = app.keyWindow()
        if not win:
            return True
        c = win.windowController()
        if not c:
            return True
        userdefaults.setObject_forKey_(c.cbAccounts.state(),            u'accounts')
        userdefaults.setObject_forKey_(c.cbAssets.state(),              u'assets')
        userdefaults.setObject_forKey_(c.cbBaseTables.state(),          u'basetables')
        userdefaults.setObject_forKey_(c.cbCustomFunctions.state(),     u'customfunctions')
        userdefaults.setObject_forKey_(c.cbCustomMenus.state(),         u'custommenus')
        userdefaults.setObject_forKey_(c.cbCustomMenuSets.state(),      u'custommenusets')
        userdefaults.setObject_forKey_(c.cbPrivileges.state(),          u'privileges')
        userdefaults.setObject_forKey_(c.cbExtendedPrivileges.state(),  u'extendedprivileges')
        userdefaults.setObject_forKey_(c.cbFileReferences.state(),      u'filereferences')
        userdefaults.setObject_forKey_(c.cbLayouts.state(),             u'layouts')
        userdefaults.setObject_forKey_(c.cbLayoutFolders.state(),       u'layoutGroups')
        userdefaults.setObject_forKey_(c.cbLayoutOrder.state(),         u'layoutOrder')
        userdefaults.setObject_forKey_(c.cbRelationships.state(),       u'relationships')
        userdefaults.setObject_forKey_(c.cbScripts.state(),             u'scripts')
        userdefaults.setObject_forKey_(c.cbScriptFolders.state(),       u'scriptGroups')
        userdefaults.setObject_forKey_(c.cbScripOrder.state(),          u'scriptOrder')
        userdefaults.setObject_forKey_(c.cbValueLists.state(),          u'valueLists')
        userdefaults.setObject_forKey_(c.tbSummaryFile.state(),         u'summaryfile')
        userdefaults.setObject_forKey_(c.tbExportFolder.state(),        u'exportfolder')
        return True

    def setstatus_show_(self, appendage, showit=False):
        global gLastUpdate
        s = appendage + u"\n"
        if type(s) != unicode:
            s = unicode(appendage, "utf-8")
        print s.encode("utf-8")
        # view
        app = NSApplication.sharedApplication()
        wins = app.windows()
        if not wins:
            return
        win = wins[0]
        controller = win.windowController()
        
        myView = controller.tfStatusText

        # 
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
        
        tm = time.time()
        if showit and tm >= gLastUpdate + 0.3:
            gLastUpdate = tm
            try:
                myView.scrollRangeToVisible_(endRange)
                myView.setNeedsDisplay_(True)
            except Exception, v:
                print
                print "ERROR status scrolling:", v
                print


def threadwrapper(cfg):
    global gIsRunning
    pool = NSAutoreleasePool.alloc().init()
    if not pool:
        return
    if gIsRunning:
        return
    gIsRunning = True
    ddrsplit.gCancel = False

    # view
    app = NSApplication.sharedApplication()
    win = app.keyWindow()
    controller = win.windowController()
    controller.setButtons()

    try:
        ddrsplit.main(cfg)

    except (Exception,), v:
        tb = traceback.format_exc()
        tb = unicode( tb )
        v = unicode( repr(v) )
        tb = tb + u"\n\n" + v
        sys.stdout.write( tb )

    finally:
        gIsRunning = False
        ddrsplit.gCancel = False
        controller.setButtons()
    del pool


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

def callFromWorkerMsg_( message ):
    PyObjCTools.AppHelper.callAfter( statwrap_, message=message)


def statwrap_(message):
    appl = NSApplication.sharedApplication()
    delg = appl.delegate()
    try:
        delg.setstatus_show_(message, 1)
    except Exception, v:
        print
        print "STATUS WRAPPER ERROR:", v
        print


if __name__ == "__main__":
    PyObjCTools.AppHelper.runEventLoop()
