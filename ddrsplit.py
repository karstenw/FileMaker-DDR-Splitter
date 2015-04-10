#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import unicodedata

import binascii
import base64
import hashlib

import pprint
pp = pprint.pprint

import pdb

import xml.etree.cElementTree
ElementTree = xml.etree.cElementTree

import xml.parsers.expat


#
# globals
#
g_dogroupfolders = True


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
        obid = str(obid).rjust(7,"0") + "_"
    filename = obid + obname + ext
    filename = filename.replace('/', '_')
    filename = filename.replace(':', '_')
    filename = filename.replace('\\', '_')

    fullpath = os.path.join( catfolder, filename)
    fullpath = makeunicode( fullpath, normalizer="NFD" )
    return fullpath.encode("utf-8")

def get_layouts_and_groups(cur_db, laynode, groups, exportfolder):

    for layout in laynode:

        layout_attr = layout.attrib
        layout_tag = layout.tag
        if layout_tag == "Group":
            groupname = layout_attr.get("name", "NONAME")
            groups.append( groupname )
            get_layouts_and_groups(cur_db, layout, groups, exportfolder)
            groups.pop()
        
        path = "Layouts"
        
        if groups and g_dogroupfolders:
            path = os.path.join("Layouts", *groups)
        s = ElementTree.tostring(layout, encoding="utf-8", method="xml")
        path = xmlexportfolder(exportfolder, cur_db, path,
                               layout_attr.get("name", "NONAME"),
                               layout_attr.get("id", "0"))
        f = open(path, "wb")
        f.write( s )
        f.close()

        for l in layout.getchildren():
            t = l.tag
            if t == u'Object':
                # get layout object
                cur_obj = get_layout_object(cur_db, l, exportfolder)

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

def get_scripts_and_groups(cur_db, scriptnode, exportfolder, groups, idx):

    for scpt in scriptnode:
        if scpt.tag == "Script":
            path = "Scripts"
            if groups and g_dogroupfolders:
                path = os.path.join("Scripts", *groups)

            sortid = str(idx).rjust(5,"0") + '-' + scpt.get("id", "0").rjust(7,"0")
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
            groupname = grp_attrib.get("name", "NONAME")
            groups.append( groupname )
            get_scripts_and_groups(cur_db, scpt, exportfolder, groups, idx)
            groups.pop()

def main():
    argumentfiles = sys.argv[1:]
    if not argumentfiles:
        print
        print "USAGE:"
        print "python ddrsplit.py /PATH/TO/Summary.xml"
        print
        exit(0)
    
    for af in argumentfiles:
        xmlfile = os.path.abspath( os.path.expanduser(af) )
        xml_folder, xmlfilename = os.path.split( xmlfile )

        ddr = ElementTree.parse( xmlfile )
        summary = ddr.getroot()

        files = summary.findall( "File" )

        filelist = {}
        for i in files:
            xffile = dbfile = False
            fmp6 = False
            try:
                xffile = i.attrib[ "link" ]
            except KeyError, m:
                print "XML Error: '%s'" % m
                # xffile = i.attrib[ "XMLReportFile" ]
                for item in i:
                    if item.tag == "XMLReportFile":
                        xffile = item.text
                        fmp6 = True
                    elif item.tag == "File":
                        dbfile = item.text
                        fmp6 = True
                        
            if not xffile:
                print
                print "ERROR: Could not find a XML file... NEXT!"
                print
                continue

            # cleanup filename
            while xffile.startswith( './/' ): xffile = xffile[ 3: ]
            while xffile.startswith( './' ):  xffile = xffile[ 2: ]

            xmlbasename, ext  = os.path.splitext( xffile )
            filelist[ xffile ] = xmlbasename
        pp(filelist)

        for cur_xml_file_name in filelist.keys():
            next_xml_file_path = os.path.join( xml_folder, cur_xml_file_name )
            line = '-' * 100
            print "\n\n%s\n\nNEXT: %s" % (line, repr(cur_xml_file_name))

            try:
                basenode = ElementTree.parse( next_xml_file_path )
            except  (xml.parsers.expat.ExpatError, SyntaxError), v:
                # pdb.set_trace()
                xml.parsers.expat.error()
                print "EXCEPTION: '%s'" % v
                print "Failed parsing '%s'" % next_xml_file_path
                print
                continue

            cur_db = filelist[ cur_xml_file_name ]

            exportfolder = os.path.join( xml_folder, "Exports")

            #
            # base table catalog
            #
            for base_table_catalog in basenode.getiterator( u'BaseTableCatalog' ):
                print ('\n\nBase Tables "%s"' % cur_db).encode( 'utf-8' )
                for base_table in base_table_catalog.getiterator( u'BaseTable' ):
                    s = ElementTree.tostring(base_table, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Basetables",
                                           base_table.get("name", "NONAME"),
                                           base_table.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

            #
            # layout catalog
            #
            for layout_catalog in basenode.getiterator ( "LayoutCatalog" ):
                print ( 'Layout Catalog "%s"' % cur_db ).encode( 'utf-8' )
                groups = []
                get_layouts_and_groups(cur_db, layout_catalog, groups, exportfolder)

            #
            # file reference catalog
            #
            for fr_cat in basenode.getiterator ( "FileReferenceCatalog" ):
                print ( 'File References "%s"' % cur_db ).encode( 'utf-8' )
                for fileref in fr_cat.getchildren():
                    fileref_attrib = fileref.attrib
                    s = ElementTree.tostring(fileref, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Filereferences",
                                           fileref_attrib.get("name", "NONAME"),
                                           fileref_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

            #
            # relationship graph
            #
            for rg_cat in basenode.getiterator ( "RelationshipGraph" ):
                print ( 'Relationship Graph "%s"' % cur_db ).encode( 'utf-8' )
                for rel in rg_cat.getchildren():
                    rel_attrib = rel.attrib
                    s = ElementTree.tostring(rel, encoding="utf-8", method="xml")
                    path = xmlexportfolder(exportfolder, cur_db, "Relationships",
                                           rel_attrib.get("name", "NONAME"),
                                           rel_attrib.get("id", "0"))
                    f = open(path, "wb")
                    f.write( s )
                    f.close()

            #
            # account catalog
            #
            #for acc_node in basenode.getiterator ( "AccountCatalog" ):
            #    print ('Accounts for "%s"' % cur_db ).encode( 'utf-8' )

            #
            # script catalog
            #
            print ('Scripts for "%s"' % cur_db ).encode( 'utf-8' )

            for scpt_cat in basenode.getiterator ( "ScriptCatalog" ):
                groups = []
                get_scripts_and_groups(cur_db, scpt_cat, exportfolder, groups, 1)

            #
            # privileges
            #
            #print ('TBD: Privileges for "%s"' % cur_db ).encode( 'utf-8' )

            #
            # extended privileges
            #
            #print ('TBD: Extended Privileges for "%s"' % cur_db ).encode( 'utf-8' )

            #
            # Custom Functions
            #
            #print ('TBD: Custom Functions for "%s"' % cur_db ).encode( 'utf-8' )



if __name__ == '__main__':
    main()