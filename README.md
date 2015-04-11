# FileMaker-DDR-Splitter

A Python script to split a FileMaker Database Design Report (DDR) into it's components.

The script has been used on OSX with V10 & V11 DDRs. Windows and DDRs V12/13 may or may not work.

It's very fast. The longest run I have measured was 86s for a 420MB / 40 file DDR, creating more than 5000 files. A 275MB one file DDR was split in 18s.

## Prerequisites

[Python 2.7](https://www.python.org/) - Version 2.5 and 2.6 should work. Version 3.x probably not. All libraries used are standard.


## Usage

```shell
python ddrsplit.py /PATH/TO/Summary.xml
```
This will create a folder named "Exports" at the ```Summary.xml```level.

Inside Exports for each database file this will create a folder with the database name. More precise: the xml filename without the extension.

Inside the database folder (drumroll) there will be up to 7 subfolders, namely **Assets, Basetables, CustomFunctions, Filereferences, Layouts, Relationships & Scripts.**

+ Assets - contains images and other stuff found in layouts. The filename will be it's [SHA-1](http://en.wikipedia.org/wiki/SHA-1) hexdigest. The file extension is either derived from it's type or .TYPE for unknown types.

+ Basetables - for each basetable there will be it's xml from the DDR. The name pattern is **"ID NAME.xml"**

+ CustomFunctions - for each custom function there will be it's xml from the DDR. The name pattern is **"ID NAME.xml"**

+ Filereferences - for each file reference there will be it's xml from the DDR. The name pattern is **"ID NAME.xml"**

+ Layouts - for each layout there will be it's xml from the DDR. The name pattern is **"SORT ID NAME.xml"**. SORT is a 5 digit number to preserve the layout order.

+ Relationships - In work. Currently only one XML file for all relationships

+ Scripts - for each script there will be it's xml from the DDR. The name pattern is **"SORT-ID_NAME.xml"**.   SORT is a 5 digit number to preserve the script order.

