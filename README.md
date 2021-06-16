## FileMaker-DDR-Splitter

A Python script to split a FileMaker Database Design Report (DDR) into it's components.

The script has been used on OSX with V10, V11 & V15 DDRs. Windows and DDRs V12-14 may or may not work.

It's very fast. The longest run I have measured was 2 min. for a 420MB / 40 file DDR, creating more than 12000 files. A 275MB single file DDR was split in 19s.

### Why would I like to do that?

#### Because it's the cheapest and one of the fastest ways to find all occurences of a field for example.

+ Split your DDR

+ Use a text editor that can search directories (TextWrangler and BBEdit on OSX come to mind) and search for a fieldname. 
![Search](./images/search1.png?raw=true)

+ The granularity of the found set is now down to scripts, layouts etc. instead of one big DDR file.
![Found](./images/search2.png?raw=true)


#### Because it makes versions of a database compaparable

+ Create a DDR and split it.

+ check the export into a git repository

+ make changes in the database

+ redo DDR and split

+ ```git status``` and ```git diff ``` are very telling what changed in the database.

### Download an OSX app for OSX 10.9 and above.

[Releases](../releases)


### Prerequisites

#### For the Python script
[Python 2.7](https://www.python.org/) - Version 2.5 and 2.6 should work. Version 3.x probably not. All libraries needed are included with Python.

#### For building the OSX app the following additional libraries are needed:

[PyObjC](https://pythonhosted.org/pyobjc/install.html)

[py2app](https://pythonhosted.org/py2app/) and it's [dependencies](https://pythonhosted.org/py2app/dependencies.html)

### Usage

```shell
python ddrsplit.py /PATH/TO/Summary.xml
```

...or run the [OSX app](../releases).


This will create a folder named "Exports" at the ```Summary.xml``` level.

Inside Exports for each database file this will create a folder with the database name. More precise: the xml filename without the extension.

Inside the database folder (drumroll) there will be up to 13 subfolders, namely **Accounts, Assets, Basetables, CustomFunctions, CustomMenus, CustomMenuSets, Privileges, ExtendedPrivileges, Filereferences, Layouts, Relationships, Scripts and ValueLists.**

+ Accounts - The name pattern for each account is **"ID NAME.xml"**

+ Assets - contains images and other stuff found in layouts. The filename will be it's [SHA-1](http://en.wikipedia.org/wiki/SHA-1) hexdigest. The file extension is either derived from it's type (JPEG -> .jpg) for known types or **".TYPE"** for unknown types. Using the SHA1 hecdigest as the filename has the advantage that identical files are stored only once.

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

#### New 2017-07-12

+ AuthFiles - The name pattern is **"ID NAME.xml"**

+ ExternalDataSources - The name pattern is **"ID NAME.xml"**

+ Themes - The name pattern is **"ID NAME.xml"**

+ BaseDirectory - The name pattern is **"ID NAME.xml"**

### The application

![Screenshot](./images/screen1.png?raw=true)

### Configuration options

+ Assets - This was the original inspiration for this program: to extract images from layouts. Somewhere between Versions 12 to 15 FileMaker stopped including images in the DDR.

+ Asset options "per Solution", "per File", "per Layout" are disabled because they were never implemented.

+ Layouts - include Layouts in split.

+ Layout option "Create Layout Folders" - recreate layout folders in export.

+ Layout option "Keep Layout Order" - recreate layout sorting in export. This is accomplished by prepending a sortindex in the filename.

+ Scripts - include Scripts in split.

+ Script option "Create Script Folders" - recreate script folders in export.

+ Script option "Keep Script Order" - recreate script sorting in export. This is accomplished by prepending a sortindex in the filename.

+ cross references - This function is in development and can't be turned off at the moment. The result is in the folder "references".

+ Drop filename IDs - Omit IDs from filenames. This is useful when comparing two exports with git.

+ OPML - disabled because they don't exist yet and remind me of writing them one day. The idea is to have a OPML file for scripts, basetables and layouts which can be opened with any outliner.

