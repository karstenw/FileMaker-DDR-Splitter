"""
Script for building the FileMaker-DDR-Splitter application

Usage:
    python setup.py py2app -gx -O2
"""
import os

from distutils.core import setup
import py2app

appname = "FileMaker DDR Splitter"
appnameshort = "FMPSplit"
version = "V0.4.0"

copyright = u"Copyright 2015 Karsten Wolf"

infostr = appname + u' ' + version + u' ' + copyright



setup(
    app=[{
        'script': "FMPDDRSplitter.py",

        'plist':{
            'CFBundleGetInfoString': infostr,
            'CFBundleIdentifier': 'org.kw.ddrsplitter',
            'CFBundleShortVersionString': version,
            'CFBundleDisplayName': appnameshort,
            'CFBundleName': appnameshort,
            'CFBundleSignature': 'KWDs',
            'LSHasLocalizedDisplayName': False,
            'NSAppleScriptEnabled': False,
            'NSHumanReadableCopyright': copyright}}],

    data_files=["English.lproj/MainMenu.nib",
                "Icon.icns"],
    options={
        'py2app':{
            'iconfile': "Icon.icns",
            # 'excludes':[],
        },
    },
)
