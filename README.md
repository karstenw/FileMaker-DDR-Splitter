# FileMaker-DDR-Splitter

A Python script to split a FileMaker Database Design Report (DDR) into it's components.

The script has been used on OSX with V10 & V11 DDRs. Windows and DDRs V12-14 may or may not work.

It's very fast. The longest run I have measured was 2 min. for a 420MB / 40 file DDR, creating more than 12000 files. A 275MB single file DDR was split in 19s.

## Download an OSX app for OSX 10.6 and above.
[dropbox](http://goo.gl/YwGc7K)


## Prerequisites

###For the Python script
[Python 2.7](https://www.python.org/) - Version 2.5 and 2.6 should work. Version 3.x probably not. All libraries needed are included with Python.

###For building the OSX app the following additional libraries are needed:

[PyObjC](https://pythonhosted.org/pyobjc/install.html)

[py2app](https://pythonhosted.org/py2app/) and it's [dependencies](https://pythonhosted.org/py2app/dependencies.html)


## Usage

```shell
python ddrsplit.py /PATH/TO/Summary.xml
```


This will create a folder named "Exports" at the ```Summary.xml```level.

Inside Exports for each database file this will create a folder with the database name. More precise: the xml filename without the extension.

Inside the database folder (drumroll) there will be up to 13 subfolders, namely **Accounts, Assets, Basetables, CustomFunctions, CustomMenus, CustomMenuSets, Privileges, ExtendedPrivileges, Filereferences, Layouts, Relationships, Scripts and ValueLists.**

+ Accounts - The name pattern is **"ID NAME.xml"**

+ Assets - contains images and other stuff found in layouts. The filename will be it's [SHA-1](http://en.wikipedia.org/wiki/SHA-1) hexdigest. The file extension is either derived from it's type (JPEG -> .jpg) for known types or **".TYPE"** for unknown types.

+ Basetables - The name pattern is **"ID NAME.xml"**

+ CustomFunctions - The name pattern is **"ID NAME.xml"**

+ CustomMenus - The name pattern is **"ID NAME.xml"**

+ CustomMenuSets - The name pattern is **"ID NAME.xml"**

+ ExtendedPrivileges - The name pattern is **"ID NAME.xml"**

+ Filereferences - The name pattern is **"ID NAME.xml"**

+ Layouts - The name pattern is **"SORT ID NAME.xml"**. SORT is a 5 digit number to preserve the layout order. Groups (layout folders) will be presented as folders.

+ Relationships - has 2 subfolders: **Relationship, TableList**. The name pattern is **"ID NAME.xml"**

+ Scripts - for each script there will be it's xml from the DDR. The name pattern is **"SORT-ID_NAME.xml"**.   SORT is a 5 digit number to preserve the script order.

+ ValueLists - The name pattern is **"ID NAME.xml"**

## The application

![Screenshot](./images/screen1.png?raw=true)

