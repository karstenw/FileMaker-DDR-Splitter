
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os

import traceback
import unicodedata

# import thread
import threading

import time
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


# py3 stuff

py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr


def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    if type(s) not in (punicode, pstr):
        s = str( s )
    if type(s) != punicode:
        s = punicode(s, srcencoding)
    s = unicodedata.normalize(normalizer, s)
    return s



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

    cbAuthFiles = objc.IBOutlet()
    cbExternalDatasources = objc.IBOutlet()
    cbThemeCatalog = objc.IBOutlet()
    cbBaseDirectories = objc.IBOutlet()

    cbLayouts = objc.IBOutlet()
    cbLayoutFolders = objc.IBOutlet()
    cbLayoutOrder = objc.IBOutlet()
    
    cbReferenceCollection = objc.IBOutlet()

    cbScripts = objc.IBOutlet()
    cbScriptFolders = objc.IBOutlet()
    cbScriptOrder = objc.IBOutlet()

    tbSummaryFile = objc.IBOutlet()
    tbExportFolder = objc.IBOutlet()

    tfStatusText = objc.IBOutlet()
    rbAssets = objc.IBOutlet()
    cbIgnoreFilenameIDs = objc.IBOutlet()

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

        self.cbIgnoreFilenameIDs.setState_(defaults.boolForKey_( u"ignoreFilenameIDs" ))

        self.cbRelationships.setState_(defaults.boolForKey_( u"relationships" ))

        self.cbValueLists.setState_(defaults.boolForKey_( u"valueLists" ))

        self.cbAuthFiles.setState_(defaults.boolForKey_( u"authfiles" ))
        self.cbExternalDatasources.setState_(defaults.boolForKey_( u"externaldatasources" ))
        self.cbThemeCatalog.setState_(defaults.boolForKey_( u"themes" ))
        self.cbBaseDirectories.setState_(defaults.boolForKey_( u"basedirectories" ))

        self.cbLayouts.setState_(defaults.boolForKey_( u"layouts" ))
        self.cbLayoutFolders.setState_(defaults.boolForKey_( u"layoutGroups" ))
        self.cbLayoutOrder.setState_(defaults.boolForKey_( u"layoutOrder" ))

        self.cbReferenceCollection.setState_(defaults.boolForKey_( u"referenceCollection" ))

        self.cbScripts.setState_(defaults.boolForKey_( u"scripts" ))

        self.cbScriptFolders.setState_(defaults.boolForKey_( u"scriptGroups" ))
        self.cbScriptOrder.setState_(defaults.boolForKey_( u"scriptOrder" ))

        self.tbSummaryFile.setStringValue_(defaults.stringForKey_( u"summaryfile" ))
        self.tbExportFolder.setStringValue_(defaults.stringForKey_( u"exportfolder" ))

    @objc.IBAction
    def openSummary_(self, sender):
        summary = getSummaryFileDialog()
        if summary and os.path.exists( summary ):
            self.summaryFile = makeunicode(summary)
            self.tbSummaryFile.setStringValue_( self.summaryFile )

    @objc.IBAction
    def openSaveFolder_(self, sender):
        # pdb.set_trace()
        folder = getFolderDialog()
        if folder and os.path.exists( folder ):
            self.saveFolder = makeunicode(folder)
            self.tbExportFolder.setStringValue_( self.saveFolder )

    @objc.IBAction
    def doCancel_(self, sender):
        ddrsplit.gCancel = True

    @objc.IBAction
    def doExport_(self, sender):
        # pdb.set_trace()
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

        # cbReferenceCollection
        cfg.referenceCollection = self.cbReferenceCollection.state()
        defaults.setObject_forKey_(cfg.referenceCollection, u'referenceCollection')


        cfg.scripts = self.cbScripts.state()
        defaults.setObject_forKey_(cfg.scripts, u'scripts')

        cfg.ignoreFilenameIDs = self.cbIgnoreFilenameIDs.state()
        defaults.setObject_forKey_(cfg.ignoreFilenameIDs, u'ignoreFilenameIDs')

        cfg.scriptGroups = self.cbScriptFolders.state()
        defaults.setObject_forKey_(cfg.scriptGroups, u'scriptGroups')

        cfg.scriptOrder = self.cbScriptOrder.state()
        defaults.setObject_forKey_(cfg.scriptOrder, u'scriptOrder')
        
        cfg.valueLists = self.cbValueLists.state()
        defaults.setObject_forKey_(cfg.valueLists, u'valueLists')

        cfg.authfile = self.cbAuthFiles.state()
        defaults.setObject_forKey_(cfg.authfile, u'authfiles')

        cfg.externaldatasources = self.cbExternalDatasources.state()
        defaults.setObject_forKey_(cfg.externaldatasources, u'externaldatasources')

        cfg.themecatalog = self.cbThemeCatalog.state()
        defaults.setObject_forKey_(cfg.themecatalog, u'themes')

        cfg.basedirectory = self.cbBaseDirectories.state()
        defaults.setObject_forKey_(cfg.basedirectory, u'basedirectories')

        cfg.summaryfile = self.tbSummaryFile.stringValue()
        defaults.setObject_forKey_(cfg.summaryfile, u'summaryfile')

        cfg.exportfolder = self.tbExportFolder.stringValue()
        defaults.setObject_forKey_(cfg.exportfolder, u'exportfolder')
        
        cfg.logfunction = callFromWorkerMsg_

        if 1:
            # thread.start_new_thread(threadwrapper, (cfg, ) )
            threading.Thread(target=threadwrapper,
                             args=(cfg, ),
                             # kwargs={'dict': 'of', 'keyword': 'args'},
                            ).start()
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
        userdefaults.setObject_forKey_(False,      u'ignoreFilenameIDs')
        userdefaults.setObject_forKey_(True,       u'layouts')
        userdefaults.setObject_forKey_(True,       u'layoutGroups')
        userdefaults.setObject_forKey_(True,       u'layoutOrder')
        userdefaults.setObject_forKey_(True,       u'relationships')
        userdefaults.setObject_forKey_(True,       u'referenceCollection')
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
        userdefaults.setObject_forKey_(c.cbIgnoreFilenameIDs.state(),   u'ignoreFilenameIDs')
        userdefaults.setObject_forKey_(c.cbLayouts.state(),             u'layouts')
        userdefaults.setObject_forKey_(c.cbLayoutFolders.state(),       u'layoutGroups')
        userdefaults.setObject_forKey_(c.cbLayoutOrder.state(),         u'layoutOrder')
        userdefaults.setObject_forKey_(c.cbRelationships.state(),       u'relationships')
        userdefaults.setObject_forKey_(c.cbReferenceCollection.state(), u'referenceCollection')
        userdefaults.setObject_forKey_(c.cbScripts.state(),             u'scripts')
        userdefaults.setObject_forKey_(c.cbScriptFolders.state(),       u'scriptGroups')
        userdefaults.setObject_forKey_(c.cbScriptOrder.state(),         u'scriptOrder')
        userdefaults.setObject_forKey_(c.cbValueLists.state(),          u'valueLists')

        userdefaults.setObject_forKey_(c.cbAuthFiles.state(),           u'authfiles')
        userdefaults.setObject_forKey_(c.cbExternalDatasources.state(), u'externaldatasources')
        userdefaults.setObject_forKey_(c.cbThemeCatalog.state(),        u'themes')
        userdefaults.setObject_forKey_(c.cbBaseDirectories.state(),     u'basedirectories')

        userdefaults.setObject_forKey_(c.tbSummaryFile.stringValue(),   u'summaryfile')
        userdefaults.setObject_forKey_(c.tbExportFolder.stringValue(),  u'exportfolder')
        return True

    def setstatus_show_(self, appendage, showit=False):
        global gLastUpdate
        s = appendage + u"\n"
        s = makeunicode( s )
        sys.stdout.write( s )
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
        except Exception as v:
            print()
            print( "ERROR status inserting:", v )
            print()
        
        tm = time.time()
        if showit and tm >= gLastUpdate + 0.3:
            gLastUpdate = tm
            try:
                myView.scrollRangeToVisible_(endRange)
                myView.setNeedsDisplay_(True)
            except Exception as v:
                print()
                print( "ERROR status scrolling:", v )
                print()


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

    except (Exception,) as v:
        tb = traceback.format_exc()
        tb = makeunicode( tb )
        v = makeunicode( v )
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
        f = [makeunicode(t) for t in panel.filenames()]
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
        f = [makeunicode(t) for t in panel.filenames()]
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
    except Exception as v:
        print()
        print( "STATUS WRAPPER ERROR:", v )
        print()


if __name__ == "__main__":
    PyObjCTools.AppHelper.runEventLoop()
