#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import unicodedata
import time
import binascii
import base64
import hashlib

import pprint
pp = pprint.pprint

import pdb

import xml.etree.cElementTree
ElementTree = xml.etree.cElementTree

import xml.parsers.expat


import Config

#
# globals
#
gCancel = False


#
# tools
#
def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    if type(s) != unicode:
        s = unicode(s, srcencoding)
    s = unicodedata.normalize(normalizer, s)
    return s

def stringhash( s ):
    m = hashlib.sha1()
    m.update(s)
    return m.hexdigest().upper()

def logfunction(s):
    s = s + u"\n"
    sys.stdout.write(s.encode("utf-8"))

#
# parsers
#
def xmlexportfolder(basefolder, dbname, category, obname, obid="", ext=".xml"):
    # create or get folder where to put layout, script or basetable xml
    path = os.path.abspath(basefolder)

    catfolder = os.path.join( path, dbname, category)
    
    if not os.path.exists(catfolder):
        os.makedirs( catfolder )
    
    if obid:
        obid = str(obid).rjust(7,"0") + " "
    filename = obid + obname + ext
    filename = filename.replace('/', '_')
    filename = filename.replace(':', '_')
    filename = filename.replace('\\', '_')

    fullpath = os.path.join( catfolder, filename)
    fullpath = makeunicode( fullpath, normalizer="NFD" )
    return fullpath.encode("utf-8")

def get_layouts_and_groups(cfg, cur_db, laynode, groups, exportfolder, idx):

    for layout in laynode:

        layout_attr = layout.attrib
        layout_tag = layout.tag
        if layout_tag == "Group":
            grp_attrib = layout_attr
            groupid = layout_attr.get("id", "0")

            groupname = groupid.rjust(7,"0") + ' ' + layout_attr.get("name", "NONAME")
            if cfg.layoutOrder:
                groupname = str(idx).rjust(5,"0") + ' ' + groupid.rjust(7,"0") + ' ' + layout_attr.get("name", "NONAME")

            groups.append( groupname )

            idx += 1
            idx = get_layouts_and_groups(cfg, cur_db, layout, groups, exportfolder, idx)
            groups.pop()
        else:
            path = "Layouts"
        
            if groups and cfg.layoutGroups:
                path = os.path.join("Layouts", *groups)
            s = ElementTree.tostring(layout, encoding="utf-8", method="xml")

            sortid = layout_attr.get("id", "0").rjust(7,"0")
            if cfg.layoutOrder:
                sortid = str(idx).rjust(5,"0") + ' ' + layout_attr.get("id", "0").rjust(7,"0")

            path = xmlexportfolder(exportfolder, cur_db, path,
                                   layout_attr.get("name", "NONAME"),
                                   sortid)
            f = open(path, "wb")
            f.write( s )
            f.close()
            idx += 1

            if not cfg.assets:
                continue

            for l in layout.getchildren():
                t = l.tag
                if t == u'Object':
                    cur_obj = get_layout_object(cur_db, l, exportfolder)
    return idx

def get_layout_object(cur_db, laynode, exportfolder):
    nodes = list(laynode)
    extensions = dict(zip( ("JPEG","PDF ", "PNGf", "PICT", "GIFf", "8BPS", "BMPf"),
                           (".jpg",".pdf", ".png", ".pict", ".gif", ".psd", ".bmp")))
    exttypelist = extensions.keys()
    for node in nodes:
        cur_tag = node.tag
        
        if cur_tag == u'Object':
            # get layout object
            cur_obj = get_layout_object(cur_db, node, exportfolder)

        elif cur_tag == u'GraphicObj':
            for grobnode in node:
                if grobnode.tag == "Stream":
                    stype = []
                    sdata = ""
                    for streamnode in grobnode:
                        streamtag = streamnode.tag
                        streamtext = streamnode.text
                        if streamtag == "Type":
                            if streamtext not in exttypelist:
                                stype.append( '.' + streamtext )
                            else:
                                stype.append( streamtext )
                        elif streamtag in ("Data", "HexData"):
                            if not stype:
                                continue
                            curtype = stype[-1]
                            ext = extensions.get( curtype, False )
                            if not ext:
                                ext = curtype
                            data = None
                            if streamtag == "HexData":
                                try:
                                    data = binascii.unhexlify ( streamtext )
                                except TypeError, err:
                                    pass
                            elif streamtag == "Data":
                                try:
                                    data = base64.b64decode( streamtext )
                                except TypeError, err:
                                    pass
                            if not data:
                                continue

                            fn = stringhash( data )
                            path = xmlexportfolder(exportfolder, cur_db, "Assets", fn, "", ext)
                            if not os.path.exists( path ):
                                f = open(path, "wb")
                                f.write( data )
                                f.close()

def get_scripts_and_groups(cfg, cur_db, scriptnode, exportfolder, groups, namecache, idx):

    for scpt in scriptnode:
        if scpt.tag == "Script":
            path = "Scripts"
            if groups and cfg.scriptGroups:
                path = os.path.join("Scripts", *groups)

            sortid = scpt.get("id", "0").rjust(7,"0")
            if cfg.scriptOrder:
                sortid = str(idx).rjust(5,"0") + ' ' + scpt.get("id", "0").rjust(7,"0")
            s = ElementTree.tostring(scpt, encoding="utf-8", method="xml")
            path = xmlexportfolder(exportfolder, cur_db, path,
                                   scpt.get("name", "NONAME"),
                                   sortid)
            idx += 1
            f = open(path, "wb")
            f.write( s )
            f.close()

        elif scpt.tag == "Group":
            grp_attrib = scpt.attrib
            groupid = grp_attrib.get("id", "0")

            groupname = groupid.rjust(7,"0") + ' ' + grp_attrib.get("name", "NONAME")
            if cfg.scriptOrder:
                groupname = (str(idx).rjust(5,"0")
                             + ' ' + groupid.rjust(7,"0")
                             + ' ' + grp_attrib.get("name", "NONAME"))
            groups.append( groupname )

            idx += 1
            idx = get_scripts_and_groups(cfg, cur_db, scpt, exportfolder, groups, namecache, idx)
            groups.pop()
    return idx

def get_relationshipgraph_catalog(cur_db, rg_cat, exportfolder):
    for tablst in rg_cat:
        if tablst.tag == u'TableList':
            for tab in tablst:
                if tab.tag == u'Table':
                    to_attr = tab.attrib
                    s = ElementTree.tostring(tab, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Relationships/TableList",
                                           tab.attrib.get("name", "NONAME"),
                                           tab.attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        elif tablst.tag == u'RelationshipList':
            for rel in tablst:
                if rel.tag == u'Relationship':
                    rel_cat = {}
                    re_attr = rel.attrib
                    relid = re_attr.get("id", "0")
                    rel_cat['id'] = re_attr.get("id", "0")

                    for rel_component in rel.getchildren():
                        if rel_component.tag == "LeftTable":
                            rel_cat['lefttable'] = rel_component.attrib.get("name", "NO-LEFTTABLENAME")
                        elif rel_component.tag == "RightTable":
                            rel_cat['righttable'] = rel_component.attrib.get("name", "NO-LEFTTABLENAME")
                            
                    s = ElementTree.tostring(rel, encoding="utf-8", method="xml")
                    filename = rel_cat['lefttable'] + "---" + rel_cat['righttable']
                    
                    path = xmlexportfolder(exportfolder, cur_db, "Relationships/Relationship",
                                           filename,
                                           rel_cat['id'])
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

def main(cfg):

    xmlfile = cfg.summaryfile
    xml_folder, xmlfilename = os.path.split( xmlfile )

    ddr = ElementTree.parse( xmlfile )

    summary = ddr.getroot()

    files = summary.findall( "File" )
    nooffiles = len( files )

    filelist = {}

    starttime = time.time()

    log = logfunction
    if cfg.logfunction:
        log = cfg.logfunction

    for i in files:
        xffile = dbfile = False
        fmp6 = False
        try:
            xffile = i.attrib[ "link" ]
        except KeyError, m:
            log( u"XML Error: '%s'" % m )
            for item in i:
                if item.tag == "XMLReportFile":
                    xffile = item.text
                    fmp6 = True
                elif item.tag == "File":
                    dbfile = item.text
                    fmp6 = True
                    
        if not xffile:
            log( u"\nERROR: Could not find a XML file... NEXT!\n" )
            continue

        # cleanup filename
        while xffile.startswith( './/' ): xffile = xffile[ 3: ]
        while xffile.startswith( './' ):  xffile = xffile[ 2: ]

        xmlbasename, ext  = os.path.splitext( xffile )
        filelist[ xffile ] = xmlbasename

    for cur_xml_file_name in filelist.keys():
        next_xml_file_path = os.path.join( xml_folder, cur_xml_file_name )
        line = '-' * 100
        log( u"\n\n%s\n\nXMLFILE: %s" % (line, cur_xml_file_name) )

        try:
            basenode = ElementTree.parse( next_xml_file_path )
        except  (xml.parsers.expat.ExpatError, SyntaxError), v:
            xml.parsers.expat.error()
            log( u"EXCEPTION: '%s'" % v )
            log( u"Failed parsing '%s'\n" % next_xml_file_path )
            continue

        cur_db = filelist[ cur_xml_file_name ]

        exportfolder = cfg.exportfolder

        #
        # base table catalog
        #
        if cfg.basetables:
            log( u'\n\nBase Tables "%s"' % cur_db )
            for base_table_catalog in basenode.getiterator( u'BaseTableCatalog' ):
                for base_table in base_table_catalog.getiterator( u'BaseTable' ):
                    s = ElementTree.tostring(base_table, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Basetables",
                                           base_table.get("name", "NONAME"),
                                           base_table.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        # BaseDirectoryCatalog
        
        #
        # layout catalog
        #
        if cfg.layouts:
            log( u'Layout Catalog "%s"' % cur_db )
            for layout_catalog in basenode.getiterator ( "LayoutCatalog" ):
                groups = []
                get_layouts_and_groups(cfg, cur_db, layout_catalog, groups, exportfolder, 1)

        #
        # file reference catalog
        #
        if cfg.filereferences:
            log( u'File References "%s"' % cur_db )
            for fr_cat in basenode.getiterator ( "FileReferenceCatalog" ):
                for fileref in fr_cat.getchildren():
                    fileref_attrib = fileref.attrib
                    prefix = ""
                    if fileref.tag == "OdbcDataSource":
                        prefix = "ODBC-"
                    elif fileref.tag == "FileReference":
                        prefix = "FREF-"
                    else:
                        prefix = "UNKN-"
                    name = prefix + fileref_attrib.get("name", "NONAME")
                
                    s = ElementTree.tostring(fileref, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Filereferences",
                                           name,
                                           fileref_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        #
        # relationship graph
        #
        if cfg.relationships:
            log( u'Relationship Graph "%s"' % cur_db )
            for rg_cat in basenode.getiterator ( "RelationshipGraph" ):
                get_relationshipgraph_catalog(cur_db, rg_cat, exportfolder)

        #
        # account catalog
        #
        if cfg.accounts:
            log( u'Accounts for "%s"' % cur_db )
            for acc_cat in basenode.getiterator ( "AccountCatalog" ):
                for acc in acc_cat.getchildren():
                    acc_attrib = acc.attrib
                    s = ElementTree.tostring(acc, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Accounts",
                                           acc_attrib.get("name", "NONAME"),
                                           acc_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        #
        # script catalog
        #
        if cfg.scripts:
            log( u'Scripts for "%s"' % cur_db )
            for scpt_cat in basenode.getiterator ( "ScriptCatalog" ):
                groups = []
                namecache = [{},{}]
                get_scripts_and_groups(cfg, cur_db, scpt_cat, exportfolder, groups, namecache, 1)

        #
        # custom function catalog
        #
        #
        if cfg.customfunctions:
            log( u'Custom Functions for "%s"' % cur_db )
            for cf_cat in basenode.getiterator ( "CustomFunctionCatalog" ):
                groups = []
                for cf in cf_cat.getchildren():
                    cf_attrib = cf.attrib
                    s = ElementTree.tostring(cf, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "CustomFunctions",
                                           cf_attrib.get("name", "NONAME"),
                                           cf_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()
        
        # privileges
        #
        if cfg.privileges:
            log( u'Privileges for "%s"' % cur_db )
            for pv_cat in basenode.getiterator( "PrivilegesCatalog" ):
                for pv in pv_cat.getchildren():
                    pv_attrib = pv.attrib
                    s = ElementTree.tostring(pv, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Privileges",
                                           pv_attrib.get("name", "NONAME"),
                                           pv_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        #
        # extended privileges
        #
        if cfg.extendedprivileges:
            log( u'Extended Privileges for "%s"' % cur_db )
            for epv_cat in basenode.getiterator( "ExtendedPrivilegeCatalog" ):
                for epv in epv_cat.getchildren():
                    epv_attrib = epv.attrib
                    s = ElementTree.tostring(epv, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "ExtendedPrivileges",
                                           epv_attrib.get("name", "NONAME"),
                                           epv_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        # AuthFileCatalog
        
        #
        # custom menus
        #
        if cfg.custommenus:
            log( u'Custom Menus for "%s"' % cur_db )
            for cm_cat in basenode.getiterator( "CustomMenuCatalog" ):
                for cm in cm_cat.getchildren():
                    cm_attrib = cm.attrib
                    s = ElementTree.tostring(cm, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "CustomMenus",
                                           cm_attrib.get("name", "NONAME"),
                                           cm_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        #
        # custom menu sets
        #
        if cfg.custommenusets:
            log( u'Custom Menu Sets for "%s"' % cur_db )
            for cms_cat in basenode.getiterator( "CustomMenuSetCatalog" ):
                for cms in cms_cat.getchildren():
                    cms_attrib = cms.attrib
                    s = ElementTree.tostring(cms, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "CustomMenuSets",
                                           cms_attrib.get("name", "NONAME"),
                                           cms_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        #
        # value lists
        #
        if cfg.valueLists:
            log('Value Lists for "%s"' % cur_db )
            for vl_cat in basenode.getiterator( "ValueListCatalog" ):
                for vl in vl_cat.getchildren():
                    vl_attrib = vl.attrib
                    s = ElementTree.tostring(vl, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "ValueLists",
                                           vl_attrib.get("name", "NONAME"),
                                           vl_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

        # ThemeCatalog

        if gCancel:
            time.sleep(0.3)
            log("\n\n####  CANCELLED.  ####")
            return

    time.sleep(0.3)
    stoptime = time.time()
    log("\nRuntime %.4f\n\n####  FINISHED.  ####\n\n" % ( round(stoptime - starttime, 4), ))

if __name__ == '__main__':

    infiles = sys.argv[1:]
    for f in infiles:
        f = os.path.abspath( os.path.expanduser(f) )
        folder, filename = os.path.split( f )

        cfg = Config.Config()
        cfg.summaryfile = f
        cfg.exportfolder = os.path.join( folder, "Exports")
        cfg.logfunction = logfunction
        main( cfg )
